#!/usr/bin/env python3
"""A source-derived recurrence orbit and its four-sample infinite peak certificate."""
import sys
from pathlib import Path
from fractions import Fraction as F
sys.path.insert(0,str(Path(__file__).resolve().parent))
from scene_common import *
a,b=F(D['a']),F(D['b']);assert D['instance_prefix']==4 and D['peak']=='6/5'
u,v=F(0),F(5);states=[]
for i in range(28):
 states.append((u,v));u,v=a*u+b*v,-b*u+a*v
assert [str(x[0]) for x in states]==D['sample_values']
# The planar state orbit uses the recurrence's exact real coordinates.
positions=[(-6.5+.54*float(x),0,1.0+.54*float(y)) for x,y in states]
for i,p in enumerate(positions):
 mat=PALETTE[i%4] if i<4 else DIM
 diamond('exact state '+str(i),N,p,.09 if i<4 else .028,mat,{'n':i,'state':[str(x) for x in states[i]]})
 if i:curve('recurrence step '+str(i),N,[positions[i-1],p],mat,.012 if i<4 else .005,False)
 if i<4:text(str(i),p[0]-.28,p[2]+.1,.19,mat)
# Initial state-radius circle; the smaller rings are exact geometric envelopes.
for n in (0,2,4,8):
 radius=.54*5*((2/5)**(n/2));pts=[(-6.5+radius*math.cos(2*math.pi*j/96),.15,1.0+radius*math.sin(2*math.pi*j/96)) for j in range(97)]
 curve('radius envelope '+str(n),N,pts,GRID,.003,False)
curve('state x-axis',N,[(-9.4,.1,1),(-3.55,.1,1)],GRID,.004,False)
curve('state y-axis',N,[(-6.5,.1,-1.9),(-6.5,.1,4.0)],GRID,.004,False)
centers=[]
for i,ss in enumerate(D['sample_values'][:4]):
 q=(.1,-.1,3.4-1.35*i);centers.append(q);mat=PALETTE[i]
 bar('certified sample '+str(i),B,q,mat,w=.65,h=.16,props={'n':i,'exact_value':ss})
 p=positions[i];curve('state to observed sample '+str(i),R,[p,(-2.1,.2,.45*p[2]+.55*q[2]),q],mat,.008,True)
 text(ss,.6,q[2]-.1,.27,mat)
 peak=(6.8,0,1.15)
 curve('sample to certified maximum '+str(i),R,[q,(3.8,-.1,.5*q[2]+.5*peak[2]),peak],GOLD if i==2 else mat,.014 if i==2 else .005,True)
diamond('infinite absolute maximum',O,(6.8,0,1.15),.19,GOLD,{'maximum':'6/5','first_index':2})
text('sup |x_n| = 6/5',4.15,2.65,.40,GOLD);text('n ≥ 0',5.1,3.22,.2)
text('tail: |x_n| ≤ 4/5',3.8,-1.38,.29,CYAN);text('n ≥ 4',5.0,-1.88,.2)
text('Σ x_n² = 175/39',4.0,-3.12,.3)
text('x_(n+2) = (6/5)x_(n+1) − (2/5)x_n',-9.0,5.1,.29)
text('c² = 1/65',5.4,4.4,.36,GOLD)
text('∞  →  4',-.8,-4.5,.80)
text('rational samples + exact tail certificate',-1.75,-5.15,.22,CYAN)
text('r² = 2/5',-8.9,-3.0,.29);text('x₀ = 0    x₁ = 1',-8.9,-3.55,.26)
finish('damped-recurrence-certificates','Exact rational states and first four scalar observations, with the proved infinite geometric tail bound. The maximum and infinite square sum are exact fractions.')
