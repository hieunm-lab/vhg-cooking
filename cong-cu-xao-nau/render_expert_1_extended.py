import subprocess
from pathlib import Path

pkg = Path(r"C:\Users\Thien\Downloads\kho video\CapCut_Project_Package")
data_clips = Path(r"d:\HIeu\content tong hop\cong-cu-xao-nau\data\clips")

cbs_src = Path(r"C:\Users\Thien\Downloads\kho video\YTSave_YouTube_Media_OAMvk1znLuw_What-s-making-the-Chiefs-good-again-The-NFL-Today_002_720p.mp4")
walker_src = pkg / "02_Highlight_Kenneth_Walker.mp4"
kelce_src = pkg / "03_Travis_Kelce_Reboot.mp4"
mahomes_dive_src = data_clips / "mahomes_run_raw.webm"

output_v1 = pkg / "01_Expert_CBS_Extended_With_Highlights.mp4"
temp_dir = data_clips / "v1_extended_temp"
temp_dir.mkdir(parents=True, exist_ok=True)

print("--- RENDERING EXPERT VIDEO 1 (CBS Extended 3m08s - Flawless Replacement) ---")

# Zoom filter to bypass copyright and focus on star player (crop 82% center and scale to 1280x720)
zoom_hl_filter = "crop=in_w*0.82:in_h*0.82:(in_w-out_w)/2:(in_h-out_h)/2,scale=1280:720,fps=30"

# Part 1: 101.4s -> 125.6s (24.2s) - Bill Cowher opening
c1 = temp_dir / "c1.mp4"
subprocess.run([
    "ffmpeg", "-y", "-ss", "101.4", "-i", str(cbs_src), "-t", "24.2",
    "-vf", "scale=1280:720,fps=30",
    "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(c1)
], check=True, capture_output=True)

# Part 2: 125.6s -> 138.0s (12.4s) - HIGHLIGHT: Kenneth Walker 73-yd run (Zoomed to bypass copyright & focus on Walker)
c2_audio = temp_dir / "c2_audio.aac"
subprocess.run([
    "ffmpeg", "-y", "-ss", "125.6", "-i", str(cbs_src), "-t", "12.4",
    "-vn", "-c:a", "aac", str(c2_audio)
], check=True, capture_output=True)

c2 = temp_dir / "c2.mp4"
subprocess.run([
    "ffmpeg", "-y", "-ss", "0.0", "-i", str(walker_src), "-i", str(c2_audio), "-t", "12.4",
    "-map", "0:v", "-map", "1:a",
    "-vf", zoom_hl_filter,
    "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(c2)
], check=True, capture_output=True)

# Part 3: 138.0s -> 204.0s (66.0s) - Bill Cowher & Nate Burleson on Toughness
c3 = temp_dir / "c3.mp4"
subprocess.run([
    "ffmpeg", "-y", "-ss", "138.0", "-i", str(cbs_src), "-t", "66.0",
    "-vf", "scale=1280:720,fps=30",
    "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(c3)
], check=True, capture_output=True)

# Part 4: 204.0s -> 218.0s (14.0s) - HIGHLIGHT: Travis Kelce catch & spike (Zoomed on Kelce)
c4_audio = temp_dir / "c4_audio.aac"
subprocess.run([
    "ffmpeg", "-y", "-ss", "204.0", "-i", str(cbs_src), "-t", "14.0",
    "-vn", "-c:a", "aac", str(c4_audio)
], check=True, capture_output=True)

c4 = temp_dir / "c4.mp4"
subprocess.run([
    "ffmpeg", "-y", "-ss", "0.0", "-i", str(kelce_src), "-i", str(c4_audio), "-t", "14.0",
    "-map", "0:v", "-map", "1:a",
    "-vf", zoom_hl_filter,
    "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(c4)
], check=True, capture_output=True)

# Part 5A: 218.0s -> 224.5s (6.5s) - HIGHLIGHT: Kenneth Walker (Replaces the CBS static stat card graphic!)
c5a_audio = temp_dir / "c5a_audio.aac"
subprocess.run([
    "ffmpeg", "-y", "-ss", "218.0", "-i", str(cbs_src), "-t", "6.5",
    "-vn", "-c:a", "aac", str(c5a_audio)
], check=True, capture_output=True)

c5a = temp_dir / "c5a.mp4"
subprocess.run([
    "ffmpeg", "-y", "-ss", "3.0", "-i", str(walker_src), "-i", str(c5a_audio), "-t", "6.5",
    "-map", "0:v", "-map", "1:a",
    "-vf", zoom_hl_filter,
    "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(c5a)
], check=True, capture_output=True)

# Part 5B: 224.5s -> 278.0s (53.5s) - Russell Wilson breakdown & studio discussion
c5b = temp_dir / "c5b.mp4"
subprocess.run([
    "ffmpeg", "-y", "-ss", "224.5", "-i", str(cbs_src), "-t", "53.5",
    "-vf", "scale=1280:720,fps=30",
    "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(c5b)
], check=True, capture_output=True)

# Part 6: 278.0s -> 284.0s (6.0s) - HIGHLIGHT: Mahomes dive in end zone game one (Zoomed on Mahomes)
c6_audio = temp_dir / "c6_audio.aac"
subprocess.run([
    "ffmpeg", "-y", "-ss", "278.0", "-i", str(cbs_src), "-t", "6.0",
    "-vn", "-c:a", "aac", str(c6_audio)
], check=True, capture_output=True)

c6 = temp_dir / "c6.mp4"
subprocess.run([
    "ffmpeg", "-y", "-ss", "8.0", "-i", str(mahomes_dive_src), "-i", str(c6_audio), "-t", "6.0",
    "-map", "0:v", "-map", "1:a",
    "-vf", "crop=in_w*0.80:in_h*0.80:(in_w-out_w)/2:(in_h-out_h)/2,scale=1280:720,fps=30",
    "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(c6)
], check=True, capture_output=True)

# Part 7: 284.0s -> 290.0s (6.0s) - Concluding sentence: 'critical' with clean fadeout
c7 = temp_dir / "c7.mp4"
subprocess.run([
    "ffmpeg", "-y", "-ss", "284.0", "-i", str(cbs_src), "-t", "6.0",
    "-vf", "scale=1280:720,fps=30",
    "-af", "afade=t=out:st=5.0:d=1.0",
    "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(c7)
], check=True, capture_output=True)

# Concatenate Part 1 to 7
concat_txt = temp_dir / "concat_v1.txt"
with open(concat_txt, "w", encoding="utf-8") as f:
    for c in [c1, c2, c3, c4, c5a, c5b, c6, c7]:
        f.write(f"file '{c.resolve().as_posix()}'\n")

subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt),
    "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-c:a", "aac", "-b:a", "192k",
    str(output_v1)
], check=True, capture_output=True)

print("SUCCESS! Created Video 1 Extended:", output_v1)
