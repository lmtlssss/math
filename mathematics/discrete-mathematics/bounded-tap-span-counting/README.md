# Exact Counting for a Boolean–Modular Equation with Bounded Tap Span

**lmtlssss🜐 · 27 October 2026 · Version 1.0.0**

Mathematics / Discrete mathematics and algorithms

[Paper](https://github.com/lmtlssss/math/releases/download/short-frontier-note-v1.0.0/paper.pdf) · [DOI](https://doi.org/10.5281/zenodo.23697063)

For `L_w(x) = ROR_r1(x) XOR ROR_r2(x) XOR SHR_s(x)`, solve
`L_w(a+D) + L_w(a) = S modulo 2^w`, with `0 < s < r1 < r2 < w`.
Set `h = r2-s`. For a fixed cyclic boundary, the last h input bits and one entering carry determine every legal continuation. The target and input difference determine the output carry exactly.

The count-and-witness algorithm visits at most `w * 2^(2h+2)` nonterminal states, with at most two transitions per state. For fixed h, the state bound is linear in w. A conservative arbitrary-precision implementation uses `O(w^2 * 2^(2h+2))` bit operations. An explicit list of all solutions has its own output-size cost.

## Exact example

The supplied 256-bit instance has **5,784,112,988,160 solutions**. The native suffix solver visits **558,622 states** and checks **1,115,268 transitions**. All 1,024 cyclic boundary choices are included. `evidence/example256.json` gives every parameter, the complete count, one witness, and the per-layer state counts.

These are exact instance results. The state bound is a theorem for the displayed equation family. The construction does not assume that L is invertible.

## Reproduce

The verifier requires Python 3.10 or later, a C++17 compiler and Boost multiprecision headers. It uses no network services.

```sh
python3 verify.py --bootstrap
python3 run_example.py
make paper
```

The replay compares 21,760 complete small-width fibers with direct enumeration. It also checks 840 queries covering every permitted tap triple at widths 4 through 8, and 54 saved cases through 256 bits. The saved cases compare the native suffix solver, a canonical Python forward solver, and a Python solver with explicit output carries.

The C++ reference limits width to 512 and span to 12. The Python reference limits span to 14. These are explicit implementation limits; the theorem holds for every permitted width and tap span. An interrupted native run reports `complete: false`.

## Files

`paper.tex` contains the full proof and references. `frontier.cpp`, `count.py` and `reference.py` are the three exact implementations. `check_small.cpp` provides the independent forward histogram comparison. `verify.py` runs the published replay. `evidence/verification.json` records the result.

`visual/graph.json` is a complete accepted-transition trace for a separate 24-bit illustration. It has 224 solutions and 496 forward state visits. `visual/build_scene.py` constructs its native Blender figure. The figure is not a timing comparison or a drawing of the 256-bit example.

The manuscript credits the established S-function and finite-state arithmetic literature. The contribution is the sufficient frontier and exact cyclic-boundary construction for this particular equation.

Paper, figure and data: CC BY 4.0. Code: MIT. See `LICENSE.md` and `CITATION.cff`.
