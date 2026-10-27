# A Three-Bit Boundary for Cyclic Boolean–Modular Inversion

**lmtlssss🜐 · 27 October 2026 · Version 1.0.0**

Mathematics / Discrete mathematics

[Paper](https://github.com/lmtlssss/math/releases/download/three-bit-note-v1.0.0/paper.pdf) · [DOI](https://doi.org/10.5281/zenodo.23680529)

For a word of width w >= 4, consider

F(x) = ((ROR1(x) XOR ROR3(x)) + (x AND c) + k) modulo 2^w.

Every preimage of a supplied target is determined by one of eight assignments to the first three input bits. The exact solver uses w local updates per assignment, then checks three cyclic closure equations. It returns the entire fiber, including an empty fiber.

The bound of eight preimages is sharp. With c = y = 2^w - 1 and k = 0, the fiber has eight members exactly when seven divides w, and one otherwise. The proof reduces this family to one fixed state and a seven-cycle on the remaining three-bit states.

## Files

`paper.tex` contains the complete proof, the periodic sharpness theorem, a worked arithmetic certificate, the r-bit extension, and references to finite-state prior work. `inverse.py` is the standard-library solver. `verify.py` compares complete fibers with direct forward enumeration and a separately written rolling-state solver. `evidence/sharp-traces.json` supplies all eight branches of the worked example. `visual/build_scene.py` constructs the Blender illustration from those traces.

## Reproduce

```sh
python3 verify.py
python3 inverse.py --width 7 --mask 127 --target 127
make paper
```

Expected inverse: `11, 22, 44, 49, 69, 88, 98, 127`.

The complete-fiber checks cover every mask and target at widths 4 through 8 with k = 0: 87,296 fibers. A further 768 queries cover widths through 1024, and 112 queries check the r-bit extension. The general completeness and complexity statements are proved in the manuscript; the checks supplement the proof.

## Figure

The native Blender scene shows eight boundary states and their actual bit paths for w = 7, c = y = 127, k = 0. The final three bits repeat the initial three bits on every path. Each bead and line is generated from the supplied recurrence trace.

## Scope

The result concerns the displayed map. The number 8w counts local bit updates. Preprocessing and writing output add linear work. The manuscript treats finite-state propagation as an established method and records this map's explicit inverse and sharp fiber bound.

Paper, figure and data: CC BY 4.0. Executable source: MIT. See `LICENSE.md`. Citation: `CITATION.cff` or `CITATION.bib`.
