#!/usr/bin/env python3
"""Exact rational peak certificates and finite quadratic sums for a damped recurrence."""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
import argparse,json,random


def mul(A,B):return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]

def add(A,B):return [[a+b for a,b in zip(x,y)] for x,y in zip(A,B)]

def transpose(A):return [list(x) for x in zip(*A)]

def matpow(A,n):
    out=[[F(int(i==j)) for j in range(len(A))] for i in range(len(A))]
    while n:
        if n&1:out=mul(out,A)
        A=mul(A,A);n//=2
    return out


def peak_certificate(a,b,x0,x1):
    r2=a*a+b*b
    if not 0<r2<1 or b==0:raise ValueError('stable nonreal roots required')
    R2=x0*x0+((x1-a*x0)/b)**2
    if R2==0:return {'values':[F(0)],'N':1,'peak':F(0),'peak_index':0,'R2':F(0),'tail_envelope_squared':F(0)}
    values=[x0,x1];M2=max(x0*x0,x1*x1);power=r2*r2
    # Invariant: power=r2**len(values), bounding every future square.
    while R2*power>=M2:
        values.append(2*a*values[-1]-r2*values[-2]);M2=max(M2,values[-1]**2);power*=r2
        if len(values)>10000:raise RuntimeError('fixture search bound')
    peak=max(abs(x) for x in values);idx=next(i for i,x in enumerate(values) if abs(x)==peak)
    assert R2*power<peak*peak
    return {'values':values,'N':len(values),'peak':peak,'peak_index':idx,'R2':R2,'tail_envelope_squared':R2*power}


def solve_linear(A,b):
    A=[list(row)+[rhs] for row,rhs in zip(A,b)];n=len(A)
    for k in range(n):
        p=next(i for i in range(k,n) if A[i][k]);A[k],A[p]=A[p],A[k];t=A[k][k];A[k]=[v/t for v in A[k]]
        for i in range(n):
            if i!=k:
                t=A[i][k];A[i]=[x-t*y for x,y in zip(A[i],A[k])]
    return [r[-1] for r in A]


def stein(A,Q):
    # Four scalar equations W-A^T W A=Q; rational Gaussian elimination.
    eq=[];rhs=[]
    for i in range(2):
        for j in range(2):
            eq.append([F(int((u,v)==(i,j)))-A[u][i]*A[v][j] for u in range(2) for v in range(2)])
            rhs.append(Q[i][j])
    x=solve_linear(eq,rhs);return [x[:2],x[2:]]


def quadratic(W,z):return sum(z[i]*W[i][j]*z[j] for i in range(2) for j in range(2))


def finite_energy(a,b,x0,x1,K):
    A=[[a,b],[-b,a]];Q=[[F(1),F(0)],[F(0),F(0)]];z=[x0,(x1-a*x0)/b]
    W=stein(A,Q);AK=matpow(A,K);tail=mul(transpose(AK),mul(W,AK));G=[[W[i][j]-tail[i][j] for j in range(2)] for i in range(2)]
    return quadratic(G,z),quadratic(W,z),W


def observation_rows(a,b,T):
    rows=[]
    for k in T:
        ak,bk=F(1),F(0)
        for _ in range(k):ak,bk=ak*a-bk*b,ak*b+bk*a
        rows.append((ak,bk))
    return rows


def strip_constant_squared(a,b,T):
    rows=observation_rows(a,b,T);vertices=set()
    for i,u in enumerate(rows):
        for v in rows[i+1:]:
            det=u[0]*v[1]-u[1]*v[0]
            if not det:continue
            for si in (-1,1):
                for sj in (-1,1):
                    z=((si*v[1]-u[1]*sj)/det,(u[0]*sj-si*v[0])/det)
                    if all(abs(q[0]*z[0]+q[1]*z[1])<=1 for q in rows):vertices.add(z)
    if not vertices:raise ValueError('observation rows must span the plane')
    maximizer=max(vertices,key=lambda z:z[0]**2+z[1]**2)
    return 1/(maximizer[0]**2+maximizer[1]**2),maximizer,sorted(vertices)


def check_all():
    rng=random.Random(20261102);observability=0;peaks=0;energy_checks=0;maxN=0;sharpness=0;polygon_inequalities=0;polygon_equalities=0
    coefficients=[(F(3,5),F(1,5)),(F(1,2),F(1,2)),(F(-2,5),F(1,3)),(F(0),F(2,3)),(F(4,5),F(1,5))]
    for a,b in coefficients:
        r2=a*a+b*b;c2=b*b/(1+r2+2*abs(a))
        # Equality witnesses: opposing endpoint observations when a>=0.
        x0=F(1);x1=F(-1 if a>=0 else 1)
        R2=x0*x0+((x1-a*x0)/b)**2
        assert max(x0*x0,x1*x1)==c2*R2;sharpness+=1
        for u in range(-4,5):
            for v in range(-4,5):
                x0=F(u,3);x1=a*x0+b*F(v,3);R2=x0*x0+F(v,3)**2
                assert max(x0*x0,x1*x1)>=c2*R2;observability+=1
        for trial in range(24):
            x0=F(rng.randrange(-5,6),3);x1=F(rng.randrange(-5,6),4)
            cert=peak_certificate(a,b,x0,x1);maxN=max(maxN,cert['N'])
            vals=[x0,x1]
            for k in range(2,320):vals.append(2*a*vals[-1]-r2*vals[-2])
            assert cert['peak']==max(abs(x) for x in vals);peaks+=1
            for K in (0,1,2,7,32,64):
                E,Einf,W=finite_energy(a,b,x0,x1,K)
                assert E==sum(x*x for x in vals[:K]);assert E<=Einf;energy_checks+=1
        # Nonadjacent two-sample bound with exact complex powers.
        ak,bk=F(1),F(0)
        for k in range(1,9):
            ak,bk=ak*a-bk*b,ak*b+bk*a
            if not bk:continue
            ck2=bk*bk/(1+r2**k+2*abs(ak))
            for u,v in ((F(1),F(2)),(F(-2),F(3)),(F(1,3),F(-2,5))):
                assert max(u*u,(ak*u+bk*v)**2)>=ck2*(u*u+v*v);observability+=1
    for a,b in coefficients:
        c2,z,vertices=strip_constant_squared(a,b,[0,1])
        assert c2==b*b/(1+a*a+b*b+2*abs(a))
        for T in ([0,1],[0,1,2],[0,1,2,4],[0,2,3,5]):
            c2,z,vertices=strip_constant_squared(a,b,T)
            rows=observation_rows(a,b,T)
            assert max((q[0]*z[0]+q[1]*z[1])**2 for q in rows)==c2*(z[0]**2+z[1]**2)
            polygon_equalities+=1
            for u in range(-5,6):
                for v in range(-5,6):
                    zz=(F(u,3),F(v,4))
                    assert max((q[0]*zz[0]+q[1]*zz[1])**2 for q in rows)>=c2*(zz[0]**2+zz[1]**2)
                    polygon_inequalities+=1
    a,b=F(3,5),F(1,5);x0,x1=F(0),F(1);cert=peak_certificate(a,b,x0,x1)
    E,Einf,W=finite_energy(a,b,x0,x1,64)
    vals=[x0,x1]
    for i in range(2,28):vals.append(2*a*vals[-1]-(a*a+b*b)*vals[-2])
    c2=b*b/(1+a*a+b*b+2*abs(a));power=F(1);universal=0
    while power>=c2:power*=a*a+b*b;universal+=1
    assert cert['N']==4 and cert['peak']==F(6,5) and cert['peak_index']==2
    fig={'a':str(a),'b':str(b),'rho_squared':str(a*a+b*b),'initial':['0','1'],
      'sharp_constant_squared':str(c2),'universal_prefix':universal,'instance_prefix':cert['N'],
      'peak':str(cert['peak']),'peak_index':cert['peak_index'],'tail_envelope_squared':str(cert['tail_envelope_squared']),
      'amplitude_squared':str(cert['R2']),'sample_values':[str(x) for x in vals],
      'exact_infinite_square_sum':str(Einf),'finite_64_square_sum':str(E),
      'stein_matrix':[[str(x) for x in row] for row in W],
      'interpretation':'Four rational samples plus a geometric envelope certify the infinite absolute peak.'}
    return {'status':'PASS','observability_inequalities':observability,'sharp_equality_witnesses':sharpness,'strip_polygon_inequalities':polygon_inequalities,'strip_polygon_equality_witnesses':polygon_equalities,'exact_peak_instances':peaks,'exact_finite_energy_checks':energy_checks,'largest_instance_prefix':maxN,'figure':fig,'arithmetic':'fractions, direct recurrence, independent rational Stein solve and matrix powers'}
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--output',default='evidence/verification.json');args=a.parse_args();p=Path(args.output);p.parent.mkdir(parents=True,exist_ok=True)
    obj=check_all();p.write_text(json.dumps(obj,indent=2)+'\n');(p.parent/'figure.json').write_text(json.dumps(obj['figure'],indent=2)+'\n');print(json.dumps({k:v for k,v in obj.items() if k!='figure'},indent=2))
