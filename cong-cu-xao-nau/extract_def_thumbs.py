import subprocess
from pathlib import Path

out_dir = Path("data/clips/play_inspect_exact")
src_def = Path("data/clips/chiefs_defense_sacks.mkv")

# Let's inspect:
# 1. Strip sack: 0s to 6s
# 2. Fumble TD: 32s to 43s
# 3. Blitz sack: 52s to 59s
# 4. Frank Clark sack: 79s to 87s

plays = [
    ("def_strip_sack", 0, 6),
    ("def_fumble_td", 33, 10),
    ("def_blitz_sack", 52, 7),
    ("def_clark_sack", 79, 8)
]

for name, s, d in plays:
    cmd = [
        "ffmpeg", "-y", "-ss", str(s), "-t", str(d),
        "-i", str(src_def),
        "-vf", "fps=1",
        str(out_dir / f"{name}_%02d.jpg")
    ]
    subprocess.run(cmd, capture_output=True)

print("Defense play thumbnails extracted!")
