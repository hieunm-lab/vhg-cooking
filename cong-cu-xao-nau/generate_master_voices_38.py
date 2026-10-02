import sys
import subprocess
from pathlib import Path
from google import genai
from google.genai import types

data_clips = Path(r"d:\HIeu\content tong hop\cong-cu-xao-nau\data\clips")

client = genai.Client(api_key="AQ.Ab8RN6LAPykeX_3tg2cxgfYVOcAm9zejgSYqa6mZPLXgL2fNlg")
cfg = types.GenerateContentConfig(
    response_modalities=["AUDIO"],
    speech_config=types.SpeechConfig(
        voice_config=types.VoiceConfig(prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Puck"))
    )
)

deepdive_text = (
    "Chiefs Kingdom, now let's break down the full picture! "
    "You heard Coach Bill Cowher, and you heard the fiery reality check from Ryan Clark! "
    "Who actually has it right?! Both of them are dead on! "
    "For two straight seasons, defenses dared Kansas City to run the football! "
    "With Kenneth Walker, everything changes! Routine handoffs become sixty-yard house calls! "
    "And the second linebackers hesitate, Patrick Mahomes hits Travis Kelce and Xavier Worthy wide open downfield! That is lethal! "
    "And make no mistake! The national media is completely sleeping on Steve Spagnuolo's defense! "
    "Chris Jones remains the most terrifying game-wrecker on the planet! "
    "In the fourth quarter, Spags dials up exotic blitzes that destroy opposing quarterbacks! "
    "This defense gives Andy Reid the ultimate safety net! "
    "Now look at the brutal road ahead! Ryan Clark is dead right about Josh Allen and the AFC gauntlet! "
    "Lamar Jackson, Joe Burrow, and a vicious battlefield are waiting! "
    "The biggest key isn't talent; it is offensive line health! "
    "If the protection holds up and keeps number fifteen clean, Kansas City controls their own destiny! "
    "So can the Chiefs achieve the first historic three-peat in NFL history?! "
    "No team in the Super Bowl era has ever won three straight titles! "
    "It takes relentless grit, clutch execution, and championship swagger! "
    "And with Patrick Mahomes in his prime, betting against the Chiefs in January is a losing bet!"
)

print("Sending DeepDive to gemini-3.8-flash-tts with Key 2...")
resp = client.models.generate_content(
    model="gemini-3.8-flash-tts",
    contents=deepdive_text,
    config=cfg
)
raw = resp.candidates[0].content.parts[0].inline_data.data
out_p = data_clips / "test_38_deepdive.mp3"
subprocess.run([
    "ffmpeg", "-y", "-f", "s16le", "-ar", "24000", "-ac", "1", "-i", "pipe:0",
    "-b:a", "192k", str(out_p)
], input=raw, check=True, capture_output=True)

cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(out_p)]
dur = float(subprocess.run(cmd, capture_output=True, text=True).stdout.strip())
print(f"SUCCESS! test_38_deepdive.mp3 generated! Duration: {dur:.2f}s, Bytes: {len(raw)}")
