# Ordered Carry Frontiers for Parallel Addition

**lmtlssss🜐 · 27 October 2026 · Version 1.0.0**

Mathematics / Arithmetic automata and exact counting

[Paper](https://github.com/lmtlssss/math/releases/download/shared-input-note-v1.0.0/paper.pdf) · [DOI](https://doi.org/10.5281/zenodo.23702847)

For m fixed offsets added to the same radix-B input, the joint carry vector at
cut i has exactly one plus the number of distinct nonzero offset residues
modulo B^i possible values. These vectors form a chain. At a nonterminal cut,
they are exactly the residual classes needed to preserve every future output.

The sharp bound is min(m+1, B^i). Thirty-two parallel binary additions have
at most 33 carry states. Six bits suffice to label that carry interface, when
the offsets and cut are known. The label records the carry state, rather than
the complete inputs or sums.

The binary solver counts all inputs satisfying arbitrary masks on the shared
word and every translated sum. It also returns the least satisfying input.
The constructor and counter use O(wm) wide-integer operations, at most
2w(m+1) transition attempts, and O(m) wide-integer storage with trace collection
disabled. The paper states elementary bit complexity separately.

## Reproduce

```sh
python3 verify.py --output evidence/replay-verification.json
python3 frontier.py --width 9 --offsets 13,45,93,157,221 --masks 15,31,7,3,127 --targets 6,22,6,2,102
make paper
blender -b --python visual/build_scene.py
```

The example query returns four solutions and the least input 9.
The whole-input verifier compares 3,840 complete masked queries with direct
addition and a separately written full-vector carry counter. It also checks
prefix classes, residual separation, and cases through 1,024 bits.

The native Blender scene uses all 256 prefixes at an eight-bit cut and the
five offsets 13, 45, 93, 157, 221. The six exact classes contain
35, 64, 64, 48, 32 and 13 prefixes. `evidence/figure.json` specifies every
source-to-state connection. The PNG and editable scene are release assets.

The threshold ordering extends a two-sum, three-state lemma to arbitrary
numbers of sums and arbitrary radices. The paper proves the exact all-output
state count, residual lower bound, linear constructor, and masked counter.
Automata and decision-diagram methods are established prior work, cited in
the manuscript. This paper makes no worldwide algorithmic-priority claim.

Paper, figure and data: CC BY 4.0. Executable source: MIT. See `LICENSE.md`.
