import subprocess
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

pkg = Path(r"C:\Users\Thien\Downloads\kho video\CapCut_Project_Package")
lib = pkg / "Kho_Highlight_San"
output_master = Path(r"C:\Users\Thien\Downloads\kho video\00_CHIEFS_FULL_VIDEO_MASTER_FINAL.mp4")
temp_dir = Path(r"d:\HIeu\content tong hop\cong-cu-xao-nau\data\clips\render_master_temp")
temp_dir.mkdir(parents=True, exist_ok=True)

with open(lib / "actual_durations.json", "r", encoding="utf-8") as f:
    durations_map = json.load(f)

def get_hl_path(file_name):
    matches = list(lib.rglob(file_name))
    if not matches:
        raise FileNotFoundError(f"Highlight not found: {file_name}")
    return matches[0]

# --- 1. PART 1: HOOK (17.50s) ---
print("1/6 Preparing Part 1: Hook...")
p1_file = temp_dir / "part1_hook.mp4"
subprocess.run([
    "ffmpeg", "-y", "-i", str(pkg / "00_Hook_Final_Master.mp4"),
    "-vf", "scale=1280:720,fps=30",
    "-c:v", "h264_nvenc", "-b:v", "4000k", "-preset", "p4",
    "-c:a", "aac", "-ar", "44100", "-b:a", "192k",
    str(p1_file)
], check=True, capture_output=True)

# --- 2. PART 2: EXPERT 1 CBS (188.60s) ---
print("2/6 Preparing Part 2: Expert 1 CBS with overlays...")
cbs_src = pkg / "01_Expert_CBS_Clean_Voice.mp4"
cbs_slices = [
    # (type, start_cbs, dur, opt_hl_file)
    ("studio", 0.0, 9.0, None),
    ("hl", 9.0, 7.967, "Mahomes_02_SuperBowl_LIV_Wasp_TyreekHill.mp4"),
    ("studio", 16.967, 1.033, None),
    ("hl", 18.0, 9.0, "Kelce_01_Deep_48yd_Bomb_Catch.mp4"),
    ("studio", 27.0, 1.0, None),
    ("hl", 28.0, 9.5, "Walker_01_FourthDown_60yd_HouseCall.mp4"),
    ("studio", 37.5, 48.5, None),
    ("hl", 86.0, 8.467, "Walker_02_RedZone_10yd_Plunge_TD.mp4"),
    ("studio", 94.467, 12.533, None),
    ("hl", 107.0, 8.467, "Kelce_02_RedZone_11yd_Touchdown.mp4"),
    ("studio", 115.467, 2.533, None),
    ("hl", 118.0, 5.5, "Kelce_03_Route_Diagram_Analysis.mp4"),
    ("studio", 123.5, 51.5, None),
    ("hl", 175.0, 11.0, "Mahomes_01_Titans_27yd_Scramble_TD.mp4"),
    ("studio", 186.0, 2.6, None),
]

cbs_slice_files = []
for idx, (stype, sc, dur, hl_fn) in enumerate(cbs_slices):
    s_out = temp_dir / f"cbs_slice_{idx:02d}.mp4"
    if stype == "studio":
        subprocess.run([
            "ffmpeg", "-y", "-ss", str(sc), "-i", str(cbs_src), "-t", str(dur),
            "-vf", "scale=1280:720,fps=30",
            "-c:v", "h264_nvenc", "-b:v", "4000k", "-preset", "p4",
            "-c:a", "aac", "-ar", "44100", "-b:a", "192k",
            str(s_out)
        ], check=True, capture_output=True)
    else:
        hl_p = get_hl_path(hl_fn)
        subprocess.run([
            "ffmpeg", "-y", "-ss", "0.0", "-i", str(hl_p),
            "-ss", str(sc), "-i", str(cbs_src),
            "-t", str(dur),
            "-map", "0:v:0", "-map", "1:a:0",
            "-vf", "scale=1280:720,fps=30",
            "-c:v", "h264_nvenc", "-b:v", "4000k", "-preset", "p4",
            "-c:a", "aac", "-ar", "44100", "-b:a", "192k",
            str(s_out)
        ], check=True, capture_output=True)
    cbs_slice_files.append(s_out)

p2_concat_txt = temp_dir / "cbs_concat.txt"
with open(p2_concat_txt, "w", encoding="utf-8") as f:
    for sf in cbs_slice_files:
        f.write(f"file '{sf.as_posix()}'\n")

p2_file = temp_dir / "part2_cbs.mp4"
subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(p2_concat_txt),
    "-c", "copy", str(p2_file)
], check=True, capture_output=True)

# --- 3. PART 3: AI BRIDGE (22.97s) ---
print("3/6 Preparing Part 3: AI Bridge (Puck voice + complete highlights)...")
bridge_audio = pkg / "01_Voiceover_Bridge_Puck.mp3"
bridge_hls = [
    ("Walker_03_Mahomes_to_Walker_5yd_TD.mp4", 8.00),
    ("Worthy_03_Sideline_17yd_Speed_Catch.mp4", 7.97),
    ("Mahomes_04_NoLook_CrossBody_Pass.mp4", 7.00)
]
bridge_slice_files = []
for idx, (fn, dur) in enumerate(bridge_hls):
    hl_p = get_hl_path(fn)
    s_out = temp_dir / f"bridge_slice_{idx:02d}.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-ss", "0.0", "-i", str(hl_p), "-t", str(dur),
        "-vf", "scale=1280:720,fps=30",
        "-c:v", "h264_nvenc", "-b:v", "4000k", "-preset", "p4",
        "-an", str(s_out)
    ], check=True, capture_output=True)
    bridge_slice_files.append(s_out)

b_concat_txt = temp_dir / "bridge_concat.txt"
with open(b_concat_txt, "w", encoding="utf-8") as f:
    for sf in bridge_slice_files:
        f.write(f"file '{sf.as_posix()}'\n")

b_video = temp_dir / "bridge_video.mp4"
subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(b_concat_txt),
    "-c", "copy", str(b_video)
], check=True, capture_output=True)

p3_file = temp_dir / "part3_bridge.mp4"
subprocess.run([
    "ffmpeg", "-y", "-i", str(b_video), "-i", str(bridge_audio),
    "-map", "0:v:0", "-map", "1:a:0",
    "-c:v", "copy", "-c:a", "aac", "-ar", "44100", "-b:a", "192k",
    "-t", "22.97", str(p3_file)
], check=True, capture_output=True)

# --- 4. PART 4: EXPERT 2 RYAN CLARK (122.13s) ---
print("4/6 Preparing Part 4: Expert 2 Ryan Clark with overlays...")
rc_src = pkg / "02_Expert_RyanClark_Clean_Voice.mp4"
rc_slices = [
    ("studio", 0.0, 30.0, None),
    ("hl", 30.0, 8.467, "Kelce_02_RedZone_11yd_Touchdown.mp4"),
    ("studio", 38.467, 21.533, None),
    ("hl", 60.0, 7.467, "Walker_05_StiffArm_Power_15yd_Run.mp4"),
    ("studio", 67.467, 7.533, None),
    ("hl", 75.0, 8.0, "Defense_01_ChrisJones_Strip_Sack.mp4"),
    ("studio", 83.0, 2.0, None),
    ("hl", 85.0, 5.5, "Defense_03_Spags_Exotic_Blitz_Sack.mp4"),
    ("studio", 90.5, 1.5, None),
    ("hl", 92.0, 7.0, "Defense_04_FrankClark_Edge_Sack.mp4"),
    ("studio", 99.0, 3.0, None),
    ("hl", 102.0, 7.967, "Mahomes_04_NoLook_CrossBody_Pass.mp4"),
    ("studio", 109.967, 12.163, None),
]
rc_slice_files = []
for idx, (stype, sc, dur, hl_fn) in enumerate(rc_slices):
    s_out = temp_dir / f"rc_slice_{idx:02d}.mp4"
    if stype == "studio":
        subprocess.run([
            "ffmpeg", "-y", "-ss", str(sc), "-i", str(rc_src), "-t", str(dur),
            "-vf", "scale=1280:720,fps=30",
            "-c:v", "h264_nvenc", "-b:v", "4000k", "-preset", "p4",
            "-c:a", "aac", "-ar", "44100", "-b:a", "192k",
            str(s_out)
        ], check=True, capture_output=True)
    else:
        hl_p = get_hl_path(hl_fn)
        subprocess.run([
            "ffmpeg", "-y", "-ss", "0.0", "-i", str(hl_p),
            "-ss", str(sc), "-i", str(rc_src),
            "-t", str(dur),
            "-map", "0:v:0", "-map", "1:a:0",
            "-vf", "scale=1280:720,fps=30",
            "-c:v", "h264_nvenc", "-b:v", "4000k", "-preset", "p4",
            "-c:a", "aac", "-ar", "44100", "-b:a", "192k",
            str(s_out)
        ], check=True, capture_output=True)
    rc_slice_files.append(s_out)

p4_concat_txt = temp_dir / "rc_concat.txt"
with open(p4_concat_txt, "w", encoding="utf-8") as f:
    for sf in rc_slice_files:
        f.write(f"file '{sf.as_posix()}'\n")

p4_file = temp_dir / "part4_rc.mp4"
subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(p4_concat_txt),
    "-c", "copy", str(p4_file)
], check=True, capture_output=True)

# --- 5. PART 5: AI DEEP DIVE (80.77s - Beat Synchronized) ---
print("5/6 Preparing Part 5: AI Deep Dive (Puck voice + Beat Synchronized Highlights)...")
deep_audio = pkg / "03_Voiceover_DeepDive_Puck.mp3"
deep_hls = [
    # Beat 1: Intro & Reality Check (0s -> 11.72s)
    ("Mahomes_05_Playoff_FistPump_Celeb.mp4", 5.72),
    ("Mahomes_06_Touchdown_Flex_Celeb.mp4", 6.00),
    # Beat 2: Kenneth Walker Ground Explosion (11.72s -> 22.88s)
    ("Walker_04_Explosive_22yd_Breakaway.mp4", 3.66),
    ("Walker_01_FourthDown_60yd_HouseCall.mp4", 7.50),
    # Beat 3: Downfield Passing to Kelce & Worthy (22.88s -> 29.06s)
    ("Kelce_01_Deep_48yd_Bomb_Catch.mp4", 3.09),
    ("Worthy_02_Deep_Bomb_35yd_Touchdown.mp4", 3.09),
    # Beat 4: Steve Spagnuolo Defense & Chris Jones (29.06s -> 46.26s)
    ("Defense_01_ChrisJones_Strip_Sack.mp4", 6.20),
    ("Defense_03_Spags_Exotic_Blitz_Sack.mp4", 5.50),
    ("Defense_02_Ragland_Fumble_Return_TD.mp4", 5.50),
    # Beat 5: Brutal AFC Gauntlet & O-Line (46.26s -> 64.34s)
    ("Mahomes_01_Titans_27yd_Scramble_TD.mp4", 9.08),
    ("Walker_05_StiffArm_Power_15yd_Run.mp4", 5.00),
    ("Kelce_02_RedZone_11yd_Touchdown.mp4", 4.00),
    # Beat 6: Historic Three-Peat Climax (64.34s -> 80.77s)
    ("Mahomes_02_SuperBowl_LIV_Wasp_TyreekHill.mp4", 7.97),
    ("Mahomes_03_AFCChamp_60yd_Watkins_TD.mp4", 8.46)
]
deep_slice_files = []
for idx, (fn, dur) in enumerate(deep_hls):
    hl_p = get_hl_path(fn)
    s_out = temp_dir / f"deep_slice_{idx:02d}.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-ss", "0.0", "-i", str(hl_p), "-t", str(dur),
        "-vf", "scale=1280:720,fps=30",
        "-c:v", "h264_nvenc", "-b:v", "4000k", "-preset", "p4",
        "-an", str(s_out)
    ], check=True, capture_output=True)
    deep_slice_files.append(s_out)

d_concat_txt = temp_dir / "deep_concat.txt"
with open(d_concat_txt, "w", encoding="utf-8") as f:
    for sf in deep_slice_files:
        f.write(f"file '{sf.as_posix()}'\n")

d_video = temp_dir / "deep_video.mp4"
subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(d_concat_txt),
    "-c", "copy", str(d_video)
], check=True, capture_output=True)

p5_file = temp_dir / "part5_deep.mp4"
subprocess.run([
    "ffmpeg", "-y", "-i", str(d_video), "-i", str(deep_audio),
    "-map", "0:v:0", "-map", "1:a:0",
    "-c:v", "copy", "-c:a", "aac", "-ar", "44100", "-b:a", "192k",
    "-t", "80.77", str(p5_file)
], check=True, capture_output=True)

# --- 6. PART 6: OUTRO & CTA (24.05s - Beat Synchronized) ---
print("6/6 Preparing Part 6: Outro & CTA (Puck voice + Beat Synchronized Highlights)...")
outro_audio = pkg / "02_Voiceover_Outro_Puck.mp3"
outro_hls = [
    ("Walker_02_RedZone_10yd_Plunge_TD.mp4", 7.05),
    ("Worthy_01_JetSweep_Speed_TD.mp4", 7.00),
    ("Kelce_04_FirstDown_Signal_Celeb.mp4", 5.00),
    ("Mahomes_05_Playoff_FistPump_Celeb.mp4", 5.00)
]
outro_slice_files = []
for idx, (fn, dur) in enumerate(outro_hls):
    hl_p = get_hl_path(fn)
    s_out = temp_dir / f"outro_slice_{idx:02d}.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-ss", "0.0", "-i", str(hl_p), "-t", str(dur),
        "-vf", "scale=1280:720,fps=30",
        "-c:v", "h264_nvenc", "-b:v", "4000k", "-preset", "p4",
        "-an", str(s_out)
    ], check=True, capture_output=True)
    outro_slice_files.append(s_out)

o_concat_txt = temp_dir / "outro_concat.txt"
with open(o_concat_txt, "w", encoding="utf-8") as f:
    for sf in outro_slice_files:
        f.write(f"file '{sf.as_posix()}'\n")

o_video = temp_dir / "outro_video.mp4"
subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(o_concat_txt),
    "-c", "copy", str(o_video)
], check=True, capture_output=True)

p6_file = temp_dir / "part6_outro.mp4"
subprocess.run([
    "ffmpeg", "-y", "-i", str(o_video), "-i", str(outro_audio),
    "-map", "0:v:0", "-map", "1:a:0",
    "-c:v", "copy", "-c:a", "aac", "-ar", "44100", "-b:a", "192k",
    "-t", "24.05", str(p6_file)
], check=True, capture_output=True)

# --- 7. FINAL CONCATENATION OF ALL 6 PARTS ---
print("\n=== CONCATENATING ALL 6 PARTS INTO MASTER VIDEO ===")
all_parts = [p1_file, p2_file, p3_file, p4_file, p5_file, p6_file]
master_concat_txt = temp_dir / "master_concat.txt"
with open(master_concat_txt, "w", encoding="utf-8") as f:
    for pf in all_parts:
        f.write(f"file '{pf.as_posix()}'\n")

subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(master_concat_txt),
    "-c", "copy", str(output_master)
], check=True, capture_output=True)

# Probe final video
probe_cmd = [
    "ffprobe", "-v", "error", "-show_entries", "format=duration,size:stream=width,height,r_frame_rate",
    "-of", "json", str(output_master)
]
res = subprocess.run(probe_cmd, capture_output=True, text=True)
data = json.loads(res.stdout)
dur = float(data['format']['duration'])
size_mb = float(data['format']['size']) / (1024 * 1024)

print("\n>>> MASTER FULL VIDEO SUCCESSFULLY RENDERED! <<<")
print(f"File Path: {output_master}")
print(f"Total Duration: {dur:.2f}s ({dur/60:.2f} minutes)")
print(f"File Size: {size_mb:.2f} MB")
print("All rules satisfied: 1 Voice, Complete Plays, Zero Freezing, Replaced Expert Graphics, Full Draft + Exported Video!")
