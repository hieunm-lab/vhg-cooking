import subprocess
from pathlib import Path

pkg = Path(r"C:\Users\Thien\Downloads\kho video\CapCut_Project_Package")
data_clips = Path(r"d:\HIeu\content tong hop\cong-cu-xao-nau\data\clips")

src_v2 = Path(r"C:\Users\Thien\Downloads\kho video\YTSave_YouTube_Media_WgXeLu4OjMU_Ryan-Clark-Life-After-ESPN-The-Eagles-Problems-Mahomes-Chiefs_002_720p.mp4")
walker_src = pkg / "02_Highlight_Kenneth_Walker.mp4"
kelce_src = pkg / "03_Travis_Kelce_Reboot.mp4"
mahomes_run_src = data_clips / "mahomes_run_raw.webm"

output_v2 = pkg / "02_Expert_RyanClark_Extended_Focused.mp4"
temp_dir = data_clips / "v2_v3_temp"
temp_dir.mkdir(parents=True, exist_ok=True)

print("--- RENDERING EXPERT VIDEO 2 (Ryan Clark & Stephen A Focused 2m02s - Muted Highlights) ---")

crop_stephen = "crop=500:281:20:70,scale=1280:720,fps=30"
crop_ryan = "crop=500:281:755:80,scale=1280:720,fps=30"
zoom_hl = "crop=in_w*0.82:in_h*0.82:(in_w-out_w)/2:(in_h-out_h)/2,scale=1280:720,fps=30"

# Segment 1: 1311.4s -> 1324.5s (13.1s) - Stephen A. Smith single speaker
s1 = temp_dir / "s1.mp4"
print("Rendering Seg 1: Stephen A (13.1s)...")
subprocess.run([
    "ffmpeg", "-y", "-ss", "1311.4", "-i", str(src_v2), "-t", "13.1",
    "-vf", crop_stephen,
    "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(s1)
], check=True, capture_output=True)

# Segment 2: 1324.5s -> 1344.0s (19.5s) - Ryan Clark single speaker
s2 = temp_dir / "s2.mp4"
print("Rendering Seg 2: Ryan Clark (19.5s)...")
subprocess.run([
    "ffmpeg", "-y", "-ss", "1324.5", "-i", str(src_v2), "-t", "19.5",
    "-vf", crop_ryan,
    "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(s2)
], check=True, capture_output=True)

# Segment 3: 1344.0s -> 1354.0s (10.0s) - HIGHLIGHT: Travis Kelce (MUTED highlight audio, ONLY Ryan voice)
s3_audio = temp_dir / "s3_audio.aac"
subprocess.run([
    "ffmpeg", "-y", "-ss", "1344.0", "-i", str(src_v2), "-t", "10.0",
    "-vn", "-c:a", "aac", str(s3_audio)
], check=True, capture_output=True)

s3 = temp_dir / "s3.mp4"
print("Rendering Seg 3: Travis Kelce Highlight Zoomed (10.0s, Muted highlight sound)...")
subprocess.run([
    "ffmpeg", "-y", "-ss", "0.0", "-i", str(kelce_src), "-i", str(s3_audio), "-t", "10.0",
    "-map", "0:v:0", "-map", "1:a:0",
    "-vf", zoom_hl,
    "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(s3)
], check=True, capture_output=True)

# Segment 4: 1354.0s -> 1373.0s (19.0s) - Ryan Clark single speaker
s4 = temp_dir / "s4.mp4"
print("Rendering Seg 4: Ryan Clark (19.0s)...")
subprocess.run([
    "ffmpeg", "-y", "-ss", "1354.0", "-i", str(src_v2), "-t", "19.0",
    "-vf", crop_ryan,
    "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(s4)
], check=True, capture_output=True)

# Segment 5: 1373.0s -> 1386.0s (13.0s) - HIGHLIGHT: Kenneth Walker 73-yd run (MUTED highlight sound, ONLY Ryan voice)
s5_audio = temp_dir / "s5_audio.aac"
subprocess.run([
    "ffmpeg", "-y", "-ss", "1373.0", "-i", str(src_v2), "-t", "13.0",
    "-vn", "-c:a", "aac", str(s5_audio)
], check=True, capture_output=True)

s5 = temp_dir / "s5.mp4"
print("Rendering Seg 5: Kenneth Walker Highlight Zoomed (13.0s, Muted highlight sound)...")
subprocess.run([
    "ffmpeg", "-y", "-ss", "0.0", "-i", str(walker_src), "-i", str(s5_audio), "-t", "13.0",
    "-map", "0:v:0", "-map", "1:a:0",
    "-vf", zoom_hl,
    "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(s5)
], check=True, capture_output=True)

# Segment 6: 1386.0s -> 1406.0s (20.0s) - Ryan Clark single speaker
s6 = temp_dir / "s6.mp4"
print("Rendering Seg 6: Ryan Clark (20.0s)...")
subprocess.run([
    "ffmpeg", "-y", "-ss", "1386.0", "-i", str(src_v2), "-t", "20.0",
    "-vf", crop_ryan,
    "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(s6)
], check=True, capture_output=True)

# Segment 7: 1406.0s -> 1419.0s (13.0s) - HIGHLIGHT: Patrick Mahomes Scramble TD (MUTED highlight sound, ONLY Ryan voice)
s7_audio = temp_dir / "s7_audio.aac"
subprocess.run([
    "ffmpeg", "-y", "-ss", "1406.0", "-i", str(src_v2), "-t", "13.0",
    "-vn", "-c:a", "aac", str(s7_audio)
], check=True, capture_output=True)

s7 = temp_dir / "s7.mp4"
print("Rendering Seg 7: Patrick Mahomes Highlight Zoomed (13.0s, Muted highlight sound)...")
subprocess.run([
    "ffmpeg", "-y", "-ss", "7.0", "-i", str(mahomes_run_src), "-i", str(s7_audio), "-t", "13.0",
    "-map", "0:v:0", "-map", "1:a:0",
    "-vf", "crop=in_w*0.80:in_h*0.80:(in_w-out_w)/2:(in_h-out_h)/2,scale=1280:720,fps=30",
    "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(s7)
], check=True, capture_output=True)

# Segment 8: 1419.0s -> 1433.5s (14.5s) - Ryan Clark final sentence with smooth fadeout
s8 = temp_dir / "s8.mp4"
print("Rendering Seg 8: Ryan Clark Final Sentence with smooth fadeout (14.5s)...")
subprocess.run([
    "ffmpeg", "-y", "-ss", "1419.0", "-i", str(src_v2), "-t", "14.5",
    "-vf", crop_ryan,
    "-af", "afade=t=out:st=13.5:d=1.0",
    "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(s8)
], check=True, capture_output=True)

# Concatenate Segments 1 to 8
concat_txt = temp_dir / "concat_v2.txt"
with open(concat_txt, "w", encoding="utf-8") as f:
    for s in [s1, s2, s3, s4, s5, s6, s7, s8]:
        f.write(f"file '{s.resolve().as_posix()}'\n")

print("Concatenating into final master Video 2...")
subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt),
    "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-c:a", "aac", "-b:a", "192k",
    str(output_v2)
], check=True, capture_output=True)

print("SUCCESS! Created Video 2 Extended Focused:", output_v2)
