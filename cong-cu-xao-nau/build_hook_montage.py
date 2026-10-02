import subprocess
import json
from pathlib import Path

pkg = Path(r"C:\Users\Thien\Downloads\kho video\CapCut_Project_Package")
data_clips = Path(r"d:\HIeu\content tong hop\cong-cu-xao-nau\data\clips")

# Source assets
voice_path = pkg / "00_Voiceover_Hook_Puck.mp3"
raw_mahomes = data_clips / "mahomes_run_raw.webm"
raw_walker = pkg / "02_Highlight_Kenneth_Walker.mp4"
raw_kelce = pkg / "03_Travis_Kelce_Reboot.mp4"
raw_clark = pkg / "01_Soundbite_Ryan_Clark.mp4"

output_hook = pkg / "00_Hook_Complete_Montage.mp4"
temp_dir = data_clips / "hook_temp"
temp_dir.mkdir(parents=True, exist_ok=True)

print("1. Preparing 5 visual segments...")

# Segment 1: Mahomes 0.0s - 5.5s (5.5s)
seg1 = temp_dir / "seg1.mp4"
subprocess.run([
    "ffmpeg", "-y", "-ss", "6.0", "-i", str(raw_mahomes), "-t", "5.5",
    "-vf", "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,fps=30",
    "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", "-b:a", "128k", str(seg1)
], check=True, capture_output=True)

# Segment 2: Kenneth Walker 5.5s - 11.0s (5.5s)
seg2 = temp_dir / "seg2.mp4"
subprocess.run([
    "ffmpeg", "-y", "-ss", "0.5", "-i", str(raw_walker), "-t", "5.5",
    "-vf", "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,fps=30",
    "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", "-b:a", "128k", str(seg2)
], check=True, capture_output=True)

# Segment 3: Travis Kelce 11.0s - 16.0s (5.0s)
seg3 = temp_dir / "seg3.mp4"
subprocess.run([
    "ffmpeg", "-y", "-ss", "1.0", "-i", str(raw_kelce), "-t", "5.0",
    "-vf", "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,fps=30",
    "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", "-b:a", "128k", str(seg3)
], check=True, capture_output=True)

# Segment 4: Ryan Clark 16.0s - 21.0s (5.0s)
seg4 = temp_dir / "seg4.mp4"
subprocess.run([
    "ffmpeg", "-y", "-ss", "2.0", "-i", str(raw_clark), "-t", "5.0",
    "-vf", "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,fps=30",
    "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", "-b:a", "128k", str(seg4)
], check=True, capture_output=True)

# Segment 5: End Celebration 21.0s - 23.5s (2.5s)
seg5 = temp_dir / "seg5.mp4"
subprocess.run([
    "ffmpeg", "-y", "-ss", "16.0", "-i", str(raw_mahomes), "-t", "2.5",
    "-vf", "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,fps=30",
    "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", "-b:a", "128k", str(seg5)
], check=True, capture_output=True)

print("2. Concatenating video segments...")
concat_list = temp_dir / "concat.txt"
with open(concat_list, "w", encoding="utf-8") as f:
    for s in [seg1, seg2, seg3, seg4, seg5]:
        f.write(f"file '{s.resolve().as_posix()}'\n")

merged_video = temp_dir / "merged_video.mp4"
subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list),
    "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(merged_video)
], check=True, capture_output=True)

print("3. Generating Sound Design (Stadium Ambience + Sub-Bass Boom + Puck Voiceover)...")
# Mix:
# Input 0: merged_video (video + original crowd audio)
# Input 1: voiceover Puck (00_Voiceover_Hook_Puck.mp3)
# Audio filter:
# [0:a] volume=0.18 [crowd];
# aevalsrc='sin(2*PI*45*t)*exp(-2.5*t)*1.8':d=1.5 [boom];
# [crowd][boom] amix=inputs=2:duration=first [bg_sfx];
# [bg_sfx][1:a] amix=inputs=2:duration=first:weights=0.3 1.0 [aout]

final_filter = (
    "[0:a]volume=0.20[crowd];"
    "aevalsrc=sin(2*PI*45*t)*exp(-2.5*t)*1.5:d=1.5[boom];"
    "[crowd][boom]amix=inputs=2:duration=first[bg_sfx];"
    "[bg_sfx][1:a]amix=inputs=2:duration=first:weights=0.35 1.0[aout]"
)

# Also burn subtitle if Chiefs_Hook_Subtitles.srt exists
srt_file = pkg / "Chiefs_Hook_Subtitles.srt"
vf_filter = "fps=30"
if srt_file.exists():
    srt_escaped = str(srt_file.resolve().as_posix()).replace(":", "\\:")
    vf_filter += f",subtitles='{srt_escaped}':force_style='FontSize=16,PrimaryColour=&H00FFFF,OutlineColour=&H000000,BorderStyle=3,Outline=2,Shadow=1,MarginV=35'"

print("4. Muxing final video with audio & styling...")
cmd = [
    "ffmpeg", "-y",
    "-i", str(merged_video),
    "-i", str(voice_path),
    "-filter_complex", final_filter,
    "-map", "0:v",
    "-map", "[aout]",
    "-vf", vf_filter,
    "-c:v", "libx264", "-preset", "medium", "-crf", "20",
    "-c:a", "aac", "-b:a", "192k",
    "-t", "23.5",
    str(output_hook)
]
res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode != 0:
    print("FFmpeg error:", res.stderr)
else:
    print("SUCCESS! Output created:", output_hook)
