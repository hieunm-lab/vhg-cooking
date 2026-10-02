import subprocess
from pathlib import Path

pkg = Path(r"C:\Users\Thien\Downloads\kho video\CapCut_Project_Package")
data_clips = Path(r"d:\HIeu\content tong hop\cong-cu-xao-nau\data\clips")
lib = pkg / "Kho_Highlight_San"

cbs_src = Path(r"C:\Users\Thien\Downloads\kho video\YTSave_YouTube_Media_OAMvk1znLuw_What-s-making-the-Chiefs-good-again-The-NFL-Today_002_720p.mp4")

output_v1 = pkg / "01_Expert_CBS_Extended_With_Highlights.mp4"
temp_dir = data_clips / "v1_flawless_temp"
temp_dir.mkdir(parents=True, exist_ok=True)

print("--- RENDERING EXPERT VIDEO 1 (CBS 3m08s - 100% GRAPHIC REPLACEMENT) ---")

# Highlights:
hl_mahomes_wasp = lib / "01_Patrick_Mahomes_Clutch" / "Mahomes_04_SuperBowl_Deep_Bomb_Wasp.mp4"
hl_kelce_deep = lib / "03_Travis_Kelce_Reboot" / "Kelce_01_Deep_Catch_Downfield.mp4"
hl_walker_73yd = lib / "02_Kenneth_Walker_Power" / "Walker_01_73yd_Breakaway_Run.mp4"
hl_walker_burst = lib / "02_Kenneth_Walker_Power" / "Walker_03_Tackle_Break_Burst.mp4"
hl_walker_4th = lib / "02_Kenneth_Walker_Power" / "Walker_02_FourthDown_60yd_HouseCall.mp4"
hl_kelce_spike = lib / "03_Travis_Kelce_Reboot" / "Kelce_02_Football_Spike_Celeb.mp4"
hl_kelce_vroute = lib / "03_Travis_Kelce_Reboot" / "Kelce_03_VRoute_PlayAction_Catch.mp4"
hl_walker_td = lib / "02_Kenneth_Walker_Power" / "Walker_04_RedZone_Plunge_TD.mp4"
hl_kelce_signal = lib / "03_Travis_Kelce_Reboot" / "Kelce_04_FirstDown_Signal_Celeb.mp4"
hl_mahomes_dive = lib / "01_Patrick_Mahomes_Clutch" / "Mahomes_01_EndZone_Dive_TD.mp4"

def make_studio(start, duration, name):
    out = temp_dir / f"{name}.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-ss", str(start), "-i", str(cbs_src), "-t", str(duration),
        "-vf", "scale=1280:720,fps=30",
        "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(out)
    ], check=True, capture_output=True)
    return out

def make_hl(start_cbs, duration, hl_file, name):
    out = temp_dir / f"{name}.mp4"
    a_out = temp_dir / f"{name}_a.aac"
    # Extract CBS audio
    subprocess.run([
        "ffmpeg", "-y", "-ss", str(start_cbs), "-i", str(cbs_src), "-t", str(duration),
        "-vn", "-c:a", "aac", str(a_out)
    ], check=True, capture_output=True)
    # Combine with muted pre-cut highlight
    subprocess.run([
        "ffmpeg", "-y", "-ss", "0.0", "-i", str(hl_file), "-i", str(a_out), "-t", str(duration),
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(out)
    ], check=True, capture_output=True)
    return out

# 1. Studio Cowher: 101.4s -> 110.4s (9.0s)
p1 = make_studio(101.4, 9.0, "p1")

# 2. Highlight 1: 110.4s -> 115.4s (5.0s) - Mahomes Wasp (Replaces CBS stat graphic)
p2 = make_hl(110.4, 5.0, hl_mahomes_wasp, "p2_wasp")

# 3. Highlight 2: 115.4s -> 120.4s (5.0s) - Kelce Deep Catch (Replaces CBS stat graphic)
p3 = make_hl(115.4, 5.0, hl_kelce_deep, "p3_kelce_deep")

# 4. Highlight 3: 120.4s -> 125.4s (5.0s) - Walker 73yd Run (Replaces CBS stat graphic)
p4 = make_hl(120.4, 5.0, hl_walker_73yd, "p4_walker_73yd")

# 5. Highlight 4: 125.4s -> 129.4s (4.0s) - Walker Tackle Break (Replaces CBS replay)
p5 = make_hl(125.4, 4.0, hl_walker_burst, "p5_walker_burst")

# 6. Studio Cowher & Burleson & Long: 129.4s -> 188.0s (58.6s) - Studio faces
p6 = make_studio(129.4, 58.6, "p6")

# 7. Highlight 5: 188.0s -> 193.0s (5.0s) - Walker 4th down TD (Replaces CBS replay)
p7 = make_hl(188.0, 5.0, hl_walker_4th, "p7_walker_4th")

# 8. Studio Kyle Long on Kelce: 193.0s -> 208.4s (15.4s) - Studio face
p8 = make_studio(193.0, 15.4, "p8")

# 9. Highlight 6: 208.4s -> 213.4s (5.0s) - Kelce Spike (Replaces CBS stat graphic)
p9 = make_hl(208.4, 5.0, hl_kelce_spike, "p9_kelce_spike")

# 10. Highlight 7: 213.4s -> 218.4s (5.0s) - Kelce V-route (Replaces CBS stat graphic)
p10 = make_hl(213.4, 5.0, hl_kelce_vroute, "p10_kelce_vroute")

# 11. Highlight 8: 218.4s -> 223.4s (5.0s) - Walker TD Plunge (Replaces CBS stat graphic)
p11 = make_hl(218.4, 5.0, hl_walker_td, "p11_walker_td")

# 12. Studio Russell Wilson: 223.4s -> 229.4s (6.0s) - Studio face
p12 = make_studio(223.4, 6.0, "p12")

# 13. Highlight 9: 229.4s -> 234.4s (5.0s) - Kelce First Down Signal (Replaces CBS replay)
p13 = make_hl(229.4, 5.0, hl_kelce_signal, "p13_kelce_signal")

# 14. Studio Russell Wilson on Mahomes ACL: 234.4s -> 278.4s (44.0s) - Studio face
p14 = make_studio(234.4, 44.0, "p14")

# 15. Highlight 10: 278.4s -> 283.4s (5.0s) - Mahomes Dive TD (Replaces CBS replay)
p15 = make_hl(278.4, 5.0, hl_mahomes_dive, "p15_mahomes_dive")

# 16. Studio Cowher final sentence: 283.4s -> 290.0s (6.6s) - Studio face with fadeout
p16 = temp_dir / "p16_conclusion.mp4"
subprocess.run([
    "ffmpeg", "-y", "-ss", "283.4", "-i", str(cbs_src), "-t", "6.6",
    "-vf", "scale=1280:720,fps=30",
    "-af", "afade=t=out:st=5.1:d=1.5",
    "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(p16)
], check=True, capture_output=True)

# Concatenate all parts
concat_txt = temp_dir / "concat_v1.txt"
parts = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16]
with open(concat_txt, "w", encoding="utf-8") as f:
    for p in parts:
        f.write(f"file '{p.resolve().as_posix()}'\n")

print("Concatenating into Master Video 1 Flawless...")
subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt),
    "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-c:a", "aac", "-b:a", "192k",
    str(output_v1)
], check=True, capture_output=True)

print("SUCCESS! Created Video 1 Flawless:", output_v1)
