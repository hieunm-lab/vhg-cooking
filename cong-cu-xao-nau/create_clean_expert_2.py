import subprocess
from pathlib import Path

pkg = Path(r"C:\Users\Thien\Downloads\kho video\CapCut_Project_Package")
src_v2 = Path(r"C:\Users\Thien\Downloads\kho video\YTSave_YouTube_Media_WgXeLu4OjMU_Ryan-Clark-Life-After-ESPN-The-Eagles-Problems-Mahomes-Chiefs_002_720p.mp4")
out_v2 = pkg / "02_Expert_RyanClark_Clean_Voice.mp4"

crop_stephen = "crop=500:281:20:70,scale=1280:720,fps=30"
crop_ryan = "crop=500:281:755:80,scale=1280:720,fps=30"

p1 = pkg / "v2_part1.mp4"
p2 = pkg / "v2_part2.mp4"
concat_txt = pkg / "v2_concat.txt"

print("Rendering Part 1 (Stephen A)...")
subprocess.run([
    "ffmpeg", "-y", "-ss", "1311.4", "-i", str(src_v2), "-t", "13.1",
    "-vf", crop_stephen, "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(p1)
], check=True)

print("Rendering Part 2 (Ryan Clark)...")
subprocess.run([
    "ffmpeg", "-y", "-ss", "1324.5", "-i", str(src_v2), "-t", "109.0",
    "-vf", crop_ryan, "-af", "afade=t=out:st=107.5:d=1.5", "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(p2)
], check=True)

with open(concat_txt, "w", encoding="utf-8") as f:
    f.write(f"file '{p1.resolve().as_posix()}'\n")
    f.write(f"file '{p2.resolve().as_posix()}'\n")

print("Concatenating into clean Video 2...")
subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt),
    "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-c:a", "aac", "-b:a", "192k",
    str(out_v2)
], check=True)

p1.unlink(missing_ok=True)
p2.unlink(missing_ok=True)
concat_txt.unlink(missing_ok=True)
print("SUCCESS:", out_v2)
