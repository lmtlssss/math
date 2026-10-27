# Two Sparse Binary Operators with Optimal Generating Length

**lmtlssss🜐 · 27 October 2026 · Version 1.0.0**

Mathematics / Algebra

[Paper](https://github.com/lmtlssss/math/releases/download/binary-algebra-note-v1.0.0/paper.pdf) · [DOI](https://doi.org/10.5281/zenodo.23701587)

On 32-bit vectors over F2, set

    A = ROR7 + ROR18 + SHR3
    B = ROR17 + ROR19 + SHR10.

The operators generate the full 32-by-32 matrix algebra. Their generating length
is exactly ten, the smallest possible length for any generating pair in this
dimension. Every binary linear map is an XOR sum of basis words, each at most
ten factors long. The statement concerns sums of words, not a single product.

A second proof uses D = B^3 + A and

    p(t) = t^31 + t^29 + t^27 + t^25 + t^19 + t^11 + t^9 + t.

The exact identity p(D) = u v^T holds for u=0xaeb51dbb and v=0xddb8ad75.
Both cyclic bases under A are invertible. Thus A^i p(D) A^j, for 0<=i,j<32,
form a constructive basis. The same identities hold in every field of
characteristic two.

## Reproduce

```sh
python3 verify.py
python3 algebra.py --elementary 5 17
make paper
blender -b --python visual/build_scene.py
```

The verifier independently reconstructs matrices by coordinate rows. It checks
both proof certificates and synthesizes every elementary matrix through both
bases. `paper.tex` contains the proof and inverse-matrix table.

The exact cumulative dimensions for word lengths 0 through 10 are
1,3,7,15,31,63,127,255,510,991,1024.

## Files and scope

`evidence/short-word-certificate.json` lists the 1024 basis words.
`evidence/rank-one-certificate.json` contains the polynomial, vectors and two
inverse matrices. `algebra.py` gives the exact construction and synthesis.
`verify.py` uses separate row arithmetic. The native Blender figure displays
both sparse matrices, every prefix edge in the word certificate, and the 33
additional basis directions at length ten.

The general rank-one criterion and word-length framework are established
mathematics. This paper records a specific sparse pair and its exact
certificates. The result is a linear-algebra statement, not a running-time or
energy measurement. It preserves the distinction between linear maps and
nonlinear computations.

Paper, figure and data: CC BY 4.0. Executable source: MIT. See `LICENSE.md`.
