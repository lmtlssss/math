#!/usr/bin/env python3
"""Whole-input verification. See VERIFICATION_PLAN.md before modifying it."""
from __future__ import annotations
from itertools import product
from pathlib import Path
from collections import defaultdict
import argparse, json, random, time
from frontier import solve, direct


def ripple_reference(w, aa, mm, tt, im=0, it=0):
    """Full carry-vector DP. Uses no thresholds, ranks or sorting."""
    d = {(0,) * len(aa): (1, 0)}
    max_states = 1
    for i in range(w):
        nxt = {}
        for carry, (number, witness) in d.items():
            for bit in (0, 1):
                if ((im >> i) & 1) and bit != ((it >> i) & 1):
                    continue
                nc = []
                valid = True
                for j, a in enumerate(aa):
                    v = bit + ((a >> i) & 1) + carry[j]
                    if ((mm[j] >> i) & 1) and (v & 1) != ((tt[j] >> i) & 1):
                        valid = False
                        break
                    nc.append(v >> 1)
                if valid:
                    key = tuple(nc)
                    old = nxt.get(key, (0, None))
                    x = witness | (bit << i)
                    nxt[key] = (old[0] + number, x if old[1] is None else min(x, old[1]))
        d = nxt
        max_states = max(max_states, len(d))
    return sum(v[0] for v in d.values()), min((v[1] for v in d.values()), default=None), max_states


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', default='evidence/verification.json')
    args = p.parse_args()
    start = time.perf_counter()
    rng = random.Random(2026102708)
    counts = {'carry_panels': 0, 'prefixes_checked': 0, 'residual_pairs': 0,
              'complete_queries': 0, 'direct_inputs': 0, 'wide_queries': 0}
    # Every offset tuple in these domains, and every prefix at every cut.
    for w in range(1, 6):
        for m in range(1, 4):
            if w * m > 12:
                continue
            for aa in product(range(1 << w), repeat=m):
                for i in range(w + 1):
                    M = 1 << i
                    groups = {}
                    for u in range(M):
                        key = tuple(((a % M) + u) // M for a in aa)
                        groups.setdefault(key, []).append(u)
                    expected = 1 + len({a % M for a in aa} - {0})
                    assert len(groups) == expected <= min(m + 1, M)
                    vectors = sorted(groups)
                    assert all(all(a <= b for a, b in zip(v, v2))
                               for v, v2 in zip(vectors, vectors[1:]))
                    # The first remaining output bit separates every pair.
                    if i < w:
                        symbols = {tuple(((a >> i) + c) & 1 for a, c in zip(aa, v))
                                   for v in vectors}
                        assert len(symbols) == len(vectors)
                        counts['residual_pairs'] += len(vectors) * (len(vectors) - 1) // 2
                    counts['carry_panels'] += 1
                    counts['prefixes_checked'] += M
    # Every input is tested in each complete query. Cases include empty results,
    # planted results, duplicate constants, zero offsets and contradictory masks.
    small_examples = []
    for w in range(1, 11):
        B = 1 << w
        for m in (1, 2, 3, 5, 8, 16):
            for q in range(64):
                aa = [rng.randrange(B) for _ in range(m)]
                if q % 8 == 0: aa = [0] * m
                elif q % 8 == 1: aa = [aa[0]] * m
                elif q % 8 == 2: aa[0] = B - 1
                mm = [rng.randrange(B) for _ in range(m)]
                tt = [rng.randrange(B) & u for u in mm]
                im = rng.randrange(B) if q % 4 else 0
                it = rng.randrange(B) & im
                if q & 1:
                    x = rng.randrange(B)
                    tt = [((x + a) % B) & u for a, u in zip(aa, mm)]
                    it = x & im
                got = solve(w, aa, mm, tt, input_mask=im, input_target=it)
                want = direct(w, aa, mm, tt, im, it)
                ref = ripple_reference(w, aa, mm, tt, im, it)
                assert got['count'] == len(want) == ref[0], (w, aa, mm, tt, got, want)
                assert got['witness'] == (want[0] if want else None) == ref[1]
                assert got['maximum_carry_states'] <= min(m + 1, B)
                assert got['transition_attempts'] == 2 * got['source_states'] <= 2 * w * (m + 1)
                counts['complete_queries'] += 1
                counts['direct_inputs'] += B
    wide = []
    for w in (16, 32, 64, 128, 256, 512, 1024):
        B = 1 << w
        for m in (2, 8, 32, 64):
            for q in range(6):
                aa = [rng.getrandbits(w) for _ in range(m)]
                x = rng.getrandbits(w)
                mm = []
                for j in range(m):
                    u = 0
                    for _ in range(2): u |= 1 << rng.randrange(w)
                    mm.append(u)
                tt = [((x + a) % B) & u for a, u in zip(aa, mm)]
                if q == 0: mm = [0] * m; tt = [0] * m
                got = solve(w, aa, mm, tt)
                ref = ripple_reference(w, aa, mm, tt)
                assert (got['count'], got['witness']) == ref[:2]
                assert got['count'] > 0
                assert all(((got['witness'] + a) % B) & u == t for a,u,t in zip(aa,mm,tt))
                assert got['maximum_carry_states'] <= m+1
                counts['wide_queries'] += 1
                if w == 256 and m == 32 and q == 1:
                    wide.append({'offsets':aa, 'masks':mm, 'targets':tt,
                                 'known_input':x, 'result':got, 'reference_count':ref[0]})
    # A fully specified diagram: five shared offsets at the cut after 8 low bits.
    offsets = [13, 45, 93, 157, 221]
    M = 256
    groups = defaultdict(list)
    for u in range(M):
        groups[tuple(int(u+a>=M) for a in offsets)].append(u)
    figure = {'width':9,'cut':8,'offsets':offsets,'possible_carry_patterns':32,
              'reachable_carry_patterns':len(groups),
              'classes':[{'carry':list(c),'members':v,'size':len(v),'start':min(v),'end':max(v)}
                         for c,v in sorted(groups.items())]}
    assert len(groups)==6 and sum(len(v) for v in groups.values())==256
    result = {'status':'pass','counts':counts,'wide_example':wide[0],
              'figure_class_sizes':[d['size'] for d in figure['classes']],
              'seconds':time.perf_counter()-start,
              'scope':'Exact arithmetic implementation verification; universal statements proved in paper.tex.'}
    output=Path(args.output);output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,indent=2)+'\n')
    (output.parent/'figure.json').write_text(json.dumps(figure,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'counts':counts,'wide_result':wide[0]['result'],
                      'figure_class_sizes':result['figure_class_sizes'],'seconds':result['seconds']},indent=2))

if __name__=='__main__':main()
