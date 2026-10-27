#!/usr/bin/env python3
"""Vector layout preview. This is NOT the native Blender render."""
from pathlib import Path
from html import escape
from geometry import geometry,PALETTE

ROOT=Path(__file__).resolve().parents[1]
data,source,functions,routes=geometry(ROOT/'evidence/figure.json')
W,H=2400,1650
s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
   '<rect width="2400" height="1650" fill="#090c11"/>']
def line(x1,y1,x2,y2,color='#47606a',width=1,opacity=1):
    s.append(f'<path d="M{x1},{y1}L{x2},{y2}" fill="none" stroke="{color}" stroke-width="{width}" opacity="{opacity}"/>')
def text(body,x,y,size=25,color='#dce9eb',anchor='start'):
    s.append(f'<text x="{x}" y="{y}" font-family="DejaVu Sans,sans-serif" font-size="{size}" fill="{color}" text-anchor="{anchor}">{escape(body)}</text>')
def diamond(x,y,size,color,opacity=1):
    s.append(f'<path d="M{x},{y-size}L{x+size},{y}L{x},{y+size}L{x-size},{y}Z" fill="{color}" opacity="{opacity}"/>')
text('N₃(B) = 16B − 15',132,142,38)
text('B ≥ 4',2200,142,28,'#d9d2aa','end')
# Actual sources. Grid coordinates encode the four radix-eight operands.
for j in range(0,64,8):
    x=132+12*j;y=270+12*j
    line(x,260,x,1036,width=.7,opacity=.32)
    line(122,y,898,y,width=.7,opacity=.32)
for p in source:diamond(*p['xy'],1.65,PALETTE[p['residue']],.45)
# Every source-to-function edge is present; only exact representatives receive emphasis.
for edge in routes:
    x,y=edge['from'];u,v=edge['to'];bright=edge['representative']
    d=f'M{x},{y} C {940},{y} {1125},{v} {u},{v}'
    s.append(f'<path d="{d}" fill="none" stroke="{PALETTE[edge["residue"]]}" stroke-width="{.9 if bright else .35}" opacity="{.46 if bright else .018}"/>')
for p in source:
    if p['representative']:diamond(*p['xy'],3.6,PALETTE[p['residue']],.95)
for r in range(8):
    x=1305+119*r
    text(str(r),x,232,22,'#9ab5bd','middle')
    line(x,270,x,1000,width=.65,opacity=.5)
for f in functions:diamond(*f['xy'],6.2,PALETTE[f['residue']])
text('4096',132,1132,42)
text('113',1725,1132,42,'#ece0b5','middle')
text('16 + 16 + 16 + 16 + 16 + 11 + 11 + 11',1725,1182,22,'#97b3bd','middle')
text('2¹²  →  113',132,1365,64)
text('⌈log₂ 113⌉ = 7',132,1430,32,'#a6d6d5')
text('128 → 36',1340,1365,64)
text('k = 3     B = 2³²',1340,1430,27,'#a6d6d5')
text('B = 8    k = 3',132,1535,23,'#829ba7')
text('lmtlssss',2200,1535,24,'#c6d4db','end')
s.append('</svg>')
out=ROOT/'visual/layout-preview.svg';out.write_text('\n'.join(s))
try:
    import cairosvg
    cairosvg.svg2png(url=str(out),write_to=str(ROOT/'visual/layout-preview.png'))
except ImportError:pass
print('VECTOR_PREVIEW',out,'source tuples',len(source),'function classes',len(functions),'exact routes',len(routes))
