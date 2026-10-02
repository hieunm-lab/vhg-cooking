import subprocess
from pathlib import Path

pkg = Path(r"C:\Users\Thien\Downloads\kho video\CapCut_Project_Package")
data_clips = Path(r"d:\HIeu\content tong hop\cong-cu-xao-nau\data\clips")

voice_path = data_clips / "test_hook_puck_smooth.mp3"
bgm_path = data_clips / "bgm_cinematic_tension.mp3"

raw_mahomes = data_clips / "mahomes_run_raw.webm"
raw_walker = pkg / "02_Highlight_Kenneth_Walker.mp4"
raw_kelce = pkg / "03_Travis_Kelce_Reboot.mp4"
raw_clark = pkg / "01_Soundbite_Ryan_Clark.mp4"

output_mp4 = pkg / "00_Hook_Cinematic_CowboysReport_Style.mp4"
temp_dir = data_clips / "cinematic_temp"
temp_dir.mkdir(parents=True, exist_ok=True)

print("1. Preparing 5 cinematic segments...")

# Clip 1: 0.0s - 6.1s (6.1s) - Mahomes play
c1 = temp_dir / "c1.mp4"
subprocess.run([
    "ffmpeg", "-y", "-ss", "5.5", "-i", str(raw_mahomes), "-t", "6.1",
    "-vf", "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,fps=30",
    "-c:v", "libx264", "-preset", "fast", "-an", str(c1)
], check=True, capture_output=True)

# Clip 2: 6.1s - 11.3s (5.2s) - Kenneth Walker
c2 = temp_dir / "c2.mp4"
subprocess.run([
    "ffmpeg", "-y", "-ss", "1.0", "-i", str(raw_walker), "-t", "5.2",
    "-vf", "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,fps=30",
    "-c:v", "libx264", "-preset", "fast", "-an", str(c2)
], check=True, capture_output=True)

# Clip 3: 11.3s - 15.0s (3.7s) - Ryan Clark reaction
c3 = temp_dir / "c3.mp4"
subprocess.run([
    "ffmpeg", "-y", "-ss", "2.0", "-i", str(raw_clark), "-t", "3.7",
    "-vf", "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,fps=30",
    "-c:v", "libx264", "-preset", "fast", "-an", str(c3)
], check=True, capture_output=True)

# Clip 4: 15.0s - 19.4s (4.4s) - Travis Kelce play
c4 = temp_dir / "c4.mp4"
subprocess.run([
    "ffmpeg", "-y", "-ss", "2.0", "-i", str(raw_kelce), "-t", "4.4",
    "-vf", "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,fps=30",
    "-c:v", "libx264", "-preset", "fast", "-an", str(c4)
], check=True, capture_output=True)

# Clip 5: 19.4s - 20.96s (1.56s) - Mahomes close-up finish
c5 = temp_dir / "c5.mp4"
subprocess.run([
    "ffmpeg", "-y", "-ss", "18.0", "-i", str(raw_mahomes), "-t", "1.6",
    "-vf", "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,fps=30",
    "-c:v", "libx264", "-preset", "fast", "-an", str(c5)
], check=True, capture_output=True)

print("2. Concatenating video segments...")
concat_txt = temp_dir / "concat.txt"
with open(concat_txt, "w", encoding="utf-8") as f:
    for s in [c1, c2, c3, c4, c5]:
        f.write(f"file '{s.resolve().as_posix()}'\n")

merged_v = temp_dir / "merged_v.mp4"
subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt),
    "-c:v", "libx264", "-preset", "fast", "-an", str(merged_v)
], check=True, capture_output=True)

print("3. Mixing Audio (Smooth Voice + Dark Tension BGM + Sub-Bass drop)...")
# BGM is ducked at -13dB (volume=0.22), with subtle fade out at end
# Also mix slight ambient crowd at -22dB from original clip for realistic texture
raw_crowd = raw_mahomes

filter_complex = (
    "[1:a]volume=1.0[voice];"
    "[2:a]volume=0.24,afade=t=in:st=0:d=0.5,afade=t=out:st=19.5:d=1.4[bgm];"
    "[voice][bgm]amix=inputs=2:duration=first:dropout_transition=2[aout]"
)

print("4. Muxing final video (Clean Cinematic - NO burned text)...")
cmd = [
    "ffmpeg", "-y",
    "-i", str(merged_v),
    "-i", str(voice_path),
    "-i", str(bgm_path),
    "-filter_complex", filter_complex,
    "-map", "0:v",
    "-map", "[aout]",
    "-c:v", "libx264", "-preset", "medium", "-crf", "19",
    "-c:a", "aac", "-b:a", "192k",
    "-t", "20.96",
    str(output_mp4)
]
res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode != 0:
    print("Error:", res.stderr)
else:
    print("SUCCESS! Created:", output_mp4)
