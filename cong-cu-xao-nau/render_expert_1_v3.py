import subprocess
from pathlib import Path

pkg = Path(r"C:\Users\Thien\Downloads\kho video\CapCut_Project_Package")
data_clips = Path(r"d:\HIeu\content tong hop\cong-cu-xao-nau\data\clips")

cbs_src = Path(r"C:\Users\Thien\Downloads\kho video\YTSave_YouTube_Media_OAMvk1znLuw_What-s-making-the-Chiefs-good-again-The-NFL-Today_002_720p.mp4")

# Highlights:
kelce_src = pkg / "03_Travis_Kelce_Reboot.mp4"
walker_73yd_src = pkg / "02_Highlight_Kenneth_Walker.mp4"
walker_broncos_src = data_clips / "walker_4th_down_broncos.webm"
mahomes_dive_src = data_clips / "mahomes_run_raw.webm"
mahomes_celeb_src = data_clips / "mahomes_celebration_raw.webm"
defense_src = data_clips / "chiefs_defense_sacks.mkv"

output_v1 = pkg / "01_Expert_CBS_Extended_With_Highlights.mp4"
temp_dir = data_clips / "v1_full_temp"
temp_dir.mkdir(parents=True, exist_ok=True)

print("--- RENDERING EXPERT VIDEO 1 (CBS Full 9m00s with Exact Muted Highlights) ---")

# Zoom filter to bypass copyright and focus on star player (crop 82% center and scale to 1280x720)
zoom_hl_filter = "crop=in_w*0.82:in_h*0.82:(in_w-out_w)/2:(in_h-out_h)/2,scale=1280:720,fps=30"

def make_studio(start, duration, name):
    out = temp_dir / f"{name}.mp4"
    print(f"Rendering studio {name} ({start}s -> {start+duration}s, dur {duration}s)...")
    subprocess.run([
        "ffmpeg", "-y", "-ss", str(start), "-i", str(cbs_src), "-t", str(duration),
        "-vf", "scale=1280:720,fps=30",
        "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(out)
    ], check=True, capture_output=True)
    return out

def make_highlight(start_cbs, duration, hl_src, hl_offset, name, custom_zoom=zoom_hl_filter):
    out = temp_dir / f"{name}.mp4"
    audio_out = temp_dir / f"{name}_audio.aac"
    print(f"Rendering highlight {name} ({start_cbs}s, dur {duration}s, hl={hl_src.name})...")
    # 1. Extract pure CBS expert audio
    subprocess.run([
        "ffmpeg", "-y", "-ss", str(start_cbs), "-i", str(cbs_src), "-t", str(duration),
        "-vn", "-c:a", "aac", str(audio_out)
    ], check=True, capture_output=True)
    # 2. Combine with highlight video (MUTING all highlight sound, ONLY CBS audio)
    subprocess.run([
        "ffmpeg", "-y", "-ss", str(hl_offset), "-i", str(hl_src), "-i", str(audio_out), "-t", str(duration),
        "-map", "0:v:0", "-map", "1:a:0",
        "-vf", custom_zoom,
        "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(out)
    ], check=True, capture_output=True)
    return out

# 1. Studio: 25.6s -> 58.6s (33.0s) - Nate Burleson on Kelce reset & reboot
p1 = make_studio(25.6, 33.0, "p1")

# 2. Highlight 1: 58.6s -> 70.6s (12.0s) - Travis Kelce catch & touchdown spike (Muted, Nate voice)
p2 = make_highlight(58.6, 12.0, kelce_src, 0.0, "p2_kelce")

# 3. Studio: 70.6s -> 125.6s (55.0s) - Nate & Bill Cowher on 24 passes vs 25 runs balance
p3 = make_studio(70.6, 55.0, "p3")

# 4. Highlight 2: 125.6s -> 138.0s (12.4s) - Kenneth Walker III explosive tackle breaking (Muted, Cowher voice)
p4 = make_highlight(125.6, 12.4, walker_73yd_src, 0.0, "p4_walker_runs")

# 5. Studio: 138.0s -> 220.0s (82.0s) - Cowher & Burleson on toughness, Eric Bieniemy, O-line pit bulls
p5 = make_studio(138.0, 82.0, "p5")

# 6. Highlight 3: 220.0s -> 236.0s (16.0s) - Walker 73-yd run & Kelce V-route (Muted, Russell Wilson voice)
# First 8s: Walker 73yd, next 8s: Kelce deep
h6a_audio = temp_dir / "p6a_audio.aac"
subprocess.run(["ffmpeg", "-y", "-ss", "220.0", "-i", str(cbs_src), "-t", "8.0", "-vn", "-c:a", "aac", str(h6a_audio)], check=True, capture_output=True)
p6a = temp_dir / "p6a.mp4"
subprocess.run(["ffmpeg", "-y", "-ss", "2.0", "-i", str(walker_73yd_src), "-i", str(h6a_audio), "-t", "8.0", "-map", "0:v:0", "-map", "1:a:0", "-vf", zoom_hl_filter, "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(p6a)], check=True, capture_output=True)

h6b_audio = temp_dir / "p6b_audio.aac"
subprocess.run(["ffmpeg", "-y", "-ss", "228.0", "-i", str(cbs_src), "-t", "8.0", "-vn", "-c:a", "aac", str(h6b_audio)], check=True, capture_output=True)
p6b = temp_dir / "p6b.mp4"
subprocess.run(["ffmpeg", "-y", "-ss", "4.0", "-i", str(kelce_src), "-i", str(h6b_audio), "-t", "8.0", "-map", "0:v:0", "-map", "1:a:0", "-vf", zoom_hl_filter, "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(p6b)], check=True, capture_output=True)

# 7. Studio: 236.0s -> 278.0s (42.0s) - Russell Wilson on Mahomes ACL recovery, longevity, schedule
p7 = make_studio(236.0, 42.0, "p7")

# 8. Highlight 4: 278.0s -> 284.5s (6.5s) - Mahomes scramble and dive in end zone (Muted, Wilson voice)
p8 = make_highlight(278.0, 6.5, mahomes_dive_src, 8.0, "p8_mahomes_dive", custom_zoom="crop=in_w*0.80:in_h*0.80:(in_w-out_w)/2:(in_h-out_h)/2,scale=1280:720,fps=30")

# 9. Studio: 284.5s -> 420.0s (135.5s) - Red zone critical, Tom Brady comparison, Nate on trimming fat
p9 = make_studio(284.5, 135.5, "p9")

# 10. Highlight 5: 420.0s -> 438.0s (18.0s) - Mahomes playoff hero ball & celebration (Muted, Nate voice)
p10 = make_highlight(420.0, 18.0, mahomes_celeb_src, 5.0, "p10_mahomes_hero", custom_zoom="crop=in_w*0.82:in_h*0.82:(in_w-out_w)/2:(in_h-out_h)/2,scale=1280:720,fps=30")

# 11. Studio: 438.0s -> 518.0s (80.0s) - Hunters vs Hunted, Chiefs edge and hunger
p11 = make_studio(438.0, 80.0, "p11")

# 12. Highlight 6: 518.0s -> 536.0s (18.0s) - EXACT PLAY: Walker 4th & 1 60-yd TD vs Broncos (Muted, Wilson voice)
p12 = make_highlight(518.0, 18.0, walker_broncos_src, 2.0, "p12_walker_4th_down", custom_zoom="crop=in_w*0.80:in_h*0.80:(in_w-out_w)/2:(in_h-out_h)/2,scale=1280:720,fps=30")

# 13. Studio: 536.0s -> 550.0s (14.0s) - Power hitters and Spags defense setup
p13 = make_studio(536.0, 14.0, "p13")

# 14. Highlight 7: 550.0s -> 562.0s (12.0s) - Chiefs Defense sacks & takeaways (Muted, Nate voice)
p14 = make_highlight(550.0, 12.0, defense_src, 3.0, "p14_defense_sacks", custom_zoom="crop=in_w*0.80:in_h*0.80:(in_w-out_w)/2:(in_h-out_h)/2,scale=1280:720,fps=30")

# 15. Studio: 562.0s -> 566.0s (4.0s) - Nate Burleson concluding sentence with audio fadeout
p15 = temp_dir / "p15.mp4"
print("Rendering p15 (conclusion with fadeout)...")
subprocess.run([
    "ffmpeg", "-y", "-ss", "562.0", "-i", str(cbs_src), "-t", "4.0",
    "-vf", "scale=1280:720,fps=30",
    "-af", "afade=t=out:st=3.0:d=1.0",
    "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", str(p15)
], check=True, capture_output=True)

# Concatenate all parts
concat_txt = temp_dir / "concat_v1.txt"
parts = [p1, p2, p3, p4, p5, p6a, p6b, p7, p8, p9, p10, p11, p12, p13, p14, p15]
with open(concat_txt, "w", encoding="utf-8") as f:
    for p in parts:
        f.write(f"file '{p.resolve().as_posix()}'\n")

print("Concatenating 15 parts into final Master Video 1 Extended...")
subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt),
    "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-c:a", "aac", "-b:a", "192k",
    str(output_v1)
], check=True, capture_output=True)

print("SUCCESS! Created Video 1 Extended Full:", output_v1)
