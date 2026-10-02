import sys
import time
import subprocess
from pathlib import Path
from xaonau import gemini_tts

pkg = Path(r"C:\Users\Thien\Downloads\kho video\CapCut_Project_Package")
data_clips = Path(r"d:\HIeu\content tong hop\cong-cu-xao-nau\data\clips")

bridge_text = (
    "Coach Bill Cowher and the CBS crew make a massive statement! "
    "When Patrick Mahomes gets legitimate backfield support, this offense becomes practically unstoppable! "
    "But not everyone is convinced Kansas City has an easy road to another Lombardi trophy! "
    "Over on the Stephen A. Smith Show, NFL analyst Ryan Clark is sounding the alarm on the brutal AFC gauntlet! "
    "Listen closely to how Ryan Clark breaks this down right now!"
)

deepdive_text = (
    "Now let's take a step back and examine the full picture! "
    "You heard Coach Bill Cowher, and you heard the fiery reality check from Ryan Clark! "
    "So who actually has it right?! The truth is, both of them are dead on! "
    "For the past two seasons, defenses played two-high safeties and dared the Chiefs to run the ball! "
    "Kansas City stalled because they lacked an explosive home-run threat in the backfield! "
    "With Kenneth Walker, everything changes! He turns routine handoffs into sixty-yard house calls! "
    "And the second linebackers hesitate, Patrick Mahomes hits Travis Kelce and Xavier Worthy wide open downfield! That is lethal! "
    "And make no mistake about it! The national media is completely sleeping on Steve Spagnuolo's defense! "
    "Everyone talks about Patrick Mahomes, but this defense closed out the Super Bowl! "
    "Chris Jones remains the most terrifying interior disruptor on the planet! "
    "When the game is on the line in the fourth quarter, Spags dials up exotic blitzes that destroy opposing quarterbacks! "
    "This defense gives Andy Reid the ultimate safety net! "
    "Now look at the brutal schedule ahead! Ryan Clark is dead right about the Buffalo Bills and Josh Allen! "
    "The road to the Super Bowl runs through Lamar Jackson, Joe Burrow, and a vicious AFC battlefield! "
    "The biggest key for Kansas City isn't talent; it is offensive line health! "
    "If the protection holds up and keeps number fifteen clean, Kansas City controls their own destiny! "
    "So here is the ultimate question! Can the Kansas City Chiefs actually achieve the first three-peat in NFL history?! "
    "No team in the Super Bowl era has ever won three straight titles! "
    "It takes relentless grit, clutch execution, and championship swagger! "
    "But with Patrick Mahomes in his prime, an explosive ground game, and a suffocating defense, betting against the Chiefs in January is a losing bet!"
)

outro_text = (
    "Chiefs Kingdom, the message is loud and clear! "
    "With Kenneth Walker pounding the rock and Patrick Mahomes commanding the field, this dynasty is ready to make history! "
    "But we want to hear from you! Can ANY team in the NFL stop Kansas City right now?! "
    "Drop your score predictions in the comments below! "
    "Smash that like button, hit subscribe, and turn on notifications so you never miss our breaking Chiefs coverage! "
    "We will catch you in the next one!"
)

def normalize_audio(in_path: Path, out_path: Path):
    """Normalize with loudnorm to ensure broadcast standard -16 LUFS and peak at -1.5 dB (zero clipping)."""
    temp = in_path.with_suffix(".norm.mp3")
    cmd = [
        "ffmpeg", "-y", "-i", str(in_path),
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
        "-c:a", "libmp3lame", "-b:a", "192k",
        str(temp)
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    temp.replace(out_path)

KEYS = [
    "AQ.Ab8RN6LAPykeX_3tg2cxgfYVOcAm9zejgSYqa6mZPLXgL2fN",
    "AQ.Ab8RN6JLSF5hvTk42FaM0pxJqlZRmKWtYFmRVU0hQiDlEm8vYg"
]

def generate_clean(text: str, target_file: Path, name: str):
    print(f"\n>>> Generating {name} with Gemini TTS (Puck)...")
    raw_file = data_clips / f"raw_{name}.mp3"
    
    success = False
    for attempt in range(5):
        key = KEYS[attempt % len(KEYS)]
        try:
            gemini_tts.generate_gemini_speech(
                text=text,
                voice_name="Puck",
                api_key=key,
                output_path=raw_file
            )
            success = True
            break
        except Exception as e:
            print(f"[{name}] Attempt {attempt+1} failed ({e}). Waiting 15s before retry...")
            time.sleep(15)
            
    if not success:
        raise RuntimeError(f"Failed to generate {name} after retries")
        
    print(f"Normalizing {name} to broadcast standard (-16 LUFS, Peak -1.5 dB)...")
    normalize_audio(raw_file, target_file)
    
    # Also copy to downloads / kho video root
    dest_copy = Path(r"C:\Users\Thien\Downloads\kho video") / target_file.name
    import shutil
    shutil.copy2(target_file, dest_copy)
    
    # Check duration and volume
    cmd_probe = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(target_file)]
    dur = float(subprocess.run(cmd_probe, capture_output=True, text=True).stdout.strip())
    print(f"SUCCESS: {name} -> Duration: {dur:.2f}s, Saved to {target_file.name} & kho video root")
    return dur

if __name__ == "__main__":
    # Generate Bridge
    dur_bridge = generate_clean(bridge_text, pkg / "01_Voiceover_Bridge_Puck.mp3", "Bridge")
    time.sleep(5)
    
    # Generate DeepDive
    dur_deepdive = generate_clean(deepdive_text, pkg / "03_Voiceover_DeepDive_Puck.mp3", "DeepDive")
    time.sleep(5)
    
    # Generate Outro
    dur_outro = generate_clean(outro_text, pkg / "02_Voiceover_Outro_Puck.mp3", "Outro")
    
    print("\n--- ALL VOICES GENERATED AND NORMALIZED PERFECTLY! ---")
