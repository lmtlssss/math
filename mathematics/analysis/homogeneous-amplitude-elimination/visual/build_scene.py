#!/usr/bin/env python3
"""Exact common-lattice phase partition and its rational selection measure."""
import sys
from pathlib import Path
from fractions import Fraction as F
sys.path.insert(0,str(Path(__file__).resolve().parent))
from scene_common import *
segments=D['winner_segments'];samples=D['phase_representatives'];probs=D['selection_probabilities']
assert len(samples)==120 and len(segments)==5 and probs=={'A':'1/4','B':'1/12','C':'5/12','D':'1/4'}
M={name:PALETTE[i] for i,name in enumerate(('A','B','C','D'))}
centers=[(0,-.1,3.2-1.05*i) for i in range(5)]
for j,row in enumerate(samples):
 rr,cc=divmod(j,12);p=(-9+.32*cc,0,3.6-.43*rr);r=row['interval'];owner=row['winner'];q=centers[r]
 assert F(segments[r]['left'])<F(row['theta'])<F(segments[r]['right']) and segments[r]['design']==owner
 diamond('phase '+row['theta'],N,p,.035,M[owner],{'phase':row['theta'],'winner':owner,'interval':r})
 curve('phase class '+str(j),R,[p,(-2.9,.10,.42*p[2]+.58*q[2]),q],M[owner],.0028)
 if cc<11:curve('phase grid h'+str(j),N,[p,(p[0]+.32,0,p[2])],DIM,.002,False)
 if rr<9:curve('phase grid v'+str(j),N,[p,(p[0],0,p[2]-.43)],DIM,.002,False)
for j,seg in enumerate(segments):
 q=centers[j];mat=M[seg['design']]
 bar('winner interval '+str(j),B,q,mat,w=.55,h=.13,props={'left':seg['left'],'right':seg['right'],'winner':seg['design']})
 text('('+seg['left']+', '+seg['right']+')',.44,q[2]-.07,.20,mat)
for j,name in enumerate(('A','B','C','D')):
 q=(6.05,-.1,3.1-1.25*j);mat=M[name]
 diamond('selection probability '+name,O,q,.15,mat,{'probability':probs[name]})
 text(name,6.40,q[2]-.06,.27,mat);text(probs[name],7.0,q[2]-.06,.27)
 for i,seg in enumerate(segments):
  if seg['design']==name:curve('interval '+str(i)+' selects '+name,R,[centers[i],(3.25,-.12,.4*centers[i][2]+.6*q[2]),q],mat,.008)
text('aᵢ(θ) = θ + Δ⌈(Lᵢ−θ)/Δ⌉',-9,5.15,.29)
text('Pr = (1/4, 1/12, 5/12, 1/4)',2.2,5.15,.31,GOLD)
text('120',-7.1,4.36,.33);text('5',-.1,4.20,.33);text('4',5.96,4.18,.33,GOLD)
text('120  →  5  →  4',-2.25,-4.18,.65)
text('exact phase intervals and selection measure',-2.75,-4.94,.22,CYAN)
# Interval lengths, not representative counts, determine the probabilities.
for j,seg in enumerate(segments):
 lo=-8.7+4.0*float(F(seg['left'])/F(D['spacing']));hi=-8.7+4.0*float(F(seg['right'])/F(D['spacing']))
 curve('exact phase length '+str(j),B,[(lo,0,-3.35),(hi,0,-3.35)],M[seg['design']],.025,False)
 diamond('phase boundary '+str(j),B,(lo,0,-3.35),.065,M[seg['design']])
text('θ ∈ [0, 1/5)',-8.65,-4.15,.25)
text('continuous minimum : D',4.35,-3.45,.24,GOLD)
text('phase measure : C = 5/12',4.35,-4.05,.24,CYAN)
text('Δ = 1/5',4.35,-4.75,.27)
finish('homogeneous-amplitude-elimination','120 exact phase representatives route through five rational intervals to four exact probability outputs; probabilities are derived from interval lengths.')
