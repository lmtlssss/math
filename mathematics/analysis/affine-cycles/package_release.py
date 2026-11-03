#!/usr/bin/env python3
"""Package the fixed public mathematical source and proof inventory."""
from pathlib import Path
import zipfile

ROOT=Path(__file__).resolve().parent
FILES=[
    'README.md','paper.tex','metadata.json','CITATION.bib','CITATION.cff',
    'LICENSE.md','Makefile','requirements.txt','verify.py','package_release.py',
    'VERIFICATION.md','VERIFICATION_PLAN.md',
    'evidence/verification.json','evidence/figure.json',
    'evidence/PROOF_REVIEW.md','evidence/PRIOR_ART.md',
    'evidence/render-receipt.json','evidence/scene-audit.json',
    'visual/build_scene.py','visual/scene_common.py',
]
missing=[name for name in FILES if not (ROOT/name).is_file()]
if missing:
    raise SystemExit('Required mathematical source missing: '+', '.join(missing))
out=ROOT/'release'/'source-and-proof.zip'
out.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for name in FILES:
        info=zipfile.ZipInfo('affine-cycles/'+name,date_time=(2026,11,3,0,0,0))
        info.compress_type=zipfile.ZIP_DEFLATED
        info.external_attr=0o644<<16
        z.writestr(info,(ROOT/name).read_bytes())
with zipfile.ZipFile(out) as z:
    assert z.testzip() is None
    assert len(z.namelist())==len(FILES)
print(f'{out.name}: {len(FILES)} mathematical source files, {out.stat().st_size} bytes')
