"""Xử lý nguồn video/audio chuyên gia: nạp video, trích xuất audio, transcribe (WhisperX / Faster-Whisper), bóc tách lượt nói."""
import hashlib
import json
import re
import shutil
import subprocess
import time
from pathlib import Path

from .config import FFMPEG, NO_WINDOW, expert_dir, load_settings, EXPERTS
from .analyze import transcribe as tr_mod


def _slug(s: str) -> str:
    s = re.sub(r"[^\w\s-]", "", s).strip().lower()
    return re.sub(r"[-\s]+", "_", s)[:40]


def _probe_duration(media_path: Path) -> float:
    try:
        cmd = [
            FFMPEG, "-i", str(media_path)
        ]
        res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL, text=True, **NO_WINDOW)
        m = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", res.stderr)
        if m:
            return int(m[1]) * 3600 + int(m[2]) * 60 + float(m[3])
    except Exception:
        pass
    return 0.0


def extract_audio(src_path: Path, dst_wav: Path) -> Path:
    """Trích xuất âm thanh mono 16kHz WAV bằng FFmpeg."""
    cmd = [
        FFMPEG, "-v", "error", "-y", "-i", str(src_path),
        "-vn", "-ac", "1", "-ar", "16000", str(dst_wav)
    ]
    subprocess.run(cmd, check=True, **NO_WINDOW)
    return dst_wav


def ingest_file(file_path: str, title: str = "", log=print) -> dict:
    """Nạp file video hoặc audio cục bộ từ máy tính."""
    p = Path(file_path)
    if not p.exists():
        raise FileNotFoundError(f"Không tìm thấy file: {file_path}")
    
    name = title.strip() or p.stem
    uid = f"exp_{int(time.time())}_{_slug(name)}"
    edir = expert_dir(uid)
    
    log(f"Đang chuẩn bị âm thanh từ file: {p.name}...")
    wav = edir / "audio.wav"
    extract_audio(p, wav)
    
    dur = _probe_duration(p) or _probe_duration(wav)
    meta = {
        "id": uid,
        "title": name,
        "original_file": str(p.resolve()),
        "duration": round(dur, 2),
        "source": "local_file",
        "created_at": time.strftime("%Y-%m-%d %H:%M"),
        "status": "ready_for_transcribe"
    }
    (edir / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"✅ Đã nạp file: {name} (Thời lượng: {int(dur)//60}p {int(dur)%60:02d}s)")
    return meta


def ingest_youtube(url: str, title: str = "", log=print) -> dict:
    """Tải và nạp audio từ link YouTube chuyên gia."""
    import yt_dlp
    from .config import NODE
    
    uid = f"exp_{int(time.time())}"
    edir = expert_dir(uid)
    raw_audio = edir / "raw_audio.m4a"
    wav = edir / "audio.wav"
    
    log(f"Đang lấy thông tin từ YouTube: {url}...")
    ydl_opts = {
        'format': 'ba[ext=m4a]/ba/b',
        'outtmpl': str(raw_audio),
        'overwrites': True,
        'quiet': True,
        'ffmpeg_location': FFMPEG,
        'js_runtimes': {'node': {'path': NODE}} if NODE else {},
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        vid_title = title.strip() or info.get("title") or "YouTube Expert Video"
        dur = info.get("duration") or 0.0
    
    # Đổi lại tên thư mục cho có slug tiêu đề
    clean_uid = f"{uid}_{_slug(vid_title)}"
    new_edir = EXPERTS / clean_uid
    if edir.exists() and edir != new_edir:
        edir.rename(new_edir)
        edir = new_edir
        raw_audio = edir / "raw_audio.m4a"
        wav = edir / "audio.wav"
    
    log(f"Đang chuẩn bị âm thanh 16kHz...")
    extract_audio(raw_audio, wav)
    raw_audio.unlink(missing_ok=True)
    
    meta = {
        "id": clean_uid,
        "title": vid_title,
        "url": url,
        "duration": round(dur, 2),
        "source": "youtube",
        "created_at": time.strftime("%Y-%m-%d %H:%M"),
        "status": "ready_for_transcribe"
    }
    (edir / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"✅ Đã nạp video YouTube: {vid_title} (Thời lượng: {int(dur)//60}p {int(dur)%60:02d}s)")
    return meta


def _transcribe_with_whisperx(wav_path: Path, model_name="small.en", device="cuda", hf_token=None, log=print) -> list[dict]:
    """Transcribe sử dụng WhisperX (nếu có cài đặt)."""
    import whisperx
    
    compute_type = "float16" if device == "cuda" else "int8"
    log(f"Đang chạy WhisperX model={model_name}, device={device}...")
    model = whisperx.load_model(model_name, device, compute_type=compute_type)
    audio = whisperx.load_audio(str(wav_path))
    result = model.transcribe(audio, batch_size=16)
    
    log("Đang căn chỉnh từ (WhisperX Alignment)...")
    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
    aligned_res = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)
    
    if hf_token:
        try:
            log("Đang phân tách người nói (Speaker Diarization)...")
            diarize_model = whisperx.DiarizationPipeline(use_auth_token=hf_token, device=device)
            diarize_segments = diarize_model(audio)
            aligned_res = whisperx.assign_word_speakers(diarize_segments, aligned_res)
        except Exception as e:
            log(f"⚠ Bỏ qua Diarization (lỗi: {e})")
            
    segments = []
    for s in aligned_res.get("segments", []):
        words = []
        for w in s.get("words", []):
            words.append({
                "s": round(w.get("start", s["start"]), 2),
                "e": round(w.get("end", s["end"]), 2),
                "w": w.get("word", "").strip(),
                "score": round(w.get("score", 1.0), 2)
            })
        segments.append({
            "start": round(s["start"], 2),
            "end": round(s["end"], 2),
            "speaker": s.get("speaker", "Speaker"),
            "text": s.get("text", "").strip(),
            "words": words
        })
    return segments


def _transcribe_with_faster_whisper(wav_path: Path, model_name="small.en", device="cuda", log=print) -> list[dict]:
    """Transcribe sử dụng Faster-Whisper siêu tốc (có sẵn, hỗ trợ GPU CUDA, chia lượt nói theo VAD & pause)."""
    log(f"Đang chạy Faster-Whisper ({model_name} trên {device})...")
    m = tr_mod.get_model(model_name, device)
    
    segs, info = m.transcribe(
        str(wav_path),
        word_timestamps=True,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=600),
        beam_size=5,
        condition_on_previous_text=False
    )
    
    segments = []
    cur_speaker_idx = 1
    prev_end = 0.0
    
    for s in segs:
        # Nếu khoảng ngắt nghỉ > 1.2s -> có thể đổi lượt nói
        if prev_end > 0 and (s.start - prev_end) > 1.2:
            cur_speaker_idx = 2 if cur_speaker_idx == 1 else 1
            
        words = []
        for w in (s.words or []):
            words.append({
                "s": round(w.start, 2),
                "e": round(w.end, 2),
                "w": w.word.strip()
            })
        segments.append({
            "start": round(s.start, 2),
            "end": round(s.end, 2),
            "speaker": f"Speaker {cur_speaker_idx}",
            "text": s.text.strip(),
            "words": words
        })
        prev_end = s.end
        
    return segments


def run_transcribe(expert_id: str, force: bool = False, log=print) -> dict:
    """Chạy toàn bộ quy trình transcribe cho một video chuyên gia."""
    edir = expert_dir(expert_id)
    wav = edir / "audio.wav"
    if not wav.exists():
        raise FileNotFoundError(f"Chưa có file audio trong {edir}")
        
    seg_file = edir / "segments.json"
    meta_file = edir / "meta.json"
    
    if seg_file.exists() and not force:
        log("Đã có sẵn transcript, bỏ qua bước nhận dạng giọng nói.")
        return json.loads(seg_file.read_text(encoding="utf-8"))
        
    settings = load_settings()
    model_name = settings.get("whisper_model", "small.en")
    device = settings.get("whisper_device", "cuda")
    
    has_whisperx = False
    try:
        import whisperx
        has_whisperx = True
    except ImportError:
        has_whisperx = False
        
    if has_whisperx:
        log("⚡ Tìm thấy thư viện WhisperX, kích hoạt chế độ WhisperX...")
        try:
            segments = _transcribe_with_whisperx(wav, model_name, device, log=log)
        except Exception as e:
            log(f"⚠ WhisperX gặp lỗi ({e}), tự động chuyển về Faster-Whisper...")
            segments = _transcribe_with_faster_whisper(wav, model_name, device, log=log)
    else:
        log("⚡ Chạy bằng Faster-Whisper tích hợp sẵn (GPU CUDA siêu tốc)...")
        segments = _transcribe_with_faster_whisper(wav, model_name, device, log=log)
        
    # Lưu segments.json
    seg_file.write_text(json.dumps(segments, ensure_ascii=False, indent=2), encoding="utf-8")
    
    # Tạo transcript.txt dễ đọc cho người dùng
    txt_lines = []
    for s in segments:
        m_s, sec_s = int(s["start"]) // 60, int(s["start"]) % 60
        m_e, sec_e = int(s["end"]) // 60, int(s["end"]) % 60
        txt_lines.append(f"[{m_s:02d}:{sec_s:02d} -> {m_e:02d}:{sec_e:02d}] {s.get('speaker', 'Speaker')}: {s['text']}")
    (edir / "transcript.txt").write_text("\n\n".join(txt_lines), encoding="utf-8")
    
    # Cập nhật meta.json
    if meta_file.exists():
        meta = json.loads(meta_file.read_text(encoding="utf-8"))
        meta["status"] = "transcribed"
        meta["segment_count"] = len(segments)
        meta["transcribed_at"] = time.strftime("%Y-%m-%d %H:%M")
        meta_file.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
        
    log(f"✅ Transcribe hoàn tất! Nhận diện được {len(segments)} câu/lượt phát biểu.")
    return segments


def get_expert_data(expert_id: str) -> dict:
    """Lấy dữ liệu đầy đủ của một chuyên gia (meta, segments, topics)."""
    edir = expert_dir(expert_id)
    meta_file = edir / "meta.json"
    seg_file = edir / "segments.json"
    top_file = edir / "topics.json"
    
    meta = json.loads(meta_file.read_text(encoding="utf-8")) if meta_file.exists() else {"id": expert_id}
    segments = json.loads(seg_file.read_text(encoding="utf-8")) if seg_file.exists() else []
    topics = json.loads(top_file.read_text(encoding="utf-8")) if top_file.exists() else []
    return {
        "meta": meta,
        "segments": segments,
        "topics": topics
    }


def list_experts() -> list[dict]:
    """Danh sách tất cả các video chuyên gia đã nạp."""
    out = []
    for m in EXPERTS.glob("*/meta.json"):
        try:
            d = json.loads(m.read_text(encoding="utf-8"))
            out.append(d)
        except Exception:
            pass
    out.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return out


def delete_expert(expert_id: str):
    """Xóa một video chuyên gia khỏi hệ thống."""
    edir = expert_dir(expert_id)
    if edir.exists():
        shutil.rmtree(edir, ignore_errors=True)
