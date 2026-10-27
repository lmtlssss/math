# Twenty Signed Products for a Twelve-State Composition Tensor

**lmtlssss🜐 · 27 October 2026 · Version 1.0.0**

Mathematics / Algebraic complexity

[Paper](https://github.com/lmtlssss/math/releases/download/signed-tensor-note-v1.0.0/paper.pdf) · [DOI](https://doi.org/10.5281/zenodo.23695066)

The composition tensor of the specified twelve-element monoid has an integer
factorization with twenty signed rank-one terms. Its nonnegative rank is
exactly 35. The signed real rank lies between 18 and 20.

For each positive integer q, the nonnegative rank of the tensor power is
35^q. The signed construction uses at most 20^q products. The ratio is
at least (7/4)^q. Each tensor-power input has 12^q coordinates.

The manuscript gives the complete coordinate formulas and proof. It cites
Strassen's seven-product matrix algorithm and the Alder–Strassen lower bound.
The exact signed minimum remains in {18, 19, 20}.

## Reproduce

Run `python3 verify.py`. The verifier uses only the Python standard library.
It checks all 1,728 tensor coefficients with exact integers and separately
checks the constructive algorithm on all 144 basis input pairs. It also checks
the monoid, quotient, radical, positive rectangle partition, and lower-bound
witnesses. The tensor-square check covers 749,700 witness pairs.

Run `make paper` to compile the manuscript with XeLaTeX. The fonts match the
preceding nonnegative-rank paper. Run
`blender -b --python visual/build_scene.py` to reconstruct the native figure.

## Files

`paper.tex` contains the manuscript. `certificate.json` contains the indexed
maps, exact product table, coordinate matrix, signed factors and positive
certificates. `verify.py` checks these objects. `evidence/verification.json`
records the completed exact run. `visual/build_scene.py` constructs the
editable figure from the certificate.

The release contains the PDF, PNG, native Blender project and source package.
Paper, figure and certificate: CC BY 4.0. Executable code: MIT.
