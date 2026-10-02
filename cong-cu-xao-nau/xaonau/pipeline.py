"""Dây chuyền phân tích một trận: tải highlight -> băm pha -> gắn nhãn. Mỗi bước lưu cache vào data/games/<id>/."""
import json
import time
from pathlib import Path

from . import nfl, yt
from .analyze import matcher, scorebug, transcribe, video
from .config import game_dir, load_settings


def _save(p: Path, obj):
    p.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")


def _load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def analyze(event_id: str, video_id: str, video_meta: dict | None = None, force: bool = False, log=print):
    """Chạy toàn bộ các bước. `log(msg)` nhận thông báo tiến độ (tiếng Việt)."""
    S = load_settings()
    gd = game_dir(event_id)
    t0 = time.time()

    log("① Lấy dữ liệu trận từ ESPN…")
    summ = nfl.summary(event_id, refresh=force)
    info = nfl.game_info(summ)
    plays = nfl.plays(summ)
    ros = nfl.roster(summ)
    _save(gd / "plays.json", plays)
    log(f"   {info['away']} {info['away_score']} – {info['home_score']} {info['home']} | {len(plays)} pha, {len(ros['lastnames'])} cầu thủ")

    proxy = gd / f"proxy_{video_id}.mp4"
    log("② Tải video highlight (bản nhẹ để phân tích)…")
    yt.download_proxy(video_id, proxy, S["proxy_height"], log=lambda m: log("   " + m))
    dur = video.probe_duration(proxy)
    log(f"   Xong: {dur/60:.1f} phút")

    vd = gd / video_id
    vd.mkdir(exist_ok=True)

    p = vd / "frames.json"
    if force or not p.exists():
        log("③ Tách cảnh và phân loại khung hình…")
        _save(p, video.shots_and_frames(proxy))
    sf = _load(p)
    log(f"   {len(sf['shots'])} shot")

    wav = vd / "audio.wav"
    if force or not wav.exists():
        video.extract_wav(proxy, wav)
    p = vd / "loud.json"
    if force or not p.exists():
        _save(p, video.loudness(wav))
    loud = _load(p)

    p = vd / "states.json"
    if force or not p.exists():
        log("④ Đọc thanh tỷ số (hiệp, đồng hồ, down)…")
        lay = scorebug.learn_layout(proxy, dur, log=lambda m: log("   " + m))
        _save(vd / "layout.json", lay)
        states = scorebug.read_states(proxy, lay, S["ocr_fps"]) if lay else []
        _save(p, states)
    states = _load(p)
    ok = sum(1 for s in states if s["clock"] is not None)
    log(f"   Đọc được {ok}/{len(states)} giây có thanh tỷ số")

    p = vd / "words.json"
    srt = next(iter(sorted(gd.glob(f"*{video_id}*.srt"))), None)
    if force or not p.exists():
        if srt:
            log(f"⑤ Dùng phụ đề có sẵn: {srt.name}")
            words = transcribe.load_srt(srt)
        else:
            log(f"⑤ Chép lời bình luận viên (Whisper {S['whisper_model']}, {S['whisper_device']})…")
            words = transcribe.transcribe(wav, ros["lastnames"], S["whisper_model"], S["whisper_device"])
        words = transcribe.fix_names(words, ros["lastnames"])
        _save(p, words)
    words = _load(p)
    log(f"   {len(words)} từ")

    log("⑥ Khớp từng đoạn video với play-by-play…")
    runs = matcher.match_runs(matcher.build_runs(states), plays)
    segs = matcher.build_segments(runs, sf["shots"], sf["per_sec"], words, loud, dur)
    segs = matcher.infer_missing(segs, plays)
    _save(vd / "segments.json", segs)
    n_play = len({s["pid"] for s in segs if s.get("pid")})
    high = sum(1 for s in segs if s["confidence"] == "cao")
    meta = {"event_id": event_id, "video_id": video_id, "info": info, "duration": dur,
            "video": video_meta or {}, "n_segments": len(segs), "n_plays": n_play, "n_high": high,
            "analyzed_at": time.strftime("%Y-%m-%d %H:%M")}
    _save(vd / "meta.json", meta)
    log(f"✅ Hoàn tất sau {time.time()-t0:.0f}s: {len(segs)} đoạn, {n_play} pha nhận diện được ({high} đoạn tin cậy cao).")
    return meta
