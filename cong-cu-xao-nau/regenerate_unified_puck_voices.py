import time
import subprocess
from pathlib import Path
from google import genai
from google.genai import types

pkg = Path(r"C:\Users\Thien\Downloads\kho video\CapCut_Project_Package")
data_clips = Path(r"d:\HIeu\content tong hop\cong-cu-xao-nau\data\clips")

client = genai.Client(api_key="AQ.Ab8RN6JLSF5hvTk42FaM0pxJqlZRmKWtYFmRVU0hQiDlEm8vYg")

cfg = types.GenerateContentConfig(
    response_modalities=["AUDIO"],
    speech_config=types.SpeechConfig(
        voice_config=types.VoiceConfig(
            prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Puck")
        )
    )
)

def make_puck_audio(text, out_mp3, tag):
    print(f"\n[{tag}] Generating with Puck voice...")
    for attempt in range(3):
        try:
            resp = client.models.generate_content(
                model="gemini-3.8-flash-tts",
                contents=text,
                config=cfg
            )
            raw = resp.candidates[0].content.parts[0].inline_data.data
            temp_wav = data_clips / f"temp_{tag}.wav"
            with open(temp_wav, "wb") as f:
                f.write(raw)
            subprocess.run([
                "ffmpeg", "-y", "-i", str(temp_wav), "-b:a", "192k", str(out_mp3)
            ], check=True, capture_output=True)
            temp_wav.unlink(missing_ok=True)
            print(f"[{tag}] Succeeded -> {out_mp3.name}")
            return out_mp3
        except Exception as e:
            print(f"[{tag}] Rate limited or error: {e}. Retrying in 25s...")
            time.sleep(25)
    raise RuntimeError(f"Failed to generate {tag}")

# 1. Bridge Script (High Energy Puck)
bridge_text = (
    "Coach Bill Cowher and the CBS crew make a massive statement! "
    "When Patrick Mahomes gets legitimate backfield support, this offense becomes practically unstoppable! "
    "But not everyone is convinced Kansas City has an easy road to another Lombardi trophy! "
    "Over on the Stephen A. Smith Show, NFL analyst Ryan Clark is sounding the alarm on the brutal AFC gauntlet! "
    "Listen closely to how Ryan Clark breaks this down right now!"
)

# 2. Outro Script (High Energy Puck)
outro_text = (
    "Chiefs Kingdom, the message is loud and clear! "
    "With Kenneth Walker pounding the rock and Patrick Mahomes commanding the field, this dynasty is ready to make history! "
    "But we want to hear from you! Can ANY team in the NFL stop Kansas City right now?! "
    "Drop your score predictions in the comments below! "
    "Smash that like button, hit subscribe, and turn on notifications so you never miss our breaking Chiefs coverage! "
    "We will catch you in the next one!"
)

# 3. Deep Dive Sections (4 Punchy Chunks)
deep_p1 = (
    "Now let's take a step back and examine the full picture! "
    "You heard Coach Bill Cowher, and you heard the fiery reality check from Ryan Clark! "
    "So who actually has it right?! The truth is, both of them are dead on! "
    "For the past two seasons, defenses played two-high safeties and dared the Chiefs to run the ball! "
    "Kansas City stalled because they lacked an explosive home-run threat in the backfield! "
    "With Kenneth Walker, everything changes! He turns routine handoffs into sixty-yard house calls! "
    "And the second linebackers hesitate, Patrick Mahomes hits Travis Kelce and Xavier Worthy wide open downfield! That is lethal!"
)

deep_p2 = (
    "And make no mistake about it! The national media is completely sleeping on Steve Spagnuolo's defense! "
    "Everyone talks about Patrick Mahomes, but this defense closed out the Super Bowl! "
    "Chris Jones remains the most terrifying interior disruptor on the planet! "
    "When the game is on the line in the fourth quarter, Spags dials up exotic blitzes that destroy opposing quarterbacks! "
    "This defense gives Andy Reid the ultimate safety net!"
)

deep_p3 = (
    "Now look at the brutal schedule ahead! Ryan Clark is dead right about the Buffalo Bills and Josh Allen! "
    "The road to the Super Bowl runs through Lamar Jackson, Joe Burrow, and a vicious AFC battlefield! "
    "The biggest key for Kansas City isn't talent; it is offensive line health! "
    "If the protection holds up and keeps number fifteen clean, Kansas City controls their own destiny!"
)

deep_p4 = (
    "So here is the ultimate question! Can the Kansas City Chiefs actually achieve the first three-peat in NFL history?! "
    "No team in the Super Bowl era has ever won three straight titles! "
    "It takes relentless grit, clutch execution, and championship swagger! "
    "But with Patrick Mahomes in his prime, an explosive ground game, and a suffocating defense, betting against the Chiefs in January is a losing bet!"
)

# Run generation with spacing
f_bridge = make_puck_audio(bridge_text, pkg / "01_Voiceover_Bridge_Puck.mp3", "bridge")
time.sleep(22)

f_outro = make_puck_audio(outro_text, pkg / "02_Voiceover_Outro_Puck.mp3", "outro")
time.sleep(22)

f_d1 = make_puck_audio(deep_p1, data_clips / "deep_p1.mp3", "deep_p1")
time.sleep(22)

f_d2 = make_puck_audio(deep_p2, data_clips / "deep_p2.mp3", "deep_p2")
time.sleep(22)

f_d3 = make_puck_audio(deep_p3, data_clips / "deep_p3.mp3", "deep_p3")
time.sleep(22)

f_d4 = make_puck_audio(deep_p4, data_clips / "deep_p4.mp3", "deep_p4")

# Concatenate deep dive parts
concat_list = data_clips / "deep_concat.txt"
with open(concat_list, "w", encoding="utf-8") as f:
    for p in [f_d1, f_d2, f_d3, f_d4]:
        f.write(f"file '{p.resolve().as_posix()}'\n")

deep_final = pkg / "03_Voiceover_DeepDive_Puck.mp3"
subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list),
    "-c:a", "libmp3lame", "-b:a", "192k", str(deep_final)
], check=True, capture_output=True)

print("\n--- ALL VOICEOVERS REGENERATED WITH PURE UNIFIED PUCK VOICE! ---")
