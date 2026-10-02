"""Chép lời (Whisper) có timestamp từng từ + gợi ý tên cầu thủ của trận để giảm sai tên riêng.

Nếu cạnh file video có sẵn file .srt (ví dụ xuất từ Whisper GUI của bạn), phần mềm sẽ dùng file đó
thay vì tự chép lời (khi đó chỉ có timestamp theo câu, không theo từng từ).
"""
import difflib
import glob
import os
import re
from pathlib import Path

_model = {}


def _cuda_dlls():
    import site
    from ..config import BUNDLE
    roots = [str(BUNDLE)]
    try:
        roots += site.getsitepackages()
    except Exception:
        pass
    for sp in roots:
        for d in glob.glob(os.path.join(sp, "nvidia", "*", "bin")):
            try:
                os.add_dll_directory(d)
            except Exception:
                pass
            os.environ["PATH"] = d + os.pathsep + os.environ.get("PATH", "")


def get_model(name="small.en", device="cuda"):
    key = (name, device)
    if key not in _model:
        from faster_whisper import WhisperModel
        if device == "cuda":
            _cuda_dlls()
            try:
                _model[key] = WhisperModel(name, device="cuda", compute_type="float16")
            except Exception:
                _model[key] = WhisperModel(name, device="cpu", compute_type="int8")
        else:
            _model[key] = WhisperModel(name, device="cpu", compute_type="int8")
    return _model[key]


def _srt_time(s):
    h, m, rest = s.replace(",", ".").split(":")
    return int(h) * 3600 + int(m) * 60 + float(rest)


def load_srt(path: Path) -> list[dict]:
    """Đọc file .srt thành danh sách 'từ' (mỗi câu chia đều thời gian cho các từ)."""
    words = []
    for block in re.split(r"\n\s*\n", path.read_text(encoding="utf-8", errors="ignore")):
        m = re.search(r"(\d+:\d+:\d+[,.]\d+)\s*-->\s*(\d+:\d+:\d+[,.]\d+)\s*\n(.*)", block, re.S)
        if not m:
            continue
        a, b, txt = _srt_time(m[1]), _srt_time(m[2]), " ".join(m[3].split())
        toks = txt.split()
        for i, w in enumerate(toks):
            words.append({"s": round(a + (b - a) * i / len(toks), 2), "e": round(a + (b - a) * (i + 1) / len(toks), 2), "w": w})
    return words


def transcribe(audio, hot_names: list[str] | None = None, model="small.en", device="cuda", progress=None) -> list[dict]:
    m = get_model(model, device)
    hot = " ".join(hot_names[:120]) if hot_names else None
    segs, info = m.transcribe(str(audio), word_timestamps=True, vad_filter=True, beam_size=5,
                              hotwords=hot, condition_on_previous_text=False)
    words = []
    for s in segs:
        for w in s.words or []:
            words.append({"s": round(w.start, 2), "e": round(w.end, 2), "w": w.word.strip()})
        if progress and info.duration:
            progress(min(1.0, s.end / info.duration))
    return words


def fix_names(words: list[dict], lastnames: list[str]) -> list[dict]:
    """Sửa các từ viết hoa gần giống họ cầu thủ trong trận (ví dụ 'Luke' -> 'Loop' chỉ khi đủ giống)."""
    ln = {n.lower(): n for n in lastnames if len(n) >= 4}
    keys = list(ln)
    for w in words:
        raw = re.sub(r"[^A-Za-z'\-]", "", w["w"])
        if len(raw) < 4 or not raw[0].isupper() or raw.lower() in ln:
            continue
        m = difflib.get_close_matches(raw.lower(), keys, n=1, cutoff=0.84)
        if m:
            w["w"] = w["w"].replace(raw, ln[m[0]])
            w["fixed"] = True
    return words


def text_between(words, a, b) -> str:
    return " ".join(w["w"] for w in words if a <= w["s"] < b)
