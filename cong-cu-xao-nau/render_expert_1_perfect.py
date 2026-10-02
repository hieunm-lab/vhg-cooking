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
temp_dir = data_clips / "v1_opt_a_perfect"
temp_dir.mkdir(parents=True, exist_ok=True)

print("--- RENDERING EXPERT VIDEO 1 (CBS Option A - 3m08s High-Retention Pacing) ---")

# Zoom filter to bypass copyright and focus on star player (crop 82% center and scale to 1280x720)
zoom_hl_filter = "crop=in_w*0.82:in_h*0.82:(in_w-out_w)/2:(in_h-out_h)/2,scale=1280:720,fps=30"

def make_studio(start, duration, name):
    out = temp_dir / f"{name}.mp4"
    print(f"Rendering studio {name} ({start}s -> {start+duration:.1f}s, dur {duration:.1f}s)...")
    subprocess.run([
        "ffmpeg", "-y", "-ss", str(start), "-i", str(cbs_src), "-t", str(duration),
        "-vf", "scale=1280:720,fps=30",
        "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(out)
    ], check=True, capture_output=True)
    return out

def make_highlight(start_cbs, duration, hl_src, hl_offset, name, custom_zoom=zoom_hl_filter):
    out = temp_dir / f"{name}.mp4"
    audio_out = temp_dir / f"{name}_audio.aac"
    print(f"Rendering highlight {name} ({start_cbs}s, dur {duration:.1f}s, hl={hl_src.name})...")
    # 1. Extract pure CBS studio voice
    subprocess.run([
        "ffmpeg", "-y", "-ss", str(start_cbs), "-i", str(cbs_src), "-t", str(duration),
        "-vn", "-c:a", "aac", str(audio_out)
    ], check=True, capture_output=True)
    # 2. Combine with highlight video (MUTING all highlight audio completely)
    subprocess.run([
        "ffmpeg", "-y", "-ss", str(hl_offset), "-i", str(hl_src), "-i", str(audio_out), "-t", str(duration),
        "-map", "0:v:0", "-map", "1:a:0",
        "-vf", custom_zoom,
        "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(out)
    ], check=True, capture_output=True)
    return out

# 1. Studio 1: 101.4s -> 125.6s (24.2s) - Bill Cowher on 24 passes vs 25 runs
s1 = make_studio(101.4, 24.2, "s1")

# 2. Highlight 1: 125.6s -> 138.0s (12.4s) - Kenneth Walker III breaking tackles (Muted, Cowher voice)
h1 = make_highlight(125.6, 12.4, walker_src, 0.0, "h1_walker")

# 3. Studio 2: 138.0s -> 185.0s (47.0s) - Cowher & Burleson on toughness and Eric Bieniemy
s2 = make_studio(138.0, 47.0, "s2")

# 4. Highlight 2: 185.0s -> 195.0s (10.0s) - Kenneth Walker power run (Kyle Long on pit bull Walker, Muted)
h2 = make_highlight(185.0, 10.0, walker_broncos_src, 5.0, "h2_walker_power")

# 5. Studio 3: 195.0s -> 205.0s (10.0s) - Kyle Long: Travis Kelce running naked downfield
s3 = make_studio(195.0, 10.0, "s3")

# 6. Highlight 3: 205.0s -> 218.0s (13.0s) - Travis Kelce catch & spike (Muted, Kyle Long voice)
h3 = make_highlight(205.0, 13.0, kelce_src, 0.0, "h3_kelce")

# 7. Highlight 4: 218.0s -> 226.0s (8.0s) - Kenneth Walker 73-yd run (Wilson on Walker running for 73 yards, Muted)
h4 = make_highlight(218.0, 8.0, walker_src, 2.0, "h4_walker_73yd")

# 8. Highlight 5: 226.0s -> 234.0s (8.0s) - Travis Kelce V-route catch (Wilson on ball down field to Kelce, Muted)
h5 = make_highlight(226.0, 8.0, kelce_src, 4.0, "h5_kelce_deep")

# 9. Studio 4: 234.0s -> 278.0s (44.0s) - Russell Wilson on Mahomes ACL recovery, longevity & schedule
s4 = make_studio(234.0, 44.0, "s4")

# 10. Highlight 6: 278.0s -> 284.5s (6.5s) - Mahomes scramble & dive into endzone (Wilson on dive TD, Muted)
h6 = make_highlight(278.0, 6.5, mahomes_dive_src, 8.0, "h6_mahomes_dive", custom_zoom="crop=in_w*0.80:in_h*0.80:(in_w-out_w)/2:(in_h-out_h)/2,scale=1280:720,fps=30")

# 11. Studio 5: 284.5s -> 290.0s (5.5s) - Bill Cowher final sentence: "...is critical" with smooth fadeout
s5 = temp_dir / "s5_conclusion.mp4"
print("Rendering s5 conclusion (5.5s with fadeout)...")
subprocess.run([
    "ffmpeg", "-y", "-ss", "284.5", "-i", str(cbs_src), "-t", "5.5",
    "-vf", "scale=1280:720,fps=30",
    "-af", "afade=t=out:st=4.5:d=1.0",
    "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(s5)
], check=True, capture_output=True)

# Concatenate all parts into master
concat_txt = temp_dir / "concat_v1.txt"
parts = [s1, h1, s2, h2, s3, h3, h4, h5, s4, h6, s5]
with open(concat_txt, "w", encoding="utf-8") as f:
    for p in parts:
        f.write(f"file '{p.resolve().as_posix()}'\n")

print("Concatenating into final Master Video 1 Option A...")
subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt),
    "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-c:a", "aac", "-b:a", "192k",
    str(output_v1)
], check=True, capture_output=True)

print("SUCCESS! Created Video 1 Option A Perfect:", output_v1)
