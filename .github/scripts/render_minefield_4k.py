#!/usr/bin/env python3
"""Re-render the published mathematical geometry at native 3840-pixel width."""
import bpy, sys, json, struct, hashlib
from pathlib import Path
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
if len(argv)!=3: raise SystemExit("blender -b --python render_4k.py -- INPUT.blend OUTPUT.png SLUG")
source, output, slug = argv
bpy.ops.wm.open_mainfile(filepath=str(Path(source).resolve()),load_ui=False)
scene=bpy.context.scene
ox,oy=scene.render.resolution_x,scene.render.resolution_y
assert 500<=ox<=16000 and 500<=oy<=16000,(ox,oy)
ny=round(3840*oy/ox)
assert 2100<=ny<=3300,(ox,oy,ny)
scene.render.resolution_x=3840;scene.render.resolution_y=ny;scene.render.resolution_percentage=100
scene.render.image_settings.file_format="PNG"
scene.render.image_settings.color_mode="RGB"
scene.render.image_settings.color_depth="8"
scene.render.image_settings.compression=25
scene.render.filepath=str(Path(output).resolve())
scene.render.film_transparent=False
if scene.render.engine=="CYCLES" and hasattr(scene,"cycles"):scene.cycles.use_denoising=False
Path(output).parent.mkdir(parents=True,exist_ok=True)
bpy.ops.render.render(write_still=True)
p=Path(output)
assert p.is_file() and p.stat().st_size>50000
h=p.open("rb").read(24)
assert h[:8]==b"\x89PNG\r\n\x1a\n"
w,y=struct.unpack(">II",h[16:24]); assert(w,y)==(3840,ny),(w,y,ny)
report={"slug":slug,"source":Path(source).name,"original":[ox,oy],"resolution":[w,y],"bytes":p.stat().st_size,"engine":scene.render.engine,"sha256":hashlib.sha256(p.read_bytes()).hexdigest()}
p.with_suffix(".json").write_text(json.dumps(report,indent=2)+"\n")
print("MINEFIELD_NATIVE_4K_VERIFIED",json.dumps(report),flush=True)
