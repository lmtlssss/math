#!/usr/bin/env python3
"""Exact disjoint affine fibers of L(a+D)+L(a)=S modulo 2**w.
Author: lmtlssss🜐. Code license: MIT. Python standard library only.
Rows encode a binary-linear map, least-significant bit first.
"""
from __future__ import annotations
import argparse
import json
from dataclasses import asdict, dataclass
from typing import Iterable, Iterator, Literal, Sequence

Side = Literal['input', 'output', 'auto']


def linear(x: int, rows: Sequence[int]) -> int:
    """Apply a binary matrix represented by its row masks."""
    return sum(((x & r).bit_count() & 1) << i for i, r in enumerate(rows))


def inverse_rows(rows: Sequence[int]) -> tuple[int, ...]:
    """Invert a square binary matrix by row reduction."""
    w = len(rows)
    if w < 1 or any(r < 0 or r >= 1 << w for r in rows):
        raise ValueError('Supply w row masks, each with exactly w permitted bits.')
    left = list(rows)
    right = [1 << i for i in range(w)]
    for j in range(w):
        p = next((i for i in range(j, w) if (left[i] >> j) & 1), None)
        if p is None:
            raise ValueError('The binary-linear map must be invertible.')
        left[j], left[p] = left[p], left[j]
        right[j], right[p] = right[p], right[j]
        for i in range(w):
            if i != j and ((left[i] >> j) & 1):
                left[i] ^= left[j]
                right[i] ^= right[j]
    return tuple(right)


def signatures(word: int, w: int, side: Literal['input', 'output']) -> Iterator[int]:
    """Enumerate distinct feasible XOR signatures, discarding final carry."""
    stack = [(0, 0, 0)]
    while stack:
        i, carry, prefix = stack.pop()
        bit = ((word >> i) & 1) ^ carry
        value = prefix | (bit << i)
        if i == w - 1:
            yield value
            continue
        branch = bool(bit) if side == 'input' else not bit
        if branch:
            stack.append((i + 1, 1, value))
            stack.append((i + 1, 0, value))
        else:
            stack.append((i + 1, carry, value))


def signature_count(word: int, w: int, side: Literal['input', 'output']) -> int:
    a, b = 1, 0
    for i in range(w - 1):
        bit = (word >> i) & 1
        if side == 'input':
            bit ^= 1
        a, b = (a + b, b) if bit else (a, a + b)
    return a + b


def solve_affine(equations: Iterable[tuple[int, int]], w: int):
    """Return a base and independent nullspace basis, or None."""
    data = [[int(mask), int(rhs)] for mask, rhs in equations]
    pivots = []
    pos = 0
    for j in range(w):
        p = next((i for i in range(pos, len(data)) if (data[i][0] >> j) & 1), None)
        if p is None:
            continue
        data[pos], data[p] = data[p], data[pos]
        for i in range(len(data)):
            if i != pos and ((data[i][0] >> j) & 1):
                data[i][0] ^= data[pos][0]
                data[i][1] ^= data[pos][1]
        pivots.append(j)
        pos += 1
    if any(mask == 0 and rhs for mask, rhs in data):
        return None
    base = sum(data[i][1] << j for i, j in enumerate(pivots))
    basis = []
    for f in range(w):
        if f not in pivots:
            v = 1 << f
            for i, j in enumerate(pivots):
                v |= ((data[i][0] >> f) & 1) << j
            basis.append(v)
    return base, tuple(basis)


@dataclass(frozen=True)
class Cell:
    signature: int
    delta: int
    base: int
    basis: tuple[int, ...]

    @property
    def count(self) -> int:
        return 1 << len(self.basis)

    def members(self) -> Iterator[int]:
        """Output expansion has a cost proportional to the returned points."""
        values = [self.base]
        for v in self.basis:
            values += [x ^ v for x in values]
        yield from values


def cells_for_signature(D: int, S: int, rows: Sequence[int], k: int, delta: int):
    w = len(rows)
    mask = (1 << w) - 1
    low = (1 << (w - 1)) - 1
    din, dout = (delta - D) & mask, (S - k) & mask
    if (din | dout) & 1:
        return None
    u, v = din >> 1, dout >> 1
    am, lm = delta & low, (~k) & low
    if u & ~am or v & ~lm:
        return None
    eqs = [(1 << i, (u >> i) & 1) for i in range(w - 1) if (am >> i) & 1]
    eqs += [(rows[i], (v >> i) & 1) for i in range(w - 1) if (lm >> i) & 1]
    solved = solve_affine(eqs, w)
    return None if solved is None else Cell(k, delta, *solved)


def inverse_fiber(D: int, S: int, rows: Sequence[int], side: Side = 'auto') -> dict:
    """Return every inverse cell and the exact counts of examined signatures."""
    w = len(rows)
    inv = inverse_rows(rows)
    if not (0 <= D < 1 << w and 0 <= S < 1 << w):
        raise ValueError('D and S must be unsigned w-bit words.')
    if side not in ('auto', 'input', 'output'):
        raise ValueError('Side must be auto, input, or output.')
    ni, no = signature_count(D, w, 'input'), signature_count(S, w, 'output')
    if side == 'auto':
        side = 'input' if ni <= no else 'output'
    cells = []
    for sig in signatures(D if side == 'input' else S, w, side):
        if side == 'input':
            delta, k = sig, linear(sig, rows)
        else:
            k, delta = sig, linear(sig, inv)
        cell = cells_for_signature(D, S, rows, k, delta)
        if cell is not None:
            cells.append(cell)
    return dict(width=w, D=D, S=S, rows=list(rows), side=side,
                input_signatures=ni, output_signatures=no,
                signatures_examined=ni if side == 'input' else no,
                count=sum(c.count for c in cells),
                cells=[{**asdict(c), 'count':c.count} for c in cells])


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--rows', required=True, help='Comma-separated row masks, decimal or 0x-prefixed.')
    p.add_argument('--D', required=True, type=lambda x: int(x, 0))
    p.add_argument('--S', required=True, type=lambda x: int(x, 0))
    p.add_argument('--side', choices=['auto', 'input', 'output'], default='auto')
    p.add_argument('--output')
    a = p.parse_args()
    rows = tuple(int(x, 0) for x in a.rows.split(','))
    result = inverse_fiber(a.D, a.S, rows, a.side)
    text = json.dumps(result, indent=2)
    if a.output:
        from pathlib import Path
        Path(a.output).write_text(text + '\n')
    print(text)

if __name__ == '__main__':
    main()
