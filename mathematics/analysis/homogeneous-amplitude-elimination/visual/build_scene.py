#!/usr/bin/env python3
"""Exact rational amplitude grid and design-order reversal."""
import sys
from pathlib import Path
from fractions import Fraction as F
sys.path.insert(0,str(Path(__file__).resolve().parent))
from scene_common import *
assert len(D['designs'])==12 and len(D['grid'])==16
centers=[]
for i,d in enumerate(D['designs']):
 z=3.55-.48*i;center=(-.3,-.10,z);centers.append(center);mat=PALETTE[i]
 bar('design '+d['name'],B,center,mat,props={'name':d['name'],'least_grid_amplitude':d['a_grid'],'grid_value':d['grid_value']})
 text(d['name'],.15,z-.06,.2,mat)
 minimum=F(d['a_continuous']);chosen=F(d['a_grid']);m=F(d['m']);upper=F(2 if i<3 else 3)
 for j,av in enumerate(D['grid']):
  a=F(av);p=(-9.05+.25*j,0,z);feasible=a>=minimum and a*m<=upper;selected=a==chosen
  diamond('design %s amplitude %s'%(d['name'],av),N,p,.06 if selected else .026,mat if feasible else DIM,{'amplitude':av,'feasible':feasible,'selected':selected})
  if feasible:
   curve('feasible grid %s %s'%(d['name'],av),R,[p,(-2.8,.2,z+.12*(j%3-1)),center],mat if selected else DIM,.008 if selected else .0023,True)
  if j<15:curve('grid row %d %d'%(i,j),N,[p,(p[0]+.25,0,z)],GRID,.002,False)
# Two exact orderings of the same twelve designs.
for name,winner,z,label,value in [('continuous','C',2.45,'a > 0','15/16'),('grid','A',-.65,'a ∈ (1/10)ℤ','1')]:
 q=(6.4,0,z);idx=next(i for i,v in enumerate(D['designs']) if v['name']==winner)
 p=centers[idx];mat=GOLD if name=='grid' else CYAN
 curve(name+' minimizer',R,[p,(3.5,-.15,.4*p[2]+.6*z),q],mat,.018,True)
 diamond(name+' exact optimum',O,q,.19,mat,{'design':winner,'value':value})
 text(label,6.8 if name=='grid' else 4.8,z+.65 if name=='grid' else z+.78,.24,mat);text(winner,6.8,z-.12,.45,mat);text('J = '+value,5.1,z-.66,.27)
text('min a^ν e(p)   subject to  L(p) ≤ a ≤ U(p)',-9.05,5.15,.28)
text('a_Δ = Δ⌈L/Δ⌉',2.0,4.48,.27,GOLD)
text('12 × 16',-8.2,4.25,.34);text('12',-.49,4.25,.36,GOLD)
text('192  →  12',-.95,-4.15,.67)
text('exact scalar elimination',-.8,-4.72,.22,CYAN)
text('continuous : C',-8.8,-4.2,.25,CYAN);text('grid : A',-8.8,-4.68,.25,GOLD)
text('C : 15/16  →  507/500',-8.8,-5.28,.23)
text('a₀ = 0    Δ = 1/10',4.4,-4.5,.3,GOLD)
finish('homogeneous-amplitude-elimination','Every point is a rational design/amplitude pair. The least feasible amplitude is selected for each design; exact global minimizers differ between continuous and grid problems.')
