#!/usr/bin/env python3
"""Exact binary matrix construction and synthesis; standard library only.
A matrix is a tuple of 32 columns, each packed least-significant-bit first.
Author: lmtlssss🜐. License: MIT.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import Iterable

N = 32
MASK = (1 << N) - 1
IDENTITY = tuple(1 << j for j in range(N))
ZERO = (0,) * N
U0 = 0xAEB51DBB
V0 = 0xDDB8AD75
EXPONENTS = (31, 29, 27, 25, 19, 11, 9, 1)


def rotate(x: int, k: int) -> int:
    return ((x >> k) | (x << (N-k))) & MASK


def map_a(x: int) -> int:
    return rotate(x,7) ^ rotate(x,18) ^ (x >> 3)


def map_b(x: int) -> int:
    return rotate(x,17) ^ rotate(x,19) ^ (x >> 10)


def generators() -> tuple[tuple[int,...],tuple[int,...]]:
    return tuple(map_a(1 << j) for j in range(N)), tuple(map_b(1 << j) for j in range(N))


def apply(matrix: tuple[int,...], x: int) -> int:
    if len(matrix) != N or x < 0 or x > MASK:
        raise ValueError('Expected a 32-column matrix and a 32-bit input.')
    y = 0
    while x:
        bit = x & -x
        y ^= matrix[bit.bit_length()-1]
        x ^= bit
    return y


def multiply(a: tuple[int,...], b: tuple[int,...]) -> tuple[int,...]:
    """Matrix product a*b: apply b first, then a."""
    return tuple(apply(a,c) for c in b)


def add(a: tuple[int,...], b: tuple[int,...]) -> tuple[int,...]:
    return tuple(x ^ y for x,y in zip(a,b))


def transpose(a: tuple[int,...]) -> tuple[int,...]:
    return tuple(sum(((a[j] >> i) & 1) << j for j in range(N)) for i in range(N))


def matrix_rank(vectors: Iterable[int]) -> int:
    pivots: dict[int,int] = {}
    for value in vectors:
        while value:
            p = value.bit_length()-1
            if p in pivots:
                value ^= pivots[p]
            else:
                pivots[p] = value
                break
    return len(pivots)


def inverse(a: tuple[int,...]) -> tuple[int,...]:
    rows = [v | (1 << (N+i)) for i,v in enumerate(transpose(a))]
    for j in range(N):
        pivot = next((i for i in range(j,N) if rows[i] >> j & 1),None)
        if pivot is None:
            raise ValueError('Matrix is singular.')
        rows[j],rows[pivot] = rows[pivot],rows[j]
        for i in range(N):
            if i != j and rows[i] >> j & 1:
                rows[i] ^= rows[j]
    return transpose(tuple(r >> N for r in rows))


def polynomial(matrix: tuple[int,...], exponents: Iterable[int]) -> tuple[int,...]:
    exps = frozenset(exponents)
    total = ZERO
    for degree in range(max(exps),-1,-1):
        total = multiply(matrix,total)
        if degree in exps:
            total = add(total,IDENTITY)
    return total


def compact_certificate() -> dict:
    a,b = generators()
    d = add(multiply(b,multiply(b,b)),a)
    p = polynomial(d,EXPONENTS)
    outer = tuple(U0 if V0 >> j & 1 else 0 for j in range(N))
    if p != outer:
        raise ArithmeticError('Rank-one identity failed.')
    ucols=[]; vrows=[]; x=U0; y=V0; at=transpose(a)
    for _ in range(N):
        ucols.append(x);vrows.append(y)
        x=apply(a,x);y=apply(at,y)
    u=tuple(ucols);v=transpose(tuple(vrows))
    ui=inverse(u);vi=inverse(v)
    return {
        'dimension':N, 'field':'F2', 'bit_order':'least significant bit has coordinate 0',
        'A':{'rotations':[7,18],'right_shift':3},
        'B':{'rotations':[17,19],'right_shift':10},
        'D':'B^3 + A', 'polynomial_exponents':list(EXPONENTS),
        'u':f'{U0:08x}', 'v':f'{V0:08x}',
        'rank_D':matrix_rank(d), 'rank_P':matrix_rank(p),
        'U_columns':[f'{c:08x}' for c in u],
        'V_rows':[f'{c:08x}' for c in vrows],
        'U_inverse_columns':[f'{c:08x}' for c in ui],
        'V_inverse_columns':[f'{c:08x}' for c in vi],
        'UV_determinants':[1,1], 'v_dot_u':(U0 & V0).bit_count() % 2,
    }


def basis_matrices(certificate: dict) -> tuple[tuple[int,...], tuple[int,...]]:
    u=tuple(int(c,16) for c in certificate['U_columns'])
    v=transpose(tuple(int(c,16) for c in certificate['V_rows']))
    return u,v


def encode(target: tuple[int,...], certificate: dict) -> tuple[int,...]:
    """Return coefficient matrix H in target = U H V."""
    ui=tuple(int(c,16) for c in certificate['U_inverse_columns'])
    vi=tuple(int(c,16) for c in certificate['V_inverse_columns'])
    return multiply(ui,multiply(target,vi))


def decode(coefficients: tuple[int,...], certificate: dict) -> tuple[int,...]:
    u,v=basis_matrices(certificate)
    return multiply(u,multiply(coefficients,v))


def word_matrix(word: str) -> tuple[int,...]:
    """Read symbols left to right as input operations: 'AB' means B*A."""
    if any(ch not in 'AB' for ch in word):
        raise ValueError('A word uses only A and B.')
    a,b=generators();m=IDENTITY
    for ch in word:
        m=multiply(a if ch=='A' else b,m)
    return m


def pack(matrix: tuple[int,...]) -> int:
    return sum(c << (N*j) for j,c in enumerate(matrix))


def short_basis() -> dict:
    """Breadth-first independent word basis, fixed deterministic order."""
    a,b=generators();basis=[];pivots={};cursor=0;attempted=0
    def insert(matrix,word):
        z=pack(matrix)
        while z:
            p=z.bit_length()-1
            if p in pivots:z ^= pivots[p]
            else:
                pivots[p]=z;basis.append((matrix,word));return
    insert(IDENTITY,'')
    while cursor<len(basis) and len(basis)<N*N:
        matrix,word=basis[cursor];cursor+=1
        for symbol,g in [('A',a),('B',b)]:
            attempted+=1;insert(multiply(g,matrix),word+symbol)
            if len(basis)==N*N:break
    if len(basis)!=N*N:raise ArithmeticError('Generators did not span the full algebra.')
    return {'dimension':N,'rank':len(basis),'max_length':max(len(w) for m,w in basis),
            'word_convention':'Apply symbols left to right to the input; empty word is identity.',
            'words':[w for m,w in basis],'products_attempted':attempted}


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-certificates',type=Path)
    parser.add_argument('--elementary',nargs=2,type=int,metavar=('ROW','COL'))
    args=parser.parse_args()
    certificate=compact_certificate()
    if args.write_certificates:
        args.write_certificates.mkdir(parents=True,exist_ok=True)
        (args.write_certificates/'rank-one-certificate.json').write_text(json.dumps(certificate,indent=2)+'\n')
        (args.write_certificates/'short-word-certificate.json').write_text(json.dumps(short_basis(),indent=2)+'\n')
    if args.elementary:
        i,j=args.elementary
        if not (0<=i<N and 0<=j<N):parser.error('Rows and columns must be between 0 and 31.')
        target=tuple((1 << i) if t==j else 0 for t in range(N))
        h=encode(target,certificate)
        if decode(h,certificate)!=target:raise ArithmeticError('Complete reconstruction failed.')
        print(json.dumps({'elementary':[i,j], 'coefficient_columns':[f'{c:08x}' for c in h],
                          'rank_one_basis_terms':sum(c.bit_count() for c in h),
                          'complete_map_reconstructed':True},indent=2))
    elif not args.write_certificates:
        print(json.dumps(certificate,indent=2))

if __name__=='__main__':main()
