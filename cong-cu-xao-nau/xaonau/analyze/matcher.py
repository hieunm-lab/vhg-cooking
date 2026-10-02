"""Khớp video highlight với play-by-play ESPN và băm thành từng pha có nhãn.

Ý tưởng:
- Thanh tỷ số hiển thị trạng thái TRƯỚC khi phát bóng của pha đang chiếu (hiệp, đồng hồ, down).
- Gom các giây liên tiếp có cùng trạng thái thành "lượt" (run). Mỗi lượt ~ một pha.
- Tìm trong play-by-play pha có cùng hiệp, cùng down, đồng hồ lúc phát bóng nằm trong khoảng đồng hồ thấy trên màn hình.
- Phần không có thanh tỷ số ngay sau pha (replay, ăn mừng, cận cảnh) được gắn vào pha đó.
"""
import bisect
from collections import Counter

from ..nfl import norm_down
from .transcribe import text_between
from .video import frame_kind

KICK_TYPES = {"Kickoff", "Extra Point Good", "Field Goal Good", "Field Goal Missed", "Blocked Field Goal",
              "Punt", "Kickoff Return Touchdown", "Two Point Conversion"}


def smooth_states(states: list[dict]) -> list[dict]:
    """Bỏ giá trị OCR đọc nhầm lẻ tẻ (vd '0:07' đọc thành '10:07'): lệch hẳn cả 2 giây kề bên mà 2 giây đó khớp nhau."""
    st = [dict(s) for s in states]
    val = [i for i, s in enumerate(st) if s["clock"] is not None]
    for a, i, b in zip(val, val[1:], val[2:]):
        pa, s, pb = st[a], st[i], st[b]
        if s["t"] - pa["t"] <= 3 and pb["t"] - s["t"] <= 3 and pa["q"] == pb["q"] and abs(pa["clock"] - pb["clock"]) <= 4:
            if abs(s["clock"] - pa["clock"]) > 6 or s["q"] != pa["q"]:
                s["clock"], s["q"] = pa["clock"], pa["q"]
    return st


def build_runs(states: list[dict]) -> list[dict]:
    runs, cur, prev = [], None, None
    for s in smooth_states(states):
        if s["clock"] is None:
            continue
        new = cur is None
        if cur is not None:
            gap = s["t"] - prev["t"]
            if s["q"] != cur["q"] or gap > 4:
                new = True
            elif s["down"] and cur["downs"] and s["down"] != cur["downs"].most_common(1)[0][0] and sum(cur["downs"].values()) >= 2:
                new = True
            elif s["clock"] > prev["clock"] + 2 or prev["clock"] - s["clock"] > 20:
                new = True
        if new:
            if cur:
                runs.append(cur)
            cur = {"t0": s["t"], "t1": s["t"] + 1, "q": s["q"], "cmax": s["clock"], "cmin": s["clock"], "downs": Counter()}
        cur["t1"] = s["t"] + 1
        cur["cmax"] = max(cur["cmax"], s["clock"]); cur["cmin"] = min(cur["cmin"], s["clock"])
        if s["down"]:
            cur["downs"][s["down"]] += 1
        prev = s
    if cur:
        runs.append(cur)
    for r in runs:
        r["down"] = r["downs"].most_common(1)[0][0] if r["downs"] else ""
        del r["downs"]
    return runs


def match_runs(runs, plays):
    last_seq = -1
    for r in runs:
        best, best_sc = None, -99
        for p in plays:
            if not p["is_play"] or p["q"] != r["q"] or p["clock_sec"] is None:
                continue
            if not (r["cmin"] - 3 <= p["clock_sec"] <= r["cmax"] + 6):
                continue
            sc = 0.0
            if r["down"] and p["down"]:
                sc += 3 if r["down"] == p["down"] else -3
            elif not p["down"] and p["type"] in KICK_TYPES:
                sc += 1
            sc -= abs(p["clock_sec"] - r["cmax"]) / 10
            if p["idx"] < last_seq:
                sc -= 4  # highlight chiếu theo thứ tự thời gian
            if p["type"] == "Penalty" and "No Play" in p["text"]:
                sc -= 1
            if sc > best_sc:
                best, best_sc = p, sc
        r["play"] = best if best_sc > -2 else None
        r["match_score"] = round(best_sc, 2)
        r["also"] = []
        if r["play"]:
            # các pha khác cùng nằm trong khoảng đồng hồ của lượt này (footage liền mạch 2 pha)
            pi = r["play"]["idx"]
            also = [p for p in plays if p["is_play"] and p["q"] == r["q"] and p["clock_sec"] is not None
                    and p["pid"] != r["play"]["pid"] and r["cmin"] - 1 <= p["clock_sec"] <= r["cmax"] + 1
                    and abs(p["idx"] - pi) <= 3 and p["type"] not in ("Penalty",)
                    # cùng down với lượt (footage liền 2 pha), hoặc cú giao bóng ngay sau pha ghi điểm
                    and ((r["down"] and p["down"] == r["down"]) or (p["idx"] == pi + 1 and p["type"] == "Kickoff"))]
            # pha ghi điểm được ưu tiên làm nhãn chính
            sc_also = [p for p in also if p["scoring"]]
            if sc_also and not r["play"]["scoring"]:
                also.append(r["play"]); r["play"] = sc_also[0]; also.remove(sc_also[0])
            r["also"] = also
            last_seq = max(last_seq, r["play"]["idx"])
    return runs


def infer_missing(segs: list[dict], plays: list[dict]) -> list[dict]:
    """Pha ghi điểm chưa tìm thấy (thường do đài ẩn thanh tỷ số lúc ghi điểm) -> gán vào đoạn ngay trước nó
    trong cùng chuỗi tấn công nếu lời bình luận viên nhắc tới (touchdown / field goal / tên cầu thủ)."""
    found = {s.get("pid") for s in segs} | {a["pid"] for s in segs for a in s.get("also", [])}
    for p in plays:
        if not p["scoring"] or p["pid"] in found or p["type"] == "Extra Point Good":
            continue
        # đoạn cuối cùng đã biết đứng TRƯỚC pha này (cùng đội tấn công, cách tối đa 8 pha)
        k_prev = None
        for k, s in enumerate(segs):
            if s.get("idx") is not None and s["idx"] < p["idx"]:
                k_prev = k
            elif s.get("idx") is not None and s["idx"] > p["idx"]:
                break
        if k_prev is None or segs[k_prev].get("team") != p["team"] or p["idx"] - segs[k_prev]["idx"] > 8:
            continue
        # xét đoạn đó và các đoạn chưa xác định ngay sau nó (trước pha đã biết kế tiếp)
        cands = [segs[k_prev]]
        for s in segs[k_prev + 1:]:
            if s.get("idx") is not None:
                break
            cands.append(s)
        keys = ["touchdown", "end zone", "into the end"] if "Touchdown" in p["type"] else \
            ["field goal", "it's good", "kick is good", "through", "puts it"]
        names = [n.split()[-1].lower() for n in p["players"][:2]]
        best = None
        for s in cands:
            c = s.get("commentary", "").lower()
            sc = 2 * any(k in c for k in keys) + any(n in c for n in names)
            if sc and (best is None or sc > best[0]):
                best = (sc, s)
        if not best:
            continue
        s = best[1]
        if s.get("pid") is None:  # đoạn chưa xác định -> gán thẳng nhãn pha
            tags = [p["type_vi"], "ghi điểm"] + (["phút cuối"] if p["q"] >= 4 and (p["clock_sec"] or 999) <= 120 else [])
            s.update({"pid": p["pid"], "seq": p["seq"], "idx": p["idx"], "type": p["type"],
                      "type_vi": p["type_vi"] + " (suy ra)", "text": p["text"], "clock": p["clock"], "down": p["down"],
                      "yardline": p["yardline"], "yards": p["yards"], "team": p["team"], "players": p["players"],
                      "mentioned": [n for n in p["players"] if n.split()[-1].lower() in s.get("commentary", "").lower()],
                      "score_after": p["score_after"], "scoring": True, "confidence": "trung bình",
                      "tags": tags, "kind": "pha", "q": p["q"]})
        else:
            s.setdefault("also", []).append({"pid": p["pid"], "type_vi": p["type_vi"] + " (suy ra từ lời bình luận)",
                                             "text": p["text"], "players": p["players"]})
            s["tags"] = list(dict.fromkeys(s.get("tags", []) + ["ghi điểm"]))
        found.add(p["pid"])
    return segs


def _snap_back(t, cut_starts, maxd=2.0):
    i = bisect.bisect_right(cut_starts, t) - 1
    if i >= 0 and t - cut_starts[i] <= maxd:
        return cut_starts[i]
    return t


def build_segments(runs, shots, per_sec, words, loud, duration, hop=0.25):
    cut_starts = [a for a, b in shots]
    # gộp lượt ngắn (<2.5s) không khớp pha vào lượt trước; gộp lượt liền nhau cùng một pha
    merged = []
    for r in runs:
        short = r["t1"] - r["t0"] < 2.5
        if merged and ((short and not r.get("play")) or
                       (r.get("play") and merged[-1].get("play") and r["play"]["pid"] == merged[-1]["play"]["pid"])):
            merged[-1]["t1"] = max(merged[-1]["t1"], r["t1"])
            continue
        merged.append(dict(r))
    segs = []
    first = _snap_back(merged[0]["t0"], cut_starts) if merged else duration
    if first > 3:
        segs.append({"start": 0.0, "end": first, "live_end": 0.0, "kind": "mo_dau", "play": None, "run": None})
    for i, r in enumerate(merged):
        st = _snap_back(r["t0"], cut_starts)
        nxt = _snap_back(merged[i + 1]["t0"], cut_starts) if i + 1 < len(merged) else duration
        end = nxt
        tail = None
        if nxt - r["t1"] > 30:  # khoảng trống quá dài sau pha -> tách phần dư thành B-roll riêng
            end = r["t1"] + 15
            tail = (end, nxt)
        kind = "pha" if r.get("play") else "khong_ro"
        # đoạn không xác định ngắn (<10s) ngay sau một pha thường là replay của pha đó -> gộp vào
        if kind == "khong_ro" and end - st < 10 and segs and segs[-1]["kind"] == "pha":
            segs[-1]["end"] = end
            continue
        segs.append({"start": st, "end": end, "live_end": min(r["t1"], end), "kind": kind,
                     "play": r.get("play"), "run": r})
        if tail:
            segs.append({"start": tail[0], "end": tail[1], "live_end": tail[0], "kind": "broll", "play": None, "run": None})
    out = []
    for k, s in enumerate(segs):
        a, b = s["start"], s["end"]
        secs = per_sec[int(a):max(int(a) + 1, int(b))]
        kinds = Counter(frame_kind(x) for x in secs)
        tot = max(1, sum(kinds.values()))
        # khoảnh khắc đỉnh: độ ồn lớn nhất trong phần pha đang diễn ra (+3s)
        la, lb = int(a / hop), int(min(b, (s["live_end"] or b) + 3) / hop)
        peak = a
        if lb > la and loud:
            window = loud[la:lb]
            if window:
                peak = round((la + window.index(max(window))) * hop, 2)
        txt = text_between(words, a, b)
        p = s["play"]
        seg = {
            "id": k + 1, "start": round(a, 2), "end": round(b, 2), "dur": round(b - a, 1),
            "live_end": round(s["live_end"], 2), "peak": peak, "kind": s["kind"],
            "pct_san": round(100 * kinds.get("san", 0) / tot), "pct_can": round(100 * kinds.get("can", 0) / tot),
            "n_shots": sum(1 for x, y in shots if a <= x < b), "commentary": txt,
            "q": s["run"]["q"] if s["run"] else None,
            "clock_screen": s["run"]["cmax"] if s["run"] else None,
            "down_screen": s["run"]["down"] if s["run"] else "",
        }
        if p:
            names = p["players"]
            mentioned = [n for n in names if n.split()[-1].lower() in txt.lower()]
            down_ok = bool(s["run"]["down"]) and s["run"]["down"] == p["down"]
            conf = "cao" if (down_ok and (mentioned or p["scoring"])) else ("trung bình" if down_ok or not p["down"] else "thấp")
            tags = [p["type_vi"]]
            if p["scoring"]:
                tags.append("ghi điểm")
            if p["turnover"]:
                tags.append("mất bóng")
            if abs(p["yards"] or 0) >= 20:
                tags.append("pha dài")
            if p["q"] >= 4 and (p["clock_sec"] or 999) <= 120:
                tags.append("phút cuối")
            also = s["run"].get("also", [])
            seg["also"] = [{"pid": x["pid"], "type_vi": x["type_vi"], "text": x["text"], "players": x["players"]} for x in also]
            for x in also:
                if x["scoring"]:
                    tags.append("ghi điểm")
                if abs(x["yards"] or 0) >= 20:
                    tags.append("pha dài")
            tags = list(dict.fromkeys(tags))
            seg.update({"pid": p["pid"], "seq": p["seq"], "idx": p["idx"], "type": p["type"], "type_vi": p["type_vi"], "text": p["text"],
                        "clock": p["clock"], "down": p["down"], "yardline": p["yardline"], "yards": p["yards"],
                        "team": p["team"], "players": names, "mentioned": mentioned, "score_after": p["score_after"],
                        "scoring": p["scoring"], "confidence": conf, "tags": tags})
        else:
            label = {"mo_dau": "Mở đầu / không khí sân", "broll": "B-roll (replay, khán giả, cận cảnh)",
                     "khong_ro": "Chưa xác định pha"}[s["kind"]]
            seg.update({"pid": None, "type": s["kind"], "type_vi": label, "text": "", "players": [], "mentioned": [], "also": [],
                        "confidence": "thấp" if s["kind"] == "khong_ro" else "-", "tags": [label]})
        out.append(seg)
    return out
