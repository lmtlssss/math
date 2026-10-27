#!/usr/bin/env python3
"""Native Blender figure from the exact forward state graph. Author: lmtlssss🜐."""
import bpy,json,math,os
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/'graph.json').read_text())
OUT=Path(os.environ.get('FIGURE_OUTPUT',str(ROOT)))
OUT.mkdir(parents=True,exist_ok=True)
w=DATA['width'];r1,r2,s=DATA['taps'];h=r2-s
assert (w,r1,r2,s)==(24,3,4,1)
assert DATA['count']=='224' and DATA['states']==496
# Each edge records one accepted local transition; multiplicities are exact.
columns={j:set() for j in range(w+1)}
edges=[]
for e in DATA['edges']:
 seed=tuple(e['seed']);j=e['layer'];a=seed+tuple(e['from']);b=seed+tuple(e['to'])
 columns[j].add(a);columns[j+1].add(b);edges.append((j,a,b,e['bit'],int(e['multiplicity'])))
assert sum(weight for j,a,b,bit,weight in edges if j==w-1)==224
bpy.ops.wm.read_factory_settings(use_empty=True)
sc=bpy.context.scene
try:sc.render.engine='BLENDER_EEVEE_NEXT'
except Exception:sc.render.engine='BLENDER_EEVEE'
sc.render.resolution_x=2400;sc.render.resolution_y=1650;sc.render.resolution_percentage=100
sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGB'
sc.render.filepath=str(OUT/'00-cover.png');sc.view_settings.view_transform='Standard'
world=bpy.data.worlds.new('graphite');world.use_nodes=True;sc.world=world
world.node_tree.nodes['Background'].inputs['Color'].default_value=(.0046,.0078,.0115,1)
world.node_tree.nodes['Background'].inputs['Strength'].default_value=.5

def coll(name):
 c=bpy.data.collections.new(name);sc.collection.children.link(c);return c
N=coll('01 exact frontier states');E=coll('02 accepted local transitions');T=coll('03 theorem');G=coll('04 backdrop and camera');B=coll('05 four-bit state space')
def material(name,c,strength=1):
 m=bpy.data.materials.new(name);m.diffuse_color=(*c,1);m.use_nodes=True;m.node_tree.nodes.clear()
 em=m.node_tree.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(*c,1);em.inputs['Strength'].default_value=strength
 out=m.node_tree.nodes.new('ShaderNodeOutputMaterial');m.node_tree.links.new(em.outputs[0],out.inputs['Surface']);return m
white=material('ivory',(.84,.91,.94),1.1);gold=material('retained frontier',(.95,.77,.42),1.1)
cyan=material('accepted paths',(.43,.77,.81),.95);muted=material('secondary paths',(.15,.31,.37),.7)
soft=material('secondary notation',(.41,.54,.59),.95);dark=material('graphite field',(.0030,.0042,.0060),1)
pal=[material('seed %02d'%i,c,.85) for i,c in enumerate([(.47,.73,.80),(.64,.77,.72),(.78,.75,.55),(.67,.69,.83)])]

def mesh(name,group,p,r,m,props=None):
 x,y,z=p;vs=[(x+r,y,z),(x-r,y,z),(x,y+r*.5,z),(x,y-r*.5,z),(x,y,z+r),(x,y,z-r)]
 fs=[(0,2,4),(2,1,4),(1,3,4),(3,0,4),(2,0,5),(1,2,5),(3,1,5),(0,3,5)]
 d=bpy.data.meshes.new(name);d.from_pydata(vs,[],fs);d.materials.append(m)
 ob=bpy.data.objects.new(name,d);group.objects.link(ob)
 for k,v in (props or {}).items():ob[k]=v
 return ob

def line(name,group,p,m,r=.005,smooth=False):
 d=bpy.data.curves.new(name,'CURVE');d.dimensions='3D';d.bevel_depth=r;d.bevel_resolution=1;d.resolution_u=10
 sp=d.splines.new('BEZIER' if smooth else 'POLY')
 if smooth:
  sp.bezier_points.add(len(p)-1)
  for bp,co in zip(sp.bezier_points,p):bp.co=co;bp.handle_left_type='AUTO';bp.handle_right_type='AUTO'
 else:
  sp.points.add(len(p)-1)
  for bp,co in zip(sp.points,p):bp.co=(*co,1)
 ob=bpy.data.objects.new(name,d);group.objects.link(ob);d.materials.append(m);return ob
fontpath='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
font=bpy.data.fonts.load(fontpath) if Path(fontpath).exists() else None

def text(body,x,z,size=.3,m=white):
 d=bpy.data.curves.new(body,'FONT');d.body=body;d.size=size
 if font:d.font=font
 ob=bpy.data.objects.new('notation '+body,d);T.objects.link(ob);d.materials.append(m)
 ob.location=(x,-.65,z);ob.rotation_euler=(math.pi/2,0,0)
 bpy.ops.object.select_all(action='DESELECT');bpy.context.view_layer.objects.active=ob;ob.select_set(True);bpy.ops.object.convert(target='MESH');ob.select_set(False)
 return ob
# Source-derived layered graph; a node is one seed-specific sufficient state.
pos={};left=-9.5;step=18.4/w
for j in range(w+1):
 nodes=sorted(columns[j]);n=len(nodes)
 for rank,key in enumerate(nodes):
  z=3.95-(rank+.5)*6.25/max(n,1)
  at=Vector((left+step*j,.10*((key[0]+key[1])%3),z));pos[j,key]=at
  selected=(j==12)
  mat=gold if selected else (white if j==w else pal[key[0]%len(pal)])
  mesh('j%d seed%d-%d state%d-%d'%((j,)+key),N,at,.045 if j not in (0,w,12) else .074,mat,{'layer':j,'boundary_tail':key[0],'boundary_carry':key[1],'history':key[2],'history_carry':key[3]})
for k,(j,a,b,bit,weight) in enumerate(edges):
 p=pos[j,a];q=pos[j+1,b]
 line('transition %d'%k,E,[p,q],pal[a[0]%len(pal)] if bit else muted,.004 if bit else .003)
# The highlighted layer stores the exact sufficient state, rather than the prefix.
xx=left+step*12
line('frontier bracket',G,[(xx-.16,.3,4.2),(xx-.16,.3,-2.6),(xx+.16,.3,-2.6),(xx+.16,.3,4.2)],muted,.008)
text('j = 0',-9.55,4.47,.22,soft);text('12',xx-.15,4.47,.24,gold);text('24',8.55,4.47,.24,soft)
text('L(a + D) + L(a) = S   mod 2ʷ',-9.55,5.38,.34)
text('N ≤ w · 2²ʰ⁺²',5.14,5.34,.44,gold)
# A complete 4-bit state space: three input-history bits and their entering carry.
for i in range(16):
 x=-9.13+.43*(i%4);z=-4.22-.40*(i//4)
 mesh('possible Q '+format(i,'04b'),B,(x,-.05,z),.074,gold if i&8 else cyan,{'history':i&7,'carry':(i>>3)&1})
 for flip in range(4):
  k=i^(1<<flip)
  if i<k:
   dest=(-9.13+.43*(k%4),-.05,-4.22-.40*(k//4))
   line('Q coordinate edge %d-%d'%(i,k),B,[(x,-.05,z),dest],muted,.004)
text('h + 1 = 4',-9.35,-3.74,.28,soft)
text('2',-4.54,-4.48,.96);text('24',-3.89,-3.93,.37,soft)
text('→',-2.80,-4.48,.88);text('496',-1.38,-4.48,.96,gold)
text('input words',-4.46,-5.10,.21,soft);text('states',-.94,-5.10,.21,soft)
text('|A| = 224',5.02,-4.49,.44,cyan)
text('h = 3',5.09,-5.11,.25,soft)
text('D = 14587853   S = 15340541',-9.55,-6.02,.20,soft)
text('lmtlssss',7.71,-6.02,.23)
sc['author']='lmtlssss🜐';sc['doi']='10.5281/zenodo.23697063';sc['exact_states']=496;sc['exact_count']=224;sc['diagram_scope']='Complete accepted local-transition graph for the supplied 24-bit instance; each node includes its boundary seed.'
t=bpy.data.texts.new('EXACT_GRAPH.json');t.write(json.dumps(DATA,separators=(',',':')))
# Orthographic geometry in the same dark figure system as the first paper.
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,2,0),rotation=(math.pi/2,0,0));ob=bpy.context.object;ob.data.materials.append(dark)
for c in list(ob.users_collection):c.objects.unlink(ob)
G.objects.link(ob)
bpy.ops.object.camera_add(location=(1.4,-35,6.8));cam=bpy.context.object
for c in list(cam.users_collection):c.objects.unlink(cam)
G.objects.link(cam);cam.data.type='ORTHO';cam.data.ortho_scale=22.6;cam.rotation_euler=(Vector((0,0,-.18))-cam.location).to_track_quat('-Z','Y').to_euler();sc.camera=cam
for f in list(bpy.data.fonts):
 if f.name!='Bfont' and f.users==0:bpy.data.fonts.remove(f)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'bounded-tap-span.blend'),compress=True)
bpy.ops.render.render(write_still=True)
print('NATIVE_RENDER_OK',sc.render.filepath,'EDGE_COUNT',len(edges),'NODE_COUNT',sum(map(len,columns.values())),flush=True)
