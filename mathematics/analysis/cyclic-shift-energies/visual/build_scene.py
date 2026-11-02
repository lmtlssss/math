#!/usr/bin/env python3
"""Native source-derived figure for the attained cyclotomic spectral gap."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from scene_common import *
states=D['states'];example=D['example'];levels=example['energy_levels']
assert len(states)==210 and example['minimum']==38 and len(levels)==20
winners=[v for v in states if v['energy']==38]
assert len(winners)==5
centers={e:(-.10,-.12,3.85-.29*i) for i,e in enumerate(levels)}
for i,row in enumerate(states):
 h=row['occupancy'];E=row['energy']
 assert len(h)==5 and sum(h)==6
 assert E==3*sum(x*x for x in h)+2*sum(h[j]*h[(j+1)%5] for j in range(5))
 rr,cc=divmod(i,15);p=(-9+.33*cc,0,3.8-.36*rr)
 mat=GOLD if E==38 else PALETTE[levels.index(E)%12]
 diamond('occupancy '+','.join(map(str,h)),N,p,.055 if E==38 else .029,mat,{'occupancy':h,'energy':E})
 q=centers[E]
 curve('occupancy %d to energy %d'%(i,E),R,[p,(-2.7,.20,.48*p[2]+.52*q[2]),q],mat,.006 if E==38 else .0018)
 if cc<14:curve('grid-row-'+str(i),N,[p,(p[0]+.33,0,p[2])],DIM,.002,False)
 if rr<13:curve('grid-col-'+str(i),N,[p,(p[0],0,p[2]-.36)],DIM,.002,False)
for j,E in enumerate(levels):
 mat=GOLD if E==38 else PALETTE[j%12]
 bar('exact energy '+str(E),B,centers[E],mat,w=.52,h=.095,props={'energy':E,'state_count':sum(v['energy']==E for v in states)})
 text(str(E),.34,centers[E][2]-.065,.17,mat)
for j,row in enumerate(winners):
 q=(6.25,-.10,3.25-.93*j)
 diamond('minimizer '+str(j),O,q,.13,GOLD,{'occupancy':row['occupancy'],'energy':38})
 curve('minimum to witness '+str(j),R,[centers[38],(3.2,-.12,.45*centers[38][2]+.55*q[2]),q],GOLD,.009)
 text('('+','.join(map(str,row['occupancy']))+')',6.62,q[2]-.065,.22,INK)
text('E = 3Σ hᵢ² + 2Σ hᵢhᵢ₊₁',-9,5.15,.31)
text('E ≥ 38',5.75,5.15,.42,GOLD)
text('210',-7.3,4.4,.33);text('20',-.27,4.4,.33);text('5',6.12,4.15,.33,GOLD)
text('210  →  5',-.80,-4.25,.72)
text('exact integer minimizers',-.76,-4.95,.23,CYAN)
text('p = 5    N = 6',-8.7,-4.85,.28)
text('Γ = 2√5 / 5',5.30,-4.35,.32,GOLD)
text('36 + 4λ_* / 5 + Γ = 38',3.75,-5.05,.23)
# A true five-cycle encodes the off-diagonal terms of K.
import math
cycle=[(-7.4+.65*math.cos(2*math.pi*j/5),0,-3.4+.65*math.sin(2*math.pi*j/5)) for j in range(5)]
for j,p in enumerate(cycle):
 diamond('cycle vertex '+str(j),B,p,.06,CYAN)
 curve('cycle edge '+str(j),B,[p,cycle[(j+1)%5]],GRID,.008,False)
finish('cyclic-shift-energies','All 210 integer occupancies of six units on a five-cycle; twenty exact energy values and five witnesses attaining the cyclotomic bound 38.')
