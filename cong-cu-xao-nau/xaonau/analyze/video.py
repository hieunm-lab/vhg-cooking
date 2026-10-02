"""Phân tích hình và tiếng: điểm cắt cảnh, loại khung hình theo giây, độ ồn theo thời gian."""
import subprocess
import wave

import cv2
import numpy as np

from ..config import FFMPEG, NO_WINDOW


def probe_duration(path) -> float:
    cap = cv2.VideoCapture(str(path))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    n = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    cap.release()
    return n / fps


def shots_and_frames(path, progress=None) -> dict:
    """Quét video 5 khung/giây.
    Trả về: shots [(start, end)], per_sec [{'green','dark','motion'}] để phân loại khung hình."""
    cap = cv2.VideoCapture(str(path))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    step = max(1, int(round(fps / 5)))
    cuts, prev_h, prev_g = [0.0], None, None
    per = {}
    i = 0
    while True:
        if not cap.grab():
            break
        if i % step == 0:
            ok, f = cap.retrieve()
            if not ok:
                break
            t = i / fps
            small = cv2.resize(f, (160, 90))
            hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)
            h = cv2.calcHist([hsv], [0, 1], None, [32, 16], [0, 180, 0, 256])
            cv2.normalize(h, h)
            g = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY).astype(np.float32)
            m = 0.0
            if prev_h is not None:
                d = cv2.compareHist(prev_h, h, cv2.HISTCMP_BHATTACHARYYA)
                m = float(np.mean(np.abs(g - prev_g)))
                if (d > 0.35 or (d > 0.2 and m > 40)) and t - cuts[-1] > 0.4:
                    cuts.append(round(t, 2))
            prev_h, prev_g = h, g
            green = float(np.mean((hsv[..., 0] > 30) & (hsv[..., 0] < 85) & (hsv[..., 1] > 60) & (hsv[..., 2] > 50)))
            dark = float(np.mean(hsv[..., 2] < 25))
            per.setdefault(int(t), []).append((green, dark, m))
            if progress and i % (step * 150) == 0:
                progress(i / max(1, n))
        i += 1
    cap.release()
    dur = n / fps
    cuts.append(round(dur, 2))
    shots = [(a, b) for a, b in zip(cuts[:-1], cuts[1:])]
    per_sec = []
    for s in range(int(dur) + 1):
        v = per.get(s, [(0, 0, 0)])
        per_sec.append({"green": round(float(np.mean([x[0] for x in v])), 3),
                        "dark": round(float(np.mean([x[1] for x in v])), 3),
                        "motion": round(float(np.mean([x[2] for x in v])), 1)})
    return {"duration": dur, "shots": shots, "per_sec": per_sec}


def frame_kind(ps: dict) -> str:
    """Phân loại khung hình: 'san' (toàn cảnh sân), 'can' (cận cảnh/khán giả/khác), 'den' (màn đen)."""
    if ps["dark"] > 0.85:
        return "den"
    if ps["green"] > 0.28:
        return "san"
    return "can"


def extract_wav(video, wav, sr=16000):
    subprocess.run([FFMPEG, "-v", "error", "-y", "-i", str(video), "-vn", "-ac", "1", "-ar", str(sr), str(wav)],
                   check=True, **NO_WINDOW)
    return wav


def loudness(wav, hop=0.25) -> list[float]:
    """Độ ồn (RMS, dB) mỗi 0,25 giây — tiếng khán giả + bình luận viên vọt lên ở khoảnh khắc đỉnh của pha."""
    with wave.open(str(wav), "rb") as w:
        sr = w.getframerate()
        a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    k = int(sr * hop)
    n = len(a) // k
    a = a[: n * k].reshape(n, k)
    rms = np.sqrt(np.mean(a ** 2, axis=1) + 1e-9)
    return [round(float(x), 1) for x in 20 * np.log10(rms)]
