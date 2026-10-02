import subprocess
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

base_out = Path(r"C:\Users\Thien\Downloads\kho video\CapCut_Project_Package\Kho_Highlight_San")
data_clips = Path(r"d:\HIeu\content tong hop\cong-cu-xao-nau\data\clips")
raw_dir = data_clips / "raw_sources"
pkg = Path(r"C:\Users\Thien\Downloads\kho video\CapCut_Project_Package")

# Source files:
src_dolphins = raw_dir / "week3_dolphins.webm"
src_ravens = raw_dir / "week1_ravens.webm"
src_top10 = raw_dir / "mahomes_top10.mkv"
src_walker_broncos = data_clips / "walker_4th_down_broncos.webm"
src_defense = data_clips / "chiefs_defense_sacks.mkv"
src_mahomes_run = data_clips / "mahomes_run_raw.webm"
src_mahomes_celeb = data_clips / "mahomes_celebration_raw.webm"
src_kelce_pkg = pkg / "03_Travis_Kelce_Reboot.mp4"

zoom_filter = "crop=in_w*0.82:in_h*0.82:(in_w-out_w)/2:(in_h-out_h)/2,scale=1280:720,fps=30"

clips_config = [
    # 01. PATRICK MAHOMES CLUTCH
    ("01_Patrick_Mahomes_Clutch", "Mahomes_01_Titans_27yd_Scramble_TD.mp4", src_mahomes_run, 8.0, 11.0),
    ("01_Patrick_Mahomes_Clutch", "Mahomes_02_SuperBowl_LIV_Wasp_TyreekHill.mp4", src_top10, 151.0, 8.0),
    ("01_Patrick_Mahomes_Clutch", "Mahomes_03_AFCChamp_60yd_Watkins_TD.mp4", src_top10, 324.5, 9.0),
    ("01_Patrick_Mahomes_Clutch", "Mahomes_04_NoLook_CrossBody_Pass.mp4", src_top10, 219.0, 8.0),
    ("01_Patrick_Mahomes_Clutch", "Mahomes_05_Playoff_FistPump_Celeb.mp4", src_mahomes_celeb, 12.0, 6.0),
    ("01_Patrick_Mahomes_Clutch", "Mahomes_06_Touchdown_Flex_Celeb.mp4", src_mahomes_celeb, 22.0, 6.0),

    # 02. KENNETH WALKER POWER
    ("02_Kenneth_Walker_Power", "Walker_01_FourthDown_60yd_HouseCall.mp4", src_walker_broncos, 2.0, 9.5),
    ("02_Kenneth_Walker_Power", "Walker_02_RedZone_10yd_Plunge_TD.mp4", src_dolphins, 63.0, 8.5),
    ("02_Kenneth_Walker_Power", "Walker_03_Mahomes_to_Walker_5yd_TD.mp4", src_dolphins, 243.0, 8.5),
    ("02_Kenneth_Walker_Power", "Walker_04_Explosive_22yd_Breakaway.mp4", src_dolphins, 406.5, 7.5),
    ("02_Kenneth_Walker_Power", "Walker_05_StiffArm_Power_15yd_Run.mp4", src_dolphins, 652.5, 7.5),

    # 03. TRAVIS KELCE REBOOT
    ("03_Travis_Kelce_Reboot", "Kelce_01_Deep_48yd_Bomb_Catch.mp4", src_dolphins, 35.5, 9.0),
    ("03_Travis_Kelce_Reboot", "Kelce_02_RedZone_11yd_Touchdown.mp4", src_dolphins, 763.0, 8.5),
    ("03_Travis_Kelce_Reboot", "Kelce_03_Route_Diagram_Analysis.mp4", src_kelce_pkg, 1.0, 5.5),
    ("03_Travis_Kelce_Reboot", "Kelce_04_FirstDown_Signal_Celeb.mp4", src_kelce_pkg, 6.5, 5.0),

    # 04. XAVIER WORTHY SPEED
    ("04_Xavier_Worthy_Speed", "Worthy_01_JetSweep_Speed_TD.mp4", src_ravens, 90.0, 7.5),
    ("04_Xavier_Worthy_Speed", "Worthy_02_Deep_Bomb_35yd_Touchdown.mp4", src_ravens, 644.5, 9.0),
    ("04_Xavier_Worthy_Speed", "Worthy_03_Sideline_17yd_Speed_Catch.mp4", src_dolphins, 302.5, 8.5),

    # 05. CHIEFS DEFENSE & SPAGS
    ("05_Chiefs_Defense_Spags", "Defense_01_ChrisJones_Strip_Sack.mp4", src_ravens, 181.0, 8.0),
    ("05_Chiefs_Defense_Spags", "Defense_02_Ragland_Fumble_Return_TD.mp4", src_defense, 33.0, 7.5),
    ("05_Chiefs_Defense_Spags", "Defense_03_Spags_Exotic_Blitz_Sack.mp4", src_defense, 52.5, 5.5),
    ("05_Chiefs_Defense_Spags", "Defense_04_FrankClark_Edge_Sack.mp4", src_defense, 77.5, 7.0),
]

print(f"=== BATCH CUTTING {len(clips_config)} COMPLETE NARRATIVE HIGHLIGHTS ===")

actual_durations = {}

for folder_name, file_name, src_file, start_sec, dur_sec in clips_config:
    target_dir = base_out / folder_name
    target_dir.mkdir(parents=True, exist_ok=True)
    out_file = target_dir / file_name

    cmd = [
        "ffmpeg", "-y", "-ss", str(start_sec), "-i", str(src_file), "-t", str(dur_sec),
        "-vf", zoom_filter,
        "-an",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        str(out_file)
    ]
    subprocess.run(cmd, check=True, capture_output=True)

    # Probe exact duration
    probe_cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(out_file)
    ]
    res = subprocess.run(probe_cmd, capture_output=True, text=True)
    dur_str = res.stdout.strip()
    actual_dur = float(dur_str)
    actual_durations[file_name] = actual_dur
    print(f"OK: [{folder_name}] {file_name} -> {actual_dur:.3f}s")

with open(base_out / "actual_durations.json", "w", encoding="utf-8") as f:
    json.dump(actual_durations, f, indent=2)

print("\n=== ALL COMPLETE HIGHLIGHTS READY & PROBED ===")
