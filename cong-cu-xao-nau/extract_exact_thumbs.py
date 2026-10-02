import subprocess
from pathlib import Path

out_dir = Path("data/clips/play_inspect_exact")
out_dir.mkdir(parents=True, exist_ok=True)

src_dolphins = Path("data/clips/raw_sources/week3_dolphins.webm")

# Let's inspect:
# 1. Kelce 48yd deep: 34s to 45s
# 2. Walker 10yd TD: 61s to 71s
# 3. Walker 5yd TD catch: 242s to 252s
# 4. Worthy 17yd catch: 302s to 311s
# 5. Walker 22yd run: 405s to 415s
# 6. Kelce 11yd TD: 761s to 772s

plays_to_extract = [
    ("kelce_48yd", 33, 11),
    ("walker_10yd_td", 61, 10),
    ("walker_5yd_td", 242, 10),
    ("worthy_17yd", 302, 9),
    ("walker_22yd", 405, 10),
    ("kelce_11yd_td", 761, 11),
]

for name, s, d in plays_to_extract:
    cmd = [
        "ffmpeg", "-y", "-ss", str(s), "-t", str(d),
        "-i", str(src_dolphins),
        "-vf", "fps=1",
        str(out_dir / f"{name}_%02d.jpg")
    ]
    subprocess.run(cmd, capture_output=True)

print("Exact play thumbnails extracted!")
