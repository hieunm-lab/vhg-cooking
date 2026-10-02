import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

p = 'data/experts/exp_1790823205_ytsave_youtube_media_oamvk1znluw_what_s_/segments.json'
with open(p, encoding='utf-8') as f:
    segs = json.load(f)

for s in segs:
    if 100 <= s['start'] <= 235:
        print(f"[{s['start']:.1f}s -> {s['end']:.1f}s]: {s['text']}")
