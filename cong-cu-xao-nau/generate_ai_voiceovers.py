import sys
from pathlib import Path

# Add workspace to path
sys.path.insert(0, r"d:\HIeu\content tong hop\cong-cu-xao-nau")
from xaonau.gemini_tts import generate_gemini_speech

pkg = Path(r"C:\Users\Thien\Downloads\kho video\CapCut_Project_Package")

bridge_script = (
    "Coach Bill Cowher and the CBS crew make a rock-solid case: when Patrick Mahomes gets legitimate backfield support, "
    "this offense becomes practically unstoppable. But not everyone in the national media is ready to hand Kansas City "
    "the Lombardi trophy just yet. In fact, over on the Stephen A. Smith Show, NFL analyst Ryan Clark is sounding the alarm "
    "on a completely different dimension: the brutal AFC gauntlet, the surging Buffalo Bills, and whether this Chiefs team "
    "can genuinely sustain this level of dominance. Listen closely to how Ryan Clark breaks this down right now."
)

deepdive_script = (
    "Now let's take a step back and examine the bigger picture here. You just heard the tactical breakdown from Coach Bill Cowher, "
    "and you heard the fiery reality check from Ryan Clark. So who actually has it right? The truth is, both of them are touching on two sides of the exact same coin. "
    "First, let's talk about what Coach Cowher pointed out. For the past two seasons, defensive coordinators across the NFL played two-high safeties "
    "and dared the Chiefs to run the football. Kansas City's offense stalled because they lacked an explosive back who could punish light boxes. "
    "With Kenneth Walker entering this backfield, everything changes. Walker isn't just picking up four yards and a cloud of dust; "
    "he is turning routine off-tackle handoffs into sixty-yard house calls. That forces linebackers to step up into the box, "
    "and the moment they hesitate, Patrick Mahomes has Travis Kelce and Xavier Worthy streaking wide open down the seam. That is lethal. "
    "Second, the mainstream media is completely sleeping on Steve Spagnuolo's defense. Everyone talks about Mahomes, but it is this defensive unit "
    "that closed out the Super Bowl and sealed three straight one-possession playoff wins. Chris Jones remains the most dominant interior game-wrecker in football. "
    "When games are on the line in the fourth quarter, Spags dials up exotic zero-blitzes that force opposing quarterbacks into fatal mistakes. "
    "This defense gives Andy Reid the luxury of playing calculated, risk-free football. "
    "Third, look at the brutal gauntlet waiting for Kansas City down the stretch. Ryan Clark is dead right about the Buffalo Bills and Josh Allen. "
    "The AFC playoffs run through a meat grinder featuring Lamar Jackson, Joe Burrow, and Jim Harbaugh's physical Chargers. "
    "The biggest question mark isn't talent; it is offensive line durability. If the interior protection holds up and keeps Mahomes clean, "
    "Kansas City controls their own destiny. "
    "Finally, the ultimate question every football fan is asking: can the Kansas City Chiefs actually pull off the historic three-peat? "
    "No franchise in the Super Bowl era has ever won three straight titles. It demands legendary coaching, clutch execution, and injury luck. "
    "But with Mahomes in his prime, a revived run game, and a championship defense, betting against the Chiefs in January is a losing proposition."
)

print("Generating Bridge voiceover (Puck)...")
f_bridge = generate_gemini_speech(
    text=bridge_script,
    voice_name="Puck",
    output_path=pkg / "01_Voiceover_Bridge_Puck.mp3"
)
print("Bridge voiceover created:", f_bridge)

print("Generating Deep Dive voiceover (Puck)...")
f_deepdive = generate_gemini_speech(
    text=deepdive_script,
    voice_name="Puck",
    output_path=pkg / "03_Voiceover_DeepDive_Puck.mp3"
)
print("Deep Dive voiceover created:", f_deepdive)
