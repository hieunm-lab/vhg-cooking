"""Kho pha bóng: liệt kê trận đã phân tích, tìm kiếm pha, xem thử, xuất clip HD."""
import json
import re
import subprocess
import unicodedata
from pathlib import Path

from . import yt
from .config import CLIPS, FFMPEG, GAMES, NO_WINDOW, load_settings

# từ khoá tiếng Việt / viết tắt -> từ khoá xuất hiện trong dữ liệu
ALIASES = {
    "td": "touchdown", "chạm bóng": "touchdown", "ghi bàn": "ghi điểm", "fg": "field goal",
    "sút": "field goal", "đá phạt": "field goal", "int": "đánh chặn", "interception": "đánh chặn",
    "chặn bóng": "đánh chặn", "pick": "đánh chặn", "mất bóng": "mất bóng", "fumble": "fumble",
    "sack": "sack", "chạy": "chạy bóng", "chuyền": "chuyền", "cuối trận": "phút cuối",
    "quyết định": "phút cuối", "walk-off": "phút cuối", "punt": "punt",
}


PHRASES = {v for v in ALIASES.values() if " " in v} | {
    "ghi điểm", "phút cuối", "pha dài", "mất bóng", "field goal", "chạy bóng", "đánh chặn", "bị chặn",
    "chuyền thành công", "chuyền hỏng", "giao bóng", "extra point"}


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFC", (s or "").lower())
    return s


def analyzed_games() -> list[dict]:
    out = []
    for m in GAMES.glob("*/*/meta.json"):
        try:
            out.append(json.loads(m.read_text(encoding="utf-8")))
        except Exception:
            pass
    out.sort(key=lambda m: m.get("analyzed_at", ""), reverse=True)
    return out


def game_label(m: dict) -> str:
    i = m["info"]
    return f"{i['season']} W{i.get('week','?')} · {i['away_abbr']} {i['away_score']}-{i['home_score']} {i['home_abbr']} · {m['video_id']}"


def load_segments(m: dict) -> list[dict]:
    p = GAMES / m["event_id"] / m["video_id"] / "segments.json"
    segs = json.loads(p.read_text(encoding="utf-8"))
    for s in segs:
        s["_game"] = game_label(m)
        s["_event"] = m["event_id"]
        s["_video"] = m["video_id"]
    return segs


def _haystack(s: dict) -> dict:
    also = " ".join(a["text"] + " " + " ".join(a["players"]) for a in s.get("also", []))
    return {
        "players": _norm(" ".join(s.get("players", [])) + " " + " ".join(p for a in s.get("also", []) for p in a["players"])),
        "text": _norm(s.get("text", "") + " " + also),
        "tags": _norm(" ".join(s.get("tags", [])) + " " + s.get("type_vi", "") + " " + s.get("type", "")),
        "comm": _norm(s.get("commentary", "")),
    }


def search(query: str, metas: list[dict], only_scoring=False, only_high=False, quarter=None) -> list[dict]:
    q = _norm(query).strip()
    for k, v in ALIASES.items():
        q = re.sub(rf"(?<!\w){re.escape(k)}(?!\w)", v, q)
    # giữ nguyên các cụm nhiều chữ (không tách "đánh chặn" thành "đánh" + "chặn")
    toks = []
    for ph in sorted(PHRASES, key=len, reverse=True):
        if ph in q:
            toks.append(ph)
            q = q.replace(ph, " ")
    toks += [t for t in re.split(r"[\s,]+", q) if t]
    rows = []
    for m in metas:
        for s in load_segments(m):
            if only_scoring and "ghi điểm" not in s.get("tags", []):
                continue
            if only_high and s.get("confidence") != "cao":
                continue
            if quarter and s.get("q") != quarter:
                continue
            if not toks:
                s["_score"] = 0
                rows.append(s)
                continue
            h = _haystack(s)
            score, hit = 0.0, 0
            for t in toks:
                w = 0
                if t in h["players"]:
                    w = max(w, 3)
                if re.search(rf"(?<!\d){re.escape(t)}(?!\d)" if t.isdigit() else re.escape(t), h["text"]):
                    w = max(w, 2)
                if t in h["tags"]:
                    w = max(w, 2)
                if t in h["comm"]:
                    w = max(w, 1)
                if w:
                    hit += 1
                    score += w
            if hit and hit >= max(1, round(len(toks) * 0.6)):
                s["_score"] = score + (0.5 if s.get("confidence") == "cao" else 0)
                rows.append(s)
    if toks:
        rows.sort(key=lambda s: -s["_score"])
    return rows


def fmt_t(x) -> str:
    x = float(x or 0)
    return f"{int(x)//60}:{int(x)%60:02d}"


def proxy_path(s: dict) -> Path:
    return GAMES / s["_event"] / f"proxy_{s['_video']}.mp4"


def preview(s: dict, pad: float = 0.0) -> str:
    """Cắt đoạn xem thử từ bản nhẹ (nhanh, không cần tải lại)."""
    out = GAMES / s["_event"] / s["_video"] / "previews" / f"seg_{s['id']:03d}_{pad:.1f}.mp4"
    out.parent.mkdir(exist_ok=True)
    if not out.exists():
        a = max(0.0, s["start"] - pad)
        subprocess.run([FFMPEG, "-v", "error", "-y", "-ss", f"{a:.2f}", "-i", str(proxy_path(s)),
                        "-t", f"{s['end'] - a + pad:.2f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "26",
                        "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", str(out)], check=True, **NO_WINDOW)
    return str(out)


def _slug(s: str) -> str:
    s = s.replace("đ", "d").replace("Đ", "D")
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_")[:50]


def export_hq(s: dict, pad: float = 0.5, log=print) -> str:
    """Tải bản chất lượng cao cho đúng đoạn này. Nếu YouTube chặn, xuất từ bản nhẹ (kèm cảnh báo)."""
    S = load_settings()
    name = f"{_slug(s['_game'])}_seg{s['id']:03d}_{_slug(s.get('type_vi',''))}"
    if s.get("players"):
        name += "_" + _slug(s["players"][0])
    out = CLIPS / f"{name}.mp4"
    if out.exists():
        return str(out)
    a, b = max(0.0, s["start"] - pad), s["end"] + pad
    try:
        yt.download_section(s["_video"], a, b, out, S["hq_height"], log=log)
    except Exception as e:
        log(f"⚠ Không tải được bản HD ({e}). Xuất tạm từ bản nhẹ 360p.")
        out = CLIPS / f"{name}_360p.mp4"
        subprocess.run([FFMPEG, "-v", "error", "-y", "-ss", f"{a:.2f}", "-i", str(proxy_path(s)), "-t", f"{b - a:.2f}",
                        "-c:v", "libx264", "-preset", "fast", "-crf", "20", "-c:a", "aac", str(out)], check=True, **NO_WINDOW)
    return str(out)
