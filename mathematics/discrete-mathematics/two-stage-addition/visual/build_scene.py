#!/usr/bin/env python3
"""Native Blender geometry for the complete radix-eight quotient.
Author: lmtlssss🜐. Executable source: MIT.
"""
from pathlib import Path
import os,json,math,hashlib
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'evidence/figure.json').read_text())
OUT=Path(os.environ.get('FIGURE_OUTPUT',str(ROOT/'visual')));OUT.mkdir(parents=True,exist_ok=True)
assert DATA['radix']==8 and len(DATA['triples'])==512 and len(DATA['classes'])==36
assert sum(c['multiplicity'] for c in DATA['classes'])==512
bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=8;s.cycles.use_denoising=False
s.render.resolution_x=2400;s.render.resolution_y=1650;s.render.resolution_percentage=100
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB'
s.render.filepath=str(OUT/'00-cover.png');s.view_settings.view_transform='Standard'
s.render.film_transparent=False
world=bpy.data.worlds.new('graphite');world.use_nodes=True;s.world=world
world.node_tree.nodes['Background'].inputs['Color'].default_value=(.0027,.0037,.0056,1)
world.node_tree.nodes['Background'].inputs['Strength'].default_value=1

def collection(name):
 c=bpy.data.collections.new(name);s.collection.children.link(c);return c
A=collection('01 / 512 operand triples')
B=collection('02 / exact quotient routing')
C=collection('03 / 36 response classes')
D=collection('04 / selected complete four-input response')
E=collection('05 / mathematical notation')
F=collection('06 / orthographic camera and graphite field')

def linear(c):return c/12.92 if c<=.04045 else ((c+.055)/1.055)**2.4

def mat(name,rgb):
 m=bpy.data.materials.new(name);m.diffuse_color=(*rgb,1);m.use_nodes=True;m.node_tree.nodes.clear()
 e=m.node_tree.nodes.new('ShaderNodeEmission');e.inputs['Color'].default_value=(*(linear(x) for x in rgb),1);e.inputs['Strength'].default_value=1
 o=m.node_tree.nodes.new('ShaderNodeOutputMaterial');m.node_tree.links.new(e.outputs[0],o.inputs['Surface']);return m
ink=mat('ivory',(.86,.93,.94));dim=mat('thin graphite cyan',(.20,.32,.36));quiet=mat('quiet notation',(.52,.65,.67))
gold=mat('witness ochre',(.98,.87,.57));cyan=mat('quotient cyan',(.63,.88,.89))
bg=mat('flat charcoal',(.0353,.0471,.0667))
palette=[(.57,.80,.84),(.66,.78,.74),(.75,.73,.83),(.87,.80,.62),(.58,.83,.82),(.80,.73,.80),(.65,.76,.89),(.91,.84,.64)]
colors=[mat('class residue %d'%i,p) for i,p in enumerate(palette)]
threads=[mat('route residue %d'%i,tuple(x*.43 for x in p)) for i,p in enumerate(palette)]

def mesh(name,col,vertices,faces,material,props=None):
 me=bpy.data.meshes.new(name);me.from_pydata(vertices,[],faces);me.update()
 ob=bpy.data.objects.new(name,me);col.objects.link(ob);me.materials.append(material)
 for k,v in (props or {}).items():ob[k]=v
 return ob

def diamond(name,col,p,size,material,props=None):
 x,y,z=p;vs=[(x+size,y,z),(x-size,y,z),(x,y+size*.45,z),(x,y-size*.45,z),(x,y,z+size),(x,y,z-size)]
 fs=[(0,2,4),(2,1,4),(1,3,4),(3,0,4),(2,0,5),(1,2,5),(3,1,5),(0,3,5)]
 return mesh(name,col,vs,fs,material,props)

def line(name,col,points,material,width=.006,smooth=False):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=width;cu.bevel_resolution=1;cu.resolution_u=12
 sp=cu.splines.new('BEZIER' if smooth else 'POLY')
 if smooth:
  sp.bezier_points.add(len(points)-1)
  for bp,p in zip(sp.bezier_points,points):bp.co=p;bp.handle_left_type='AUTO';bp.handle_right_type='AUTO'
 else:
  sp.points.add(len(points)-1)
  for bp,p in zip(sp.points,points):bp.co=(*p,1)
 ob=bpy.data.objects.new(name,cu);col.objects.link(ob);cu.materials.append(material);return ob

def block(name,p,width,height,material,props):
 x,y,z=p;dx=width/2;dy=.09;dz=height/2
 v=[(x+i*dx,y+j*dy,z+k*dz) for i,j,k in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]]
 return mesh(name,C,v,[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)],material,props)
fontpath=Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
font=bpy.data.fonts.load(str(fontpath)) if fontpath.exists() else None

def text(body,x,z,size=.30,material=ink,align='LEFT'):
 cu=bpy.data.curves.new(body,'FONT');cu.body=body;cu.size=size;cu.align_x=align
 if font:cu.font=font
 ob=bpy.data.objects.new('type / '+body,cu);E.objects.link(ob);cu.materials.append(material)
 ob.location=(x,-2.4,z);ob.rotation_euler=(math.pi/2,0,0)
 bpy.ops.object.select_all(action='DESELECT');bpy.context.view_layer.objects.active=ob;ob.select_set(True)
 bpy.ops.object.convert(target='MESH');ob.select_set(False);return ob

# 8 x 8 x 8 actual source lattice; each point has one canonical class.
origin=Vector((-10.0,.15,-2.3))
u=Vector((.47,0,-.13));v=Vector((.18,.26,.20));w=Vector((0,0,.49))
feature=27
positions={}
centers={}
for row in DATA['classes']:
 label=row['label'];q=row['residue'];p=Vector((.48,-.1,4.10-.223*label));centers[label]=p
 material=gold if label==feature else colors[q]
 block('class %d / residue %d / multiplicity %d'%(label,q,row['multiplicity']),p,.62,.115,material,
       {'label':label,'residue':q,'multiplicity':row['multiplicity'],'carry_table':row['carry_table']})
for c,t,h,label in DATA['triples']:
 p=origin+c*u+t*v+h*w;positions[c,t,h]=p;q=DATA['classes'][label]['residue']
 material=gold if label==feature else colors[q]
 diamond('operand (%d,%d,%d) → %d'%(c,t,h,label),A,p,.055 if label==feature else .029,material,
         {'C':c,'S':t,'H':h,'label':label})
 dest=centers[label]-Vector((.32,0,0))
 mid=Vector((-2.58,1.9,.35*p.z+.65*dest.z))
 line('fiber %d ← (%d,%d,%d)'%(label,c,t,h),B,[p,mid,dest],gold if label==feature else threads[q],.008 if label==feature else .0030,True)
# Twelve actual bounding edges of the source cube.
for axis,direction in enumerate((u,v,w)):
 other=[x for i,x in enumerate((u,v,w)) if i!=axis]
 for i in (0,7):
  for j in (0,7):
   p=origin+i*other[0]+j*other[1]
   line('lattice edge %d %d %d'%(axis,i,j),A,[p,p+7*direction],dim,.008)

# One highlighted class is expanded into its complete response table.
row=DATA['classes'][feature]
assert row['representative']==[0,7,6] and row['residue']==5
for index,(a,b) in enumerate(((0,0),(0,1),(1,0),(1,1))):
 p=centers[feature];dest=Vector((7.3,-.30,2.75-index*1.4));carry=row['carry_table'][index]
 output=((row['residue']+a+b)%8,carry//2,carry%2)
 line('query (%d,%d) → %s'%(a,b,output),D,[p+Vector((.32,0,0)),Vector((4.35,-.25,.3*p.z+.7*dest.z)),dest],gold,.012,True)
 diamond('complete response '+str(output),D,dest,.145,cyan)
 text('%d%d'%(a,b),6.65,dest.z+.27,.215,quiet)
 text('(%d, %d, %d)'%output,7.70,dest.z-.075,.255,ink)

text('Q : (a,b) ↦ (ρ,c₁,c₂)',-10.1,5.50,.36,ink)
text('N(B) = 5B − 4',5.8,5.50,.44,gold)
text('512',-8.05,4.40,.38,ink)
text('36',.48,4.65,.38,gold,'CENTER')
text('4',7.3,4.40,.36,ink,'CENTER')
text('B = 8',-9.8,-4.1,.24,quiet)
text('(C,S,H) = (0,7,6)',6.0,-3.0,.23,quiet)
# Main exact encoding consequence, with the input width stated separately.
text('96',-2.5,-5.17,.90,ink)
text('→',-.4,-5.17,.88,ink)
text('35',1.18,-5.17,.90,gold)
text('w = 32',-.22,-5.85,.25,cyan,'CENTER')
text('⌈log₂(5B−4)⌉',6.0,-5.17,.39,cyan)
text('lmtlssss',8.2,-6.75,.22,ink)
text('10.5281/zenodo.23698617',-10.0,-6.75,.20,quiet)

source=bpy.data.texts.new('EXACT_CLASS_DATA.json');source.write(json.dumps(DATA,indent=2))
s['author']='lmtlssss🜐';s['doi']='10.5281/zenodo.23698617';s['radix']=8
s['source_operand_triples']=512;s['canonical_states']=36;s['highlighted_state']=feature
s['source_sha256']=hashlib.sha256((ROOT/'evidence/figure.json').read_bytes()).hexdigest()
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,5,0),rotation=(math.pi/2,0,0))
ob=bpy.context.object
for old in list(ob.users_collection):old.objects.unlink(ob)
F.objects.link(ob);ob.name='flat graphite field';ob.data.materials.append(bg)
bpy.ops.object.camera_add(location=(.3,-40,1.0));camera=bpy.context.object
for old in list(camera.users_collection):old.objects.unlink(camera)
F.objects.link(camera);camera.name='orthographic proof plate'
aim=Vector((-.1,0,-.45));camera.rotation_euler=(aim-camera.location).to_track_quat('-Z','Y').to_euler()
camera.data.type='ORTHO';camera.data.ortho_scale=23.5;s.camera=camera
for ft in list(bpy.data.fonts):
 if ft.name!='Bfont' and ft.users==0:bpy.data.fonts.remove(ft)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'two-stage-addition.blend'),compress=True)
bpy.ops.render.render(write_still=True)
print('NATIVE_RENDER_OK',s.render.filepath,'SOURCE_TRIPLES',512,'STATES',36,flush=True)
