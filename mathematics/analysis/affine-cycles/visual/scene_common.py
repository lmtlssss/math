"""Native mathematical figure primitives, using the author's saved Blender style."""
from pathlib import Path
import bpy, math, json, os, hashlib, struct, shutil
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[1]
D=json.loads((ROOT/'evidence/figure.json').read_text())
META=json.loads((ROOT/'metadata.json').read_text())
OUT=Path(os.environ.get('FIGURE_OUTPUT',str(ROOT/'release')));OUT.mkdir(parents=True,exist_ok=True)
# Start Blender with the saved canonical .blend as its positional input. The
# original file is read only; every new artifact has a distinct output path.
TEMPLATE=Path(bpy.data.filepath)
if not TEMPLATE.is_file():raise RuntimeError('Open the saved mathematical style .blend before running this script')
TEMPLATE_HASH=hashlib.sha256(TEMPLATE.read_bytes()).hexdigest()
s=bpy.context.scene
original={'engine':s.render.engine,'resolution':[s.render.resolution_x,s.render.resolution_y],
          'view_transform':s.view_settings.view_transform,'world':s.world.name if s.world else None}
# Preserve the original world and render/color configuration. Clear only the
# in-memory objects and proof text of the template; its file is untouched.
for ob in list(bpy.data.objects):bpy.data.objects.remove(ob,do_unlink=True)
for col in list(bpy.data.collections):bpy.data.collections.remove(col)
for txt in list(bpy.data.texts):bpy.data.texts.remove(txt)
# Retain the saved visual style while replacing the prior mathematical state.
for key in list(s.keys()):del s[key]
for datablocks in (bpy.data.meshes,bpy.data.curves):
 for block in list(datablocks):
  if block.users==0:datablocks.remove(block)
# The original certificate used these exact emissive materials.
def material(name,rgb,strength=1.0):
 m=bpy.data.materials.get(name)
 if m is not None:return m
 m=bpy.data.materials.new(name);m.diffuse_color=(*rgb,1);m.use_nodes=True
 nd=m.node_tree.nodes;nd.clear();e=nd.new('ShaderNodeEmission');e.inputs['Color'].default_value=(*rgb,1);e.inputs['Strength'].default_value=strength
 o=nd.new('ShaderNodeOutputMaterial');m.node_tree.links.new(e.outputs[0],o.inputs['Surface']);return m
INK=material('etched white math',(.85,.91,.94),1.1)
GRID=material('technical lattice',(.16,.28,.34),.55)
GOLD=material('lower bound / 35',(.96,.70,.28),2)
CYAN=material('mathematical cyan',(.47,.83,.82))
DIM=material('subdued connections',(.13,.22,.25),.55)
PALETTE=[]
colors=[(.41,.67,.84),(.45,.76,.74),(.57,.63,.85),(.72,.56,.76),(.91,.70,.40),(.58,.80,.56),(.39,.76,.65),(.82,.53,.58),(.91,.60,.39),(.49,.68,.88),(.67,.61,.83),(.79,.69,.48)]
for i,c in enumerate(colors):PALETTE.append(material(f'k={i:02d} / exact output assignment',c,1.85))
def collection(name):
 c=bpy.data.collections.new(name);s.collection.children.link(c);return c
N=collection('01 / mathematical source objects');R=collection('02 / exact relations');B=collection('03 / retained mathematical state');O=collection('04 / certified outputs');T=collection('05 / notation');S=collection('06 / camera')
def mesh(name,col,verts,faces,mat,props=None):
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();ob=bpy.data.objects.new(name,me);col.objects.link(ob);me.materials.append(mat)
 for k,v in (props or {}).items():ob[k]=v
 return ob

def diamond(name,col,p,r,mat,props=None):
 x,y,z=p;v=[(x+r,y,z),(x-r,y,z),(x,y+r*.65,z),(x,y-r*.65,z),(x,y,z+r),(x,y,z-r)]
 f=[(0,2,4),(2,1,4),(1,3,4),(3,0,4),(2,0,5),(1,2,5),(3,1,5),(0,3,5)]
 return mesh(name,col,v,f,mat,props)

def curve(name,col,pts,mat,width=.006,smooth=True,props=None):
 c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.bevel_depth=width;c.bevel_resolution=2;c.resolution_u=16
 sp=c.splines.new('BEZIER' if smooth else 'POLY')
 if smooth:
  sp.bezier_points.add(len(pts)-1)
  for bp,p in zip(sp.bezier_points,pts):bp.co=p;bp.handle_left_type='AUTO';bp.handle_right_type='AUTO'
 else:
  sp.points.add(len(pts)-1)
  for bp,p in zip(sp.points,pts):bp.co=(*p,1)
 ob=bpy.data.objects.new(name,c);col.objects.link(ob);c.materials.append(mat)
 for k,v in (props or {}).items():ob[k]=v
 return ob

def bar(name,col,p,mat,w=.46,h=.11,props=None):
 x,y,z=p;d=.045
 v=[(x+a,y+b,z+c) for a,b,c in [(-w/2,-d,-h/2),(w/2,-d,-h/2),(w/2,-d,h/2),(-w/2,-d,h/2),(-w/2,d,-h/2),(w/2,d,-h/2),(w/2,d,h/2),(-w/2,d,h/2)]]
 return mesh(name,col,v,[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)],mat,props)
FONT=None
path=os.environ.get('MATHEMATICS_FONT')
if path and Path(path).is_file():FONT=bpy.data.fonts.load(path)
else:
 for p in ['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']:
  if Path(p).is_file():FONT=bpy.data.fonts.load(p);break

def text(body,x,z,size=.27,mat=None):
 mat=mat or INK;cu=bpy.data.curves.new('type '+body,'FONT');cu.body=body;cu.size=size;cu.extrude=0
 if FONT is not None:cu.font=FONT
 ob=bpy.data.objects.new('notation / '+body,cu);T.objects.link(ob);ob.location=(x,-.8,z);ob.rotation_euler=(math.pi/2,0,0);cu.materials.append(mat)
 bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.context.view_layer.objects.active=ob;bpy.ops.object.convert(target='MESH');ob.select_set(False)
 return ob

def finish(scene_name,meaning):
 s.render.resolution_x=3840;s.render.resolution_y=round(3840*original['resolution'][1]/original['resolution'][0]);s.render.resolution_percentage=100
 s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.image_settings.color_depth='8';s.render.image_settings.compression=30
 s.render.film_transparent=False
 s.render.engine=os.environ.get('MATHEMATICS_RENDER_ENGINE','CYCLES')
 if s.render.engine=='CYCLES':
  s.cycles.device='CPU';s.cycles.samples=32;s.cycles.use_denoising=False
 bpy.ops.object.camera_add(location=(1.8,-36,5.3));cam=bpy.context.object
 for col in list(cam.users_collection):col.objects.unlink(cam)
 S.objects.link(cam);cam.name='Mathematical publication / orthographic';cam.rotation_euler=(Vector((0,0,-.2))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=22.8;s.camera=cam
 text(META['doi'],-9.0,-6.6,.16,DIM);text('lmtlssss',7.0,-6.6,.22)
 # All type is converted to geometry; no external or packed font files.
 for f in list(bpy.data.fonts):
  if f.name!='Bfont':bpy.data.fonts.remove(f)
 proof=bpy.data.texts.new('MATHEMATICAL_CERTIFICATE.json');proof.write(json.dumps(D,indent=2))
 s['author']='lmtlssss🜐';s['doi']=META['doi'];s['title']=META['title'];s['meaning']=meaning
 s['style_source']='tensor-note-v1.0.0';s['style_source_sha256']=TEMPLATE_HASH
 blend=OUT/(scene_name+'.blend');png=OUT/'00-cover.png';s.render.filepath='//00-cover.png'
 bpy.ops.wm.save_as_mainfile(filepath=str(blend),compress=True)
 s.render.filepath=str(png)
 bpy.ops.render.render(write_still=True)
 h=png.read_bytes()[:24];assert h[:8]==b'\x89PNG\r\n\x1a\n'
 width,height=struct.unpack('>II',h[16:24]);assert width==3840 and height==s.render.resolution_y
 assert hashlib.sha256(TEMPLATE.read_bytes()).hexdigest()==TEMPLATE_HASH
 receipt={'blender':bpy.app.version_string,'engine':s.render.engine,'source_style':'tensor-note-v1.0.0','source_style_sha256':TEMPLATE_HASH,'original_settings':original,'render_device':'CPU' if s.render.engine=='CYCLES' else 'graphics','samples':s.cycles.samples if s.render.engine=='CYCLES' else None,'threads':s.render.threads,'resolution':[width,height],'certificate_sha256':hashlib.sha256((ROOT/'evidence/figure.json').read_bytes()).hexdigest(),'png_sha256':hashlib.sha256(png.read_bytes()).hexdigest(),'blend_sha256':hashlib.sha256(blend.read_bytes()).hexdigest(),'source_template_preserved':True,'font_assets_distributed':False,'objects':len(s.objects),'title':META['title'],'doi':META['doi']}
 (OUT/'render-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
 (ROOT/'evidence/render-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
 shutil.copy2(png,OUT/'cover_4k.png')
 print('NATIVE_MATHEMATICS_4K_VERIFIED',json.dumps(receipt),flush=True)
