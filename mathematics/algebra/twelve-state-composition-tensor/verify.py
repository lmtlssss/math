#!/usr/bin/env python3
"""Exact certificate verification for a twelve-state composition tensor.

Author: lmtlssss🜐
Python 3.9 or later; standard library only.
"""
import argparse
import json
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path

MAPS = (
    (0, 0, 0, 0), (0, 0, 0, 1), (0, 1, 1, 1),
    (0, 1, 2, 2), (0, 1, 2, 3), (1, 1, 1, 1),
    (1, 1, 2, 2), (1, 1, 2, 3), (2, 2, 2, 2),
    (2, 2, 2, 3), (2, 3, 3, 3), (3, 3, 3, 3),
)
GENERATORS = (1, 2, 3, 7, 9, 10)
RANKS = (3, 2, 3, 2, 1, 5, 4, 2, 5, 3, 2, 3)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def compose(first, second):
    """Return second after first, matching the paper's product convention."""
    return tuple(second[first[x]] for x in range(4))


def determinant(matrix):
    """Gaussian elimination over the rationals, without rounding."""
    a = [[Fraction(x) for x in row] for row in matrix]
    n, result = len(a), Fraction(1)
    for col in range(n):
        pivot = next((row for row in range(col, n) if a[row][col]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            result = -result
        value = a[col][col]
        result *= value
        for row in range(col + 1, n):
            ratio = a[row][col] / value
            for j in range(col + 1, n):
                a[row][j] -= ratio * a[col][j]
            a[row][col] = Fraction(0)
    return result


def indices(values, label):
    require(isinstance(values, list) and len(values) > 0, label + ': empty set')
    require(all(type(x) is int and 0 <= x < 12 for x in values),
            label + ': invalid index')
    require(len(set(values)) == len(values), label + ': duplicate index')
    return values


def verify(path):
    with path.open(encoding='utf-8') as stream:
        data = json.load(stream)
    require(data['schema'] == 'composition-tensor-certificate-v1', 'schema')
    require(data['maps'] == [list(x) for x in MAPS], 'map labels')
    require(data['generator_indices'] == list(GENERATORS), 'generators')
    require(data['identity_index'] == 4, 'identity label')
    require(data['slice_ranks'] == list(RANKS), 'claimed slice ranks')
    require(data['nonnegative_tensor_rank'] == 35, 'claimed tensor rank')

    lookup = {m: i for i, m in enumerate(MAPS)}
    require(len(lookup) == 12, 'distinct maps')
    table = []
    for first in MAPS:
        row = []
        for second in MAPS:
            value = compose(first, second)
            require(value in lookup, 'closure')
            row.append(lookup[value])
        table.append(row)
    require(data['multiplication_table'] == table, 'composition table')
    for i in range(12):
        require(table[4][i] == i == table[i][4], 'identity')
    for i, j, k in product(range(12), repeat=3):
        require(table[table[i][j]][k] == table[i][table[j][k]], 'associativity')
    generated = {MAPS[4]}
    while True:
        enlarged = generated | {
            compose(value, MAPS[g]) for value in generated for g in GENERATORS
        }
        if enlarged == generated:
            break
        generated = enlarged
    require(generated == set(MAPS), 'generated monoid')

    counts = [[[0] * 12 for _ in range(12)] for _ in range(12)]
    per_output = [0] * 12
    rectangles = data['rectangles']
    require(len(rectangles) == 35, 'rectangle count')
    for r, rectangle in enumerate(rectangles):
        k = rectangle['output']
        require(type(k) is int and 0 <= k < 12, 'rectangle output')
        left = indices(rectangle['left'], 'left ' + str(r))
        right = indices(rectangle['right'], 'right ' + str(r))
        per_output[k] += 1
        for i, j in product(left, right):
            require(table[i][j] == k, 'rectangle crosses an output slice')
            counts[i][j][k] += 1
    for i, j, k in product(range(12), repeat=3):
        require(counts[i][j][k] == int(table[i][j] == k),
                'coefficient mismatch at ' + str((i, j, k)))
    require(tuple(per_output) == RANKS, 'upper-bound vector')

    witnesses = data['witnesses']
    require(len(witnesses) == 12, 'witness slices')
    determinants = []
    for k, entries in enumerate(witnesses):
        require(len(entries) == RANKS[k], 'witness count')
        for pair in entries:
            require(isinstance(pair, list) and len(pair) == 2, 'witness pair')
            require(all(type(v) is int and 0 <= v < 12 for v in pair),
                    'witness range')
        pairs = [tuple(pair) for pair in entries]
        require(len(set(pairs)) == len(pairs), 'duplicate witness')
        require(all(table[i][j] == k for i, j in pairs), 'witness membership')
        for (i, j), (u, v) in combinations(pairs, 2):
            require(table[i][v] != k or table[u][j] != k, 'fooling condition')
        rows = [i for i, _ in pairs]
        cols = [j for _, j in pairs]
        require(len(set(rows)) == len(rows) and len(set(cols)) == len(cols),
                'minor has repeated indices')
        minor = [[int(table[i][j] == k) for j in cols] for i in rows]
        value = determinant(minor)
        require(value == 1, 'witness minor determinant')
        determinants.append(int(value))
    require(sum(len(x) for x in witnesses) == 35, 'lower bound')
    return {
        'status': 'PASS',
        'monoid_order': 12,
        'composition_entries': 144,
        'tensor_coefficients': 1728,
        'rectangle_terms': 35,
        'fooling_witnesses': 35,
        'slice_ranks': list(RANKS),
        'minor_determinants': determinants,
        'nonnegative_tensor_rank': 35,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('certificate', nargs='?', type=Path,
                        default=Path(__file__).with_name('certificate.json'))
    args = parser.parse_args()
    try:
        result = verify(args.certificate)
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, 'Verification failed: ' + str(error) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
