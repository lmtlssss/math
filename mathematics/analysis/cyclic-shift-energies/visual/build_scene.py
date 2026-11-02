#!/usr/bin/env python3
"""Exact incidence of 64 translated profiles, sixteen occupancies and sixteen outputs."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from scene_common import *
assert D['P']==16 and D['N']==64 and D['occupancy']==[4]*16 and D['aggregate']==[12]*16
centers=[(-.65,-.1,3.65-.43*k) for k in range(16)]
outputs=[(7.0,0,3.65-.43*k) for k in range(16)]
for i,d in enumerate(D['shifts']):
 row,col=divmod(i,8);p=(-8.8+.40*col,0,3.55-.40*row);mat=PALETTE[d%12]
 diamond('copy '+str(i),N,p,.05,mat,{'copy':i,'shift':d})
 q=centers[d];curve('copy %d → occupancy %d'%(i,d),R,[p,(-3.8,.18,.5*p[2]+.5*q[2]),q],mat,.004,True,{'shift':d})
 if col<7:curve('source-row '+str(i),N,[p,(p[0]+.4,0,p[2])],GRID,.003,False)
 if row<7:curve('source-col '+str(i),N,[p,(p[0],0,p[2]-.4)],GRID,.003,False)
for d,p in enumerate(centers):
 mat=PALETTE[d%12];bar('occupancy '+str(d),B,p,mat,props={'shift':d,'copies':4})
 text(str(d),-1.18,p[2]-.07,.15,mat)
 for off,w in enumerate(D['profile']):
  if not w:continue
  j=(d+off)%16;q=outputs[j]
  curve('shift %d contributes %d to sample %d'%(d,4*w,j),R,[p,(3.6,.1,.55*p[2]+.45*q[2]),q],mat,.004+w*.002,True,{'source_shift':d,'output_position':j,'coefficient':4*w})
for j,q in enumerate(outputs):
 diamond('aggregate sample '+str(j),O,q,.095,PALETTE[j%12],{'value':12,'position':j});text('12',7.35,q[2]-.07,.18)
# Exact integer aggregate values, shown as two small independent coordinate plots.
for label,values,x0 in [('aligned',[128,64]+[0]*14,-8.8),('balanced',[12]*16,-5.8)]:
 pts=[(x0+.15*i,0,-3.95+.0125*v) for i,v in enumerate(values)]
 curve(label+' exact samples',N,pts,GOLD if label=='aligned' else CYAN,.012,False)
 for i,p in enumerate(pts):diamond(label+' sample '+str(i),N,p,.022,GOLD if label=='aligned' else CYAN)
 text(label,x0,-4.35,.19)
text('E(d) = ‖ Σ T_d p ‖²',-9.0,5.2,.31)
text('q_min = 16',4.65,5.2,.39,GOLD)
text('64',-7.7,4.2,.36);text('16',-.84,4.2,.36,GOLD);text('16',6.85,4.2,.32)
text('20 480  →  2 304',-.6,-4.8,.56)
text('exact quadratic energy',.15,-5.3,.2,CYAN)
text('65 536  →  32',3.8,-5.85,.35,GOLD)
text('pair-kernel entries → retained arrays',3.2,-6.18,.16)
finish('cyclic-shift-energies','64 actual profiles, exact shift occupancy and coefficient-labelled output relations; energy values evaluated from the certified integer aggregate.')
