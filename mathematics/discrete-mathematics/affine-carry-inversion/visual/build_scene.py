#!/usr/bin/env python3
"""Native Blender geometry from the complete eight-bit affine-fiber certificate.
Author: lmtlssss🜐. Source: MIT; rendered figure: CC BY 4.0.
Run: blender -b --python visual/build_scene.py
"""
import bpy,json,math,os
from pathlib import Path
from mathutils import Vector,Euler
ROOT=Path(__file__).resolve().parents[1]
D=json.loads((ROOT/'evidence/figure.json').read_text())
OUT=Path(os.environ.get('FIGURE_OUTPUT',str(ROOT/'visual')))
OUT.mkdir(parents=True,exist_ok=True)
assert D['width']==8 and D['count']==17 and len(D['cells'])==5
M=256;rows=D['rows'];offset=D['D'];target=D['S']
def L(x):return sum(((x&r).bit_count()&1)<<i for i,r in enumerate(rows))
expected={a for a in range(M) if (L((a+offset)&255)+L(a))&255==target}
members={x for c in D['cells'] for x in c['members']}
assert members==expected and len(members)==17
signatures=D['input_signature_list'];assert len(signatures)==13
assert {a^((a+offset)&255) for a in range(256)}==set(signatures)

bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=8
s.cycles.use_denoising=False
for layer in s.view_layers:layer.cycles.use_denoising=False
s.render.threads_mode='FIXED';s.render.threads=4
s.render.resolution_x=2400;s.render.resolution_y=1650;s.render.resolution_percentage=100
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB'
s.render.filepath=str(OUT/'00-cover.png');s.render.film_transparent=False
s.view_settings.view_transform='Standard'
try:s.view_settings.look='None'
except Exception:pass
world=bpy.data.worlds.new('Graphite');world.use_nodes=True;s.world=world
world.node_tree.nodes['Background'].inputs['Color'].default_value=(.00273,.00368,.00560,1)
world.node_tree.nodes['Background'].inputs['Strength'].default_value=1.0

def collection(name):
 c=bpy.data.collections.new(name);s.collection.children.link(c);return c
A=collection('01 / 256 source words');B=collection('02 / 13 exact input signatures')
C=collection('03 / five affine solution cells');R=collection('04 / source-to-signature relation')
N=collection('05 / mathematical notation');P=collection('06 / binary matrix and camera')

def material(name,rgb,strength=1):
 m=bpy.data.materials.new(name);m.use_nodes=True;m.diffuse_color=(*rgb,1)
 nodes=m.node_tree.nodes;nodes.clear();e=nodes.new('ShaderNodeEmission');e.inputs['Color'].default_value=(*rgb,1);e.inputs['Strength'].default_value=strength
 out=nodes.new('ShaderNodeOutputMaterial');m.node_tree.links.new(e.outputs[0],out.inputs['Surface']);return m
white=material('ivory',(.83,.89,.91));cyan=material('cyan',(.46,.79,.80));gold=material('gold',(.94,.78,.42));dim=material('construction',(.045,.082,.105));faint=material('inactive',(.012,.025,.035))
cols=[cyan,material('pale blue',(.54,.70,.84)),material('pale lavender',(.74,.71,.86)),material('pale ivory',(.87,.84,.68)),gold]

def diamond(name,col,pos,r,mat,props=None):
 x,y,z=pos;d=[(r,0,0),(-r,0,0),(0,r*.6,0),(0,-r*.6,0),(0,0,r),(0,0,-r)]
 verts=[(x+a,y+b,z+c) for a,b,c in d]
 faces=[(0,2,4),(2,1,4),(1,3,4),(3,0,4),(2,0,5),(1,2,5),(3,1,5),(0,3,5)]
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update();ob=bpy.data.objects.new(name,mesh);col.objects.link(ob);mesh.materials.append(mat)
 for k,v in (props or {}).items():ob[k]=v
 return ob

def line(name,col,points,mat,r=.008,smooth=False):
 data=bpy.data.curves.new(name,'CURVE');data.dimensions='3D';data.bevel_depth=r;data.bevel_resolution=1;data.resolution_u=12
 sp=data.splines.new('BEZIER' if smooth else 'POLY')
 if smooth:
  sp.bezier_points.add(len(points)-1)
  for p,co in zip(sp.bezier_points,points):p.co=co;p.handle_left_type='AUTO';p.handle_right_type='AUTO'
 else:
  sp.points.add(len(points)-1)
  for p,co in zip(sp.points,points):p.co=(*co,1)
 ob=bpy.data.objects.new(name,data);col.objects.link(ob);data.materials.append(mat);return ob

fontpath='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
font=bpy.data.fonts.load(fontpath) if Path(fontpath).exists() else None

def text(body,x,z,size=.28,mat=white,center=False):
 data=bpy.data.curves.new(body,'FONT');data.body=body;data.size=size;data.align_x='CENTER' if center else 'LEFT'
 if font:data.font=font
 ob=bpy.data.objects.new('Notation / '+body,data);N.objects.link(ob);ob.location=(x,-.7,z);ob.rotation_euler=(math.pi/2,0,0);data.materials.append(mat)
 bpy.ops.object.select_all(action='DESELECT');bpy.context.view_layer.objects.active=ob;ob.select_set(True);bpy.ops.object.convert(target='MESH');ob.select_set(False)

# Exact source input grid, with color inherited from the solution-cell membership.
owner={x:i for i,c in enumerate(D['cells']) for x in c['members']}
pos={}
for x in range(256):
 q=Vector((-9.35+(x%16)*.34,.0,3.60-(x//16)*.34));pos[x]=q
 diamond('input %03d'%x,A,q,.061 if x in members else .022,cols[owner[x]] if x in members else dim,{'input':x,'solution':x in members})
for i in range(16):
 line('input row %d'%i,A,[pos[16*i],pos[16*i+15]],faint,.004)
 line('input col %d'%i,A,[pos[i],pos[240+i]],faint,.004)

# All 13 feasible XOR signatures; only five survive the output constraints.
cell_index={c['delta']:i for i,c in enumerate(D['cells'])}
sigpos={}
for i,delta in enumerate(signatures):
 q=Vector((-.55,-.08,3.73-i*.435));sigpos[delta]=q
 mat=cols[cell_index[delta]] if delta in cell_index else dim
 # A rectangular factor plate, matching the earlier tensor figure.
 bpy.ops.mesh.primitive_cube_add(size=1,location=q)
 ob=bpy.context.object
 for old in list(ob.users_collection):old.objects.unlink(ob)
 B.objects.link(ob);ob.name='signature delta=%d'%delta;ob.dimensions=(.57,.16,.14);ob.data.materials.append(mat);ob['delta']=delta;ob['nonempty']=delta in cell_index
for x,q in pos.items():
 delta=x^((x+offset)&255);dest=sigpos[delta]
 mat=cols[owner[x]] if x in members else faint
 line('a=%d -> delta=%d'%(x,delta),R,[q,(-2.45,.15,.52*q.z+.48*dest.z),dest],mat,.006 if x in members else .0024,True)

# Each right-hand component is the true cube of its basis coefficients.
# Its vertices have exact binary-word values; its edges change one basis coefficient.
rotation=Euler((.26,.35,.25)).to_matrix()
for idx,c in enumerate(D['cells']):
 d=len(c['basis']);center=Vector((6.05,.05,3.60-idx*1.30));points={};values={}
 scale=.44 if d<3 else .48
 for b in range(1<<d):
  value=c['base']
  for j,v in enumerate(c['basis']):
   if b>>j&1:value^=v
  if d==0:local=Vector((0,0,0))
  elif d==1:local=Vector((((b&1)*2-1)*.52,0,0))
  elif d==2:local=Vector((((b&1)*2-1)*.43,0,(((b>>1)&1)*2-1)*.35))
  else:local=rotation@Vector(tuple((((b>>j)&1)*2-1)*scale for j in range(3)))
  points[b]=center+local;values[b]=value
  diamond('cell %d word %d'%(idx,value),C,points[b],.09,cols[idx],{'base':c['base'],'word':value,'basis_coefficients':b,'dimension':d})
 assert set(values.values())==set(c['members'])
 for a in points:
  for j in range(d):
   b=a^(1<<j)
   if a<b:line('cell %d basis %d'%(idx,j),C,[points[a],points[b]],cols[idx],.011)
 delta=c['delta'];line('nonempty affine cell %d'%idx,R,[sigpos[delta],(2.50,-.17,.48*sigpos[delta].z+.52*center.z),(center.x-.85,-.15,center.z)],cols[idx],.012,True)
 text(str(1<<d),7.26,center.z-.05,.27,cols[idx])

# Exact matrix of the selected binary-linear map, with no decorative geometry.
for i,row in enumerate(rows):
 for j in range(8):
  bit=(row>>j)&1
  diamond('matrix row%d col%d=%d'%(i,j,bit),P,(-9.06+j*.19,-.08,-3.65-i*.19),.037 if bit else .018,cyan if bit else dim)
text('L',-9.05,-3.28,.28,white)
text('L(a + D) + L(a) = S   mod 2ʷ',-9.45,5.02,.32,white)
text('N ≤ F',4.93,5.02,.46,gold);text('w+1',6.32,4.92,.245,gold)
text('256',-7.15,4.20,.31,white,True);text('13',-.55,4.20,.34,gold,True)
text('5',6.03,4.40,.33,white,True)
text('2',-2.8,-4.12,.83,white);text('8',-2.32,-3.60,.31,white)
text('→',-1.5,-4.10,.68,white);text('13',-.10,-4.12,.86,gold)
text('|A| = 1 + 2 + 2 + 4 + 8 = 17',3.72,-4.23,.31,cyan)
text('w = 8     D = 30     S = 146',-2.8,-4.97,.245,white)
text('lmtlssss',6.55,-5.92,.23,white)
text('10.5281/zenodo.23697726',-9.45,-5.92,.19,dim)

s['author']='lmtlssss🜐';s['doi']='10.5281/zenodo.23697726'
s['input_words']=256;s['carry_signatures']=13;s['affine_cells']=5;s['solutions']=17
proof=bpy.data.texts.new('EXACT_AFFINE_CELLS.json');proof.write(json.dumps(D,indent=2))
bpy.ops.object.camera_add(location=(1.55,-36,7.5));camera=bpy.context.object
camera.rotation_euler=(Vector((-.35,0,-.35))-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.type='ORTHO';camera.data.ortho_scale=22.2;s.camera=camera
for f in list(bpy.data.fonts):
 if f.name!='Bfont' and f.users==0:bpy.data.fonts.remove(f)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'affine-carry.blend'),compress=True)
bpy.ops.render.render(write_still=True)
print('NATIVE_RENDER_OK',s.render.filepath,'INPUT_WORDS',256,'SIGNATURES',13,'AFFINE_CELLS',5,'OUTPUT_POINTS',17,flush=True)
