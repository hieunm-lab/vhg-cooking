"""Dữ liệu NFL từ ESPN (API công khai không chính thức): lịch trận, kết quả, play-by-play, danh sách cầu thủ."""
import json
import re

import requests

from .config import game_dir

BASE = "https://site.api.espn.com/apis/site/v2/sports/football/nfl"
UA = {}  # ESPN chặn một số User-Agent; để mặc định của requests thì cho qua

# loại pha không phải pha bóng thật (không có hình để cắt)
NON_PLAYS = {"Official Timeout", "Timeout", "End Period", "Two-minute warning", "End of Half",
             "End of Game", "End of Regulation", "Coin Toss"}

TYPE_VI = {
    "Rush": "Chạy bóng", "Pass Reception": "Chuyền thành công", "Pass Incompletion": "Chuyền hỏng",
    "Kickoff": "Giao bóng", "Penalty": "Phạm lỗi", "Punt": "Punt", "Field Goal Good": "Field goal ghi điểm",
    "Field Goal Missed": "Field goal trượt", "Blocked Field Goal": "Field goal bị chặn",
    "Rushing Touchdown": "TOUCHDOWN chạy", "Passing Touchdown": "TOUCHDOWN chuyền", "Sack": "Sack",
    "Interception Return": "Đánh chặn (INT)", "Interception Return Touchdown": "INT ghi TD (pick-six)",
    "Fumble Recovery (Own)": "Fumble (đội mình giữ)", "Fumble Recovery (Opponent)": "Fumble (mất bóng)",
    "Fumble Return Touchdown": "Fumble ghi TD", "Extra Point Good": "Extra point", "Safety": "Safety",
    "Kickoff Return Touchdown": "Giao bóng ghi TD", "Punt Return Touchdown": "Punt ghi TD",
    "Two Point Conversion": "2 điểm",
}


def _get(url, params=None):
    r = requests.get(url, params=params, headers=UA, timeout=30)
    r.raise_for_status()
    return r.json()


def week_games(season: int, week: int, seasontype: int = 2) -> list[dict]:
    """Danh sách trận của một tuần. seasontype: 1 tiền mùa giải, 2 mùa chính, 3 playoff."""
    d = _get(f"{BASE}/scoreboard", {"seasontype": seasontype, "week": week, "dates": season})
    out = []
    for e in d.get("events", []):
        comp = e["competitions"][0]
        teams = {c["homeAway"]: c for c in comp["competitors"]}
        a, h = teams["away"], teams["home"]
        out.append({
            "id": e["id"], "date": e["date"][:10], "short": e["shortName"],
            "status": e["status"]["type"]["name"],
            "away": a["team"]["displayName"], "home": h["team"]["displayName"],
            "away_abbr": a["team"]["abbreviation"], "home_abbr": h["team"]["abbreviation"],
            "away_nick": a["team"].get("name", ""), "home_nick": h["team"].get("name", ""),
            "away_score": a.get("score"), "home_score": h.get("score"),
            "season": season, "week": week, "seasontype": seasontype,
        })
    return out


def current_week() -> tuple[int, int, int]:
    d = _get(f"{BASE}/scoreboard")
    return d["season"]["year"], d["week"]["number"], d["season"]["type"]


def summary(event_id: str, refresh: bool = False) -> dict:
    p = game_dir(event_id) / "espn_summary.json"
    if p.exists() and not refresh:
        return json.loads(p.read_text(encoding="utf-8"))
    d = _get(f"{BASE}/summary", {"event": event_id})
    p.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    return d


def clock_to_sec(s: str) -> int | None:
    m = re.match(r"^(\d{1,2}):(\d{2})$", (s or "").strip())
    return int(m[1]) * 60 + int(m[2]) if m else None


def norm_down(s: str | None) -> str:
    """'1st & 10' / '1ST&10' / '4th & Goal' -> '1ST&10' / '4TH&GOAL'."""
    if not s:
        return ""
    s = s.upper().replace(" ", "").replace("INCHES", "1").replace("IN", "1")
    m = re.match(r"^([1-4])(ST|ND|RD|TH)&(\d{1,2}|GOAL)$", s)
    return f"{m[1]}{m[2]}&{m[3]}" if m else ""


def game_info(summ: dict) -> dict:
    comp = summ["header"]["competitions"][0]
    teams = {c["homeAway"]: c for c in comp["competitors"]}
    return {
        "season": summ["header"]["season"]["year"], "week": summ["header"].get("week"),
        "away": teams["away"]["team"]["displayName"], "home": teams["home"]["team"]["displayName"],
        "away_abbr": teams["away"]["team"]["abbreviation"], "home_abbr": teams["home"]["team"]["abbreviation"],
        "away_id": teams["away"]["team"]["id"], "home_id": teams["home"]["team"]["id"],
        "away_score": teams["away"].get("score"), "home_score": teams["home"].get("score"),
    }


def roster(summ: dict) -> dict:
    """Trả về {'T.Loop': 'Tyler Loop', ...} và danh sách họ để gợi ý cho Whisper."""
    abbr, lastnames = {}, set()
    for team in summ.get("boxscore", {}).get("players", []):
        for st in team.get("statistics", []):
            for a in st.get("athletes", []):
                ath = a["athlete"]
                fn, ln = ath.get("firstName", ""), ath.get("lastName", "")
                if fn and ln:
                    abbr[f"{fn[0]}.{ln}"] = ath["displayName"]
                    lastnames.add(ln)
    return {"abbr": abbr, "lastnames": sorted(lastnames)}


PLAYER_RE = re.compile(r"\b([A-Z][a-z]?\.[A-Z][A-Za-z'\-]+(?:-[A-Z][A-Za-z]+)?)")


def plays(summ: dict) -> list[dict]:
    """Chuẩn hoá play-by-play thành danh sách pha."""
    ros = roster(summ)
    out, prev = [], (0, 0)
    for dr in summ.get("drives", {}).get("previous", []):
        team = dr.get("team", {}).get("abbreviation", "")
        for p in dr.get("plays", []):
            typ = p.get("type", {}).get("text", "")
            clock = p.get("clock", {}).get("displayValue", "")
            txt = p.get("text", "")
            abbrs = list(dict.fromkeys(PLAYER_RE.findall(txt)))
            names = [ros["abbr"].get(a, a) for a in abbrs]
            item = {
                "pid": p["id"], "seq": int(p.get("sequenceNumber", 0) or 0),
                "q": p.get("period", {}).get("number"), "clock": clock, "clock_sec": clock_to_sec(clock),
                "type": typ, "type_vi": TYPE_VI.get(typ, typ), "text": txt, "team": team,
                "down": norm_down(p.get("start", {}).get("shortDownDistanceText")),
                "yardline": p.get("start", {}).get("possessionText", ""),
                "yards": p.get("statYardage", 0),
                "scoring": bool(p.get("scoringPlay")), "turnover": bool(p.get("isTurnover")),
                "score_before": prev, "score_after": (p.get("awayScore", 0), p.get("homeScore", 0)),
                "players": names,
                "is_play": typ not in NON_PLAYS,
            }
            prev = item["score_after"]
            out.append(item)
    for i, it in enumerate(out):
        it["idx"] = i  # thứ tự thực của pha trong trận (sequenceNumber của ESPN nhảy theo bước 100)
    return out
