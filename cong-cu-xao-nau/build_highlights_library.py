import subprocess
from pathlib import Path

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
src_walker_pkg = pkg / "02_Highlight_Kenneth_Walker.mp4"
src_kelce_pkg = pkg / "03_Travis_Kelce_Reboot.mp4"

# Filter: 18% center zoom, scale 1280x720, 30fps, completely MUTED (-an)
zoom_filter = "crop=in_w*0.82:in_h*0.82:(in_w-out_w)/2:(in_h-out_h)/2,scale=1280:720,fps=30"

clips_config = [
    # 01. PATRICK MAHOMES
    ("01_Patrick_Mahomes_Clutch", "Mahomes_01_EndZone_Dive_TD.mp4", src_mahomes_run, 8.5, 4.5),
    ("01_Patrick_Mahomes_Clutch", "Mahomes_02_Sideline_Scramble_Magic.mp4", src_top10, 385.0, 4.5),
    ("01_Patrick_Mahomes_Clutch", "Mahomes_03_SuperBowl_GameWinner_TD.mp4", src_top10, 420.0, 5.0),
    ("01_Patrick_Mahomes_Clutch", "Mahomes_04_SuperBowl_Deep_Bomb_Wasp.mp4", src_top10, 155.0, 4.5),
    ("01_Patrick_Mahomes_Clutch", "Mahomes_05_Playoff_FistPump_Celeb.mp4", src_mahomes_celeb, 14.0, 4.5),
    ("01_Patrick_Mahomes_Clutch", "Mahomes_06_Touchdown_Flex_Celeb.mp4", src_mahomes_celeb, 23.0, 4.5),

    # 02. KENNETH WALKER III
    ("02_Kenneth_Walker_Power", "Walker_01_73yd_Breakaway_Run.mp4", src_walker_pkg, 2.0, 4.5),
    ("02_Kenneth_Walker_Power", "Walker_02_FourthDown_60yd_HouseCall.mp4", src_walker_broncos, 6.0, 5.0),
    ("02_Kenneth_Walker_Power", "Walker_03_Tackle_Break_Burst.mp4", src_walker_pkg, 0.0, 4.5),
    ("02_Kenneth_Walker_Power", "Walker_04_RedZone_Plunge_TD.mp4", src_dolphins, 40.0, 4.5),
    ("02_Kenneth_Walker_Power", "Walker_05_StiffArm_FirstDown.mp4", src_walker_broncos, 1.0, 4.5),

    # 03. TRAVIS KELCE
    ("03_Travis_Kelce_Reboot", "Kelce_01_Deep_Catch_Downfield.mp4", src_kelce_pkg, 1.0, 4.5),
    ("03_Travis_Kelce_Reboot", "Kelce_02_Football_Spike_Celeb.mp4", src_kelce_pkg, 4.0, 4.5),
    ("03_Travis_Kelce_Reboot", "Kelce_03_VRoute_PlayAction_Catch.mp4", src_kelce_pkg, 7.0, 4.5),
    ("03_Travis_Kelce_Reboot", "Kelce_04_FirstDown_Signal_Celeb.mp4", src_kelce_pkg, 9.0, 4.5),

    # 04. XAVIER WORTHY
    ("04_Xavier_Worthy_Speed", "Worthy_01_JetSweep_Speed_TD.mp4", src_ravens, 131.0, 4.5),
    ("04_Xavier_Worthy_Speed", "Worthy_02_Deep_Bomb_Touchdown.mp4", src_ravens, 650.0, 4.5),
    ("04_Xavier_Worthy_Speed", "Worthy_03_EndZone_HighStep_Celeb.mp4", src_ravens, 137.0, 4.5),

    # 05. CHIEFS DEFENSE & SPAGS
    ("05_Chiefs_Defense_Spags", "Defense_01_ChrisJones_Strip_Sack.mp4", src_defense, 7.5, 4.5),
    ("05_Chiefs_Defense_Spags", "Defense_02_Pocket_Crush_Sack.mp4", src_defense, 14.0, 4.5),
    ("05_Chiefs_Defense_Spags", "Defense_03_Edge_Pressure_Tackle.mp4", src_defense, 20.0, 4.5),
    ("05_Chiefs_Defense_Spags", "Defense_04_ThirdDown_Stop_Celeb.mp4", src_defense, 26.0, 4.5),
]

print(f"--- BATCH CUTTING {len(clips_config)} STANDARDIZED HIGHLIGHTS ---")
count = 0
for folder_name, file_name, src_file, start_sec, dur_sec in clips_config:
    target_dir = base_out / folder_name
    target_dir.mkdir(parents=True, exist_ok=True)
    out_file = target_dir / file_name

    cmd = [
        "ffmpeg", "-y", "-ss", str(start_sec), "-i", str(src_file), "-t", str(dur_sec),
        "-vf", zoom_filter,
        "-an", # 100% MUTED
        "-c:v", "libx264", "-preset", "fast", "-crf", "19",
        str(out_file)
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    count += 1
    print(f"[{count}/{len(clips_config)}] Generated: {folder_name}/{file_name} ({dur_sec}s)")

print("=== ALL HIGHLIGHTS SUCCESSFULLY GENERATED IN KHO_HIGHLIGHT_SAN ===")
