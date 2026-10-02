"""Tìm và tải video highlight trên YouTube bằng yt-dlp."""
import re
from pathlib import Path

import yt_dlp
import yt_dlp.utils

from .config import FFMPEG, NODE

NFL_CHANNEL = "UCDVYQ4Zhbm3S2dlz7P1GBDg"
# thứ tự chế độ tải thử lần lượt khi YouTube chặn (403)
CLIENTS = ["tv_simply", "mweb", "default"]


def _ydl_base():
    import os
    node = {"path": NODE} if os.path.isabs(NODE) else {}
    return {"quiet": True, "no_warnings": True, "js_runtimes": {"node": node}}


def search(query: str, n: int = 15) -> list[dict]:
    opts = _ydl_base() | {"extract_flat": True}
    with yt_dlp.YoutubeDL(opts) as ydl:
        d = ydl.extract_info(f"ytsearch{n}:{query}", download=False)
    return [{
        "id": e["id"], "title": e.get("title") or "", "channel": e.get("channel") or "",
        "channel_id": e.get("channel_id") or "", "duration": e.get("duration") or 0,
        "views": e.get("view_count") or 0,
    } for e in d.get("entries", []) if e]


def find_highlights(g: dict) -> list[dict]:
    """Tìm video highlight của một trận, chấm điểm độ phù hợp, trả về danh sách đã sắp xếp."""
    season, week = str(g["season"]), g.get("week")
    q = f"{g['away']} vs {g['home']} game highlights {season} week {week}"
    cands = search(q, 15)
    nicks = [g.get("away_nick") or g["away"].split()[-1], g.get("home_nick") or g["home"].split()[-1]]
    out = []
    for c in cands:
        t = c["title"].lower()
        s, notes = 0, []
        if c["channel_id"] == NFL_CHANNEL:
            s += 50; notes.append("kênh NFL chính thức")
        if all(n.lower() in t for n in nicks):
            s += 25
        else:
            s -= 40; notes.append("thiếu tên đội")
        years = set(re.findall(r"\b(20\d\d)\b", t))
        if season in years:
            s += 20
        elif years:
            s -= 80; notes.append("sai mùa giải")
        if week and re.search(rf"week {week}\b", t):
            s += 15
        elif re.search(r"week \d+", t):
            s -= 30; notes.append("sai tuần")
        if "highlight" in t:
            s += 10
        # video trước trận / bình luận / dự đoán không phải highlight
        if re.search(r"\b(preview|prediction|predictions|picks|reaction|reacts|recap show|podcast|breakdown|film)\b", t):
            s -= 70; notes.append("không phải highlight (preview/bình luận)")
        if "full game" in t:
            notes.append("FULL GAME (rất dài, nhiều footage)")
        if not (6 * 60 <= c["duration"] <= 40 * 60) and "full game" not in t:
            s -= 15; notes.append("độ dài lạ")
        c["score"], c["notes"] = s, ", ".join(notes)
        out.append(c)
    out.sort(key=lambda c: -c["score"])
    return out


class _Log:
    """Gom thông báo lỗi của yt-dlp để báo lại cho người dùng."""
    def __init__(self):
        self.errors = []

    def debug(self, m):
        pass

    def info(self, m):
        pass

    def warning(self, m):
        pass

    def error(self, m):
        self.errors.append(str(m))


def _download(url: str, out: Path, fmt: str, client: str, section=None) -> tuple[bool, str]:
    lg = _Log()
    opts = _ydl_base() | {
        "format": fmt, "merge_output_format": "mp4", "outtmpl": str(out), "nopart": True,
        "overwrites": True, "logger": lg, "noprogress": True, "ffmpeg_location": FFMPEG,
    }
    if client != "default":
        opts["extractor_args"] = {"youtube": {"player_client": [client]}}
    if section:
        opts["download_ranges"] = yt_dlp.utils.download_range_func([], [section])
        opts["force_keyframes_at_cuts"] = True
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])
        return True, ""
    except Exception as e:
        return False, (lg.errors[-1] if lg.errors else str(e))


def download_proxy(video_id: str, out: Path, height: int = 360, log=print) -> Path:
    """Tải bản nhẹ để phân tích. Thử lần lượt các chế độ tải khi bị chặn."""
    if out.exists() and out.stat().st_size > 1_000_000:
        return out
    url = f"https://www.youtube.com/watch?v={video_id}"
    fmt = f"bv*[height<={height}][ext=mp4]+ba[ext=m4a]/b[height<={height}]/b"
    last = ""
    for c in CLIENTS:
        log(f"Đang tải bản phân tích ({c})…")
        ok, last = _download(url, out, fmt, c)
        if ok and out.exists() and out.stat().st_size > 1_000_000:
            return out
        out.unlink(missing_ok=True)
    raise RuntimeError("Không tải được video. " + last)


def download_section(video_id: str, start: float, end: float, out: Path, height: int = 1080, log=print) -> Path:
    """Tải bản chất lượng cao cho đúng một đoạn [start, end] giây."""
    url = f"https://www.youtube.com/watch?v={video_id}"
    fmt = f"bv*[height<={height}]+ba/b[height<={height}]/b"
    last = ""
    for c in ["default", "mweb", "tv_simply"]:
        log(f"Đang tải bản HD đoạn {start:.1f}-{end:.1f}s ({c})…")
        ok, last = _download(url, out, fmt, c, (start, end))
        if ok and out.exists() and out.stat().st_size > 10_000:
            return out
        out.unlink(missing_ok=True)
    raise RuntimeError("Không tải được đoạn HD. " + last)
