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

def make_puck_chunk(text, out_mp3, tag):
    print(f"\n[{tag}] Generating...")
    for attempt in range(5):
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
            print(f"[{tag}] Attempt {attempt+1} got error/429. Sleeping 45s...")
            time.sleep(45)
    raise RuntimeError(f"Failed {tag}")

# Half 1: Coach Cowher vs Ryan Clark, Kenneth Walker & Defense
half_1 = (
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
    "This defense gives Andy Reid the ultimate safety net!"
)

# Half 2: Brutal AFC Schedule & 3-Peat Dynasty
half_2 = (
    "Now look at the brutal schedule ahead! Ryan Clark is dead right about the Buffalo Bills and Josh Allen! "
    "The road to the Super Bowl runs through Lamar Jackson, Joe Burrow, and a vicious AFC battlefield! "
    "The biggest key for Kansas City isn't talent; it is offensive line health! "
    "If the protection holds up and keeps number fifteen clean, Kansas City controls their own destiny! "
    "So here is the ultimate question! Can the Kansas City Chiefs actually achieve the first three-peat in NFL history?! "
    "No team in the Super Bowl era has ever won three straight titles! "
    "It takes relentless grit, clutch execution, and championship swagger! "
    "But with Patrick Mahomes in his prime, an explosive ground game, and a suffocating defense, betting against the Chiefs in January is a losing bet!"
)

part_1 = make_puck_chunk(half_1, data_clips / "deep_half1.mp3", "half1")
print("Sleeping 35s to respect API rate limits...")
time.sleep(35)
part_2 = make_puck_chunk(half_2, data_clips / "deep_half2.mp3", "half2")

concat_list = data_clips / "deep_concat.txt"
with open(concat_list, "w", encoding="utf-8") as f:
    f.write(f"file '{part_1.resolve().as_posix()}'\n")
    f.write(f"file '{part_2.resolve().as_posix()}'\n")

deep_final = pkg / "03_Voiceover_DeepDive_Puck.mp3"
subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list),
    "-c:a", "libmp3lame", "-b:a", "192k", str(deep_final)
], check=True, capture_output=True)

print("SUCCESS! Generated unified Deep Dive voiceover:", deep_final)
