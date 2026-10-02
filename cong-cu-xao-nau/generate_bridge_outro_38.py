import time
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

bridge_text = (
    "Chiefs Kingdom, Coach Bill Cowher and the CBS crew make a massive statement! "
    "When Patrick Mahomes gets legitimate backfield support, this offense becomes practically unstoppable! "
    "But over on the Stephen A. Smith Show, NFL analyst Ryan Clark is sounding the alarm on the brutal AFC gauntlet! "
    "Listen closely to how Ryan Clark breaks this down right now!"
)

outro_text = (
    "Chiefs Kingdom, the message is loud and clear! "
    "With Kenneth Walker pounding the rock and Patrick Mahomes commanding the field, this dynasty is ready to make history! "
    "Can ANY team in the NFL stop Kansas City right now?! "
    "Drop your score predictions in the comments below! "
    "Smash that like button, hit subscribe, and turn on notifications so you never miss our breaking Chiefs coverage! "
    "We will catch you in the next one!"
)

def make_clip(text, out_mp3, tag):
    print(f"Generating {tag} with gemini-3.8-flash-tts...")
    resp = client.models.generate_content(model="gemini-3.8-flash-tts", contents=text, config=cfg)
    raw = resp.candidates[0].content.parts[0].inline_data.data
    subprocess.run([
        "ffmpeg", "-y", "-f", "s16le", "-ar", "24000", "-ac", "1", "-i", "pipe:0",
        "-b:a", "192k", str(out_mp3)
    ], input=raw, check=True, capture_output=True)
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(out_mp3)]
    dur = float(subprocess.run(cmd, capture_output=True, text=True).stdout.strip())
    print(f"SUCCESS {tag}: Duration = {dur:.2f}s")
    return dur

# Generate Bridge
make_clip(bridge_text, data_clips / "test_38_bridge.mp3", "Bridge")
print("Sleeping 20s to respect rate limit...")
time.sleep(20)
# Generate Outro
make_clip(outro_text, data_clips / "test_38_outro.mp3", "Outro")
print("ALL 3.8 FLASH VOICES GENERATED!")
