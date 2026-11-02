#!/usr/bin/env python3
"""Exact shortest uniform peak certificate and invariant observation hexagon."""
import sys,math
from pathlib import Path
from fractions import Fraction as F
sys.path.insert(0,str(Path(__file__).resolve().parent))
from scene_common import *
assert D['example']['minimal_uniform_horizon']==3 and D['exact_peak']=='6/5'
states=D['states'];points=[]
for row in states:
 u,v=F(row['u']),F(row['v']);points.append((-6.5+.60*float(u),0,.8+.60*float(v)))
for j,p in enumerate(points):
 diamond('state '+str(j),N,p,.07 if j<3 else .025,PALETTE[j%12] if j<3 else DIM,{'n':j,'u':states[j]['u'],'v':states[j]['v']})
 if j:curve('trajectory '+str(j),R,[points[j-1],p],GRID,.007,False)
for rad in (.8,1.7,3.0):
 pts=[(-6.5+rad*math.cos(2*math.pi*j/100),.15,.8+rad*math.sin(2*math.pi*j/100)) for j in range(101)]
 curve('radius '+str(rad),N,pts,DIM,.003,False)
curve('state axis x',N,[(-9.7,0,.8),(-3.3,0,.8)],GRID,.004,False)
curve('state axis y',N,[(-6.5,0,-2.4),(-6.5,0,4)],GRID,.004,False)
for j in range(3):
 q=(.25,-.10,3.1-1.3*j);p=points[j];mat=GOLD if j==2 else PALETTE[j]
 curve('sample '+str(j),R,[p,(-2.2,.0,.45*p[2]+.55*q[2]),q],mat,.009)
 bar('retained sample '+str(j),B,q,mat,w=.65,h=.16,props={'n':j,'value':states[j]['u']})
 text(states[j]['u'],.75,q[2]-.07,.25,mat)
 dest=(6.6,-.1,1.65)
 curve('retained peak '+str(j),R,[q,(3.6,-.1,.4*q[2]+.6*dest[2]),dest],mat,.01 if j==2 else .006)
 text(str(j),p[0]-.28,p[2]-.07,.20)
diamond('certified infinite peak',O,dest,.16,GOLD,{'peak':'6/5','uniform_horizon':3})
text('xₙ₊₂ = (6/5)xₙ₊₁ − (2/5)xₙ',-9,5.15,.29)
text('N_min = 3',5.10,4.55,.40,GOLD)
text('sup |xₙ| = 6/5',4.35,2.65,.34,GOLD)
text('all initial states : 3 samples',3.3,-.4,.25,CYAN)
text('x₃ = (13/15)x₂ − (2/15)x₀',2.65,-1.1,.25)
text('∞  →  3',-.9,-4.1,.75)
text('shortest uniform peak horizon',-1.8,-4.90,.24,CYAN)
# H3 in the initial-coordinate plane; v3 is on its exposed facet.
hull=[(F(a),F(b)) for a,b in D['rational_hull_points']]
hpts=[(-6.5+.75*float(x),0,-3.8+.75*float(y)) for x,y in hull]
for j,p in enumerate(hpts):
 diamond('observation hull vertex '+str(j),B,p,.055,CYAN)
 curve('observation hull edge '+str(j),B,[p,hpts[(j+1)%len(hpts)]],GRID,.009,False)
v3=(-6.5+.75*float(F(-12,25)),0,-3.8+.75*float(F(26,25)))
diamond('first redundant row',B,v3,.07,GOLD)
text('v₃ ∈ conv{±v₀, ±v₁, ±v₂}',-9,-5.25,.21)
text('Σ xₙ² = 175/39',4.75,-4.1,.27)
text('x₀ = 0    x₁ = 1',4.75,-4.8,.23)
finish('damped-recurrence-certificates','Three observed values determine the infinite peak for every initial state; an exact invariant hexagon certifies the uniform horizon and a separate witness proves minimality.')
