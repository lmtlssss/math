#!/usr/bin/env python3
"""Reproduce the exact new theorem certificates and source-derived figure data."""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import json, math, hashlib
import sympy as sp
W=Path(__file__).resolve().parent / "evidence"
W.mkdir(exist_ok=True)

def compositions(n,p,prefix=()):
 if p==1:yield prefix+(n,);return
 for i in range(n+1):yield from compositions(n-i,p-1,prefix+(i,))

def cyclic():
 X=sp.Symbol('X');checks=0;minnorm=None
 for p in (3,5,7):
  phi=sp.cyclotomic_poly(p,X)
  for bits in product((0,1),repeat=p):
   n=sum(bits)
   if not 0<n<p:continue
   f=sum(bits[j]*X**j for j in range(p))
   resultant=abs(int(sp.resultant(phi,f,X)))
   assert resultant>=1
   minnorm=resultant if minnorm is None else min(minnorm,resultant);checks+=1
 # independent enumeration: five-cycle kernel 3I+T+T^-1 and total six
 p,N=5,6;states=[]
 for h in compositions(N,p):
  E=3*sum(x*x for x in h)+2*sum(h[j]*h[(j+1)%p] for j in range(p))
  r=N%p;m=min(r,p-r);lam=(5-sp.sqrt(5))/2
  base=F(N*N)+lam*F(r*(p-r),p)
  gamma=2*sp.sqrt(5)/(5*m*m)
  bound=base+gamma # here gamma < 2lambda*
  assert sp.simplify(bound)==N*N+2
  assert E>=bound
  states.append({'occupancy':h,'energy':E})
 winners=[x for x in states if x['energy']==min(s['energy'] for s in states)]
 assert len(winners)==5 and all(sorted(x['occupancy'])==[1,1,1,1,2] for x in winners)
 # exact cyclotomic support test for all binary polynomials up to period 9
 packet_checks=0
 for P in range(2,10):
  ds=sp.divisors(P)[1:]
  for bits in product((0,1),repeat=P):
   f=sp.Poly(sum(bits[j]*X**j for j in range(P)),X)
   for d in ds:
    rem=f.rem(sp.Poly(sp.cyclotomic_poly(d,X),X))
    zero=rem.is_zero
    # Evaluate numerically at all primitive dth roots, only to cross-check exact divisibility.
    for k in range(1,d):
     if math.gcd(k,d)!=1:continue
     v=sum(bits[j]*complex(math.cos(2*math.pi*k*j/d),math.sin(2*math.pi*k*j/d)) for j in range(P))
     assert (abs(v)<1e-8)==zero
     packet_checks+=1
 out={'status':'PASS','prime_binary_norm_certificates':checks,'smallest_resultant':minnorm,'cyclotomic_packet_crosschecks':packet_checks,'example':{'P':p,'N':N,'kernel_first_row':[3,1,0,0,1],'occupancies':len(states),'energy_levels':sorted(set(s['energy'] for s in states)),'minimum':min(s['energy'] for s in states),'winners':winners,'lambda_star':'(5-sqrt(5))/2','spectral_bound':'36+4*lambda_star/5','cyclotomic_gap':'2*sqrt(5)/5','improved_bound':'38'},'states':states}
 (W/'discovery.json').write_text(json.dumps(out,indent=2))
 print('CYCLIC',{k:v for k,v in out.items() if k!='states'})

 (W/'figure.json').write_text((W/'discovery.json').read_text())


if __name__=="__main__":
 cyclic()
