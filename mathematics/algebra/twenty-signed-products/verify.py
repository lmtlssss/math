#!/usr/bin/env python3
"""Exact, standard-library verification of the complete tensor certificate.

Run: python3 verify.py
All tensor identities use integers. Matrix ranks use rational arithmetic.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
import hashlib, json


def rank(rows):
    a=[[F(x) for x in row] for row in rows]
    if not a:return 0
    p=0
    for j in range(len(a[0])):
        k=next((k for k in range(p,len(a)) if a[k][j]),None)
        if k is None:continue
        a[p],a[k]=a[k],a[p]
        scale=a[p][j];a[p]=[x/scale for x in a[p]]
        for k in range(p+1,len(a)):
            if a[k][j]:
                scale=a[k][j];a[k]=[x-scale*y for x,y in zip(a[k],a[p])]
        p+=1
        if p==len(a):break
    return p


def mulmat(a,b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]


def algorithm(a,b):
    """Constructive 20-product algorithm, independent of the rank-one vectors."""
    def transform(x):
        return [x[4],x[4]+x[7],x[3]+x[4],x[3]+x[4]+x[6]+x[7],sum(x),
                x[10],x[1],x[4]+x[7]+x[9],x[2]+x[3]+x[4],
                sum(x[8:12]),x[11],x[0]]
    u,v=transform(a),transform(b)
    z=[0]*12
    for i in range(5):z[i]=u[i]*v[i]
    z[9]=u[9]*v[3]+u[4]*v[9]
    z[10]=u[10]*v[7]+(u[4]-u[6]-u[8]-u[11])*v[5]+u[4]*v[10]
    z[11]=u[4]*v[11]+(u[4]-u[5]-u[7]-u[10])*v[6]+u[11]*v[8]
    # Strassen on X=rho(b), Y=rho(a), in the required reverse order.
    p1=(u[8]+u[7])*(v[8]+v[7])
    p2=u[8]*(v[5]+v[7])
    p3=(u[6]-u[7])*v[8]
    p4=(u[5]-u[8])*v[7]
    p5=u[7]*(v[8]+v[6])
    p6=(u[8]+u[6])*(v[5]-v[8])
    p7=(u[5]+u[7])*(v[6]-v[7])
    z[8]=p1+p4-p5+p7;z[6]=p3+p5
    z[5]=p2+p4;z[7]=p1-p2+p3+p6
    # Explicit inverse of the same integral output coordinates.
    return [z[11],z[6],z[8]-z[2],z[2]-z[0],z[0],
            z[2]-z[3]+z[4]-z[6]-z[8]-z[9]-z[11],
            z[0]-z[1]-z[2]+z[3],z[1]-z[0],
            z[1]-z[5]-z[7]+z[9]-z[10],z[7]-z[1],z[5],z[10]]


def verify(path: Path, tensor_square: bool=True):
    d=json.loads(path.read_text());maps=[tuple(x) for x in d['maps']];M=d['multiplication_table']
    assert len(maps)==len(set(maps))==12
    compose=lambda i,j:tuple(j[i[x]] for x in range(4))
    generated={(0,1,2,3)}
    while True:
        new=generated|{compose(a,maps[g]) for a in generated for g in d['generator_indices']}
        if new==generated:break
        generated=new
    assert set(maps)==generated
    assert [[maps.index(compose(i,j)) for j in maps] for i in maps]==M
    assert all(M[4][i]==M[i][4]==i for i in range(12))
    assert all(M[M[i][j]][k]==M[i][M[j][k]] for i,j,k in product(range(12),repeat=3))
    terms=d['terms'];assert len(terms)==20
    assert all(type(x) is int and abs(x)<=2 for t in terms for key in ('alpha','beta','gamma') for x in t[key])
    coefficient_checks=0
    eye=[[int(i==j) for j in range(12)] for i in range(12)]
    for i,j in product(range(12),repeat=2):
        expected=eye[M[i][j]]
        got=[sum(t['alpha'][i]*t['beta'][j]*t['gamma'][k] for t in terms) for k in range(12)]
        assert got==expected,(i,j,'certificate')
        assert algorithm(eye[i],eye[j])==expected,(i,j,'constructive algorithm')
        coefficient_checks+=12
    Q=d['output_basis'];assert rank(Q)==12
    chars=Q[:5];rho=d['representation']
    for i,j in product(range(12),repeat=2):
        assert all(ch[M[i][j]]==ch[i]*ch[j] for ch in chars)
        assert rho[M[i][j]]==mulmat(rho[j],rho[i])
    phi=chars+[[rho[i][u][v] for i in range(12)] for u,v in [(0,0),(0,1),(1,0),(1,1)]]
    assert rank(phi)==9
    # Explicit kernel basis: e5-e0, e8-e0, e11-e0.
    J=[[int(i==j)-int(i==0) for i in range(12)] for j in (5,8,11)]
    assert rank(J)==3 and all(sum(a*b for a,b in zip(row,j))==0 for row in phi for j in J)
    def algebra(a,b):
        c=[0]*12
        for i in range(12):
            for j in range(12):c[M[i][j]]+=a[i]*b[j]
        return c
    assert all(algebra(a,b)==[0]*12 for a,b in product(J,repeat=2))
    assert all(sum(x*y for x,y in zip(row,algebra(a,b)))==0 for row in phi for a in J for b in eye)
    assert all(sum(x*y for x,y in zip(row,algebra(b,a)))==0 for row in phi for a in J for b in eye)
    # Nonnegative upper bound: exactly 35 disjoint monochromatic rectangles.
    covered={}
    assert len(d['positive_rectangles'])==35
    for r,rect in enumerate(d['positive_rectangles']):
        for i,j in product(rect['left'],rect['right']):
            assert M[i][j]==rect['output'] and (i,j) not in covered
            covered[i,j]=r
    assert len(covered)==144
    W=[(i,j,k) for k,items in enumerate(d['positive_witnesses']) for i,j in items]
    assert len(W)==len(set(W))==35
    assert all(M[i][j]==k for i,j,k in W)
    def incompatible(a,b):
        return any(M[i][j]!=k for i,j,k in product((a[0],b[0]),(a[1],b[1]),(a[2],b[2])))
    assert all(incompatible(a,b) for a,b in combinations(W,2))
    slice_ranks=[rank([[int(M[i][j]==k) for j in range(12)] for i in range(12)]) for k in range(12)]
    assert slice_ranks==d['slice_ranks'] and sum(slice_ranks)==35
    square_pairs=0
    if tensor_square:
        W2=[tuple(zip(a,b)) for a,b in product(W,repeat=2)]
        for a,b in combinations(W2,2):
            assert any(any(M[i[t]][j[t]]!=k[t] for t in range(2)) for i,j,k in product((a[0],b[0]),(a[1],b[1]),(a[2],b[2])))
            square_pairs+=1
        assert square_pairs==749700
    return {'status':'PASS','certificate_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'monoid_elements':12,'multiplication_pairs':144,'associativity_triples':1728,
            'signed_tensor_coefficients':coefficient_checks,'constructive_algorithm_basis_cases':144,
            'signed_products':20,'maximum_absolute_coefficient':2,'output_basis_rank':12,
            'semisimple_quotient_rank':9,'radical_dimension':3,'radical_square_zero_products':9,
            'real_rank_lower_bound':18,'real_rank_upper_bound':20,'nonnegative_rank':35,
            'slice_ranks':slice_ranks,'positive_partition_pairs':144,'base_fooling_pairs':595,
            'tensor_square_fooling_pairs':square_pairs,'field':'exact integers and rational matrices'}

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--certificate',type=Path,default=Path(__file__).with_name('certificate.json'))
    ap.add_argument('--quick',action='store_true',help='Omit the redundant finite tensor-square check.')
    ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    result=verify(args.certificate,not args.quick)
    text=json.dumps(result,indent=2,ensure_ascii=False)+'\n'
    if args.output:args.output.write_text(text)
    print(text,end='')
