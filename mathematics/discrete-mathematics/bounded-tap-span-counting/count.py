#!/usr/bin/env python3
"""Exact forward counting by the bounded carry frontier. Python standard library.
Author: lmtlssss🜐. License: MIT.
"""
from __future__ import annotations
import argparse
import json
from dataclasses import dataclass


def linear_word(a: int, w: int, r1: int, r2: int, s: int) -> int:
    mask = (1 << w) - 1
    def rotate(r: int) -> int:
        return ((a >> r) | (a << (w-r))) & mask
    return rotate(r1) ^ rotate(r2) ^ (a >> s)


def count_fiber(w: int, r1: int, r2: int, s: int, D: int, S: int,
                collect_graph: bool = False) -> dict:
    """Return the exact count and one witness; enumerate no complete fiber.

    Each boundary seed is processed separately. The dictionary uses only the
    h input-history bits and their entering carry. Redundant carry data are
    retained as an executable check of the sufficient-state theorem.
    """
    if not 0 < s < r1 < r2 < w:
        raise ValueError('Require 0 < s < r1 < r2 < w.')
    h = r2-s
    if h > 14:
        raise ValueError('This reference interface limits the tap span to 14.')
    mask = (1 << w)-1
    if not (0 <= D <= mask and 0 <= S <= mask):
        raise ValueError('D and S must be unsigned w-bit words.')
    hm = (1 << h)-1
    db = [(D >> j) & 1 for j in range(w)]
    sb = [(S >> j) & 1 for j in range(w)]
    total = 0
    witness = None
    visited = 0
    transitions = 0
    layers = [0]*w
    merges = 0
    peak = 0
    graph = []
    def reverse(v: int) -> int:
        return sum(((v >> j) & 1) << (h-1-j) for j in range(h))
    def op(i: int, current: int, history: int) -> int:
        val = current ^ ((history >> (r2-r1-1)) & 1)
        if i+s < w:
            val ^= (history >> (h-1)) & 1
        return val
    for tail in range(1 << h):
        for guess in (0, 1):
            tail_b = (tail + (D >> (w-h)) + guess) & hm
            ha, hb = reverse(tail), reverse(tail_b)
            # Value: b-history, current carry, path multiplicity, representative.
            states = {(ha, 0): (hb, 0, 1, 0)}
            for j in range(w):
                nxt = {}
                i = (j-r2) % w
                visited += len(states)
                layers[j] += len(states)
                peak = max(peak, len(states))
                for (ah, old), (bh, tin, mult, rep) in states.items():
                    if j == w-h and tin != guess:
                        continue
                    carry = sb[i] ^ op(i, db[j] ^ tin, ah ^ bh)
                    if i == 0 and carry:
                        continue
                    values = ((tail >> (j-w+h)) & 1,) if j >= w-h else (0, 1)
                    for av in values:
                        transitions += 1
                        q = av + db[j] + tin
                        bv, tout = q & 1, q >> 1
                        if j >= w-h and bv != ((tail_b >> (j-w+h)) & 1):
                            continue
                        x, y = op(i, av, ah), op(i, bv, bh)
                        outgoing = (x+y+carry) >> 1
                        an, bn = ((ah << 1) | av) & hm, ((bh << 1) | bv) & hm
                        if i != w-1:
                            dnext = db[(j+1) % w] ^ (0 if j == w-1 else tout)
                            required = sb[i+1] ^ op(i+1, dnext, an ^ bn)
                            if outgoing != required:
                                continue
                        # An input segment and its entering carry reconstruct b.
                        entering = 0 if j+1 < h else (((an ^ bn) >> (h-1)) & 1) ^ db[j+1-h]
                        key = (an, entering)
                        candidate = rep | (av << j)
                        if key in nxt:
                            bb, tt, ct, rr = nxt[key]
                            assert (bb, tt) == (bn, tout), 'Insufficient frontier key.'
                            nxt[key] = (bb, tt, ct+mult, rr)
                            merges += 1
                        else:
                            nxt[key] = (bn, tout, mult, candidate)
                        if collect_graph:
                            graph.append({'seed': [tail, guess], 'layer': j,
                                'from': [ah, old], 'to': list(key),
                                'bit': av, 'multiplicity': str(mult)})
                states = nxt
                if not states:
                    break
            else:
                for _, _, mult, rep in states.values():
                    total += mult
                    if witness is None:
                        witness = rep
    if witness is not None:
        assert (linear_word((witness+D)&mask,w,r1,r2,s)+linear_word(witness,w,r1,r2,s)) & mask == S
    assert visited <= w*(1 << (2*h+2))
    result = {'width': w, 'taps': [r1,r2,s], 'D': str(D), 'S': str(S),
        'count': str(total), 'witness': str(witness) if witness is not None else None,
        'states': visited, 'transitions': transitions, 'merges': merges,
        'peak_per_seed': peak, 'layer_states': layers,
        'state_bound': str(w*(1 << (2*h+2)))}
    if collect_graph:
        result['edges'] = graph
    return result


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('width',type=int)
    p.add_argument('r1',type=int)
    p.add_argument('r2',type=int)
    p.add_argument('shift',type=int)
    p.add_argument('D',type=lambda x:int(x,0))
    p.add_argument('S',type=lambda x:int(x,0))
    a = p.parse_args()
    print(json.dumps(count_fiber(a.width,a.r1,a.r2,a.shift,a.D,a.S),indent=2))

if __name__ == '__main__':
    main()
