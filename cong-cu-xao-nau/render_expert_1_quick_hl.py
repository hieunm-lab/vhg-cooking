import subprocess
from pathlib import Path

pkg = Path(r"C:\Users\Thien\Downloads\kho video\CapCut_Project_Package")
data_clips = Path(r"d:\HIeu\content tong hop\cong-cu-xao-nau\data\clips")

cbs_src = Path(r"C:\Users\Thien\Downloads\kho video\YTSave_YouTube_Media_OAMvk1znLuw_What-s-making-the-Chiefs-good-again-The-NFL-Today_002_720p.mp4")
walker_src = pkg / "02_Highlight_Kenneth_Walker.mp4"
kelce_src = pkg / "03_Travis_Kelce_Reboot.mp4"
mahomes_dive_src = data_clips / "mahomes_run_raw.webm"
walker_broncos_src = data_clips / "walker_4th_down_broncos.webm"

output_v1 = pkg / "01_Expert_CBS_Extended_With_Highlights.mp4"
temp_dir = data_clips / "v1_quick_hl_temp"
temp_dir.mkdir(parents=True, exist_ok=True)

print("--- RENDERING EXPERT VIDEO 1 (Standard 4-5s Punchy Highlights) ---")

zoom_hl_filter = "crop=in_w*0.82:in_h*0.82:(in_w-out_w)/2:(in_h-out_h)/2,scale=1280:720,fps=30"

def make_studio(start, duration, name):
    out = temp_dir / f"{name}.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-ss", str(start), "-i", str(cbs_src), "-t", str(duration),
        "-vf", "scale=1280:720,fps=30",
        "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(out)
    ], check=True, capture_output=True)
    return out

def make_highlight(start_cbs, duration, hl_src, hl_offset, name, custom_zoom=zoom_hl_filter):
    out = temp_dir / f"{name}.mp4"
    audio_out = temp_dir / f"{name}_audio.aac"
    # Extract clean CBS voice
    subprocess.run([
        "ffmpeg", "-y", "-ss", str(start_cbs), "-i", str(cbs_src), "-t", str(duration),
        "-vn", "-c:a", "aac", str(audio_out)
    ], check=True, capture_output=True)
    # Combine with muted highlight (ONLY CBS voice)
    subprocess.run([
        "ffmpeg", "-y", "-ss", str(hl_offset), "-i", str(hl_src), "-i", str(audio_out), "-t", str(duration),
        "-map", "0:v:0", "-map", "1:a:0",
        "-vf", custom_zoom,
        "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(out)
    ], check=True, capture_output=True)
    return out

# 1. Studio 1: 101.4s -> 129.0s (27.6s) - Cowher opening
s1 = make_studio(101.4, 27.6, "s1")

# 2. Highlight 1 (Walker burst): 129.0s -> 134.0s (5.0s) - Punchy 5s
h1 = make_highlight(129.0, 5.0, walker_src, 1.0, "h1_walker_5s")

# 3. Studio 2: 134.0s -> 188.0s (54.0s) - Cowher, Burleson, Kyle Long
s2 = make_studio(134.0, 54.0, "s2")

# 4. Highlight 2 (Walker power run): 188.0s -> 193.0s (5.0s) - Punchy 5s
h2 = make_highlight(188.0, 5.0, walker_broncos_src, 6.0, "h2_walker_power_5s")

# 5. Studio 3: 193.0s -> 208.0s (15.0s) - Kyle Long on Kelce
s3 = make_studio(193.0, 15.0, "s3")

# 6. Highlight 3 (Kelce catch & spike): 208.0s -> 213.0s (5.0s) - Punchy 5s
h3 = make_highlight(208.0, 5.0, kelce_src, 2.0, "h3_kelce_5s")

# 7. Studio 4: 213.0s -> 222.0s (9.0s) - Wilson on 73-yd run & play action
s4 = make_studio(213.0, 9.0, "s4")

# 8. Highlight 4 (Walker 73-yd run): 222.0s -> 226.5s (4.5s) - Punchy 4.5s
h4 = make_highlight(222.0, 4.5, walker_src, 2.0, "h4_walker_73yd_4.5s")

# 9. Studio 5: 226.5s -> 230.0s (3.5s) - Wilson: puts ball in front of Walker
s5 = make_studio(226.5, 3.5, "s5")

# 10. Highlight 5 (Kelce deep V-route): 230.0s -> 234.5s (4.5s) - Punchy 4.5s
h5 = make_highlight(230.0, 4.5, kelce_src, 4.0, "h5_kelce_deep_4.5s")

# 11. Studio 6: 234.5s -> 279.0s (44.5s) - Wilson on Mahomes ACL recovery & schedule
s6 = make_studio(234.5, 44.5, "s6")

# 12. Highlight 6 (Mahomes dive TD): 279.0s -> 283.5s (4.5s) - Punchy 4.5s
h6 = make_highlight(279.0, 4.5, mahomes_dive_src, 9.0, "h6_mahomes_dive_4.5s", custom_zoom="crop=in_w*0.80:in_h*0.80:(in_w-out_w)/2:(in_h-out_h)/2,scale=1280:720,fps=30")

# 13. Studio 7: 283.5s -> 290.0s (6.5s) - Cowher final sentence with smooth fadeout
s7 = temp_dir / "s7_conclusion.mp4"
subprocess.run([
    "ffmpeg", "-y", "-ss", "283.5", "-i", str(cbs_src), "-t", "6.5",
    "-vf", "scale=1280:720,fps=30",
    "-af", "afade=t=out:st=5.5:d=1.0",
    "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(s7)
], check=True, capture_output=True)

# Concatenate all parts
concat_txt = temp_dir / "concat_v1.txt"
parts = [s1, h1, s2, h2, s3, h3, s4, h4, s5, h5, s6, h6, s7]
with open(concat_txt, "w", encoding="utf-8") as f:
    for p in parts:
        f.write(f"file '{p.resolve().as_posix()}'\n")

print("Concatenating into Master Video 1 with 4-5s highlights...")
subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt),
    "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-c:a", "aac", "-b:a", "192k",
    str(output_v1)
], check=True, capture_output=True)

print("SUCCESS! Created Video 1 with Punchy 4-5s Highlights:", output_v1)
