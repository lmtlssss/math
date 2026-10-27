#!/usr/bin/env python3
"""Build the exact cascaded-addition plate in native Blender, then render it.
Run with Blender 4.2 or later: blender -b --python visual/build_scene.py
The source-to-class incidence is complete. Font binaries are not embedded.
"""
from __future__ import annotations
from collections import defaultdict
from pathlib import Path
import json, math, os, sys
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from geometry import geometry, PALETTE

ROOT=Path(__file__).resolve().parents[1]
OUT=Path(os.environ.get('FIGURE_OUTPUT',str(ROOT/'visual/render')))
OUT.mkdir(parents=True,exist_ok=True)
data,sources,classes,routes=geometry(ROOT/'evidence/figure.json')
bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene
s.render.engine='CYCLES'
s.cycles.device='CPU';s.cycles.samples=8;s.cycles.use_denoising=False
s.render.resolution_x=2400;s.render.resolution_y=1650;s.render.resolution_percentage=100
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB'
s.render.filepath=str(OUT/'00-cover.png');s.render.film_transparent=False
s.view_settings.view_transform='Standard'
try:s.view_settings.look='None'
except TypeError:pass
s.view_settings.exposure=0;s.view_settings.gamma=1

def linear_channel(v):
    v=v/255
    return v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4

def rgb(code):
    return tuple(linear_channel(int(code[i:i+2],16)) for i in (1,3,5))

def material(name,code,scale=1):
    m=bpy.data.materials.new(name);m.use_nodes=True;m.node_tree.nodes.clear()
    e=m.node_tree.nodes.new('ShaderNodeEmission');e.inputs['Color'].default_value=(*rgb(code),1)
    e.inputs['Strength'].default_value=scale
    out=m.node_tree.nodes.new('ShaderNodeOutputMaterial');m.node_tree.links.new(e.outputs[0],out.inputs['Surface'])
    return m

bg=material('Graphite', '#090c11')
inks=[material('Function residue '+str(r),p) for r,p in enumerate(PALETTE)]
ink=material('Ivory type','#dce9eb');muted=material('Secondary type','#97b3bd')
gold=material('Exact class count','#ece0b5');cyan=material('Minimal code','#a6d6d5')
construction=material('Construction grid','#26333a')

world=bpy.data.worlds.new('Graphite field');world.use_nodes=True;s.world=world
world.node_tree.nodes['Background'].inputs['Color'].default_value=(*rgb('#090c11'),1)
world.node_tree.nodes['Background'].inputs['Strength'].default_value=1

def collection(name):
    c=bpy.data.collections.new(name);s.collection.children.link(c);return c
C0=collection('01 / 4096 actual operand tuples')
C1=collection('02 / 4096 exact equivalence assignments')
C2=collection('03 / 113 distinct complete functions')
C3=collection('04 / notation and source dimensions')
C4=collection('05 / camera and field')

def point(xy,z=0):return ((xy[0]-1200)/100,(825-xy[1])/100,z)

def diamonds(name,records,size,mat,col):
    verts=[];faces=[]
    for record in records:
        x,y,z=point(record['xy'],.05 if record.get('representative') else 0)
        r=size/100;v=len(verts)
        verts += [(x-r,y,z),(x,y-r,z),(x+r,y,z),(x,y+r,z),(x,y,z+r*.4)]
        faces += [(v,v+1,v+4),(v+1,v+2,v+4),(v+2,v+3,v+4),(v+3,v,v+4)]
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update()
    ob=bpy.data.objects.new(name,mesh);col.objects.link(ob);mesh.materials.append(mat);ob['items']=len(records)

for r in range(8):
    subset=[v for v in sources if v['residue']==r]
    dark=material('Source residue '+str(r),PALETTE[r],.40)
    diamonds('source bank '+str(r),subset,1.65,dark,C0)
    diamonds('certified representatives '+str(r),[v for v in subset if v['representative']],3.6,inks[r],C0)
    diamonds('complete-function bank '+str(r),[v for v in classes if v['residue']==r],6.2,inks[r],C2)

def paths_mesh(name,paths,mat,width,col):
    curve=bpy.data.curves.new(name,'CURVE');curve.dimensions='3D';curve.bevel_depth=width/100;curve.bevel_resolution=0
    for path in paths:
        spl=curve.splines.new('POLY');spl.points.add(len(path)-1)
        for v,xyz in zip(spl.points,path):v.co=(*xyz,1)
    ob=bpy.data.objects.new(name,curve);col.objects.link(ob);curve.materials.append(mat)
    return ob

def bezier(xy,uv,n=24):
    x,y=xy;u,v=uv;out=[]
    for j in range(n+1):
        t=j/n;a=(1-t)
        out.append(point((a**3*x+3*a*a*t*940+3*a*t*t*1125+t**3*u,
                          a**3*y+3*a*a*t*y+3*a*t*t*v+t**3*v),-.10))
    return out

for r in range(8):
    for strong in (False,True):
        edges=[e for e in routes if e['residue']==r and e['representative']==strong]
        mat=material(('Main' if strong else 'Secondary')+' incidence '+str(r),PALETTE[r],.50 if strong else .045)
        ob=paths_mesh('Exact source→class edges '+str(r)+' '+str(strong),[bezier(e['from'],e['to']) for e in edges],mat,.48 if strong else .17,C1)
        ob['edge_count']=len(edges)

guides=[]
for j in range(0,64,8):
    x=132+12*j;y=270+12*j
    guides += [[point((x,260),-.15),point((x,1036),-.15)], [point((122,y),-.15),point((898,y),-.15)]]
for r in range(8):
    x=1305+119*r;guides.append([point((x,270),-.15),point((x,1000),-.15)])
paths_mesh('Measured grid',guides,construction,.35,C3)
fontpath=Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
font=bpy.data.fonts.load(str(fontpath)) if fontpath.exists() else None

def text(body,x,y,size,mat=ink,align='LEFT'):
    cu=bpy.data.curves.new(body,'FONT');cu.body=body;cu.size=size/100;cu.align_x=align
    if font is not None:cu.font=font
    cu.materials.append(mat)
    ob=bpy.data.objects.new(body,cu);C3.objects.link(ob);ob.location=point((x,y),.25)
    bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.context.view_layer.objects.active=ob
    bpy.ops.object.convert(target='MESH');ob.select_set(False)

text('N₃(B) = 16B − 15',132,142,38)
text('B ≥ 4',2200,142,28,gold,'RIGHT')
for r in range(8):text(str(r),1305+119*r,232,22,muted,'CENTER')
text('4096',132,1132,42)
text('113',1725,1132,42,gold,'CENTER')
text('16 + 16 + 16 + 16 + 16 + 11 + 11 + 11',1725,1182,22,muted,'CENTER')
text('2¹²  →  113',132,1365,64)
text('⌈log₂ 113⌉ = 7',132,1430,32,cyan)
text('128 → 36',1340,1365,64)
text('k = 3     B = 2³²',1340,1430,27,cyan)
text('B = 8    k = 3',132,1535,23,muted)
text('lmtlssss',2200,1535,24,ink,'RIGHT')
text('10.5281/zenodo.23700193',1200,1535,19,muted,'CENTER')
# Fonts have been converted to mesh; the .blend contains no redistributed font file.
for f in list(bpy.data.fonts):
    if f.name!='Bfont' and f.users==0:bpy.data.fonts.remove(f)

bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-1))
plane=bpy.context.object;plane.name='Graphite background';plane.data.materials.append(bg)
for c in list(plane.users_collection):c.objects.unlink(plane)
C4.objects.link(plane)
bpy.ops.object.camera_add(location=(0,0,30))
cam=bpy.context.object;cam.data.type='ORTHO';cam.data.ortho_scale=24;cam.rotation_euler=(0,0,0);s.camera=cam
for c in list(cam.users_collection):c.objects.unlink(cam)
C4.objects.link(cam)
s['author']='lmtlssss🜐';s['radix']=8;s['addition_count']=3;s['operand_tuples']=4096;s['complete_functions']=113
s['meaning']='Each source tuple is assigned to its complete function under all eight incoming-carry assignments.'
s['source']='evidence/figure.json';s['edge_count']=4096
record=bpy.data.texts.new('EXACT_FUNCTION_CLASSES.json');record.write(json.dumps(data,separators=(',',':')))
blend=OUT/'cascaded-addition.blend'
bpy.ops.wm.save_as_mainfile(filepath=str(blend),compress=True)
bpy.ops.render.render(write_still=True)
assert Path(s.render.filepath).is_file()
receipt={'engine':s.render.engine,'blender':bpy.app.version_string,'source_nodes':4096,'function_nodes':113,'edges':4096,
         'size':[s.render.resolution_x,s.render.resolution_y],'image':str(s.render.filepath),'scene':str(blend)}
(OUT/'render-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('NATIVE_RENDER_COMPLETE',json.dumps(receipt))
