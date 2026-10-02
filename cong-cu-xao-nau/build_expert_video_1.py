import subprocess
from pathlib import Path

pkg = Path(r"C:\Users\Thien\Downloads\kho video\CapCut_Project_Package")
data_clips = Path(r"d:\HIeu\content tong hop\cong-cu-xao-nau\data\clips")

cbs_src = Path(r"C:\Users\Thien\Downloads\kho video\YTSave_YouTube_Media_OAMvk1znLuw_What-s-making-the-Chiefs-good-again-The-NFL-Today_002_720p.mp4")
walker_hl = pkg / "02_Highlight_Kenneth_Walker.mp4"
kelce_hl = pkg / "03_Travis_Kelce_Reboot.mp4"

output_v1 = pkg / "01_Expert_CBS_With_Highlights.mp4"
temp_dir = data_clips / "v1_temp"
temp_dir.mkdir(parents=True, exist_ok=True)

print("1. Slicing Expert Video 1 (CBS) with Speaker Focus & Highlights...")

# Part 1A: 104.0s -> 125.6s (21.6s) - Bill Cowher opening breakdown (already close-up on Cowher)
p1 = temp_dir / "p1.mp4"
subprocess.run([
    "ffmpeg", "-y", "-ss", "104.0", "-i", str(cbs_src), "-t", "21.6",
    "-vf", "scale=1280:720,fps=30",
    "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(p1)
], check=True, capture_output=True)

# Part 1B (HIGHLIGHT 1): 125.6s -> 136.0s (10.4s) - Kenneth Walker 73-yard run with CBS commentary
# We take the audio from CBS (125.6 to 136.0) and video from Walker highlight!
p2_audio = temp_dir / "p2_audio.aac"
subprocess.run([
    "ffmpeg", "-y", "-ss", "125.6", "-i", str(cbs_src), "-t", "10.4",
    "-vn", "-c:a", "aac", str(p2_audio)
], check=True, capture_output=True)

p2 = temp_dir / "p2.mp4"
subprocess.run([
    "ffmpeg", "-y", "-ss", "0.0", "-i", str(walker_hl), "-i", str(p2_audio), "-t", "10.4",
    "-map", "0:v", "-map", "1:a",
    "-vf", "scale=1280:720,fps=30",
    "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(p2)
], check=True, capture_output=True)

# Part 1C: 136.0s -> 204.0s (68.0s) - Bill Cowher & Nate Burleson on Toughness
p3 = temp_dir / "p3.mp4"
subprocess.run([
    "ffmpeg", "-y", "-ss", "136.0", "-i", str(cbs_src), "-t", "68.0",
    "-vf", "scale=1280:720,fps=30",
    "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(p3)
], check=True, capture_output=True)

# Part 1D (HIGHLIGHT 2): 204.0s -> 216.0s (12.0s) - Travis Kelce wide open catch & spike
p4_audio = temp_dir / "p4_audio.aac"
subprocess.run([
    "ffmpeg", "-y", "-ss", "204.0", "-i", str(cbs_src), "-t", "12.0",
    "-vn", "-c:a", "aac", str(p4_audio)
], check=True, capture_output=True)

p4 = temp_dir / "p4.mp4"
subprocess.run([
    "ffmpeg", "-y", "-ss", "0.0", "-i", str(kelce_hl), "-i", str(p4_audio), "-t", "12.0",
    "-map", "0:v", "-map", "1:a",
    "-vf", "scale=1280:720,fps=30",
    "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(p4)
], check=True, capture_output=True)

# Part 1E: 216.0s -> 235.0s (19.0s) - Play action wrap-up
p5 = temp_dir / "p5.mp4"
subprocess.run([
    "ffmpeg", "-y", "-ss", "216.0", "-i", str(cbs_src), "-t", "19.0",
    "-vf", "scale=1280:720,fps=30",
    "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(p5)
], check=True, capture_output=True)

print("2. Concatenating into final Expert Video 1...")
concat_txt = temp_dir / "concat.txt"
with open(concat_txt, "w", encoding="utf-8") as f:
    for p in [p1, p2, p3, p4, p5]:
        f.write(f"file '{p.resolve().as_posix()}'\n")

subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt),
    "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-c:a", "aac", "-b:a", "192k",
    str(output_v1)
], check=True, capture_output=True)

print("SUCCESS! Created Expert Video 1:", output_v1)
