#!/usr/bin/env python3
"""Exact sum-and-carry functions for cascaded addition. Author: lmtlssss🜐.
Standard-library implementation; arbitrary integer radix and word size.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence
import argparse
import json


def arrangement_number(k: int) -> int:
    """Return A_0=1, A_k=k*A_(k-1)+1 (OEIS A000522)."""
    if k < 0:
        raise ValueError('The number of stages must be nonnegative.')
    value = 1
    for i in range(1, k + 1):
        value = i * value + 1
    return value


def function_count(radix: int, stages: int) -> int:
    """Number of complete functions, including the final residue and all carries."""
    if radix < 2 or stages < 0:
        raise ValueError('Require radix >= 2 and stages >= 0.')
    t = min(stages, radix - 1)
    return radix ** (stages - t) * ((radix - 1) * arrangement_number(t) + 1)


def minimum_bits(radix: int, stages: int) -> int:
    return (function_count(radix, stages) - 1).bit_length()


@dataclass(frozen=True)
class Descriptor:
    radix: int
    residue: int
    profiles: tuple[tuple[int, ...], ...]

    def evaluate(self, incoming: Sequence[int]) -> tuple[int, ...]:
        if len(incoming) != len(self.profiles) or any(a not in (0, 1) for a in incoming):
            raise ValueError('Supply one incoming bit per stage.')
        weight, previous = 0, 0
        carries: list[int] = []
        for profile, bit in zip(self.profiles, incoming):
            weight += bit
            current = profile[weight]
            carries.append(current - previous)
            previous = current
        return ((self.residue + weight) % self.radix, *carries)


def describe(radix: int, operands: Sequence[int]) -> Descriptor:
    """Construct a complete canonical function descriptor, not raw-operand storage."""
    if radix < 2 or not operands or any(x < 0 or x >= radix for x in operands):
        raise ValueError('Require radix >= 2 and operands in [0, radix).')
    total = operands[0]
    profiles: list[tuple[int, ...]] = []
    for i, operand in enumerate(operands[1:], 1):
        total += operand
        profiles.append(tuple((total + t) // radix for t in range(i + 1)))
    return Descriptor(radix, total % radix, tuple(profiles))


def encode_two(radix: int, c: int, s: int, h: int) -> int:
    """Dense optimal two-stage label in [0, 5*radix-4)."""
    if radix < 2 or any(x < 0 or x >= radix for x in (c, s, h)):
        raise ValueError('Invalid radix or operand.')
    q, r = divmod(c + s, radix)
    t, v = divmod(r + h, radix)
    cut = 5 * (radix - 2)
    if v < radix - 2:
        kind = 4 if r == radix - 1 else 2 * q + t
        return 5 * v + kind
    kind = 2 if r == radix - 1 else q
    return cut + 3 * (v - (radix - 2)) + kind


def decode_two(radix: int, label: int, a: int, b: int) -> tuple[int, int, int]:
    if radix < 2 or not 0 <= label < 5 * radix - 4 or a not in (0, 1) or b not in (0, 1):
        raise ValueError('Invalid radix, label, or incoming bit.')
    cut = 5 * (radix - 2)
    if label < cut:
        v, kind = divmod(label, 5)
        ca, cb = (a, 1 - a) if kind == 4 else divmod(kind, 2)
    else:
        offset, kind = divmod(label - cut, 3)
        v = radix - 2 + offset
        if kind < 2:
            ca, cb = kind, (a & b if offset == 0 else a | b)
        else:
            ca, cb = a, ((1 - a) | b if offset == 0 else (1 - a) & b)
    return ((v + a + b) % radix, ca, cb)



def _residue_offset(radix: int, stages: int, residue: int) -> int:
    """Offset of a fixed-residue family in the short-stage ordering."""
    a = arrangement_number(stages)
    if residue < radix - stages:
        return residue * a
    e = a - arrangement_number(stages-1)
    return (radix-stages)*a + (residue-radix+stages)*e


def _determined_residue(radix: int, profile: tuple[int, ...]) -> int:
    baseline = profile[0]
    for t, value in enumerate(profile[1:radix], 1):
        if value > baseline:
            return radix-t
    # In the stable regime, no jump within 1..B-1 identifies residue zero.
    return 0


def rank_function(descriptor: Descriptor) -> int:
    """Optimal dense label. Equal complete functions have equal labels.

    The source descriptor must come from describe or unrank_function.
    Cost uses a linear number of recursive stages; integer sizes vary.
    """
    B, v, profiles = descriptor.radix, descriptor.residue, descriptor.profiles
    k = len(profiles)
    if k == 0:
        return v
    q0 = profiles[-2][0] if k > 1 else 0
    q = profiles[-1][0]
    if k >= B:
        r = _determined_residue(B, profiles[-2])
        parent = Descriptor(B, r, profiles[:-1])
        return B*rank_function(parent) + (v-r) % B
    a = arrangement_number(k-1)
    regular = k == 1 or len(set(profiles[-2])) == 1
    if regular:
        parent = Descriptor(B, 0, profiles[:-1])
        p = rank_function(parent)
        local = 2*p + q-q0 if v < B-k else p
    else:
        r = _determined_residue(B, profiles[-2])
        parent = Descriptor(B, r, profiles[:-1])
        p = rank_function(parent) - _residue_offset(B, k-1, r)
        e = a-arrangement_number(k-2)
        first_group = 2*a if v < B-k else a
        local = first_group + (r-(B-k+1))*e + p
    return _residue_offset(B, k, v) + local


def unrank_function(radix: int, stages: int, label: int) -> tuple[int, ...]:
    """Decode a dense label to one operand tuple with exactly that function.

    The returned operands are a representative, not necessarily the originals.
    Every label in [0, function_count(radix, stages)) is valid.
    """
    B, k = radix, stages
    total = function_count(B, k)
    if not 0 <= label < total:
        raise ValueError('The label is outside the complete-function range.')
    if k == 0:
        return (label,)
    if k >= B:
        parent_label, h = divmod(label, B)
        return (*unrank_function(B, k-1, parent_label), h)
    a_k = arrangement_number(k)
    a = arrangement_number(k-1)
    if label < (B-k)*a_k:
        v, local = divmod(label, a_k)
        regular_output = True
        group_size = 2*a
    else:
        v_off, local = divmod(label-(B-k)*a_k, a_k-a)
        v = B-k+v_off
        regular_output = False
        group_size = a
    if local < group_size:
        p, e = divmod(local, 2) if regular_output else (local, 0)
        r = 0 if e == 0 else v+1
        parent_label = _residue_offset(B, k-1, r)+p
    else:
        exceptional = a-arrangement_number(k-2)
        offset, p = divmod(local-group_size, exceptional)
        r = B-k+1+offset
        parent_label = _residue_offset(B,k-1,r)+p
    parent = unrank_function(B,k-1,parent_label)
    return (*parent, (v-r) % B)

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--radix', type=int, default=8)
    parser.add_argument('--stages', type=int, default=3)
    parser.add_argument('--operands', type=str)
    parser.add_argument('--incoming', type=str)
    args = parser.parse_args()
    result: dict[str, object] = {
        'radix': args.radix, 'stages': args.stages,
        'complete_functions': function_count(args.radix, args.stages),
        'minimum_fixed_bits': minimum_bits(args.radix, args.stages),
    }
    if args.operands is not None:
        operands = tuple(map(int, args.operands.split(',')))
        if len(operands) != args.stages + 1:
            parser.error('The operand count must be stages + 1.')
        d = describe(args.radix, operands)
        result['descriptor'] = {'residue': d.residue, 'profiles': d.profiles}
        result['minimal_label'] = rank_function(d)
        result['representative_operands'] = unrank_function(args.radix,args.stages,rank_function(d))
        if args.incoming is not None:
            result['output'] = d.evaluate(tuple(map(int, args.incoming.split(','))))
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
