#!/usr/bin/env python3
"""Native Blender proof plate from exact binary-algebra certificates.
Run on a native/cloud host: blender -b --python visual/build_scene.py
"""
import bpy,json,math,os
from pathlib import Path
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[1]
OUT=Path(os.environ.get('FIGURE_OUTPUT',str(ROOT/'visual')))
OUT.mkdir(parents=True,exist_ok=True)
words=json.loads((ROOT/'evidence/short-word-certificate.json').read_text())['words']
c=json.loads((ROOT/'evidence/rank-one-certificate.json').read_text())
assert len(words)==len(set(words))==1024 and max(map(len,words))==10
levels={d:sorted(w for w in words if len(w)==d) for d in range(11)}
assert [len(levels[d]) for d in range(11)]==[1,2,4,8,16,32,64,128,255,481,33]

bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=12
s.cycles.use_denoising=False;s.cycles.device='CPU'
s.render.resolution_x=2400;s.render.resolution_y=1650;s.render.resolution_percentage=100
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB'
s.render.filepath=str(OUT/'00-cover.png');s.view_settings.view_transform='Standard'
world=bpy.data.worlds.new('graphite');world.use_nodes=True;s.world=world
world.node_tree.nodes['Background'].inputs['Color'].default_value=(.0028,.0037,.0056,1)
world.node_tree.nodes['Background'].inputs['Strength'].default_value=1

def material(name,color,strength=1):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True;m.node_tree.nodes.clear()
 e=m.node_tree.nodes.new('ShaderNodeEmission');e.inputs[0].default_value=(*color,1);e.inputs[1].default_value=strength
 o=m.node_tree.nodes.new('ShaderNodeOutputMaterial');m.node_tree.links.new(e.outputs[0],o.inputs['Surface']);return m
INK=material('ivory',(.79,.86,.88));CYAN=material('cyan',(.45,.72,.78))
DIM=material('structural thread',(.10,.22,.27),.64);ZERO=material('zero entry',(.025,.05,.065),.5)
GOLD=material('ten-factor words',(.90,.72,.36),1.35);FAINT=material('secondary type',(.30,.46,.50),.9)

cols={}
for name in ['01 sparse generators','02 exact word basis tree','03 full basis coordinates','04 rank-one witness','05 notation','06 camera']:
 z=bpy.data.collections.new(name);s.collection.children.link(z);cols[name]=z

def obj(name,data,coll,mat=None,props=None):
 o=bpy.data.objects.new(name,data);cols[coll].objects.link(o)
 if mat is not None:data.materials.append(mat)
 for k,v in (props or {}).items():o[k]=v
 return o

def dots(name,points,size,mat,coll):
 vs=[];fs=[]
 for x,y,z in points:
  off=len(vs);vs.extend([(x-size,y,z),(x,y-.025,z+size),(x+size,y,z),(x,y+.025,z-size)])
  fs.append(tuple(off+j for j in range(4)))
 m=bpy.data.meshes.new(name);m.from_pydata(vs,[],fs);m.update()
 return obj(name,m,coll,mat,{'point_count':len(points)})

def line(name,points,mat=DIM,width=.006,coll='02 exact word basis tree',smooth=False):
 m=bpy.data.curves.new(name,'CURVE');m.dimensions='3D';m.bevel_depth=width;m.bevel_resolution=1;m.resolution_u=12
 p=m.splines.new('BEZIER' if smooth else 'POLY')
 if smooth:
  p.bezier_points.add(len(points)-1)
  for b,co in zip(p.bezier_points,points):b.co=co;b.handle_left_type='AUTO';b.handle_right_type='AUTO'
 else:
  p.points.add(len(points)-1)
  for b,co in zip(p.points,points):b.co=(*co,1)
 return obj(name,m,coll,mat)

fontpath=Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
font=bpy.data.fonts.load(str(fontpath)) if fontpath.is_file() else None

def label(text,x,z,size=.28,mat=INK,align='LEFT'):
 m=bpy.data.curves.new(text,'FONT');m.body=text;m.size=size;m.align_x=align
 if font:m.font=font
 m.extrude=.0001
 o=obj('type '+text,m,'05 notation',mat);o.location=(x,-.6,z);o.rotation_euler=(math.pi/2,0,0)
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
 bpy.ops.object.convert(target='MESH');o.select_set(False)
 return o

# Two actual sparse 32 x 32 matrices; each point is a coefficient, not decoration.
for name,rots,shift,cz,mat in [('A',(7,18),3,2.35,CYAN),('B',(17,19),10,-1.25,INK)]:
 x0=-10.12;z0=cz+1.38;step=.0835;ones=[];zeros=[]
 for i in range(32):
  for j in range(32):
   value=(j==(i+rots[0])%32)^(j==(i+rots[1])%32)^((i+shift<32) and j==i+shift)
   (ones if value else zeros).append((x0+j*step,0,z0-i*step))
 dots(name+' / nonzero coefficients',ones,.037,mat,'01 sparse generators')
 dots(name+' / zero coefficients',zeros,.010,ZERO,'01 sparse generators')
 for dx in [0,31*step]:line(name+' vertical frame',[(x0+dx-.06,.12,z0+.09),(x0+dx-.06,.12,z0-31*step-.09)],DIM,.005,'01 sparse generators')
 label(name,x0-.12,cz+1.75,.34,mat)

# Every independent word and every prefix edge from the finite certificate.
pos={}
for d,group in levels.items():
 for i,w in enumerate(group):
  z=0.50 if len(group)==1 else 3.77-6.65*i/(len(group)-1)
  pos[w]=Vector((-5.9+.78*d,.04,z))
for d,group in levels.items():
 pts=[pos[w] for w in group]
 dots('basis words length '+str(d),pts,.038 if d<8 or d==10 else .021,GOLD if d==10 else CYAN,'02 exact word basis tree')
 for w in group:
  if not w:continue
  p=pos[w[:-1]];q=pos[w]
  line('prefix '+w,[p,Vector(((p.x+q.x)/2,.15,(p.z+q.z)/2)),q],GOLD if d==10 else DIM,.0045 if d==10 else .0032,smooth=True)
label('I',pos[''].x-.15,4.28,.23,FAINT)
label('9',pos[levels[9][0]].x,4.28,.24,FAINT,align='CENTER')
label('10',pos[levels[10][0]].x,4.28,.29,GOLD,align='CENTER')
# The matrices specify the two edge labels; connect them to the corresponding one-letter word.
line('A first action',[(-7.35,-.1,2.55),(-6.90,-.15,3.1),pos['A']],CYAN,.010,smooth=True)
line('B first action',[(-7.35,-.1,-1.15),(-6.70,-.15,-2.2),pos['B']],INK,.010,smooth=True)

# The 1024 independent words, in their exact certificate order, on a square index grid.
grid={};early=[];last=[]
for index,w in enumerate(words):
 i,j=divmod(index,32);p=Vector((4.88+.147*j,0,3.20-.147*i));grid[w]=p
 (last if len(w)==10 else early).append(p)
dots('991 independent shorter words',early,.042,CYAN,'03 full basis coordinates')
dots('33 additional length-ten words',last,.052,GOLD,'03 full basis coordinates')
for w in levels[10]:
 p=pos[w];q=grid[w]
 line('new basis direction '+w,[p,Vector((3.30,.22,.45*p.z+.55*q.z)),q],GOLD,.004,'03 full basis coordinates',True)
label('1024',7.2,3.74,.43,INK,align='CENTER')
label('W₀ , … , W₁₀₂₃',7.2,-2.05,.22,FAINT,align='CENTER')

# Exact rank-one support, shown as a small independent proof witness.
u=int(c['u'],16);v=int(c['v'],16);ones=[]
for i in range(32):
 for j in range(32):
  if ((u>>i)&1) and ((v>>j)&1):ones.append((-9.92+.053*j,.0,-4.22-.053*i))
dots('rank-one polynomial support',ones,.022,GOLD,'04 rank-one witness')
label('p(B³ + A) = uvᵀ',-7.82,-4.84,.27,INK)
label('rank = 1',-7.82,-5.34,.22,FAINT)

# One theorem, one sharp bound. The geometry supplies the rest.
label('F₂[A, B] = M₃₂(F₂)',-10.22,5.15,.43,INK)
label('ℓ(A, B) = 10',5.74,5.15,.47,GOLD)
label('991  →  1024',-.02,-4.91,.68,INK,align='CENTER')
label('dim L₉        dim L₁₀',-.02,-5.53,.245,FAINT,align='CENTER')
label('2¹⁰ − 1 < 32²',6.73,-4.91,.34,GOLD,align='CENTER')
label('lmtlssss',8.44,-6.67,.22,INK)
label('10.5281/zenodo.23701587',-10.16,-6.67,.19,FAINT)

# Pure emission retains the matte graphite technical field and fine ink geometry.
bpy.ops.object.camera_add(location=(1.0,-35,4.5));camera=bpy.context.object
for co in list(camera.users_collection):co.objects.unlink(camera)
cols['06 camera'].objects.link(camera)
camera.rotation_euler=(Vector((-.2,0,-.3))-camera.location).to_track_quat('-Z','Y').to_euler()
camera.data.type='ORTHO';camera.data.ortho_scale=23.5;s.camera=camera
s['author']='lmtlssss🜐';s['doi']='10.5281/zenodo.23701587'
s['basis_dimension']=1024;s['maximum_word_length']=10;s['length9_dimension']=991
s['exact_prefix_edges']=1023;s['new_length10_directions']=33
for name,path in [('SHORT_WORD_CERTIFICATE','short-word-certificate.json'),('RANK_ONE_CERTIFICATE','rank-one-certificate.json')]:
 t=bpy.data.texts.new(name);t.write((ROOT/'evidence'/path).read_text())
# Remove unused file fonts. No font binaries are included in the source package.
for f in list(bpy.data.fonts):
 if f.name!='Bfont' and f.users==0:bpy.data.fonts.remove(f)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'binary-algebra.blend'),compress=True)
bpy.ops.render.render(write_still=True)
receipt={'renderer':'Blender Cycles CPU','size':[2400,1650], 'basis_words':1024,'prefix_edges':1023,'generator_matrices':2,'rank_one_nonzero_entries':len(ones),'length10_words':33,'diagram_source':'exact word certificate and matrix entries'}
(OUT/'render-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('NATIVE_RENDER_OK',s.render.filepath,json.dumps(receipt),flush=True)
