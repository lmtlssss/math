#!/usr/bin/env python3
"""Exact cyclic-shift energy checks. Python standard library; SymPy for rank checks.
All objective comparisons use integers or fractions. No optimization tolerance.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse, json, math, random


def shift(x: tuple[int,...], d: int) -> tuple[int,...]:
    p=len(x)
    return tuple(x[(t-d)%p] for t in range(p))


def dot(x,y): return sum(a*b for a,b in zip(x,y))


def filtered(x):
    return tuple(x[t]+2*x[(t-1)%len(x)] for t in range(len(x)))


def energy(xs, ds):
    p=len(xs[0]); s=tuple(sum(shift(x,d)[t] for x,d in zip(xs,ds)) for t in range(p))
    f=filtered(s)
    return dot(f,f)


def kernel(x,y):
    fx=filtered(x)
    return tuple(dot(fx,filtered(shift(y,d))) for d in range(len(x)))


def coordinate_scores(xs, ds, i):
    """Independent pair-kernel expansion of all one-coordinate objective values."""
    p=len(xs[0]); other=[j for j in range(len(xs)) if j!=i]
    rest=energy([xs[j] for j in other],[ds[j] for j in other]) if other else 0
    self_term=dot(filtered(xs[i]),filtered(xs[i]))
    ks={j:kernel(xs[i],xs[j]) for j in other}
    return [rest+self_term+2*sum(ks[j][(ds[j]-s)%p] for j in other) for s in range(p)]


def compositions(n,p):
    if p==1:
        yield (n,);return
    for first in range(n+1):
        for tail in compositions(n-first,p-1):yield (first,)+tail


def retained_common(p,weights,ds):
    k=kernel(p,p);P=len(p)
    return [sum(a*k[(d-s)%P] for a,d in zip(weights,ds)) for s in range(P)]


def check_all():
    rng=random.Random(20261102)
    result={'coordinate_objectives':0,'retained_updates':0,'balanced_occupancies':0,'rank_instances':0}
    # Full finite configurations, compared with direct sums then direct filtering.
    for P in range(2,7):
        xs=[tuple(rng.randrange(-2,3) for _ in range(P)) for j in range(3)]
        for ds in product(range(P),repeat=3):
            for i in range(3):
                scores=coordinate_scores(xs,ds,i)
                for s in range(P):
                    d=list(ds);d[i]=s
                    assert scores[s]==energy(xs,d)
                    result['coordinate_objectives']+=1
    # Common-profile retained potential: all signs and zero weights permitted.
    for P in range(2,10):
        p=tuple(rng.randrange(-3,4) for _ in range(P));ks=kernel(p,p)
        ws=[-2,0,1,3];ds=[rng.randrange(P) for _ in ws]
        phi=retained_common(p,ws,ds)
        for move in range(150):
            i=move%4;old=ds[i];new=rng.randrange(P)
            phi=[v+ws[i]*(ks[(new-s)%P]-ks[(old-s)%P]) for s,v in enumerate(phi)]
            ds[i]=new
            assert phi==retained_common(p,ws,ds)
            xs=[tuple(a*x for x in p) for a in ws]
            assert sum(a*phi[d] for a,d in zip(ws,ds))==energy(xs,ds)
            result['retained_updates']+=1
    # Sharp occupancy lower bound for K=alpha I+beta 11^T, alpha>0,beta>=0.
    for P in range(2,8):
        for N in range(0,10):
            q,r=divmod(N,P);alpha,beta=3,2
            expected=alpha*(P*q*q+2*q*r+r)+beta*N*N
            spectral=F((alpha+beta*P)*N*N,P)+F(alpha*r*(P-r),P)
            assert expected==spectral
            best=None;minimizers=[]
            for h in compositions(N,P):
                E=alpha*dot(h,h)+beta*N*N
                best=E if best is None else min(best,E)
                if E==expected:
                    assert max(h)-min(h)<=1
                    minimizers.append(h)
                result['balanced_occupancies']+=1
            assert best==expected
            assert len(minimizers)==math.comb(P,r)
    # Exact linear-summary rank equals the sum of frequency Gram ranks.
    import sympy as sp
    P=4;w=-sp.I
    for trial in range(32):
        m,N=2,3
        xs=[[[sp.Integer(rng.randrange(-2,3)) for _ in range(P)] for c in range(m)] for i in range(N)]
        cols=[]
        for i in range(N):
            for d in range(P):cols.append(sp.Matrix([xs[i][c][(t-d)%P] for c in range(m) for t in range(P)]))
        L=sp.Matrix.hstack(*cols);qrank=L.rank()
        ranks=[]
        for k in range(P):
            X=sp.Matrix(m,N,lambda c,i:sum(xs[i][c][t]*w**(k*t) for t in range(P)))
            G=X.conjugate().T*X
            ranks.append(G.rank())
        assert qrank==sum(ranks)
        result['rank_instances']+=1
    # Source-derived figure: 64 identical profiles in 16 cyclic positions.
    P,N=16,64;p=(2,1)+(0,)*14;ds=[i%P for i in range(N)];h=[ds.count(d) for d in range(P)]
    s=[sum(shift(p,d)[t] for d in ds) for t in range(P)]
    assert h==[4]*P and s==[12]*P
    dc_energy=dot(s,s);aligned=dot(tuple(N*x for x in p),tuple(N*x for x in p))
    figure={'P':P,'N':N,'profile':list(p),'shifts':ds,'occupancy':h,'aggregate':s,
            'aligned_energy':aligned,'balanced_energy':dc_energy,'nonconstant_energy':0,
            'pair_kernel_scalars':N*N*P,'shared_kernel_and_potential_scalars':2*P,
            'interpretation':'Actual cyclic positions, exact occupancy and integer quadratic objective.'}
    result.update(status='PASS',figure=figure,arithmetic='integers, fractions, exact Gaussian-integer matrix ranks',global_scope='sharp balanced bound for the specified spectral family')
    return result

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--output',default='evidence/verification.json');args=a.parse_args()
    out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True)
    obj=check_all();out.write_text(json.dumps(obj,indent=2)+'\n')
    (out.parent/'figure.json').write_text(json.dumps(obj['figure'],indent=2)+'\n')
    print(json.dumps({k:v for k,v in obj.items() if k!='figure'},indent=2))
