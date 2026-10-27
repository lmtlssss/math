# Exact State Complexity of Two-Stage Addition

**lmtlssss🜐 · 27 October 2026 · Version 1.0.0**

Mathematics / Discrete mathematics

[Paper](https://github.com/lmtlssss/math/releases/download/addition-state-note-v1.0.0/paper.pdf) · [DOI](https://doi.org/10.5281/zenodo.23698617)

For fixed radix-B operands C,S,H, add C+S+a modulo B, then add H+b.
The incoming carries a,b each range over zero and one. The response consists
of the residue and both outgoing carries for all four inputs.

There are exactly 5B-4 distinct complete response functions for every B >= 2.
The manuscript proves a normal form, constructive representatives, class
multiplicities, a contiguous code, and its exact fixed-length bit bound.
For B=2^32 the code needs precisely 35 bits. It preserves the response, not
the original 96 operand bits. Four separately queryable byte stages require
42 bits under their explicitly stronger output contract.

## Reproduce

```sh
python3 verify.py
g++ -O3 -std=c++17 verify_full.cpp -o /tmp/addition-state-verify
/tmp/addition-state-verify
python3 state.py --radix 256 --C 37 --S 218 --H 13
make paper
blender -b --threads 4 --python visual/build_scene.py
```

The example gives state 62 and outputs (12,0,1), (13,0,1), (13,1,0),
(14,1,0) for incoming pairs 00,01,10,11. Exactly 256 operand triples share
that response.

The figure uses all 512 radix-eight operand triples and their 36 exact
response classes. The highlighted class has representative (0,7,6).
Each displayed source-to-class link comes from the included encoder.

`state.py` contains the encoder, decoder, representatives and stage composition.
`verify.py` compares full functions with a separate arithmetic oracle.
`verify_full.cpp` checks every binary operand triple through eight bits.
`evidence/` records the observed census and exact figure data.
`paper.tex` contains the general proofs and references.

Paper, figure and data: CC BY 4.0. Code: MIT. See `LICENSE.md`.
