#!/usr/bin/env python3
"""Exact masked counting for fixed-offset sums sharing one input.

The implementation uses ordered threshold ranks. It does not construct the
2**m set of independent carry patterns. Python integers preserve exact counts.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence
import argparse, json

@dataclass(frozen=True)
class Layer:
    width: int
    boundaries: tuple[int, ...]  # 0, interior thresholds, 2**width
    switches: tuple[int, ...]   # first state where each carry is 1
    @property
    def states(self) -> int:
        return len(self.boundaries) - 1


def _layer(width: int, thresholds: Sequence[int], order: Sequence[int]) -> Layer:
    limit = 1 << width
    boundaries = [0]
    switches = [0] * len(thresholds)
    for j in order:
        t = thresholds[j]
        if t < limit and t != boundaries[-1]:
            boundaries.append(t)
        switches[j] = len(boundaries) - 1 if t < limit else -1
    count = len(boundaries)
    for j, t in enumerate(thresholds):
        if t == limit:
            switches[j] = count
    boundaries.append(limit)
    return Layer(width, tuple(boundaries), tuple(switches))


def _successors(current: Layer, following: Layer, bit: int) -> tuple[int, ...]:
    """Two ordered sweeps replace separate binary searches."""
    target = []
    r = 0
    shift = bit << current.width
    for left in current.boundaries[:-1]:
        v = left + shift
        while r + 1 < following.states and following.boundaries[r + 1] <= v:
            r += 1
        target.append(r)
    return tuple(target)


def solve(width: int, offsets: Sequence[int], masks: Sequence[int] | None = None,
          targets: Sequence[int] | None = None, *, input_mask: int = 0,
          input_target: int = 0, keep_trace: bool = False) -> dict:
    """Return the exact count and least input satisfying every masked sum.

    All sums are modulo 2**width. Set bits in a target must also be set in its
    corresponding mask. Trace collection is optional and is not part of the
    streaming memory bound.
    """
    if not isinstance(width, int) or isinstance(width, bool) or width < 1:
        raise ValueError('width must be a positive integer')
    aa = tuple(offsets)
    if not aa:
        raise ValueError('at least one offset is required')
    limit = 1 << width
    m = len(aa)
    mm = (0,) * m if masks is None else tuple(masks)
    tt = (0,) * m if targets is None else tuple(targets)
    if len(mm) != m or len(tt) != m:
        raise ValueError('offsets, masks and targets must have equal length')
    for v in aa + mm + tt + (input_mask, input_target):
        if not isinstance(v, int) or isinstance(v, bool) or not 0 <= v < limit:
            raise ValueError('every word must be an unsigned word of the given width')
    if input_target & ~input_mask or any(t & ~u for t, u in zip(tt, mm)):
        raise ValueError('target bits must be contained in the corresponding mask')
    thresholds = [1] * m
    order = list(range(m))
    current = _layer(0, thresholds, order)
    counts = [1]
    witnesses: list[int | None] = [0]
    trace = []
    attempted = accepted = source_states = 0
    max_width = 1
    for i in range(width):
        span = 1 << i
        bits = [(a >> i) & 1 for a in aa]
        order = [j for j in order if bits[j]] + [j for j in order if not bits[j]]
        thresholds = [t + (1 - e) * span for t, e in zip(thresholds, bits)]
        following = _layer(i + 1, thresholds, order)
        next_counts = [0] * following.states
        next_witnesses: list[int | None] = [None] * following.states
        source_states += current.states
        max_width = max(max_width, current.states, following.states)
        row = {'bit': i, 'states': current.states, 'next_states': following.states,
               'prefixes': sum(counts), 'live_states': sum(c > 0 for c in counts),
               'edges': []} if keep_trace else None
        for b in (0, 1):
            dest = _successors(current, following, b)
            lo, hi = 0, current.states - 1
            if (input_mask >> i) & 1 and b != ((input_target >> i) & 1):
                lo, hi = 1, 0
            for j in range(m):
                if (mm[j] >> i) & 1:
                    required = b ^ bits[j] ^ ((tt[j] >> i) & 1)
                    if required:
                        lo = max(lo, current.switches[j])
                    else:
                        hi = min(hi, current.switches[j] - 1)
            for r, n in enumerate(counts):
                attempted += 1
                allowed = lo <= r <= hi
                if row is not None:
                    row['edges'].append([r, b, dest[r], allowed, n])
                if not n or not allowed:
                    continue
                accepted += 1
                d = dest[r]
                next_counts[d] += n
                witness = witnesses[r]
                assert witness is not None
                candidate = witness | (b << i)
                if next_witnesses[d] is None or candidate < next_witnesses[d]:
                    next_witnesses[d] = candidate
        if row is not None:
            row['next_counts'] = next_counts[:]
            trace.append(row)
        current, counts, witnesses = following, next_counts, next_witnesses
    valid = [v for v in witnesses if v is not None]
    result = {'count': sum(counts), 'witness': min(valid) if valid else None,
              'width': width, 'outputs': m, 'maximum_carry_states': max_width,
              'source_states': source_states, 'transition_attempts': attempted,
              'accepted_live_edges': accepted, 'final_state_counts': counts}
    if keep_trace:
        result['trace'] = trace
    return result


def direct(width: int, offsets: Sequence[int], masks: Sequence[int],
           targets: Sequence[int], input_mask: int = 0, input_target: int = 0) -> list[int]:
    """Small-domain integer oracle; deliberately independent of carry code."""
    word_mask = (1 << width) - 1
    return [x for x in range(1 << width)
            if x & input_mask == input_target
            and all(((x + a) & word_mask) & u == t
                    for a, u, t in zip(offsets, masks, targets))]


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--width', type=int, required=True)
    p.add_argument('--offsets', type=str, required=True)
    p.add_argument('--masks', type=str)
    p.add_argument('--targets', type=str)
    p.add_argument('--input-mask', type=lambda s: int(s, 0), default=0)
    p.add_argument('--input-target', type=lambda s: int(s, 0), default=0)
    a = p.parse_args()
    parse = lambda s: [int(v, 0) for v in s.split(',')] if s is not None else None
    print(json.dumps(solve(a.width, parse(a.offsets), parse(a.masks), parse(a.targets),
                           input_mask=a.input_mask, input_target=a.input_target), indent=2))

if __name__ == '__main__':
    main()
