#!/usr/bin/env python3
"""Build the exact affine-cycle fibres in the author's canonical Blender scene.

Start Blender with the unmodified tensor-note-v1.0.0 .blend as input.
Every visible state, route, class and defect vector comes from figure.json.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from scene_common import *

states=D['states'];example=D['example'];levels=example['levels']
assert len(states)==343 and len(levels)==7
assert example['defect_rank']==1 and example['total_rank']==2
assert example['prefix_rank']==2 and example['cut_invariant_count']==49
assert example['R']==[[1,1,0],[2,2,1],[3,3,-1]]
assert example['K']==[[1,0,0],[2,0,0],[3,0,0]]

centres={r['t']:(-.30,-.12,3.80-.59*j) for j,r in enumerate(levels)}
positions={};colours={}
for j,level in enumerate(levels):
    t=level['t'];colours[t]=GOLD if t==0 else PALETTE[j%12]
    assert level['defects']==[t,2*t,3*t] and level['multiplicity']==49

# The complete 7 x 7 x 7 input lattice: x is vertical, y horizontal,
# z is depth. The x=-1 cut-invariant fibre is an actual 49-point plane.
for row in states:
    x,y,z=row['state'];t=row['t'];defects=row['defects']
    assert t==x+1 and defects==[t,2*t,3*t]
    assert row['cut_invariant']==(x==-1)
    assert row['cost']==4*x+5*y+2*z+1
    p=(-9+.48*(y+3),.42*(z+3),3.80-.52*(x+3))
    positions[x,y,z]=p;mat=colours[t]
    diamond('state (%d,%d,%d)'%(x,y,z),N,p,.047 if t==0 else .026,mat,
            {'state':row['state'],'summary_x':x,'t':t,'defects':defects,
             'cut_invariant':row['cut_invariant'],'cost':row['cost']})
    target=centres[t]
    curve('state (%d,%d,%d) to t=%d'%(x,y,z,t),R,
          [p,(-3.50,-.30,.50*p[2]+.50*target[2]),target],mat,
          .0045 if t==0 else .0017,
          props={'initial_state':row['state'],'t':t})

# Coordinate edges mark the true lattice adjacency.
for (x,y,z),p in positions.items():
    for axis,neighbour in [('x',(x+1,y,z)),('y',(x,y+1,z)),('z',(x,y,z+1))]:
        if neighbour in positions:
            curve('lattice %s %s'%(axis,(x,y,z)),N,[p,positions[neighbour]],DIM,.0016,False)

# Outline the exact zero-defect plane inside the source lattice.
plane=[positions[-1,-3,-3],positions[-1,3,-3],positions[-1,3,3],positions[-1,-3,3]]
for j in range(4):
    curve('zero-defect plane boundary '+str(j),B,[plane[j],plane[(j+1)%4]],GOLD,.010,False,
          props={'equation':'x=-1','grid_states':49})

# Seven affine scalar values and their seven exact output triples.
for j,level in enumerate(levels):
    t=level['t'];mat=colours[t];p=centres[t]
    bar('retained value t=%d'%t,B,p,mat,w=.56,h=.12,
        props={'linear_summary_x':level['summary'],'known_offset':1,'t':t,'fibre_cardinality':49})
    text(str(t),.15,p[2]-.075,.23,mat)
    dest=(5.35,-.12,p[2])
    diamond('defect vector '+str(level['defects']),O,dest,.095 if t else .14,mat,
            {'defect_vector':level['defects'],'t':t,'fibre_cardinality':49})
    curve('t=%d to exact defect vector'%t,R,[p,(2.75,-.30,p[2]),dest],mat,.009)
    text('('+', '.join(str(v) for v in level['defects'])+')',5.73,p[2]-.075,.25,INK if t else GOLD)

text('D = R((M − I)x + b)',-9,5.18,.34)
text('q_defect = 1',4.90,5.18,.38,GOLD)
text('343 states',-8.80,4.38,.29)
text('t = x + 1',-.80,4.38,.29)
text('7 defect vectors',5.10,4.38,.29)
text('49 states per fibre',-8.65,-.42,.25,CYAN)
text('7 exact scalar values',-1.30,-.42,.24,CYAN)

text('R =',-9,-1.55,.27)
for j,row in enumerate(example['R']):
    text('('+', '.join(str(v) for v in row)+')',-8.15,-1.55-.36*j,.24)
text('rank R = 2',-5.94,-1.88,.25,CYAN)
text('rank R(M − I) = 1',-1.25,-1.88,.27,GOLD)
text('D = (x+1)(1,2,3)',4.35,-1.88,.28)

text('3  →  1',-.90,-3.33,.72)
text('minimum linear defect state',-1.70,-3.92,.23,CYAN)
text('q_total = 2',-.50,-4.62,.28)
text('F(x,y,z) = (2x,y+1,z)',-9,-3.60,.26)
text('49 cut-invariant states',4.57,-3.32,.28,GOLD)
text('x = −1',5.95,-4.03,.46,GOLD)
text('δ = (−1,1,0)',5.33,-4.67,.28)
text('zero cost defect; nonzero state displacement',-8.95,-5.45,.235,INK)

finish('affine-cycles',
       'The complete 343-state rational grid of the four-step affine cycle. '
       'Seven scalar values determine seven exact cut-defect vectors, each with 49 preimages. '
       'The 49 gold states lie on x=-1, have zero cut defect and nonzero displacement (-1,1,0). '
       'The minimum linear dimension is one for defects and two for all transported cut totals.')
