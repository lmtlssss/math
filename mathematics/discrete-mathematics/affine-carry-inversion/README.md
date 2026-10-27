# Affine Fibers and a Fibonacci Bound for Boolean–Modular Inversion

**lmtlssss🜐 · 27 October 2026 · Version 1.0.0**

Mathematics / Discrete mathematics

[Paper](https://github.com/lmtlssss/math/releases/download/affine-carry-note-v1.0.0/paper.pdf) · [DOI](https://doi.org/10.5281/zenodo.23697726)

For any invertible binary-linear map L on w-bit words, the complete inverse of
L(a+D)+L(a)=S modulo 2^w is a disjoint union of affine binary cells. Each cell
comes from one feasible XOR signature. Two carry automata provide alternative
signature lists. The algorithm enumerates the smaller list.

Each list has at most F_(w+1) signatures. Binary elimination gives a conservative
O(w^3 F_(w+1)) bit-operation bound for compact output. This bound applies to dense
maps as well as maps with short bit dependencies. For two reflection targets,
the complete inverse is a single mask equation or the empty set.

## Reproduce

```sh
python3 verify.py
python3 atlas.py --rows 34,68,134,14,213,186,122,142 --D 30 --S 146
make paper
blender -b --python visual/build_scene.py
```

The example returns five disjoint affine cells of sizes 1, 2, 2, 4 and 8, for a
total of 17 solutions. It considers 13 input signatures rather than 26 output
signatures. The figure is built from this exact example.

The verifier compares 65,532 complete small-width fibers across three enumeration
modes. It checks direct addition-derived signatures, the sharp Fibonacci maxima,
full 32-bit reflection examples and wide certificates through 512 bits.

`paper.tex` contains all proofs. `atlas.py` is the standard-library inverse.
`verify.py` uses an independent bit-by-bit forward oracle. `evidence/figure.json`
contains exact cells, signatures and members. `visual/build_scene.py` builds the
native Blender scene. The proof concerns compact output; listing every solution
adds a cost proportional to the output size. Signature counts are not speed ratios.

Paper, figure and data: CC BY 4.0. Code: MIT. See `LICENSE.md`.
