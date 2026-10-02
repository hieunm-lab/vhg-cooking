import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

seg_file = 'data/experts/exp_1790823205_ytsave_youtube_media_oamvk1znluw_what_s_/segments.json'
with open(seg_file, encoding='utf-8') as f:
    segments = json.load(f)

for s in segments:
    txt = s['text'].lower()
    if any(k in txt for k in ['mahomes', 'walker', 'kelce', 'run', 'pass', 'touchdown']):
        print(f"[{s['start']:.1f}s -> {s['end']:.1f}s]: {s['text']}")
