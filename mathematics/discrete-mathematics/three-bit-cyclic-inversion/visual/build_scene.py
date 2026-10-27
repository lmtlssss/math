#!/usr/bin/env python3
"""Exact native Blender figure in the established graphite/cyan tensor visual system.
All traces derive from the published three-bit source certificate.
Author: lmtlssss🜐. The Blender file contains the full eight paths.
"""
import bpy, json, math, hashlib, os
from pathlib import Path
from mathutils import Vector
from collections import defaultdict

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parent/'evidence/sharp-traces.json'
if not SOURCE.is_file():
    SOURCE=ROOT.parent/'stage/paper/evidence/sharp-traces.json'
DATA=json.loads(SOURCE.read_text(encoding='utf-8'))
paths=sorted(DATA['paths'],key=lambda d:d['candidate'])
assert len(paths)==8
assert sorted(p['candidate'] for p in paths)==[11,22,44,49,69,88,98,127]
for p in paths:
    assert p['accepted'] and p['steps']==7 and len(p['bits'])==10
    assert p['bits'][7:10]==p['initial_bits']
    assert len(p['initial_bits'])==3

bpy.ops.wm.read_factory_settings(use_empty=True)
scene=bpy.context.scene
try: scene.render.engine='BLENDER_EEVEE_NEXT'
except Exception: scene.render.engine='BLENDER_EEVEE'
scene.render.resolution_x=2400
scene.render.resolution_y=1650
scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
scene.render.image_settings.color_mode='RGB'
scene.render.filepath=str(ROOT/'three-bit-boundary.png')
scene.render.film_transparent=False
scene.view_settings.view_transform='Standard'
try: scene.view_settings.look='Medium High Contrast'
except Exception: pass

world=bpy.data.worlds.new('Graphite / #080d12')
scene.world=world;world.use_nodes=True
world.node_tree.nodes['Background'].inputs['Color'].default_value=(.0046,.0078,.0115,1)
world.node_tree.nodes['Background'].inputs['Strength'].default_value=.5

def col(name):
    c=bpy.data.collections.new(name);scene.collection.children.link(c);return c
A=col('01 / eight three-bit boundary conditions')
B=col('02 / deterministic forced input bits')
C=col('03 / closure, each bit repeats')
D=col('04 / eight exact preimages')
E=col('05 / seven-cycle sharpness certificate')
F=col('06 / mathematical type and dimensions')
G=col('07 / camera and background')

def make_emission(name, color, strength=1.0):
    mat=bpy.data.materials.new(name)
    mat.diffuse_color=tuple(color)+(1,)
    mat.use_nodes=True
    nodes=mat.node_tree.nodes;nodes.clear()
    em=nodes.new('ShaderNodeEmission')
    em.inputs['Color'].default_value=tuple(color)+(1,)
    em.inputs['Strength'].default_value=strength
    output=nodes.new('ShaderNodeOutputMaterial')
    mat.node_tree.links.new(em.outputs['Emission'],output.inputs['Surface'])
    return mat

ink=make_emission('white / foreground',(.84,.90,.93),1.15)
pale=make_emission('soft white',(.54,.68,.73),.88)
dim=make_emission('construction / graphite blue',(.17,.31,.38),.65)
ghost=make_emission('zero bit dim',(.10,.16,.20),.49)
gold=make_emission('sharp witness / 3-bit',(.96,.75,.38),1.3)
goldsoft=make_emission('unlit witness gold',(.49,.38,.23),.78)
green=make_emission('steps / cyan',(.45,.85,.79),1.1)
palette=[
  (.53,.79,.85),(.62,.78,.74),(.76,.70,.83),(.87,.75,.58),
  (.56,.84,.80),(.84,.69,.78),(.62,.73,.94),(.95,.80,.55)
]
route_mats=[make_emission('route %d'%i,p,1.0) for i,p in enumerate(palette)]
node_mats=[make_emission('node %d'%i,p,1.2) for i,p in enumerate(palette)]

def mesh(name, collection, positions, faces, mat, props=None):
    m=bpy.data.meshes.new(name);m.from_pydata(positions,[],faces);m.update()
    ob=bpy.data.objects.new(name,m);collection.objects.link(ob)
    m.materials.append(mat)
    for k,v in (props or {}).items(): ob[k]=v
    return ob

def diamond(name,collection,pos,r,mat,props=None):
    x,y,z=pos
    offsets=((r,0,0),(-r,0,0),(0,r*.57,0),(0,-r*.57,0),(0,0,r),(0,0,-r))
    verts=[(x+a,y+b,z+c) for a,b,c in offsets]
    faces=((0,2,4),(2,1,4),(1,3,4),(3,0,4),(2,0,5),(1,2,5),(3,1,5),(0,3,5))
    return mesh(name,collection,verts,faces,mat,props)

def line(name,collection,points,mat,thickness=.008,smooth=False):
    curve=bpy.data.curves.new(name,'CURVE');curve.dimensions='3D'
    curve.bevel_depth=thickness;curve.bevel_resolution=2;curve.resolution_u=15
    spline=curve.splines.new('BEZIER' if smooth else 'POLY')
    if smooth:
        spline.bezier_points.add(len(points)-1)
        for bp,p in zip(spline.bezier_points,points):
            bp.co=p;bp.handle_left_type='AUTO';bp.handle_right_type='AUTO'
    else:
        spline.points.add(len(points)-1)
        for sp,p in zip(spline.points,points):sp.co=(*p,1)
    ob=bpy.data.objects.new(name,curve);collection.objects.link(ob)
    curve.materials.append(mat)
    return ob

FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
MONO='/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
font=bpy.data.fonts.load(FONT) if Path(FONT).exists() else None
mono=bpy.data.fonts.load(MONO) if Path(MONO).exists() else None

def label(body,x,z,size=.28,material=ink,center=False,monospace=False):
    curve=bpy.data.curves.new(body,'FONT')
    curve.body=body;curve.size=size;curve.align_x='CENTER' if center else 'LEFT'
    curve.space_character=1.0
    if (mono if monospace else font) is not None:
        curve.font=mono if monospace else font
    curve.extrude=.0001
    ob=bpy.data.objects.new('Text / '+body,curve);F.objects.link(ob)
    ob.location=(x,-.78,z);ob.rotation_euler=(math.pi/2,0,0)
    curve.materials.append(material)
    # Convert to mesh so font binaries aren't embedded in the source archive.
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active=ob;ob.select_set(True)
    bpy.ops.object.convert(target='MESH');ob.select_set(False)
    return ob

# Header: one mathematical definition and one theorem, like the prior tensor plate.
label('F(x) = (R₁x ⊕ R₃x) + (x ∧ c) + k    mod 2ʷ',-10.08,5.30,.31,ink)
label('|F⁻¹(y)| ≤ 8',5.45,5.30,.45,gold)
# Eight proof paths: every site comes from the published recurrence, not a conceptual illustration.
# The initial three bit values are gold-marked, closure bits are pale-gold; intervening nodes show actual 0/1.
source_x=-9.19
x0=-5.93
dx=.94
top=3.75
dy=.77
yfront=-.15
rows={}
labels=[]
for idx,p in enumerate(paths):
    z=top-idx*dy
    seed=p['initial_bits']
    code=''.join(map(str,seed))
    rgb=route_mats[idx]
    dimbit=route_mats[idx]
    # Three physical input bits, one per assigned coordinate.
    for j,b in enumerate(seed):
        x=source_x+j*.34
        diamond('source bit seed=%s j=%d v=%d'%(code,j,b),A,
                (x,yfront,z),.095 if b else .057,gold if b else goldsoft,
                {'seed':code,'bit_index':j,'bit':b})
    line('source port %s'%code,A,
         [(source_x-.12,yfront,z),(source_x+.89,yfront,z)],dim,.008)
    label(code,source_x-.98,z-.075,.245,pale,monospace=True)
    positions=[]
    for j,bit in enumerate(p['bits']):
        x=x0+dx*j
        extra=.12 if bit else -.09
        # Use the bit value as a small measurable path displacement, not decoration.
        pos=Vector((x,yfront-.10*bit,z+extra))
        positions.append(pos)
        if j<3:
            material=gold if bit else goldsoft
            size=.085 if bit else .065
            target=A
        elif j<7:
            material=node_mats[idx] if bit else ghost
            size=.075 if bit else .045
            target=B
        else:
            material=gold if bit else goldsoft
            size=.080 if bit else .062
            target=C
        diamond('row %d exact x_%d = %d'%(idx,j,bit),target,pos,size,material,
                {'path':idx,'seed':code,'bit_index':j,'bit_value':bit,'closure':j>=7})
        if j>0:
            line('forced step %d / %d'%(idx,j),B,
                 [positions[-2],pos],rgb,.010 if bit else .007)
    rows[p['candidate']]=positions
    # Across the source-to-trace junction, exact data are conveyed by 3 bits.
    line('source → path %s'%code,B,
         [(source_x+.91,yfront,z),(-7.20,-.36,z),positions[0]],rgb,.008,True)
    # The three terminal coordinates repeat the first three by exact cyclic closure.
    for j in range(3):
        assert p['bits'][j]==p['bits'][j+7]
    # Explicit expected inverse value, as the output sites in the reference tensor graphic.
    dest=Vector((7.93,yfront,z))
    line('validated inverse %d'%p['candidate'],D,
         [positions[-1],(5.72,-.35,z+.035),dest],rgb,.010,True)
    diamond('preimage '+str(p['candidate']),D,dest,.145,node_mats[idx],
            {'preimage':p['candidate'],'seed':code})
    label(str(p['candidate']),8.33,z-.07,.245,pale,monospace=True)

# Each emitted bit depends on two earlier positions in the exact recurrence
# x_(i+3) = t_i XOR x_(i+1) XOR (x_i AND c_i) XOR carry_i.
# The thin threads show these genuine dependencies, analogous to source→factor
# routes in the twelve-state tensor publication. None is randomly generated.
dep=col('08 / exact local recurrence dependency threads')
thread=make_emission('dependency cyan / substructure',(.18,.44,.49),.48)
thread_gold=make_emission('dependency ochre / substructure',(.53,.39,.20),.47)
for row,p in enumerate(paths):
    pos=rows[p['candidate']]
    for i in range(7):
        a=pos[i];b=pos[i+1];target=pos[i+3]
        # Two distinct causal bit inputs to every forced later bit.
        lift=.22+0.045*(i%3)
        line('recurrence x_%d → x_%d seed %d'%(i,i+3,row),dep,
             [(a.x,.31,a.z),(a.x+.69,.35,a.z+lift),
              (target.x-.55,.35,target.z+lift*.64),(target.x,.31,target.z)],
             thread_gold if i<3 else thread,.0038,True)
        line('recurrence x_%d → x_%d seed %d'%(i+1,i+3,row),dep,
             [(b.x,.29,b.z),(b.x+.36,.31,b.z-lift*.68),
              (target.x-.35,.31,target.z-lift*.58),(target.x,.29,target.z)],
             thread,.0027,True)

# Guides and small labels reveal structure but do not repeat the theorem.
line('boundary divider',G,[(-6.45,-.02,4.24),(-6.45,-.02,-2.31)],dim,.007)
line('closure divider',G,[(.20,-.02,4.24),(.20,-.02,-2.31)],dim,.006)
line('trace frame top',G,[(-6.13,-.02,4.28),(2.72,-.02,4.28)],dim,.006)
line('trace frame bottom',G,[(-6.13,-.02,-2.30),(2.72,-.02,-2.30)],dim,.006)
label('3',-8.72,4.48,.34,gold)
label('7',-1.83,4.48,.34,pale)
label('8',7.89,4.48,.34,ink)
label('x₀',-5.95,4.42,.16,pale,center=True)
label('x₉',2.55,4.42,.16,pale,center=True)

# Exact seven-cycle plus fixed point for the sharpness witness.
# T(a,b,c)=(b,c,1 ⊕ b ⊕ a) when w=7 and c=y=127, k=0.
def transition(state):
    a,b,c=state
    return (b,c,1^b^a)
states=[tuple((i>>j)&1 for j in range(3)) for i in range(8)]
fixed=[s for s in states if transition(s)==s]
assert fixed==[(1,1,1)]
ring=[(0,0,0)]
for _ in range(6): ring.append(transition(ring[-1]))
assert len(set(ring))==7 and transition(ring[-1])==ring[0]
cx=-8.52;cz=-4.62;radius=1.08
orbit={}
for j,state in enumerate(ring):
    a=math.tau*j/7-math.pi/2
    pos=Vector((cx+radius*math.cos(a),-.22,cz+radius*math.sin(a)))
    orbit[state]=pos
    diamond('period-seven state '+''.join(map(str,state)),E,pos,.11,gold)
for s in ring:
    nxt=transition(s)
    p=orbit[s];q=orbit[nxt]
    line('seven-cycle arrow '+''.join(map(str,s)),E,[p,q],route_mats[3],.012)
diamond('fixed point 111',E,(cx,-.20,cz),.15,ink,
        {'state':111,'fixed_point':True})
label('7 + 1',-6.96,-4.67,.30,pale)

# The main claim, one visual hierarchy: input domain to eight source seeds.
label('2',-1.92,-4.41,.86,ink)
label('w',-1.35,-3.91,.36,pale)
label('→',-.55,-4.40,.78,ink)
label('8',.77,-4.42,.94,gold)
label('≤ 8w',-.24,-5.23,.42,green,center=True)
label('w = 7     c = y = 127     k = 0',4.84,-4.23,.225,pale,monospace=True)

# Quiet footer, no decorative slogan, no re-captioning of every quantity.
label('lmtlssss',7.66,-6.00,.23,ink,monospace=True)
label('10.5281/zenodo.23680529',-1.95,-6.00,.195,pale,monospace=True)
# Embed source for audit and reproducibility.
tt=bpy.data.texts.new('EXACT_EIGHT_PREIMAGES.json')
tt.write(json.dumps(DATA,sort_keys=True,indent=2))
readme=bpy.data.texts.new('SCENE_STRUCTURE')
readme.write('Graphite figure for the exact three-bit inversion theorem. Eight input triples feed eight deterministic seven-step recurrences. Every preimage is exact. T has a seven-cycle and the fixed point (1,1,1). No simulated branches.\n')
scene['author']='lmtlssss🜐'
scene['doi']='10.5281/zenodo.23680529'
scene['proof']='sharp-traces.json'
scene['exact_preimages']=str(sorted(rows))
scene['three_bit_states']=8
scene['forced_updates']=8*7
scene['sharpness_cycles']='7 + 1'
scene['source_sha256']=hashlib.sha256(SOURCE.read_bytes()).hexdigest()

# Native orthographic camera, not a rasterized SVG.
bpy.ops.object.camera_add(location=(1.8,-35,7.0))
camera=bpy.context.object;camera.name='Proof plate / orthographic'
for co in list(camera.users_collection):co.objects.unlink(camera)
G.objects.link(camera)
target=Vector((-.04,0,-.18))
camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler()
camera.data.type='ORTHO'
camera.data.ortho_scale=22.8
scene.camera=camera

# An opaque, matte world plane eliminates soft gradients and spotlight artifacts.
background=make_emission('flat graphite field',(.0066,.0105,.0148),1.0)
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,1.0,0),rotation=(math.pi/2,0,0))
ob=bpy.context.object;ob.name='Backdrop / graphite'
for co in list(ob.users_collection):co.objects.unlink(ob)
G.objects.link(ob);ob.data.materials.append(background)
for o in bpy.data.objects:
    if o.type=='MESH':
        o.hide_set(False)
try:bpy.ops.file.pack_all()
except Exception:pass
blend=ROOT/'three-bit-boundary.blend'
bpy.ops.wm.save_as_mainfile(filepath=str(blend),compress=True)
bpy.ops.render.render(write_still=True)
assert blend.is_file() and Path(scene.render.filepath).is_file()
print('RENDER_COMPLETE',blend,scene.render.filepath,'SHA256',scene['source_sha256'],flush=True)
