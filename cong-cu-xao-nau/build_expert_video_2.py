import subprocess
from pathlib import Path

pkg = Path(r"C:\Users\Thien\Downloads\kho video\CapCut_Project_Package")
data_clips = Path(r"d:\HIeu\content tong hop\cong-cu-xao-nau\data\clips")

src_video = Path(r"C:\Users\Thien\Downloads\kho video\YTSave_YouTube_Media_WgXeLu4OjMU_Ryan-Clark-Life-After-ESPN-The-Eagles-Problems-Mahomes-Chiefs_002_720p.mp4")
output_v2 = pkg / "02_Expert_RyanClark_StephenA_Focused.mp4"
temp_dir = data_clips / "v2_temp"
temp_dir.mkdir(parents=True, exist_ok=True)

print("1. Slicing Expert Video 2 (Stephen A. & Ryan Clark) with 1-Person Focus...")

# Part 2A: 1311.4s -> 1324.5s (13.1s) - Stephen A. Smith asking the question -> Focus on Stephen A.
stephen_clip = temp_dir / "stephen.mp4"
subprocess.run([
    "ffmpeg", "-y", "-ss", "1311.4", "-i", str(src_video), "-t", "13.1",
    "-vf", "crop=560:630:30:50,scale=1280:720,fps=30",
    "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(stephen_clip)
], check=True, capture_output=True)

# Part 2B: 1324.5s -> 1433.0s (108.5s) - Ryan Clark passionate response -> Focus on Ryan Clark
ryan_clip = temp_dir / "ryan.mp4"
subprocess.run([
    "ffmpeg", "-y", "-ss", "1324.5", "-i", str(src_video), "-t", "108.5",
    "-vf", "crop=560:630:690:50,scale=1280:720,fps=30",
    "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(ryan_clip)
], check=True, capture_output=True)

print("2. Concatenating into final Expert Video 2...")
concat_txt = temp_dir / "concat.txt"
with open(concat_txt, "w", encoding="utf-8") as f:
    f.write(f"file '{stephen_clip.resolve().as_posix()}'\n")
    f.write(f"file '{ryan_clip.resolve().as_posix()}'\n")

subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt),
    "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-c:a", "aac", "-b:a", "192k",
    str(output_v2)
], check=True, capture_output=True)

print("SUCCESS! Created Expert Video 2:", output_v2)
