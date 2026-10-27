#!/usr/bin/env python3
"""Native proof figure: all 221 coefficient routes come from certificate.json.
Author: lmtlssss🜐. License: MIT. Run with Blender's Python interpreter.
"""
from pathlib import Path
import bpy,json,math,os,hashlib
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
D=json.loads((ROOT/'certificate.json').read_text())
OUT=Path(os.environ.get('FIGURE_OUTPUT',str(ROOT/'visual')));OUT.mkdir(parents=True,exist_ok=True)
terms=D['terms'];assert len(terms)==20
for i in range(12):
 for j in range(12):
  assert [sum(t['alpha'][i]*t['beta'][j]*t['gamma'][k] for t in terms) for k in range(12)]==[int(D['multiplication_table'][i][j]==k) for k in range(12)]
bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene
try:s.render.engine='BLENDER_EEVEE_NEXT'
except Exception:s.render.engine='BLENDER_EEVEE'
s.render.resolution_x=2400;s.render.resolution_y=1650;s.render.resolution_percentage=100
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB'
s.render.filepath=str(OUT/'twenty-signed-products.png');s.render.film_transparent=False
s.view_settings.view_transform='Standard'
w=bpy.data.worlds.new('Graphite');s.world=w;w.use_nodes=True
w.node_tree.nodes['Background'].inputs['Color'].default_value=(.003,.0045,.006,1)
w.node_tree.nodes['Background'].inputs['Strength'].default_value=.5

def col(n):
 c=bpy.data.collections.new(n);s.collection.children.link(c);return c
A=col('01 / a and b inputs');B=col('02 / 20 bilinear products');C=col('03 / signed coefficient routes');P=col('04 / twelve output coordinates');T=col('05 / mathematical notation');S=col('06 / proof count');V=col('07 / camera and field')

def mat(n,rgb,strength=1):
 m=bpy.data.materials.new(n);m.diffuse_color=(*rgb,1);m.use_nodes=True
 nd=m.node_tree.nodes;nd.clear();e=nd.new('ShaderNodeEmission');e.inputs['Color'].default_value=(*rgb,1);e.inputs['Strength'].default_value=strength
 o=nd.new('ShaderNodeOutputMaterial');m.node_tree.links.new(e.outputs[0],o.inputs['Surface']);return m
ink=mat('ivory',(.85,.91,.94),1.0)
cyan=mat('positive coefficient',(.45,.79,.83),.9)
neg=mat('negative coefficient',(.88,.75,.44),.95)
dim=mat('construction line',(.13,.23,.28),.65)
faint=mat('positive support',(.27,.45,.48),.75)
quiet=mat('secondary type',(.44,.55,.58),.95)
gold=mat('signed product',(.96,.83,.52),1.0)
groups=[mat('scalar characters',(.55,.81,.84)),mat('residual coordinates',(.77,.78,.82)),mat('matrix component',(.92,.84,.61))]

def move(o,c):
 for q in list(o.users_collection):q.objects.unlink(o)
 c.objects.link(o);return o

def diamond(n,pos,r,m,c,properties=None):
 x,y,z=pos;verts=[(x+r,y,z),(x-r,y,z),(x,y+r*.5,z),(x,y-r*.5,z),(x,y,z+r),(x,y,z-r)]
 faces=[(0,2,4),(2,1,4),(1,3,4),(3,0,4),(2,0,5),(1,2,5),(3,1,5),(0,3,5)]
 me=bpy.data.meshes.new(n);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(n,me);c.objects.link(o);me.materials.append(m)
 for k,v in (properties or {}).items():o[k]=v
 return o

def tube(n,pts,m,r=.007,c=C):
 d=bpy.data.curves.new(n,'CURVE');d.dimensions='3D';d.bevel_depth=r;d.bevel_resolution=1
 sp=d.splines.new('POLY');sp.points.add(len(pts)-1)
 for p,co in zip(sp.points,pts):p.co=(*co,1)
 o=bpy.data.objects.new(n,d);c.objects.link(o);d.materials.append(m);return o

def route(n,start,end,coefficient,kind):
 # Cubic paths carry exactly one nonzero coefficient. Negative routes are dashed.
 a,b=Vector(start),Vector(end);delta=b-a
 c1=a+Vector((.36*delta.x,.20,0));c2=b-Vector((.34*delta.x,-.20,0))
 pts=[]
 for k in range(41):
  t=k/40;pts.append((1-t)**3*a+3*(1-t)**2*t*c1+3*(1-t)*t*t*c2+t**3*b)
 m=neg if coefficient<0 else (cyan if kind!='output' else ink)
 radius=.006 if kind!='output' else .009
 if abs(coefficient)==2:radius*=1.55
 if coefficient<0:
  for i in range(0,40,4):
   o=tube(n+' negative %d'%i,pts[i:min(i+3,41)],m,radius);o['coefficient']=coefficient
 else:
  o=tube(n,pts,m,radius);o['coefficient']=coefficient

fontpath=Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
font=bpy.data.fonts.load(str(fontpath)) if fontpath.exists() else None

def text(body,x,z,size=.3,m=ink,align='LEFT'):
 d=bpy.data.curves.new(body,'FONT');d.body=body;d.size=size;d.align_x=align;d.extrude=.0001
 if font:d.font=font
 o=bpy.data.objects.new('Notation / '+body,d);T.objects.link(o);o.location=(x,-.9,z);o.rotation_euler=(math.pi/2,0,0);d.materials.append(m)
 bpy.ops.object.select_all(action='DESELECT');bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.convert(target='MESH');o.select_set(False)
 return o

# All input/output coordinates and factor counts are literal, not sampled.
a_positions=[];b_positions=[];p_positions=[]
for i in range(12):
 z=3.55-.57*i
 a_positions.append((-9.25,-.02,z));b_positions.append((-6.65,-.25,z));p_positions.append((8.35,-.15,z))
 diamond('a_%d'%i,a_positions[-1],.081,cyan,A,{'coordinate':i,'input_bank':'a'})
 diamond('b_%d'%i,b_positions[-1],.081,ink,A,{'coordinate':i,'input_bank':'b'})
 diamond('p_%d'%i,p_positions[-1],.14,ink,P,{'coordinate':i})
 text(str(i),8.68,z-.068,.175,quiet)
text('a',-9.28,4.05,.32);text('b',-6.69,4.05,.32);text('p',8.29,4.05,.32)
# Source banks retain their independent identities.
for x in (-9.25,-6.65):tube('bank rail',[(x,.08,3.72),(x,.08,-2.88)],dim,.006,A)
count={'alpha':0,'beta':0,'gamma':0,'negative':0,'double':0}
for r,t in enumerate(terms):
 z=4.01-.39*r;center=Vector((.85,-.23,z))
 bpy.ops.mesh.primitive_cube_add(size=1,location=center)
 o=move(bpy.context.object,B);o.name='Product %02d'%(r+1);o.dimensions=(.55,.16,.14)
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 o.data.materials.append(groups[0 if r<5 else 1 if r<13 else 2])
 bevel=o.modifiers.new('small machined edge','BEVEL');bevel.width=.018;bevel.segments=2
 o['factor_index']=r;o['alpha']=t['alpha'];o['beta']=t['beta'];o['gamma']=t['gamma']
 for bank,points,offset in [('alpha',a_positions,-.047),('beta',b_positions,.047)]:
  for i,c in enumerate(t[bank]):
   if not c:continue
   end=(center.x-.28,center.y,z+offset)
   route('%s_%d -> product_%d'%(bank,i,r+1),points[i],end,c,bank)
   count[bank]+=1;count['negative']+=int(c<0);count['double']+=int(abs(c)==2)
 for k,c in enumerate(t['gamma']):
  if not c:continue
  route('product_%d -> p_%d'%(r+1,k),(center.x+.28,center.y,z),p_positions[k],c,'output')
  count['gamma']+=1;count['negative']+=int(c<0);count['double']+=int(abs(c)==2)
assert (count['alpha'],count['beta'],count['gamma'])==(104,66,51)
text('20',.85,4.47,.43,gold,'CENTER')
# One source equation and one rank bound; sparse notation matches the earlier plate.
text('C[i,j,k] = 1[M(i,j)=k]',-9.9,5.55,.32)
text('18 ≤ rank_R(C) ≤ 20',4.10,5.53,.38,gold)
# Sign legend describes the encoded coefficient routes.
tube('plus sample',[(-9.25,-.2,-3.42),(-8.45,-.2,-3.42)],cyan,.012,T);text('+',-8.18,-3.50,.25,cyan)
for j in range(4):tube('minus sample',[(-6.65+j*.20,-.2,-3.42),(-6.53+j*.20,-.2,-3.42)],neg,.012,T)
text('−',-5.56,-3.50,.25,neg)
# Count comparison, with 35 exact nonnegative rectangles and 20 signed terms.
for i in range(35):
 diamond('nonnegative rectangle %d'%i,S and (-9.18+.25*(i%7),-.12,-4.51-.25*(i//7)),.045,cyan,S,{'rectangle':i})
for i in range(20):
 diamond('signed term count %d'%i,(-6.02+.25*(i%5),-.12,-4.51-.25*(i//5)),.055,gold,S,{'factor':i})
text('35',-8.43,-6.06,.32,quiet,'CENTER');text('20',-5.52,-6.06,.32,quiet,'CENTER')
text('35  →  20',-.65,-4.85,.91,ink)
text('35',.10,-5.91,.40,cyan);text('q',.70,-5.62,.20,cyan)
text('/',1.01,-5.91,.40,quiet);text('20',1.37,-5.91,.40,gold);text('q',1.97,-5.62,.20,gold)
text('= (7/4)',2.36,-5.91,.40,ink);text('q',4.03,-5.62,.20,ink)
text('lmtlssss',7.90,-6.10,.23,quiet)
# The caption lives in the archive; no promotional text in the render.
s['author']='lmtlssss🜐';s['doi']='10.5281/zenodo.23695066'
s['exact_coefficients_checked']=1728;s['coefficient_routes']=json.dumps(count)
s['certificate_sha256']=hashlib.sha256((ROOT/'certificate.json').read_bytes()).hexdigest()
s['mathematical_scope']='Exact 20-product signed construction; nonnegative minimum 35; real rank interval [18,20].'
s['figure_legend']='Solid cyan/ivory: positive coefficient. Dashed gold: negative coefficient. Thicker input routes: coefficient 2.'
txt=bpy.data.texts.new('CERTIFICATE.json');txt.write(json.dumps(D,ensure_ascii=False,indent=2))
txt=bpy.data.texts.new('README');txt.write('Twenty factor blocks, two twelve-coordinate input banks, and twelve output coordinates. Every route is a nonzero alpha, beta or gamma coefficient. A signed factor is a product of two linear forms. The lower two arrays count 35 nonnegative terms and 20 signed terms. The main figure describes the signed circuit. The tensor-power ratio compares the exact positive minimum with the explicit signed construction.')
background=mat('flat graphite',(.0035,.0050,.0070),1)
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,1.0,0),rotation=(math.pi/2,0,0));o=move(bpy.context.object,V);o.data.materials.append(background)
bpy.ops.object.camera_add(location=(1.5,-35,5.5));cam=move(bpy.context.object,V)
cam.rotation_euler=(Vector((-.05,0,-.12))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=22.5;s.camera=cam
# Convert labels to meshes and remove unused fonts; no external font file is packed.
for f in list(bpy.data.fonts):
 if f.name!='Bfont' and f.users==0:bpy.data.fonts.remove(f)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'twenty-signed-products.blend'),compress=True)
bpy.ops.render.render(write_still=True)
print('SIGNED_RENDER_COMPLETE',s.render.filepath,dict(count),flush=True)
