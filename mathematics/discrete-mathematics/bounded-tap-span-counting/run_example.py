#!/usr/bin/env python3
"""Count the supplied 256-bit instance using the exact Python frontier."""
import json
from pathlib import Path
from count import count_fiber
p=Path(__file__).resolve().parent
c=json.loads((p/'evidence/example256.json').read_text())
a=c['parameters'];r=count_fiber(a['width'],*c['taps'],int(a['D']),int(a['S']))
assert r['count']=='5784112988160'
print(json.dumps(r,indent=2))
