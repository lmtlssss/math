# Exact Counts of Sum-and-Carry Functions for Cascaded Addition

**lmtlssss🜐 · 27 October 2026 · Version 1.0.0**

Mathematics / Enumerative combinatorics

[Paper](https://github.com/lmtlssss/math/releases/download/cascade-carry-note-v1.0.0/paper.pdf) · [DOI](https://doi.org/10.5281/zenodo.23700193)

For radix B >= 2, fix operands x0,...,xk. At stage i, add xi and an independently
variable bit ai to the preceding residue. Retain the final residue and every
stage's outgoing carry, for all 2^k assignments of the incoming bits.

The paper counts the distinct complete functions of these incoming bits.
Let A0 = 1, Aj = j A(j-1) + 1, and t = min(k, B-1). The exact count is

    N_k(B) = B^(k-t) ((B-1) A_t + 1).

The proof classifies the possible residue supports of each carry function.
It also gives a dense encoder and decoder. The minimum fixed-length label
therefore has ceil(log2 N_k(B)) bits.

For three 32-bit additions, N_3(2^32) = 68,719,476,721 = 2^36 - 15. A 36-bit
label preserves the complete sum-and-carry function of four 32-bit operands,
including every one of the eight incoming-bit assignments. The decoder returns
one representative operand tuple with the same arithmetic function.

## Reproduce

```sh
python3 verify.py
python3 cascade.py --radix 8 --stages 3 --operands 2,5,7,1 --incoming 1,0,1
make paper
blender -b --python visual/build_scene.py
```

The native Blender builder uses `evidence/figure.json`. Its exact diagram groups
all 4096 operand tuples at B=8, k=3 into 113 complete functions. There are 16
classes at each residue 0 through 4, and 11 at each residue 5 through 7.
`visual/preview.py` creates a vector layout preview; that preview is separately
identified from a native Blender render.

`cascade.py` contains the exact formula, cumulative-profile description, dense
rank/unrank codec, and a direct two-stage codec. `verify.py` compares complete
functions against separately written sequential integer arithmetic.

The two-stage companion is published as *Exact State Complexity of Two-Stage
Addition*, DOI 10.5281/zenodo.23698617. This paper gives the all-stage
extension, with its own source certificate and DOI.

## Mathematical scope

The label preserves the final residue and every outgoing stage carry for all
incoming-bit assignments. Several operand tuples can have the same label.
The original operands are not recovered. The bit minimum is a representation
bound, rather than a running-time or energy measurement. The coefficient
sequence A_k is classical; the manuscript cites its prior sources and related
arithmetic literature.

The release contains the manuscript, exact source, source-derived PNG,
native `.blend`, and verification receipt.

Paper, figure and data: CC BY 4.0. Executable source: MIT. See `LICENSE.md`.
