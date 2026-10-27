#!/usr/bin/env python3
"""Verify complete binary maps with independent row arithmetic and exact pivots."""
from __future__ import annotations
import argparse
import json
import random
import time
from pathlib import Path
import algebra

N=32
I=tuple(1<<i for i in range(N))
ZERO=(0,)*N
ROOT=Path(__file__).resolve().parent


def coordinate_rows(r:int,t:int,h:int) -> tuple[int,...]:
    # Direct coordinate definition, not evaluations of algebra.map_a/map_b.
    return tuple((1<<((i+r)%N)) ^ (1<<((i+t)%N)) ^
                 ((1<<(i+h)) if i+h<N else 0) for i in range(N))


def row_product(left:tuple[int,...],right:tuple[int,...]) -> tuple[int,...]:
    result=[]
    for coefficients in left:
        value=0
        for j in range(N):
            if coefficients>>j&1:value^=right[j]
        result.append(value)
    return tuple(result)


def row_xor(left,right):return tuple(a^b for a,b in zip(left,right))


def rows_from_columns(columns):
    return tuple(sum(((columns[j]>>i)&1)<<j for j in range(N)) for i in range(N))


def rank_low(values):
    pivots={}
    for v in values:
        while v:
            key=v&-v
            if key in pivots:v^=pivots[key]
            else:pivots[key]=v;break
    return len(pivots)


def packed_rows(matrix):return sum(r<<(N*i) for i,r in enumerate(matrix))


def from_packed_rows(value):
    return tuple((value>>(N*i))&((1<<N)-1) for i in range(N))


def validate_compact(certificate):
    a=coordinate_rows(7,18,3);b=coordinate_rows(17,19,10)
    d=row_xor(row_product(b,row_product(b,b)),a)
    p=ZERO;power=I
    for exponent in range(32):
        if exponent in certificate['polynomial_exponents']:p=row_xor(p,power)
        power=row_product(power,d)
    u=int(certificate['u'],16);v=int(certificate['v'],16)
    expected=tuple(v if (u>>i)&1 else 0 for i in range(N))
    assert p==expected, 'rank-one polynomial identity'
    assert rank_low(p)==1 and rank_low(d)==31
    assert row_product(p,p)==ZERO, 'nilpotence, not idempotence'
    # Reconstruct the cyclic arrays, rather than trusting stored bases.
    uc=[];vr=[];x=u;y=v
    for _ in range(N):
        uc.append(x);vr.append(y)
        x=sum(((a[i]&x).bit_count()%2)<<i for i in range(N))
        z=0
        for i in range(N):
            if y>>i&1:z^=a[i]
        y=z
    U=rows_from_columns(uc);V=tuple(vr)
    assert uc==[int(t,16) for t in certificate['U_columns']]
    assert vr==[int(t,16) for t in certificate['V_rows']]
    Ui=rows_from_columns(tuple(int(t,16) for t in certificate['U_inverse_columns']))
    Vi=rows_from_columns(tuple(int(t,16) for t in certificate['V_inverse_columns']))
    for left,right in ((U,Ui),(Ui,U),(V,Vi),(Vi,V)):
        assert row_product(left,right)==I,'cyclic-basis inverse'
    assert rank_low(U)==rank_low(V)==N
    return a,b,d,p,U,V


def validate_words(certificate,a,b):
    matrices={'':I}
    for w in sorted(certificate['words'],key=lambda w:(len(w),w)):
        if w:
            assert set(w)<={'A','B'}
            # Prefixes of the supplied breadth-first certificate are retained.
            matrices[w]=row_product(a if w[-1]=='A' else b,matrices[w[:-1]])
    packed=[packed_rows(matrices[w]) for w in certificate['words']]
    assert len(set(certificate['words']))==1024
    assert max(map(len,certificate['words']))==10
    assert rank_low(packed)==1024
    return matrices,packed


def all_word_dimensions(a,b):
    pivots={};frontier=[I];dimensions=[];words=0
    for length in range(11):
        for matrix in frontier:
            words+=1;v=packed_rows(matrix)
            while v:
                key=v&-v
                if key in pivots:v^=pivots[key]
                else:pivots[key]=v;break
        dimensions.append(len(pivots))
        if length<10:
            frontier=[row_product(g,m) for m in frontier for g in (a,b)]
    assert dimensions==[1,3,7,15,31,63,127,255,510,991,1024]
    assert words==2047
    return dimensions,words


def short_word_solver(basis):
    pivots={}
    for i,original in enumerate(basis):
        value=original;mask=1<<i
        while value:
            key=value&-value
            if key in pivots:value^=pivots[key][0];mask^=pivots[key][1]
            else:pivots[key]=(value,mask);break
        assert value
    def solve(target):
        coefficients=0;remaining=target
        while remaining:
            key=remaining&-remaining
            remaining^=pivots[key][0];coefficients^=pivots[key][1]
        result=0;selected=coefficients
        while selected:
            key=selected&-selected
            result^=basis[key.bit_length()-1];selected^=key
        assert result==target
        return coefficients
    return solve


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'evidence/verification.json')
    args=parser.parse_args();start=time.perf_counter()
    compact=json.loads((ROOT/'evidence/rank-one-certificate.json').read_text())
    words=json.loads((ROOT/'evidence/short-word-certificate.json').read_text())
    a,b,d,p,U,V=validate_compact(compact)
    matrices,basis=validate_words(words,a,b)
    dimensions,all_words=all_word_dimensions(a,b)
    solve=short_word_solver(basis)
    elementary_checks=0;coefficient_popcounts=[]
    for i in range(N):
        for j in range(N):
            columns=tuple((1<<i) if col==j else 0 for col in range(N))
            h=algebra.encode(columns,compact)
            # Independent row arithmetic reconstructs the full map.
            got=row_product(U,row_product(rows_from_columns(h),V))
            expected=tuple((1<<j) if row==i else 0 for row in range(N))
            assert got==expected
            assert algebra.decode(h,compact)==columns
            c=solve(packed_rows(expected));coefficient_popcounts.append(c.bit_count())
            elementary_checks+=1
    rng=random.Random(0x20261027)
    random_checks=64
    for _ in range(random_checks):
        columns=tuple(rng.getrandbits(N) for j in range(N))
        h=algebra.encode(columns,compact)
        assert row_product(U,row_product(rows_from_columns(h),V))==rows_from_columns(columns)
        assert algebra.decode(h,compact)==columns
        solve(packed_rows(rows_from_columns(columns)))
    rejected=0
    for key in ('polynomial_exponents','u','v','U_inverse_columns'):
        c=json.loads(json.dumps(compact))
        if key=='polynomial_exponents':c[key]=c[key][1:]
        elif key in ('u','v'):c[key]=f'{int(c[key],16)^1:08x}'
        else:c[key][0]=f'{int(c[key][0],16)^1:08x}'
        try:validate_compact(c)
        except AssertionError:rejected+=1
        else:raise AssertionError('invalid compact certificate accepted')
    bad=dict(words);bad['words']=list(words['words']);bad['words'][-1]=bad['words'][0]
    try:validate_words(bad,a,b)
    except AssertionError:rejected+=1
    else:raise AssertionError('dependent word certificate accepted')
    assert rejected==5
    result={
        'status':'pass','date':'2026-10-27','field':'F2','dimension':32,
        'rank_D':rank_low(d),'rank_P':rank_low(p),
        'compact_identity_complete_coefficients':1024,
        'cyclic_basis_ranks':[rank_low(U),rank_low(V)],
        'two_sided_inverse_matrix_products':4,
        'short_certificate_words':len(basis),
        'short_certificate_rank':rank_low(basis),
        'all_words_through_length10':all_words,
        'cumulative_dimensions':dimensions,
        'elementary_maps_reconstructed_by_each_of_two_methods':elementary_checks,
        'random_complete_maps_by_each_of_two_methods':random_checks,
        'input_basis_images_per_method':(elementary_checks+random_checks)*32,
        'altered_certificates_rejected':rejected,
        'short_word_terms_elementary_min':min(coefficient_popcounts),
        'short_word_terms_elementary_max':max(coefficient_popcounts),
        'elapsed_seconds':time.perf_counter()-start,
        'scope':'Complete exact matrix identities and synthesis; internal independent algorithms, not proof-kernel acceptance or execution-speed evidence.'
    }
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
