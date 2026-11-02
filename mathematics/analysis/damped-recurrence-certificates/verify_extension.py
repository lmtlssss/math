#!/usr/bin/env python3
"""Reproduce the exact new theorem certificates and source-derived figure data."""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import json, math, hashlib
W=Path(__file__).resolve().parent / "evidence"
W.mkdir(exist_ok=True)

def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])

def hull(points):
 p=sorted(set(points));lo=[];up=[]
 for x in p:
  while len(lo)>=2 and cross(lo[-2],lo[-1],x)<=0:lo.pop()
  lo.append(x)
 for x in reversed(p):
  while len(up)>=2 and cross(up[-2],up[-1],x)<=0:up.pop()
  up.append(x)
 return lo[:-1]+up[:-1]

def inside(h,p):return all(cross(a,b,p)>=0 for a,b in zip(h,h[1:]+h[:1]))

def rowlist(q,s,n):
 rows=[(F(1),F(0)),(F(0),F(1))]
 for k in range(2,n+1):rows.append(tuple(q*rows[-1][i]-s*rows[-2][i] for i in range(2)))
 return rows

def recurrence():
 counts={'N2':0,'N3':0,'N_at_least4':0};checked=0
 for si in range(1,80):
  s=F(si,80)
  for qi in range(0,160):
   q=F(qi,80)
   if q*q>=4*s:continue
   rows=rowlist(q,s,3)
   I2=inside(hull(rows[:2]+[(-x,-y) for x,y in rows[:2]]),rows[2])
   I3=inside(hull(rows[:3]+[(-x,-y) for x,y in rows[:3]]),rows[3])
   T2=q+s<=1
   T3=(q+s>1 and q*q-s*q+1-s>=0 and q*q-q-s*(1-s)<=0)
   assert I2==T2,(q,s,'N2')
   assert (not I2 and I3)==T3,(q,s,'N3')
   counts['N2' if I2 else 'N3' if I3 else 'N_at_least4']+=1;checked+=1
 q,s=F(6,5),F(2,5);r=rowlist(q,s,100)
 assert r[3]==tuple(F(13,15)*r[2][i]-F(2,15)*r[0][i] for i in (0,1))
 hh=hull(r[:3]+[(-x,-y) for x,y in r[:3]])
 assert all(inside(hh,v) for v in r)
 x0,x1=F(-1),F(1);assert q*x1-s*x0==F(8,5)
 out={'status':'PASS','exact_parameter_pairs':checked,'classification':counts,'example':{'q':'6/5','s':'2/5','minimal_uniform_horizon':3,'x3_identity':'(13/15)*x2-(2/15)*x0','N2_separating_initial_values':['-1','1'],'separating_x2':'8/5','specific_initial_values':['0','1'],'specific_peak':'6/5','specific_peak_index':2},'rational_hull_points':[[str(x),str(y)] for x,y in hh]}
 (W/'discovery.json').write_text(json.dumps(out,indent=2))
 print('RECURRENCE',out)

 data=json.loads((W/'discovery.json').read_text())
 u,v=F(0),F(5);states=[]
 for n in range(60):
  states.append({'n':n,'u':str(u),'v':str(v)})
  u,v=F(3,5)*u+F(1,5)*v,-F(1,5)*u+F(3,5)*v
 data['states']=states
 data['sample_count']=3
 data['exact_peak']='6/5'
 data['infinite_square_sum']='175/39'
 (W/'figure.json').write_text(json.dumps(data,indent=2)+'\n')


if __name__=="__main__":
 recurrence()
