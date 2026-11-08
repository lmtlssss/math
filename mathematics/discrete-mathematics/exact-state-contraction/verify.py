#!/usr/bin/env python3
"""Exact rational checks for the ᑕ. terminology note. No dependencies."""
from fractions import Fraction as F
from itertools import product
import json


def compose(a, b):
    """b after a: (linear, shift, quadratic, linear_cost, constant)."""
    f, c, q, r, d = a
    g, e, p, t, h = b
    return (
        g * f,
        g * c + e,
        q + p * f * f,
        r + f * (t + 2 * p * c),
        d + h + t * c + p * c * c,
    )


def direct(intervals, x):
    total = F(0)
    for f, c, q, r, d in intervals:
        total += q * x * x + r * x + d
        x = f * x + c
    return x, total


def retained(intervals, x):
    merged = (F(1), F(0), F(0), F(0), F(0))
    for interval in intervals:
        merged = compose(merged, interval)
    f, c, q, r, d = merged
    return f * x + c, q * x * x + r * x + d


def trace_contract(state, controls):
    """An example of a retained observation coordinate."""
    full = state
    short = state[0]
    for u in controls:
        assert full[0] == short
        full = (2 * full[0] + u, full[1] + 1)
        short = 2 * short + u
    assert full[0] == short


def main():
    a = (F(2), F(1), F(1), F(0), F(1))
    b = (F(3), F(-2), F(2), F(3), F(4))
    expected = (F(6), F(1), F(9), F(14), F(10))
    assert compose(a, b) == expected
    assert direct([a, b], F(2)) == (F(13), F(74))

    states = [F(i, 3) for i in range(-6, 7)]
    samples = [
        (F(i + 1, 3), F(j - 2, 4), F(k, 5), F(i - k, 7), F(j + 1, 2))
        for i, j, k in product(range(3), range(3), range(3))
    ]
    count = 0
    for a, b, c in product(samples[::6], repeat=3):
        assert compose(compose(a, b), c) == compose(a, compose(b, c))
        for x in states:
            assert direct([a, b, c], x) == retained([a, b, c], x)
            count += 1
    for x, y in product(range(-3, 4), repeat=2):
        for controls in product((-1, 0, 1), repeat=4):
            trace_contract((x, y), controls)
    result = {
        "schema": "taa.exact-state-contraction.example.v1",
        "result": "pass",
        "example_coefficients": [str(x) for x in expected],
        "example_at_x_2": {"state": 13, "cost": 74},
        "rational_composition_cases": count,
        "trace_cases": 49 * 81,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
