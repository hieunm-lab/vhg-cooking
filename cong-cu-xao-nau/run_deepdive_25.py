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
        voice_config=types.VoiceConfig(prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Puck"))
    )
)

half_1 = (
    "Now let us take a step back and examine the full picture! "
    "You heard Coach Bill Cowher, and you heard the fiery reality check from Ryan Clark! "
    "So who actually has it right?! The truth is, both of them are dead on! "
    "For the past two seasons, defenses played two-high safeties and dared the Chiefs to run the ball! "
    "Kansas City stalled because they lacked an explosive home-run threat in the backfield! "
    "With Kenneth Walker, everything changes! He turns routine handoffs into sixty-yard house calls! "
    "And the second linebackers hesitate, Patrick Mahomes hits Travis Kelce and Xavier Worthy wide open downfield! That is lethal! "
    "And make no mistake about it! The national media is completely sleeping on Steve Spagnuolo defense! "
    "Everyone talks about Patrick Mahomes, but this defense closed out the Super Bowl! "
    "Chris Jones remains the most terrifying interior disruptor on the planet! "
    "When the game is on the line in the fourth quarter, Spags dials up exotic blitzes that destroy opposing quarterbacks! "
    "This defense gives Andy Reid the ultimate safety net!"
)

half_2 = (
    "Now look at the brutal schedule ahead! Ryan Clark is dead right about the Buffalo Bills and Josh Allen! "
    "The road to the Super Bowl runs through Lamar Jackson, Joe Burrow, and a vicious AFC battlefield! "
    "The biggest key for Kansas City is not talent; it is offensive line health! "
    "If the protection holds up and keeps number fifteen clean, Kansas City controls their own destiny! "
    "So here is the ultimate question! Can the Kansas City Chiefs actually achieve the first three-peat in NFL history?! "
    "No team in the Super Bowl era has ever won three straight titles! "
    "It takes relentless grit, clutch execution, and championship swagger! "
    "But with Patrick Mahomes in his prime, an explosive ground game, and a suffocating defense, betting against the Chiefs in January is a losing bet!"
)

def make_chunk(text, out_mp3):
    resp = client.models.generate_content(model="gemini-2.5-flash-preview-tts", contents=text, config=cfg)
    raw = resp.candidates[0].content.parts[0].inline_data.data
    subprocess.run([
        "ffmpeg", "-y", "-f", "s16le", "-ar", "24000", "-ac", "1", "-i", "pipe:0",
        "-b:a", "192k", str(out_mp3)
    ], input=raw, check=True, capture_output=True)
    return out_mp3

print("Generating Part 1...")
p1 = make_chunk(half_1, data_clips / "deep25_1.mp3")
print("Generated Part 1:", p1)

print("Generating Part 2...")
p2 = make_chunk(half_2, data_clips / "deep25_2.mp3")
print("Generated Part 2:", p2)

# Concat
concat_txt = data_clips / "deep25_concat.txt"
with open(concat_txt, "w", encoding="utf-8") as f:
    f.write(f"file '{p1.resolve().as_posix()}'\n")
    f.write(f"file '{p2.resolve().as_posix()}'\n")

out_final = pkg / "03_Voiceover_DeepDive_Puck.mp3"
subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt),
    "-c:a", "libmp3lame", "-b:a", "192k", str(out_final)
], check=True, capture_output=True)

print("SUCCESS! Created unified Deep Dive Puck:", out_final)
