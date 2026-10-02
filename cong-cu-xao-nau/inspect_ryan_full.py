import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

p = 'data/experts/exp_1790823302_ytsave_youtube_media_wgxelu4ojmu_ryan_cl/segments.json'
with open(p, encoding='utf-8') as f:
    segs = json.load(f)

for s in segs:
    if 1310 <= s['start'] <= 1460:
        print(f"[{s['start']:06.1f}s -> {s['end']:06.1f}s]: {s['text']}")
