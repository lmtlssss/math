#!/usr/bin/env python3
"""Native Blender scene from the exact prefix-to-carry certificate.
Run: blender -b --python visual/build_scene.py
Every connection is generated from the accompanying exact certificate.
"""
from pathlib import Path
import json, math, os
import bpy
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[1]
D=json.loads((ROOT/'evidence/figure.json').read_text())
OUT=Path(os.environ.get('FIGURE_OUTPUT',str(ROOT/'visual')))
OUT.mkdir(parents=True,exist_ok=True)
assert D['offsets']==[13,45,93,157,221] and D['cut']==8
classes=D['classes'];assert len(classes)==6
owner={}
for r,c in enumerate(classes):
 for u in c['members']:
  assert u not in owner
  assert [int(u+a>=256) for a in D['offsets']]==c['carry']
  owner[u]=r
assert len(owner)==256
bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene
s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=32;s.cycles.use_denoising=False
s.render.resolution_x=2400;s.render.resolution_y=1650;s.render.resolution_percentage=100
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB'
s.render.filepath=str(OUT/'00-cover.png');s.view_settings.view_transform='Standard'
s.render.film_transparent=False
world=bpy.data.worlds.new('graphite');world.use_nodes=True;s.world=world
world.node_tree.nodes['Background'].inputs['Color'].default_value=(.0027,.0037,.0056,1)
world.node_tree.nodes['Background'].inputs['Strength'].default_value=1

def collection(name):
 c=bpy.data.collections.new(name);s.collection.children.link(c);return c
P=collection('01 / 256 actual input prefixes')
R=collection('02 / exact prefix-to-carry incidence')
Q=collection('03 / six distinct residual states')
V=collection('04 / complete ordered carry vectors')
H=collection('05 / threshold staircase')
T=collection('06 / mathematical type')
S=collection('07 / camera and background')

def mat(name,c,strength=1):
 m=bpy.data.materials.new(name);m.diffuse_color=(*c,1);m.use_nodes=True
 n=m.node_tree.nodes;n.clear();e=n.new('ShaderNodeEmission')
 e.inputs['Color'].default_value=(*c,1);e.inputs['Strength'].default_value=strength
 o=n.new('ShaderNodeOutputMaterial');m.node_tree.links.new(e.outputs[0],o.inputs['Surface'])
 return m
palette=[(.56,.83,.86),(.59,.80,.73),(.71,.76,.90),(.79,.69,.84),(.88,.81,.61),(.96,.83,.50)]
colors=[mat('state '+str(i),c) for i,c in enumerate(palette)]
ink=mat('ivory',(.82,.88,.91));dim=mat('fine graphite line',(.09,.16,.19));faint=mat('zero carry',(.08,.13,.15))
gold=mat('proof gold',(.95,.79,.43));cyan=mat('cyan',(.47,.83,.82))

def mesh(name,col,verts,faces,material):
 d=bpy.data.meshes.new(name);d.from_pydata(verts,[],faces);d.update()
 o=bpy.data.objects.new(name,d);col.objects.link(o);d.materials.append(material);return o

def diamond(name,col,p,r,material):
 x,y,z=p
 verts=[(x+r,y,z),(x-r,y,z),(x,y+r/2,z),(x,y-r/2,z),(x,y,z+r),(x,y,z-r)]
 faces=[(0,2,4),(2,1,4),(1,3,4),(3,0,4),(2,0,5),(1,2,5),(3,1,5),(0,3,5)]
 return mesh(name,col,verts,faces,material)

def line(name,col,pts,material,width=.006,curved=False):
 d=bpy.data.curves.new(name,'CURVE');d.dimensions='3D';d.bevel_depth=width;d.bevel_resolution=1;d.resolution_u=16
 sp=d.splines.new('BEZIER' if curved else 'POLY')
 if curved:
  sp.bezier_points.add(len(pts)-1)
  for p,c in zip(sp.bezier_points,pts):p.co=c;p.handle_left_type='AUTO';p.handle_right_type='AUTO'
 else:
  sp.points.add(len(pts)-1)
  for p,c in zip(sp.points,pts):p.co=(*c,1)
 o=bpy.data.objects.new(name,d);col.objects.link(o);d.materials.append(material);return o

FONT_PATH=Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
FONT=bpy.data.fonts.load(str(FONT_PATH)) if FONT_PATH.is_file() else None

def text(body,x,z,size=.28,material=ink):
 d=bpy.data.curves.new(body,'FONT');d.body=body;d.size=size;d.extrude=0
 if FONT is not None:d.font=FONT
 o=bpy.data.objects.new('notation / '+body,d);T.objects.link(o)
 o.location=(x,-.7,z);o.rotation_euler=(math.pi/2,0,0);d.materials.append(material)
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
 bpy.ops.object.convert(target='MESH');o.select_set(False)
 return o

def bar(name,col,p,material):
 x,y,z=p
 verts=[(x+dx,y+dy,z+dz) for dx,dy,dz in [(-.25,-.04,-.07),(.25,-.04,-.07),(.25,-.04,.07),(-.25,-.04,.07),(-.25,.04,-.07),(.25,.04,-.07),(.25,.04,.07),(-.25,.04,.07)]]
 return mesh(name,col,verts,[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)],material)

centers=[Vector((.0,-.10,3.42-.91*r)) for r in range(6)]
for u in range(256):
 row,col=divmod(u,16);p=Vector((-9.05+.29*col,0,3.65-.29*row));r=owner[u]
 o=diamond('prefix '+str(u),P,p,.038,colors[r]);o['input_prefix']=u;o['carry_rank']=r
 q=centers[r]
 line('prefix %d to rank %d'%(u,r),R,[p,(-3.4,.16,.55*p.z+.45*q.z),q],colors[r],.0027,True)
 if col<15:line('grid h'+str(u),P,[p,p+Vector((.29,0,0))],dim,.003)
 if row<15:line('grid v'+str(u),P,[p,p+Vector((0,0,-.29))],dim,.003)
for r,c in enumerate(classes):
 p=centers[r];o=bar('rank '+str(r),Q,p,colors[r]);o['prefix_count']=c['size'];o['carry_vector']=c['carry']
 line('rank %d output bus'%r,V,[p,(2.6,.0,p.z),(4.6,0,p.z)],colors[r],.01,True)
 for j,b in enumerate(c['carry']):
  q=Vector((5.0+.48*j,-.1,p.z))
  diamond('rank%d carry%d=%d'%(r,j,b),V,q,.10 if b else .055,colors[r] if b else faint)
  if j:line('rank%d component%d'%(r,j),V,[(q.x-.48,q.y,q.z),q],dim,.004)
 text(''.join(str(b) for b in c['carry']),8.0,p.z-.07,.23,colors[r])
 text(str(c['size']),.48,p.z-.06,.19,colors[r])

# The staircase is the exact rank as a function of u, not decorative curvature.
last=None
for r,c in enumerate(classes):
 x1=-8.9+4.2*c['start']/256;x2=-8.9+4.2*(c['end']+1)/256;z=-4.8+.24*r
 if last is not None:line('threshold '+str(c['start']),H,[last,(x1,0,z)],colors[r],.012)
 line('interval '+str(r),H,[(x1,0,z),(x2,0,z)],colors[r],.012)
 diamond('threshold state '+str(r),H,(x1,0,z),.065,colors[r]);last=(x2,0,z)
line('prefix axis',H,[(-8.9,0,-5.05),(-4.6,0,-5.05)],dim,.006)
text('0',-9.0,-5.45,.18);text('256',-4.9,-5.45,.18)
text('yⱼ = x + αⱼ   mod 2ʷ',-9.05,5.10,.32)
text('qᵢ ≤ m + 1',5.07,5.08,.40,gold)
text('256',-7.15,4.32,.33);text('6',-.12,4.32,.33,gold)
text('256  →  6',-1.45,-3.85,.65)
text('m = 5    i = 8',-.98,-4.65,.23,cyan)
text('m = 32 : qᵢ ≤ 33',4.40,-4.10,.29,gold)
text('lmtlssss',7.20,-6.0,.23)
text('10.5281/zenodo.23702847',-9.05,-6.0,.17,dim)
t=bpy.data.texts.new('EXACT_PREFIX_CLASSES.json');t.write(json.dumps(D,indent=2))
s['author']='lmtlssss🜐';s['input_prefixes']=256;s['classes']=6;s['source']='evidence/figure.json'
s['meaning']='Every displayed source is an actual prefix. Class counts partition all prefixes.'
bpy.ops.object.camera_add(location=(1.8,-36,5.3));cam=bpy.context.object
for c in list(cam.users_collection):c.objects.unlink(cam)
S.objects.link(cam);cam.rotation_euler=(Vector((0,0,-.2))-cam.location).to_track_quat('-Z','Y').to_euler()
cam.data.type='ORTHO';cam.data.ortho_scale=22.8;s.camera=cam
bg=mat('flat charcoal',(.0027,.0037,.0056))
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,1,0),rotation=(math.pi/2,0,0));bpy.context.object.data.materials.append(bg)
blend=OUT/'shared-input-carry.blend';bpy.ops.wm.save_as_mainfile(filepath=str(blend),compress=True)
bpy.ops.render.render(write_still=True)
(OUT/'render-receipt.json').write_text(json.dumps({'engine':s.render.engine,'blender':bpy.app.version_string,'image':'00-cover.png','scene':blend.name,'resolution':[2400,1650],'prefixes':256,'classes':6,'source':'evidence/figure.json'},indent=2)+'\n')
print('NATIVE_RENDER_COMPLETE',str(blend),s.render.filepath)
