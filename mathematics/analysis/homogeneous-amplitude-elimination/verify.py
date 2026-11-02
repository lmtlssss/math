#!/usr/bin/env python3
"""Rational certificates for robust amplitude elimination and grid rounding."""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
import argparse,json,random


def ceilq(x:F)->int:return -((-x.numerator)//x.denominator)

def solve(scenarios, origin=F(0), step=None):
    # Scenarios are (positive minimum response, positive maximum response,
    # positive objective coefficient, required minimum, permitted maximum).
    if not scenarios or any(m<=0 or M<=0 or e<=0 or f<=0 or h<=0 for m,M,e,f,h in scenarios):
        raise ValueError('positive responses, cost and limits are required')
    low=max(f/m for m,M,e,f,h in scenarios)
    high=min(h/M for m,M,e,f,h in scenarios)
    if step is None:a=low
    else:
        if step<=0 or origin<0:raise ValueError('grid parameters')
        a=origin+step*max(0,ceilq((low-origin)/step))
    if a>high:return None
    return a,max(e*a*a for m,M,e,f,h in scenarios),low,high


def direct(scenarios,origin,step,maxk):
    vals=[]
    for k in range(maxk+1):
        a=origin+k*step
        if all(a*m>=f and a*M<=h for m,M,e,f,h in scenarios):
            vals.append((max(e*a*a for m,M,e,f,h in scenarios),a))
    if not vals:return None
    cost,a=min(vals);return a,cost


def check_all():
    rng=random.Random(20261102);checked=0;feasible=0;bound_checks=0
    for case in range(2400):
        scenarios=[]
        for j in range(1+case%4):
            m=F(rng.randrange(3,17),10);M=m+F(rng.randrange(1,9),10)
            e=F(rng.randrange(1,30),10);f=F(rng.randrange(3,13),10);h=F(rng.randrange(15,50),10)
            scenarios.append((m,M,e,f,h))
        origin=F(case%4,20);step=F(1+case%5,20)
        a=solve(scenarios,origin,step);b=direct(scenarios,origin,step,100)
        assert (a is None)==(b is None)
        if a:
            feasible+=1;assert (a[0],a[1])==b
            L=max(origin,a[2]);assert L<=a[0]<L+step
            # Sharp scalar rounding bound for quadratic costs.
            assert a[1] < max(s[2] for s in scenarios)*(L+step)**2
            bound_checks+=1
        checked+=1
    # Quantization changes the optimal design: exact three-design certificate.
    base=[('A',F(1),F(1)),('B',F(21,20),F(27,25)),('C',F(4,5),F(3,5))]
    designs=[]
    for name,m,e in base:
        scenarios=[(m,m,e,F(1),F(2))]
        con=solve(scenarios);grid=solve(scenarios,step=F(1,10))
        designs.append({'name':name,'m':str(m),'e':str(e),'a_continuous':str(con[0]),'continuous_value':str(con[1]),'a_grid':str(grid[0]),'grid_value':str(grid[1])})
    assert min(designs,key=lambda x:F(x['continuous_value']))['name']=='C'
    assert min(designs,key=lambda x:F(x['grid_value']))['name']=='A'
    # Nine further exact designs are dominated; retained for the figure grid.
    for j in range(9):
        m=F(7+j,10);e=F(6,5)*m*m
        scenarios=[(m,m,e,F(1),F(3))]
        con=solve(scenarios);grid=solve(scenarios,step=F(1,10))
        designs.append({'name':chr(68+j),'m':str(m),'e':str(e),'a_continuous':str(con[0]),'continuous_value':str(con[1]),'a_grid':str(grid[0]),'grid_value':str(grid[1])})
    # Tiny upper interval can exclude the rounded continuous optimum.
    infeasible=[(F(1),F(1),F(1),F(101,100),F(102,100))]
    assert solve(infeasible) is not None and solve(infeasible,step=F(1,10)) is None
    # Homogeneous two-dimensional recurrence; direct rational state scaling.
    A=((F(1,2),F(1,5)),(F(-1,5),F(1,2)));b=(F(2,3),F(1,4));x0=(F(1,7),F(2,7));scaling=0
    for scale in (F(1,10),F(2,3),F(7,5),F(5)):
        y=list(x0);z=[scale*v for v in x0]
        for n in range(50):
            force=F((n%7)-3,5)
            y=[sum(A[i][j]*y[j] for j in range(2))+force*b[i] for i in range(2)]
            z=[sum(A[i][j]*z[j] for j in range(2))+scale*force*b[i] for i in range(2)]
            assert z==[scale*v for v in y];scaling+=1
    return {'status':'PASS','grid_instances':checked,'feasible_instances':feasible,'rounding_bound_checks':bound_checks,'exact_scaling_steps':scaling,
      'admissibility_counterexample':'[101/100,102/100] intersects positive reals and contains no multiple of 1/10',
      'figure':{'designs':designs,'grid':[str(F(k,10)) for k in range(5,21)],'grid_step':'1/10','lower_floor':'1','continuous_winner':'C','grid_winner':'A','full_grid_points':192,'eliminated_candidates':12},
      'arithmetic':'Python fractions; direct finite enumeration and separately computed exact ceilings'}
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--output',default='evidence/verification.json');args=a.parse_args();o=Path(args.output);o.parent.mkdir(parents=True,exist_ok=True)
    obj=check_all();o.write_text(json.dumps(obj,indent=2)+'\n');(o.parent/'figure.json').write_text(json.dumps(obj['figure'],indent=2)+'\n')
    print(json.dumps({k:v for k,v in obj.items() if k!='figure'},indent=2))
