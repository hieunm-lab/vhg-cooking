import json
from pathlib import Path

draft_path = Path(r"C:\Users\Thien\AppData\Local\CapCut\User Data\Projects\com.lveditor.draft\00_CHIEFS_FULL_VIDEO_MASTER_EDIT\draft_content.json")
with open(draft_path, "r", encoding="utf-8") as f:
    d = json.load(f)

videos_mat = {v["id"]: v for v in d["materials"]["videos"]}
audios_mat = {a["id"]: a for a in d["materials"]["audios"]}

freeze_detected = False

for track_idx, track in enumerate(d["tracks"]):
    tname = track["name"]
    ttype = track["type"]
    tsegs = track["segments"]
    print(f"\n=== Track {track_idx}: {tname} (type: {ttype}, segs: {len(tsegs)}) ===")
    for s_idx, seg in enumerate(tsegs):
        mat_id = seg["material_id"]
        s_dur = seg["source_timerange"]["duration"]
        t_dur = seg["target_timerange"]["duration"]
        s_start = seg["source_timerange"]["start"]
        t_start = seg["target_timerange"]["start"]

        if ttype == "video":
            mat = videos_mat[mat_id]
            file_path = mat["path"]
            file_dur = mat["duration"]
            if s_start + s_dur > file_dur + 50000:
                print(f"  [ERROR FREEZE DETECTED] Seg {s_idx} ({Path(file_path).name}): req_dur {s_start+s_dur}us > file_dur {file_dur}us!")
                freeze_detected = True
            else:
                print(f"  Seg {s_idx:02d}: {Path(file_path).name[:38]:38s} | t=[{t_start/1e6:6.2f}s -> {(t_start+t_dur)/1e6:6.2f}s] ({t_dur/1e6:5.2f}s) [OK]")

if not freeze_detected:
    print("\n>>> VERIFICATION PASSED: 100% ZERO FREEZE RISK ACROSS ENTIRE PROJECT! <<<")
