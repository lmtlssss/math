#!/usr/bin/env python3
"""Exact all-fiber replay and independent carry-transducer comparison.
Author: lmtlssss🜐. License: MIT.
"""
import json
import random
from pathlib import Path
from inverse import branches, preimages


def direct(x, c, k, w, r=3):
    """Independent reference: rotate by quotient/remainder, then integer sum."""
    a = x // 2 + (x % 2) * (1 << (w - 1))
    b = x // (1 << r) + (x % (1 << r)) * (1 << (w - r))
    return ((a ^ b) + (x & c) + k) % (1 << w)


def transducer(y, c, k, w, r=3):
    """Independent rolling-register path with early cyclic rejection."""
    t = (y - k) % (1 << w)
    answers = []
    for seed in range(1 << r):
        state = seed
        carry = 0
        word = 0
        valid = True
        for i in range(w):
            bit = state & 1
            word |= bit << i
            masked = bit & ((c >> i) & 1)
            q = ((t >> i) & 1) ^ masked ^ carry
            next_bit = ((state >> 1) & 1) ^ q
            carry = (q & masked) | (q & carry) | (masked & carry)
            if i + r >= w and next_bit != ((seed >> (i + r - w)) & 1):
                valid = False
                break
            state = (state >> 1) | (next_bit << (r - 1))
        if valid:
            answers.append(word)
    return sorted(answers)


def main():
    records = []
    for w in range(4, 9):
        target_sets = 0
        max_fiber = 0
        for c in range(1 << w):
            fibers = [[] for _ in range(1 << w)]
            for x in range(1 << w):
                fibers[direct(x, c, 0, w)].append(x)
            for y, expected in enumerate(fibers):
                got = preimages(y, c, 0, w)
                if got != expected:
                    raise AssertionError((w, c, y, got, expected))
                max_fiber = max(max_fiber, len(got))
                target_sets += 1
        records.append({"width": w, "all_masks": 1 << w,
                        "complete_fibers": target_sets,
                        "max_fiber": max_fiber})
    rng = random.Random(0x3B172026)
    wide = 0
    widths = [9, 12, 16, 24, 31, 32, 64, 127, 128, 255, 256, 1024]
    for w in widths:
        for j in range(64):
            c, k, x = (rng.getrandbits(w) for _ in range(3))
            y = direct(x, c, k, w) if j % 2 == 0 else rng.getrandbits(w)
            got = preimages(y, c, k, w)
            assert got == transducer(y, c, k, w)
            assert len(got) <= 8 and len(got) == len(set(got))
            assert all(direct(a, c, k, w) == y for a in got)
            if j % 2 == 0:
                assert x in got
            wide += 1
    extensions = 0
    for w in [6, 8, 10]:
        for r in range(2, min(7, w)):
            for _ in range(8):
                c, k, y = (rng.getrandbits(w) for _ in range(3))
                expected = [x for x in range(1 << w) if direct(x, c, k, w, r) == y]
                assert preimages(y, c, k, w, r) == expected
                extensions += 1
    sharp = {"width": 7, "mask": 127, "constant": 0, "target": 127,
             "preimages": [11, 22, 44, 49, 69, 88, 98, 127]}
    assert preimages(127, 127, 0, 7) == sharp["preimages"]
    assert all(direct(x,127,0,7)==127 for x in sharp["preimages"])
    for width in range(4,129):
        m = (1 << width) - 1
        extreme = preimages(m,m,0,width)
        assert len(extreme) == (8 if width % 7 == 0 else 1) and m in extreme
    traces = list(branches(127,127,0,7))
    assert all(p["accepted"] for p in traces)
    result = {"complete": True, "exhaustive": records,
              "complete_fibers": sum(r["complete_fibers"] for r in records),
              "wider_queries": wide, "wider_widths": widths,
              "general_rotation_queries": extensions,
              "sharp_example": sharp, "extremal_family_widths_checked": [4,128],
              "extremal_family_checks":125,
              "theorem_scope": "Exact prescribed cyclic Boolean-modular maps; all widths by proof."}
    out = Path(__file__).resolve().parent / "evidence"
    out.mkdir(exist_ok=True)
    (out / "verification.json").write_text(json.dumps(result,indent=2)+"\n")
    (out / "sharp-traces.json").write_text(json.dumps({"parameters":sharp,"paths":traces},indent=2)+"\n")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
