import subprocess
from pathlib import Path

out_dir = Path("data/clips/cowboys_frames")
out_dir.mkdir(parents=True, exist_ok=True)

# Extract frames every 1 second from 0 to 18s
for s in range(0, 19):
    cmd = [
        "ffmpeg", "-y", "-ss", str(s), "-i", "data/clips/cowboys_report_hook.webm",
        "-vframes", "1", "-q:v", "2", str(out_dir / f"f_{s:02d}s.jpg")
    ]
    subprocess.run(cmd, capture_output=True)

print("Frames 0s to 18s extracted to data/clips/cowboys_frames")
