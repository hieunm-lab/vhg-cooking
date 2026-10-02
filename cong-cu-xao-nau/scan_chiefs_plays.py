import json
from pathlib import Path

p = Path(r"D:\HIeu\content tong hop\CongCuXaoNau\data\games\401872952\eyM7QUODW6c\segments.json")
with open(p, "r", encoding="utf-8") as f:
    segs = json.load(f)

for sid in [2, 4, 16, 19, 26, 45, 53]:
    s = next(x for x in segs if x["id"] == sid)
    print(f"ID {sid}: start={s['start']} -> peak={s.get('peak')} -> live_end={s['live_end']} | text={s['text'][:60]}")
