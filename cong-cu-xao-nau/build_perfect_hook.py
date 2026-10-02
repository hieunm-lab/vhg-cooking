import subprocess
from pathlib import Path

pkg = Path(r"C:\Users\Thien\Downloads\kho video\CapCut_Project_Package")
data_clips = Path(r"d:\HIeu\content tong hop\cong-cu-xao-nau\data\clips")

voice_path = pkg / "00_Voiceover_Hook_Puck.mp3"
bgm_path = data_clips / "bgm_cinematic_tension.mp3"

raw_celeb = data_clips / "mahomes_celebration_raw.webm"
raw_walker = pkg / "02_Highlight_Kenneth_Walker.mp4"
raw_kelce = pkg / "03_Travis_Kelce_Reboot.mp4"
raw_clark = pkg / "01_Soundbite_Ryan_Clark.mp4"

output_mp4 = pkg / "00_Hook_Perfect_Puck_Celebration.mp4"
temp_dir = data_clips / "perfect_temp"
temp_dir.mkdir(parents=True, exist_ok=True)

print("1. Preparing visual segments (Starting with Patrick Mahomes celebration)...")

# Clip 1 (0.0s - 6.0s, 6.0s): Patrick Mahomes explosive touchdown celebration
c1 = temp_dir / "c1.mp4"
subprocess.run([
    "ffmpeg", "-y", "-ss", "12.5", "-i", str(raw_celeb), "-t", "6.0",
    "-vf", "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,fps=30",
    "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(c1)
], check=True, capture_output=True)

# Clip 2 (6.0s - 11.5s, 5.5s): Kenneth Walker III explosive 73-yard run
c2 = temp_dir / "c2.mp4"
subprocess.run([
    "ffmpeg", "-y", "-ss", "0.5", "-i", str(raw_walker), "-t", "5.5",
    "-vf", "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,fps=30",
    "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(c2)
], check=True, capture_output=True)

# Clip 3 (11.5s - 16.5s, 5.0s): Travis Kelce catch & run sideline
c3 = temp_dir / "c3.mp4"
subprocess.run([
    "ffmpeg", "-y", "-ss", "1.0", "-i", str(raw_kelce), "-t", "5.0",
    "-vf", "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,fps=30",
    "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(c3)
], check=True, capture_output=True)

# Clip 4 (16.5s - 21.0s, 4.5s): Ryan Clark on Stephen A. Smith show
c4 = temp_dir / "c4.mp4"
subprocess.run([
    "ffmpeg", "-y", "-ss", "2.0", "-i", str(raw_clark), "-t", "4.5",
    "-vf", "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,fps=30",
    "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(c4)
], check=True, capture_output=True)

# Clip 5 (21.0s - 23.5s, 2.5s): Mahomes close-up walk in Arrowhead
c5 = temp_dir / "c5.mp4"
subprocess.run([
    "ffmpeg", "-y", "-ss", "21.5", "-i", str(raw_celeb), "-t", "2.5",
    "-vf", "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,fps=30",
    "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(c5)
], check=True, capture_output=True)

print("2. Concatenating video segments...")
concat_txt = temp_dir / "concat.txt"
with open(concat_txt, "w", encoding="utf-8") as f:
    for s in [c1, c2, c3, c4, c5]:
        f.write(f"file '{s.resolve().as_posix()}'\n")

merged_v = temp_dir / "merged_v.mp4"
subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt),
    "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(merged_v)
], check=True, capture_output=True)

print("3. Mixing Audio (Puck Voice 100% + Cinematic Dark 808 BGM -13dB + Subtle Stadium Texture)...")
# Input 0: merged_v (video + live audio)
# Input 1: voice_path (00_Voiceover_Hook_Puck.mp3)
# Input 2: bgm_path (bgm_cinematic_tension.mp3)

filter_complex = (
    "[0:a]volume=0.10[crowd_subtle];"
    "[1:a]volume=1.0[voice];"
    "[2:a]volume=0.22,afade=t=in:st=0:d=0.5,afade=t=out:st=22.0:d=1.5[bgm];"
    "[voice][bgm]amix=inputs=2:duration=first:dropout_transition=2[v_bgm];"
    "[v_bgm][crowd_subtle]amix=inputs=2:duration=first[aout]"
)

print("4. Muxing final video (Clean, no text clutter)...")
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
    "-t", "23.5",
    str(output_mp4)
]
res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode != 0:
    print("Error:", res.stderr)
else:
    print("SUCCESS! Created:", output_mp4)
