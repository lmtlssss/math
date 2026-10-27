#!/usr/bin/env python3
"""Native Blender scene from exact eight-branch recurrence data.
Author: lmtlssss🜐. License: MIT.
Run: blender -b --python visual/build_scene.py
"""
import json,math,os
from pathlib import Path
import bpy
from mathutils import Vector,Euler
ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'evidence/sharp-traces.json').read_text())
OUT=Path(os.environ.get('FIGURE_OUTPUT',str(ROOT/'visual')))
OUT.mkdir(parents=True,exist_ok=True)
paths=DATA['paths']
assert len(paths)==8 and all(p['accepted'] for p in paths)
assert sorted(p['candidate'] for p in paths)==[11,22,44,49,69,88,98,127]
for p in paths:
 assert p['bits'][7:10]==p['initial_bits']
 assert len(p['bits'])==10 and p['steps']==7
bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene
try:s.render.engine='BLENDER_EEVEE_NEXT'
except TypeError:s.render.engine='BLENDER_EEVEE'
s.render.resolution_x=2600;s.render.resolution_y=1650;s.render.resolution_percentage=100
s.render.image_settings.file_format='PNG';s.render.filepath=str(OUT/'three-bit-boundary.png')
s.render.film_transparent=False
s.view_settings.view_transform='Standard'
s.render.image_settings.color_mode='RGBA'
world=bpy.data.worlds.new('Paper light');s.world=world;world.use_nodes=True
world.node_tree.nodes['Background'].inputs['Color'].default_value=(0.89,0.88,0.84,1)
world.node_tree.nodes['Background'].inputs['Strength'].default_value=.65

def collection(name):
 c=bpy.data.collections.new(name);s.collection.children.link(c);return c
CUBE=collection('01 | eight boundary states')
ROUTES=collection('02 | exact seed-to-branch routes')
PATHS=collection('03 | 80 trace bits, 8 times 10')
CLOSURE=collection('04 | three closure coordinates per branch')
TYPE=collection('05 | mathematical notation')
STUDIO=collection('06 | camera, lights, ground')

def move(o,c):
 for old in list(o.users_collection):old.objects.unlink(o)
 c.objects.link(o);return o

def material(name,color,metal=0,rough=.5,emission=False):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
 bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1)
 bs.inputs['Metallic'].default_value=metal;bs.inputs['Roughness'].default_value=rough
 if emission:
  bs.inputs['Emission Color'].default_value=(*color,1);bs.inputs['Emission Strength'].default_value=.6
 return m
BLACK=material('graphite',(.025,.032,.035),.15,.4)
PAPER=material('warm white',(.92,.91,.865),0,.72)
PALE=material('bit zero / porcelain',(.72,.74,.73),.12,.37)
GOLD=material('boundary / ochre',(.83,.37,.075),.28,.3)
GRAY=material('construction line',(.43,.47,.47),0,.65)
DARK=material('notation',(.025,.032,.035),0,.9,True)
ORANGE=material('notation ochre',(.68,.25,.03),0,.9,True)

def sphere(name,position,radius,mat,c):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=12,radius=radius,location=position)
 o=move(bpy.context.object,c);o.name=name;o.data.materials.append(mat)
 for f in o.data.polygons:f.use_smooth=True
 return o

def line(name,points,mat,r=.014,c=ROUTES,bezier=False):
 d=bpy.data.curves.new(name,'CURVE');d.dimensions='3D';d.resolution_u=24;d.bevel_depth=r;d.bevel_resolution=3
 sp=d.splines.new('BEZIER' if bezier else 'POLY')
 if bezier:
  sp.bezier_points.add(len(points)-1)
  for p,co in zip(sp.bezier_points,points):p.co=co;p.handle_left_type='AUTO';p.handle_right_type='AUTO'
 else:
  sp.points.add(len(points)-1)
  for p,co in zip(sp.points,points):p.co=(*co,1)
 o=bpy.data.objects.new(name,d);c.objects.link(o);d.materials.append(mat);return o

sanspath='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
serifpath='/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'
monopath='/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
fonts={}
for key,p in [('sans',sanspath),('serif',serifpath),('mono',monopath),('symbol','/usr/share/fonts/truetype/noto/NotoSansSymbols-Regular.ttf')]:
 if Path(p).exists():fonts[key]=bpy.data.fonts.load(p)

def text(body,x,z,size=.3,mat=DARK,align='LEFT',font='sans',y=-2):
 d=bpy.data.curves.new(body,'FONT');d.body=body;d.size=size;d.align_x=align;d.space_character=1.05
 if font in fonts:d.font=fonts[font]
 d.extrude=.0002
 o=bpy.data.objects.new('Text | '+body,d);TYPE.objects.link(o)
 o.location=(x,y,z);o.rotation_euler=(math.pi/2,0,0);d.materials.append(mat);o['text']=body
 # Keep native mesh typography and avoid embedding or distributing font files.
 bpy.ops.object.select_all(action='DESELECT');bpy.context.view_layer.objects.active=o;o.select_set(True)
 bpy.ops.object.convert(target='MESH');o.select_set(False)
 return o

# A true three-dimensional cube: 8 seed vertices, 12 edges.
rot=Euler((.32,.48,.16)).to_matrix();center=Vector((-6.9,.0,.2));scale=1.5
points={}
for p in paths:
 seed=p['seed'];b=p['initial_bits'];local=Vector(tuple((2*v-1)*scale for v in b));q=center+rot@local
 points[seed]=q
 o=sphere('Boundary '+''.join(map(str,b)),q,.14,GOLD,CUBE);o['seed']=seed;o['bits']=b
 text(''.join(map(str,b)),q.x-.12,q.z+.25,.215,font='mono',y=q.y-.4)
for a in range(8):
 for bit in range(3):
  b=a^(1<<bit)
  if a<b:line('Cube edge %s-%s'%(a,b),[points[a],points[b]],BLACK,.02,CUBE)

# Every row is an actual recurrence. The last three beads certify closure.
xstart=-2.15; spacing=.94; top=3.02;dy=.77
trace_positions={}
for row,p in enumerate(paths):
 z=top-row*dy;seed=p['seed'];positions=[]
 for j,bit in enumerate(p['bits']):
  x=xstart+j*spacing+(0.3 if j>=7 else 0)
  co=Vector((x,-.20-.27*bit,z+.13*bit));positions.append(co)
  mat=GOLD if j<3 or j>=7 else (BLACK if bit else PALE)
  o=sphere('seed %d / x%d=%d'%(seed,j,bit),co,.105 if bit else .067,mat,CLOSURE if j>=7 else PATHS)
  o['seed']=seed;o['coordinate']=j;o['bit']=bit
  if j>0:line('path %d segment %d'%(seed,j),[positions[-2],co],BLACK,.009,PATHS)
 trace_positions[seed]=positions
 line('seed %d route'%seed,[points[seed],Vector((-4.2,-.08,z)),positions[0]],GRAY,.009,ROUTES,True)
 text(str(p['candidate']),8.05,z-.075,.23,font='mono')
 # Equality links, not new transitions: three links pair first and last bits.
 for j in range(3):
  a=positions[j];b=positions[7+j]
  line('closure %d coordinate %d'%(seed,j),[a,Vector((a.x+.45,.30,z-.22)),Vector((b.x-.45,.30,z-.22)),b],GOLD,.0045,CLOSURE,True)

# Coordinate labels, separation marks and measured range.
for j in range(10):
 x=xstart+j*spacing+(.3 if j>=7 else 0)
 subs=['₀','₁','₂','₃','₄','₅','₆','₇','₈','₉']
 text('x'+subs[j],x,3.7,.245,align='CENTER',font='serif')
line('closure divider',[(4.11,.05,3.4),(4.11,.05,-2.65)],GRAY,.007,STUDIO)
text('x',8.05,3.7,.3,font='serif')
text('w = 7     c = y = 127     k = 0',-.55,-3.25,.27,align='CENTER',font='mono')

# Sparse equation hierarchy. Superscripts are explicit geometry where needed.
text('2',-8.65,4.66,1.2,font='serif');text('w',-7.85,5.36,.48,font='serif')
text('→',-6.42,4.8,.9)
text('2',-4.85,4.66,1.2,font='serif');text('3',-4.04,5.36,.48,font='serif')
text('= 8',-3.45,4.66,1.2,ORANGE,font='serif')
text('|F⁻¹(y)| ≤ 8',8.75,4.9,.63,align='RIGHT',font='serif')
line('header rule',[(-9.1,-.6,4.3),(9.1,-.6,4.3)],BLACK,.007,STUDIO)
text('F(x) = ((R₁x ⊕ R₃x) + (x ∧ c) + k) mod 2ʷ',0,-4.33,.44,align='CENTER',font='serif')
text('(x₇, x₈, x₉) = (x₀, x₁, x₂)',-8.9,-5.23,.30,font='serif')
text('≤ 8w',8.8,-5.23,.65,ORANGE,align='RIGHT',font='serif')
line('footer rule',[(-9.1,-.6,-5.7),(9.1,-.6,-5.7)],BLACK,.006,STUDIO)
text('lmtlssss',-9.05,-6.15,.22,font='mono')
text('🜐',-7.89,-6.15,.22,font='symbol')
text('10.5281/zenodo.23680529',9.05,-6.15,.22,align='RIGHT',font='mono')
text('w ≥ 4',0,-6.15,.23,align='CENTER',font='serif')

# Background panel and light, all in the native Blender scene.
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,2,0),rotation=(math.pi/2,0,0))
o=move(bpy.context.object,STUDIO);o.name='paper plane';o.data.materials.append(PAPER)
bpy.ops.object.camera_add(location=(0,-38,0));cam=move(bpy.context.object,STUDIO)
cam.name='Orthographic publication view';cam.rotation_euler=(Vector((0,0,-.15))-cam.location).to_track_quat('-Z','Y').to_euler()
cam.data.type='ORTHO';cam.data.ortho_scale=20.7;s.camera=cam
for name,loc,power,size in [('key',(-5,-11,9),1350,9),('fill',(8,-7,2),900,7)]:
 bpy.ops.object.light_add(type='AREA',location=loc);l=move(bpy.context.object,STUDIO);l.name=name;l.data.energy=power;l.data.shape='DISK';l.data.size=size
 l.rotation_euler=(Vector((0,0,0))-l.location).to_track_quat('-Z','Y').to_euler()
for f in list(bpy.data.fonts):
 if f.name!='Bfont' and f.users==0:bpy.data.fonts.remove(f)
s['author']='lmtlssss🜐';s['source']='evidence/sharp-traces.json';s['boundary_states']=8;s['trace_bits']=80;s['closure_equalities']=24
s['meaning']='Exact recurrence paths for the sharp seven-bit fiber; three chosen bits and zero initial carry.'
t=bpy.data.texts.new('EXACT_TRACE.json');t.write(json.dumps(DATA,indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'three-bit-boundary.blend'),compress=True)
if os.environ.get('RENDER','1')=='1':bpy.ops.render.render(write_still=True)
print('SCENE_OK',str(OUT/'three-bit-boundary.blend'),'TRACE_PATHS',len(paths),'BIT_NODES',80,flush=True)
