import subprocess
from pathlib import Path

pkg = Path(r"C:\Users\Thien\Downloads\kho video\CapCut_Project_Package")
data_clips = Path(r"d:\HIeu\content tong hop\cong-cu-xao-nau\data\clips")
lib = pkg / "Kho_Highlight_San"

src_v2 = Path(r"C:\Users\Thien\Downloads\kho video\YTSave_YouTube_Media_WgXeLu4OjMU_Ryan-Clark-Life-After-ESPN-The-Eagles-Problems-Mahomes-Chiefs_002_720p.mp4")

output_v2 = pkg / "02_Expert_RyanClark_Extended_Focused.mp4"
temp_dir = data_clips / "v2_flawless_temp"
temp_dir.mkdir(parents=True, exist_ok=True)

print("--- RENDERING EXPERT VIDEO 2 (Ryan Clark & Stephen A - 100% GRAPHIC REPLACEMENT) ---")

crop_stephen = "crop=500:281:20:70,scale=1280:720,fps=30"
crop_ryan = "crop=500:281:755:80,scale=1280:720,fps=30"

hl_kelce = lib / "03_Travis_Kelce_Reboot" / "Kelce_02_Football_Spike_Celeb.mp4"
hl_walker = lib / "02_Kenneth_Walker_Power" / "Walker_01_73yd_Breakaway_Run.mp4"
hl_def1 = lib / "05_Chiefs_Defense_Spags" / "Defense_01_ChrisJones_Strip_Sack.mp4"
hl_def2 = lib / "05_Chiefs_Defense_Spags" / "Defense_02_Pocket_Crush_Sack.mp4"
hl_mahomes = lib / "01_Patrick_Mahomes_Clutch" / "Mahomes_02_NoLook_Magic_Pass.mp4"

def make_hl(start_v2, duration, hl_file, name):
    out = temp_dir / f"{name}.mp4"
    a_out = temp_dir / f"{name}_a.aac"
    subprocess.run([
        "ffmpeg", "-y", "-ss", str(start_v2), "-i", str(src_v2), "-t", str(duration),
        "-vn", "-c:a", "aac", str(a_out)
    ], check=True, capture_output=True)
    subprocess.run([
        "ffmpeg", "-y", "-ss", "0.0", "-i", str(hl_file), "-i", str(a_out), "-t", str(duration),
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(out)
    ], check=True, capture_output=True)
    return out

# Segment 1: 1311.4s -> 1324.5s (13.1s) - Stephen A. Smith
s1 = temp_dir / "s1.mp4"
subprocess.run([
    "ffmpeg", "-y", "-ss", "1311.4", "-i", str(src_v2), "-t", "13.1",
    "-vf", crop_stephen,
    "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(s1)
], check=True, capture_output=True)

# Segment 2: 1324.5s -> 1346.0s (21.5s) - Ryan Clark
s2 = temp_dir / "s2.mp4"
subprocess.run([
    "ffmpeg", "-y", "-ss", "1324.5", "-i", str(src_v2), "-t", "21.5",
    "-vf", crop_ryan,
    "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(s2)
], check=True, capture_output=True)

# Segment 3: 1346.0s -> 1351.0s (5.0s) - HIGHLIGHT: Travis Kelce (5s, Muted)
s3 = make_hl(1346.0, 5.0, hl_kelce, "s3_kelce")

# Segment 4: 1351.0s -> 1378.0s (27.0s) - Ryan Clark
s4 = temp_dir / "s4.mp4"
subprocess.run([
    "ffmpeg", "-y", "-ss", "1351.0", "-i", str(src_v2), "-t", "27.0",
    "-vf", crop_ryan,
    "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(s4)
], check=True, capture_output=True)

# Segment 5: 1378.0s -> 1383.0s (5.0s) - HIGHLIGHT: Kenneth Walker (5s, Muted)
s5 = make_hl(1378.0, 5.0, hl_walker, "s5_walker")

# Segment 6: 1383.0s -> 1388.5s (5.5s) - Ryan Clark before standings table
s6 = temp_dir / "s6.mp4"
subprocess.run([
    "ffmpeg", "-y", "-ss", "1383.0", "-i", str(src_v2), "-t", "5.5",
    "-vf", crop_ryan,
    "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(s6)
], check=True, capture_output=True)

# Segment 7A: 1388.5s -> 1393.5s (5.0s) - HIGHLIGHT: Defense Chris Jones Strip Sack (Replaces standings table!)
s7a = make_hl(1388.5, 5.0, hl_def1, "s7a_def1")

# Segment 7B: 1393.5s -> 1398.5s (5.0s) - HIGHLIGHT: Defense Pocket Crush Sack (Replaces standings table!)
s7b = make_hl(1393.5, 5.0, hl_def2, "s7b_def2")

# Segment 7C: 1398.5s -> 1402.5s (4.0s) - HIGHLIGHT: Defense Stop (Replaces end of standings table!)
hl_def3 = lib / "05_Chiefs_Defense_Spags" / "Defense_03_Edge_Pressure_Tackle.mp4"
s7c = make_hl(1398.5, 4.0, hl_def3, "s7c_def3")

# Segment 8: 1402.5s -> 1410.0s (7.5s) - Ryan Clark on Josh Allen & Bills
s8 = temp_dir / "s8.mp4"
subprocess.run([
    "ffmpeg", "-y", "-ss", "1402.5", "-i", str(src_v2), "-t", "7.5",
    "-vf", crop_ryan,
    "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(s8)
], check=True, capture_output=True)

# Segment 9: 1410.0s -> 1415.0s (5.0s) - HIGHLIGHT: Patrick Mahomes No-Look / Scramble (5s, Muted)
s9 = make_hl(1410.0, 5.0, hl_mahomes, "s9_mahomes")

# Segment 10: 1415.0s -> 1433.5s (18.5s) - Ryan Clark final verdict with fadeout
s10 = temp_dir / "s10.mp4"
subprocess.run([
    "ffmpeg", "-y", "-ss", "1415.0", "-i", str(src_v2), "-t", "18.5",
    "-vf", crop_ryan,
    "-af", "afade=t=out:st=17.0:d=1.5",
    "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(s10)
], check=True, capture_output=True)

# Concatenate all parts
concat_txt = temp_dir / "concat_v2.txt"
parts = [s1, s2, s3, s4, s5, s6, s7a, s7b, s7c, s8, s9, s10]
with open(concat_txt, "w", encoding="utf-8") as f:
    for p in parts:
        f.write(f"file '{p.resolve().as_posix()}'\n")

print("Concatenating into Master Video 2 Flawless...")
subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt),
    "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-c:a", "aac", "-b:a", "192k",
    str(output_v2)
], check=True, capture_output=True)

print("SUCCESS! Created Video 2 Flawless:", output_v2)
