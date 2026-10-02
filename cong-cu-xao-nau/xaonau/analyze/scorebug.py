"""Đọc thanh tỷ số (scorebug) của sóng truyền hình: hiệp, đồng hồ, down & distance, tỷ số.

Cách làm:
1. learn_layout: chạy OCR đầy đủ trên ~20 khung hình rải đều để tìm vị trí cố định của các ô chữ
   (đồng hồ, hiệp, down). Ưu tiên thanh ở đáy màn hình để bỏ qua ticker tỷ số các trận khác.
2. read_states: với mỗi giây, chỉ nhận dạng chữ ở đúng các ô đã học (bỏ bước dò tìm) -> nhanh ~15 lần.
"""
import re

import cv2
import numpy as np

_ocr = None


def ocr():
    global _ocr
    if _ocr is None:
        from rapidocr_onnxruntime import RapidOCR
        _ocr = RapidOCR()
    return _ocr


CLOCK_RE = re.compile(r"^(\d{1,2}):(\d{2})$")
Q_RE = re.compile(r"^(1ST|2ND|3RD|4TH|OT)$")
QC_RE = re.compile(r"^(1ST|2ND|3RD|4TH|OT)(\d{1,2}:\d{2})$")
DOWN_RE = re.compile(r"^([1-4])(ST|ND|RD|TH)&(\d{1,2}|GOAL)$")
Q_NUM = {"1ST": 1, "2ND": 2, "3RD": 3, "4TH": 4, "OT": 5}


def _clean(s: str) -> str:
    return s.upper().replace(" ", "").replace(".", ":").replace(";", ":")


def _fix_digits(s: str) -> str:
    return s.replace("O", "0").replace("I", "1").replace("L", "1").replace("S", "5").replace("B", "8")


def parse_clock(s: str, strict: bool = True):
    # dưới 1 phút nhiều đài hiện dạng "12.3" (giây + phần mười)
    m = re.match(r"^:?(\d{1,2})\.(\d)$", s.strip())
    if m:
        return int(m[1])
    s = _fix_digits(_clean(s))
    m = CLOCK_RE.match(s) if strict else re.search(r"(\d{1,2}):(\d{2})", s)
    if not m or int(m[2]) >= 60:
        return None
    mins = int(m[1])
    if mins > 15 and not strict:
        mins = int(m[1][-1])  # "19:47" = chữ của ô bên cạnh dính vào -> "9:47"
    return mins * 60 + int(m[2]) if mins <= 15 else None


def _fix_ord(s: str) -> str:
    return _clean(s).replace("IST", "1ST").replace("ZND", "2ND").replace("SRD", "3RD").replace("ATH", "4TH")


def parse_quarter(s: str, strict: bool = True):
    s = _fix_ord(s)
    m = Q_RE.match(s) if strict else re.search(r"(1ST|2ND|3RD|4TH|OT)", s)
    if m:
        return Q_NUM[m[1]]
    # OCR hay đọc lệch hậu tố: "1SR", "1S", "2N", "20", "3R", "4T"… (vị trí ô đã đảm bảo đây là ô hiệp)
    m = re.match(r"^([1-4])(ST|SR|SI|S|ND|N|NO|N0|0|O|RD|R|TH|T|TN)$", s) if strict else \
        re.search(r"(?<![\d:])([1-4])(ST|SR|SI|ND|NO|N0|RD|TH|TN|S|N|R|T|0|O)?(?![\d:])", s)
    return int(m[1]) if m else None


def parse_down(s: str, strict: bool = True):
    s = _fix_ord(s).replace("INCHES", "1")
    m = DOWN_RE.match(s) if strict else re.search(r"([1-4])(ST|ND|RD|TH)&(\d{1,2}|GOAL)", s)
    return f"{m[1]}{m[2]}&{m[3]}" if m else ""


def _frame_at(cap, t):
    cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
    ok, f = cap.read()
    return f if ok else None


def _box(pts):
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    return [min(xs), min(ys), max(xs), max(ys)]


def learn_layout(video, duration, n=20, log=print) -> dict | None:
    cap = cv2.VideoCapture(str(video))
    W = cap.get(cv2.CAP_PROP_FRAME_WIDTH); H = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    found = []  # mỗi khung: {'clock': box, 'q': box, 'down': box|None}
    for k in range(n):
        t = duration * (0.08 + 0.84 * k / max(1, n - 1))
        f = _frame_at(cap, t)
        if f is None:
            continue
        res, _ = ocr()(f)
        if not res:
            continue
        items = [(_box(b), _clean(txt)) for b, txt, sc in res]
        # chấp nhận cả trường hợp đồng hồ dính đồng hồ phát bóng: "1:5840"
        clocks = [(b, x) for b, x in items if parse_clock(x) is not None or re.match(r"^\d{1,2}:\d{2}\d{1,2}$", x)]
        qs = [(b, x) for b, x in items if parse_quarter(x)]
        # trường hợp OCR dính "1ST8:14" thành một ô
        for b, x in items:
            m = QC_RE.match(x)
            if m:
                w = b[2] - b[0]
                qs.append(([b[0], b[1], b[0] + w * 0.4, b[3]], m[1]))
                clocks.append(([b[0] + w * 0.4, b[1], b[2], b[3]], m[2]))
        downs = [(b, x) for b, x in items if parse_down(x)]
        best = None
        for cb, _ in clocks:
            ch = cb[3] - cb[1]
            for qb, qx in qs:
                cy, qy = (cb[1] + cb[3]) / 2, (qb[1] + qb[3]) / 2
                same_line = abs(cy - qy) < 0.6 * ch
                exact = bool(Q_RE.match(qx))
                left_gap = cb[0] - qb[2]  # ô hiệp thường nằm ngay bên trái đồng hồ
                right_gap = qb[0] - cb[2]
                # dạng đọc lệch ("1SR", "20") chỉ nhận khi nằm bên trái — bên phải thường là đồng hồ phát bóng "40"
                gap = left_gap if left_gap > -5 else (right_gap if (right_gap > -5 and exact) else None)
                if gap is None or gap > 0.12 * W:
                    if not (abs(cy - qy) < 0.08 * H and abs(cb[0] - qb[0]) < 0.3 * W):
                        continue
                    gap = 0.12 * W  # xếp chồng khác hàng: chấp nhận nhưng ưu tiên thấp
                # ưu tiên: cùng hàng, sát đồng hồ, thanh ở đáy màn hình
                score = (1.0 if same_line else 0.0) - gap / W + 0.5 * cy / H
                if best is None or score > best[0]:
                    best = (score, cb, qb)
        if best:
            _, cb, qb = best
            db = None
            for b, _ in downs:
                if abs((b[1] + b[3]) / 2 - (cb[1] + cb[3]) / 2) < 0.12 * H and abs(b[0] - cb[0]) < 0.35 * W:
                    db = b
            found.append({"clock": cb, "q": qb, "down": db})
    cap.release()
    if len(found) < 3:
        log(f"Không tìm thấy thanh tỷ số ổn định (chỉ thấy {len(found)} khung).")
        return None
    # gom cụm theo vị trí đồng hồ, lấy cụm đông nhất
    centers = np.array([[(f["clock"][0] + f["clock"][2]) / 2, (f["clock"][1] + f["clock"][3]) / 2] for f in found])
    best_i, best_n = 0, 0
    for i, c in enumerate(centers):
        nn = int(np.sum(np.linalg.norm(centers - c, axis=1) < 0.04 * W))
        if nn > best_n:
            best_i, best_n = i, nn
    grp = [f for f, c in zip(found, centers) if np.linalg.norm(c - centers[best_i]) < 0.04 * W]

    def union(key, padx, pady, widen=0.0):
        """Khung bao của một ô qua các khung hình, bỏ ngoại lai (dùng phân vị 20–80%)."""
        bs = np.array([g[key] for g in grp if g.get(key)], dtype=float)
        if not len(bs):
            return None
        x0 = np.percentile(bs[:, 0], 20); y0 = np.percentile(bs[:, 1], 20)
        x1 = np.percentile(bs[:, 2], 80); y1 = np.percentile(bs[:, 3], 80)
        w = x1 - x0
        return [max(0, int(x0 - padx - widen * w)), max(0, int(y0 - pady)),
                min(int(W), int(x1 + padx + widen * w)), min(int(H), int(y1 + pady))]

    def med(key):
        bs = np.array([g[key] for g in grp if g.get(key)], dtype=float)
        return np.median(bs, axis=0) if len(bs) else None

    mc, mq = med("clock"), med("q")
    lay = {"W": W, "H": H, "frames_found": len(grp),
           "clock": union("clock", 3, 3, 0.12), "q": union("q", 3, 3, 0.05), "down": union("down", 4, 3, 0.2)}
    raw_c, raw_q = (list(mc) if mc is not None else None), (list(mq) if mq is not None else None)
    # không cho ô "hiệp" và ô "đồng hồ" chồng lên nhau (nếu không OCR sẽ đọc "1ST|8" hoặc "19:47")
    if raw_c and raw_q:
        c, q = lay["clock"], lay["q"]
        if (raw_q[0] + raw_q[2]) / 2 < (raw_c[0] + raw_c[2]) / 2:
            q[2] = int(min(q[2], raw_c[0] - 1)); c[0] = int(max(c[0], raw_q[2] + 1))
        else:
            c[2] = int(min(c[2], raw_q[0] - 1)); q[0] = int(max(q[0], raw_c[2] + 1))
        # an toàn: nếu ô bị cắt hỏng thì dùng lại khung gốc
        if c[2] - c[0] < 8:
            lay["clock"] = [raw_c[0] - 2, raw_c[1] - 3, raw_c[2] + 3, raw_c[3] + 3]
        if q[2] - q[0] < 6:
            lay["q"] = [raw_q[0] - 2, raw_q[1] - 3, raw_q[2] + 2, raw_q[3] + 3]
    log(f"Đã học vị trí thanh tỷ số ({len(grp)}/{n} khung khớp): đồng hồ {lay['clock']}, hiệp {lay['q']}, down {lay['down']}")
    return lay


def _rec(img):
    if img is None or img.size == 0:
        return ""
    h = img.shape[0]
    if h < 28:
        s = 32 / h
        img = cv2.resize(img, None, fx=s, fy=s, interpolation=cv2.INTER_CUBIC)
    res, _ = ocr()(img, use_det=False, use_cls=False)
    if not res:
        return ""
    txt, sc = res[0][0], res[0][1]
    return txt if sc > 0.5 else ""


def read_states(video, lay, fps=1.0, progress=None) -> list[dict]:
    """Đọc trạng thái thanh tỷ số theo từng giây. Trả về [{t, q, clock, down}] (None nếu không có thanh)."""
    cap = cv2.VideoCapture(str(video))
    vfps = cap.get(cv2.CAP_PROP_FPS) or 30
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    step = max(1, int(round(vfps / fps)))
    out = []
    i = 0
    while True:
        if not cap.grab():
            break
        if i % step == 0:
            ok, f = cap.retrieve()
            if not ok:
                break
            st = {"t": round(i / vfps, 2), "q": None, "clock": None, "down": ""}

            def crop(b):
                return f[b[1]:b[3], b[0]:b[2]] if b else None
            c = parse_clock(_rec(crop(lay["clock"])), strict=False)
            if c is not None:
                q = parse_quarter(_rec(crop(lay["q"])), strict=False)
                if q:
                    st["q"], st["clock"] = q, c
                    if lay.get("down"):
                        st["down"] = parse_down(_rec(crop(lay["down"])), strict=False)
            out.append(st)
            if progress and len(out) % 50 == 0:
                progress(i / max(1, n))
        i += 1
    cap.release()
    return out
