#!/usr/bin/env python3
"""Canonical complete-response states for two-stage radix-B addition.
Author: lmtlssss🜐. Code license: MIT.
"""
from __future__ import annotations
from typing import Iterable

# Incoming pairs are ordered (0,0), (0,1), (1,0), (1,1).
# Each table entry is 2*first_carry + second_carry.
MID = ((0,0,0,0), (1,1,1,1), (1,1,2,2), (2,2,2,2), (3,3,3,3))
PENULT = ((0,0,0,1), (1,1,2,3), (2,2,2,3))
LAST = ((0,1,1,1), (0,1,2,2), (2,3,3,3))

def _radix(B: int) -> None:
    if not isinstance(B, int) or isinstance(B, bool) or B < 2:
        raise ValueError('radix must be an integer at least two')

def encode(B: int, C: int, S: int, H: int) -> int:
    """Return a state in range(5*B-4) for the three supplied operands."""
    _radix(B)
    if not all(isinstance(x, int) and 0 <= x < B for x in (C,S,H)):
        raise ValueError('each operand must be an integer in range(B)')
    q, r = divmod(C+S, B)
    k, v = divmod(r+H, B)
    if v < B-2:
        t = 2 if r == B-1 else (3+k if q else k)
        return 5*v+t
    t = 1 if r == B-1 else 2*q
    return 5*(B-2) + 3*(v-(B-2)) + t

def normal_form(B: int, label: int) -> tuple[int, tuple[int,...]]:
    _radix(B)
    if not isinstance(label, int) or not 0 <= label < 5*B-4:
        raise ValueError('state label is outside the canonical range')
    cut = 5*(B-2)
    if label < cut:
        v,t = divmod(label,5)
        return v, MID[t]
    v,t = divmod(label-cut,3)
    return B-2+v, (PENULT if v == 0 else LAST)[t]

def evaluate(B: int, label: int, a: int, b: int) -> tuple[int,int,int]:
    """Return (residue, first outgoing carry, second outgoing carry)."""
    if a not in (0,1) or b not in (0,1):
        raise ValueError('incoming carries must be zero or one')
    v, table = normal_form(B,label)
    carry = table[2*a+b]
    return (v+a+b) % B, carry//2, carry%2

def representative(B: int, label: int) -> tuple[int,int,int]:
    """Construct one actual operand triple for every canonical state."""
    v,_ = normal_form(B,label)
    cut = 5*(B-2)
    if label < cut:
        t = label%5
        return ((0,v,0), (0,v+1,B-1), (0,B-1,v+1),
                (B-1,v+1,0), (B-1,v+2,B-1))[t]
    t = (label-cut)%3
    if t == 0: return 0,0,v
    if t == 2: return B-1,1,v
    return 0,B-1,(v+1)%B

def multiplicity(B: int, label: int) -> int:
    """Exact number of operand triples in this complete-response class."""
    v,_ = normal_form(B,label)
    if v >= B-2:
        return B if (label-5*(B-2))%3 == 1 else B*(B-1)//2
    t = label%5
    return ((v+1)*(v+2)//2,
            (B*(B-1)-(v+1)*(v+2))//2,
            B,
            (v+1)*(2*B-2-v)//2,
            (B-v-2)*(B-v-1)//2)[t]

def compose(radices: Iterable[int], labels: Iterable[int], a: int, b: int):
    """Evaluate independently recoverable stages from least to most significant."""
    bases, states = tuple(radices), tuple(labels)
    if len(bases) != len(states) or not bases:
        raise ValueError('radices and labels must have equal positive length')
    scale, result, trace = 1,0,[]
    for B, label in zip(bases,states):
        value,a,b = evaluate(B,label,a,b)
        result += scale*value
        scale *= B
        trace.append((a,b))
    return result,a,b,tuple(trace)

if __name__ == '__main__':
    import argparse,json
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--radix',type=int,default=256)
    p.add_argument('--C',type=int,default=37)
    p.add_argument('--S',type=int,default=218)
    p.add_argument('--H',type=int,default=13)
    ns=p.parse_args();label=encode(ns.radix,ns.C,ns.S,ns.H)
    print(json.dumps({'radix':ns.radix,'operands':[ns.C,ns.S,ns.H],
      'state':label,'class_size':multiplicity(ns.radix,label),
      'outputs':[evaluate(ns.radix,label,a,b) for a in (0,1) for b in (0,1)]},indent=2))
