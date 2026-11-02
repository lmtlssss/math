#!/usr/bin/env python3
"""Reproduce the exact new theorem certificates and source-derived figure data."""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import json, math, hashlib
W=Path(__file__).resolve().parent / "evidence"
W.mkdir(exist_ok=True)

def ceil(x):return -((-x.numerator)//x.denominator)

def chosen(D,theta,step):
 vals=[]
 for name,L,U,alpha in D:
  k=max(0,ceil((L-theta)/step));a=theta+step*k
  if a>0 and a<=U:vals.append((alpha*a,name,k,a))
 if not vals:return []
 m=min(x[0] for x in vals);return [x for x in vals if x[0]==m]

def phase_diagram(D,step):
 bounds={F(0),step}
 for _,L,U,_ in D:
  bounds.add(L%step);bounds.add(U%step)
 bounds=sorted(bounds)
 segments=[]
 for left,right in zip(bounds,bounds[1:]):
  mid=(left+right)/2;active=[]
  for name,L,U,a in D:
   k=max(0,ceil((L-mid)/step));amp=mid+step*k
   if 0<amp<=U:active.append((name,a,k))
  candidates=[]
  for name,a,k in active:
   lo,hi=left,right
   for other,b,j in active:
    slope=a-b;constant=step*(b*j-a*k)
    if slope==0:
     if constant<0:lo=hi=left;break
    elif slope>0:hi=min(hi,constant/slope)
    else:lo=max(lo,constant/slope)
   if lo<hi:candidates.append({'left':lo,'right':hi,'design':name,'k':k,'alpha':a})
  segments.extend(candidates)
  for c in candidates:
   for t in ((2*c['left']+c['right'])/3,(c['left']+2*c['right'])/3):
    assert c['design'] in [x[1] for x in chosen(D,t,step)]
 # Boundary points always checked literally, retaining all ties.
 points=[{'theta':t,'winners':[(v[1],v[2],v[3]) for v in chosen(D,t,step)]} for t in bounds[:-1]]
 return bounds,segments,points

def amplitude():
 D=[('A',F(1),F(3,2),F(1)),('B',F(21,20),F(7,5),F(19,20)),('C',F(5,4),F(8,5),F(4,5)),('D',F(11,10),F(23,20),F(9,10))]
 step=F(1,5);bd,seg,pts=phase_diagram(D,step)
 phase_checks=0
 for j in range(1,2000):
  t=step*F(j,2000)
  if t in bd or any(t==s['left'] or t==s['right'] for s in seg):continue
  expected={x[1] for x in chosen(D,t,step)}
  observed={s['design'] for s in seg if s['left']<t<s['right']}
  assert observed==expected,(t,observed,expected)
  phase_checks+=1
 tests=0
 for q in [F(3,2),F(5,3),F(7,4)]:
  for n in range(1,101):
   # exact-alignment sequences demonstrate persistent reversals, avoid common alignments
   t=F(n);d=1/t
   if (q*t).denominator!=1:
    assert d*ceil(1/d)<d/q*ceil(q/d);tests+=1
   t=F(n)/q;d=1/t
   if t.denominator!=1:
    assert d/q*ceil(q/d)<d*ceil(1/d);tests+=1
 def serial(v):
  if isinstance(v,F):return str(v)
  if isinstance(v,dict):return {k:serial(x) for k,x in v.items()}
  if isinstance(v,(list,tuple)):return [serial(x) for x in v]
  return v
 out=serial({'status':'PASS','designs':D,'spacing':step,'breakpoints':bd,'winner_segments':seg,'boundary_winners':pts,'independent_origin_comparisons':phase_checks,'persistent_reversal_checks':tests})
 (W/'discovery.json').write_text(json.dumps(out,indent=2))
 print('AMPLITUDE',out)

 data=json.loads((W/'discovery.json').read_text())
 step=F(data['spacing'])
 allpoints=set(F(x) for x in data['breakpoints'])
 for seg in data['winner_segments']:
  allpoints.add(F(seg['left']));allpoints.add(F(seg['right']))
 data['all_boundary_winners']=[{'theta':str(t),'winners':[x[1] for x in chosen(D,t,step)]} for t in sorted(allpoints) if t<step]
 prob={x[0]:F(0) for x in D};expect=F(0)
 for seg in data['winner_segments']:
  l,r=F(seg['left']),F(seg['right']);a=F(seg['alpha']);k=seg['k']
  prob[seg['design']]+=(r-l)/step
  expect+=a*a*((r+k*step)**3-(l+k*step)**3)/(3*step)
 assert list(prob.values())==[F(1,4),F(1,12),F(5,12),F(1,4)]
 data['selection_probabilities']={k:str(v) for k,v in prob.items()}
 data['expected_optimum_quadratic_cost']=str(expect)
 brute_checks=0
 for j in range(400):
  theta=step*F(j,400)
  costs=[]
  for name,L,U,alpha in D:
   for k in range(0,20):
    a=theta+k*step
    if L<=a<=U:costs.append((alpha*a,name))
  best=min(v for v,_ in costs)
  assert {name for v,name in costs if v==best}=={x[1] for x in chosen(D,theta,step)}
  brute_checks+=1
 data['independent_grid_enumeration_cases']=brute_checks
 (W/'discovery.json').write_text(json.dumps(data,indent=2)+'\n')
 sample=[]
 for j in range(120):
  theta=step*F(2*j+1,240)
  owner=next(i for i,s in enumerate(data['winner_segments']) if F(s['left'])<theta<F(s['right']))
  sample.append({'theta':str(theta),'interval':owner,'winner':data['winner_segments'][owner]['design']})
 data['phase_representatives']=sample
 (W/'figure.json').write_text(json.dumps(data,indent=2)+'\n')
 print('EXACT_PHASE_SELECTION_LAW',data['selection_probabilities'],'EXPECTED_COST',expect)


if __name__=="__main__":
 amplitude()
