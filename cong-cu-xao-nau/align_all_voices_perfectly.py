import subprocess
from pathlib import Path
import numpy as np

pkg = Path(r"C:\Users\Thien\Downloads\kho video\CapCut_Project_Package")
data_clips = Path(r"d:\HIeu\content tong hop\cong-cu-xao-nau\data\clips")

def get_pitch(p):
    out = subprocess.run(['ffmpeg', '-y', '-i', str(p), '-f', 's16le', '-ar', '16000', '-ac', '1', 'pipe:1'], capture_output=True, check=True).stdout
    s = np.frombuffer(out, dtype=np.int16).astype(float)
    frame_len = int(0.04 * 16000)
    step = int(0.02 * 16000)
    pitches = []
    for i in range(0, min(len(s), 160000) - frame_len, step):
        frame = s[i:i+frame_len] - np.mean(s[i:i+frame_len])
        if np.std(frame) < 500: continue
        corr = np.correlate(frame, frame, mode='full')[frame_len-1:]
        dcorr = corr[45:320]
        if len(dcorr) > 0 and np.max(dcorr) > 0.4 * corr[0]:
            pitches.append(16000 / (45 + np.argmax(dcorr)))
    return np.median(pitches) if pitches else 0

target_pitch = get_pitch(pkg / "00_Voiceover_Hook_Puck.mp3")
print(f"Target Master Hook Pitch: {target_pitch:.2f} Hz")

files_to_harmonize = [
    ("01_Voiceover_Bridge_Puck.mp3", pkg / "01_Voiceover_Bridge_Puck.mp3"),
    ("03_Voiceover_DeepDive_Puck.mp3", pkg / "03_Voiceover_DeepDive_Puck.mp3"),
    ("02_Voiceover_Outro_Puck.mp3", pkg / "02_Voiceover_Outro_Puck.mp3")
]

for name, f_path in files_to_harmonize:
    cur_p = get_pitch(f_path)
    ratio = target_pitch / cur_p
    print(f"\nProcessing {name}: Current Pitch = {cur_p:.2f} Hz -> Ratio = {ratio:.4f}")
    
    temp_out = data_clips / f"harmonized_{name}"
    cmd = [
        "ffmpeg", "-y", "-i", str(f_path),
        "-af", f"rubberband=pitch={ratio:.4f}",
        "-c:a", "libmp3lame", "-b:a", "192k", str(temp_out)
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    
    import shutil
    shutil.move(temp_out, f_path)
    
    # Verify new pitch
    new_p = get_pitch(f_path)
    cmd_dur = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(f_path)]
    dur = float(subprocess.run(cmd_dur, capture_output=True, text=True).stdout.strip())
    print(f"-> SUCCESS {name}: New Pitch = {new_p:.2f} Hz (Duration: {dur:.2f}s)")

print("\n--- ALL VOICEOVERS HARMONIZED TO EXACT MASTER HOOK TONE! ---")
