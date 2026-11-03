# Exact verification record

The mathematical verifier completed successfully with exact rational arithmetic.

| Certificate | Observed result |
| --- | --- |
| Named words | 5 |
| Deterministic additional words | 64 |
| Nontrivial cyclic cut identities | 165 |
| Zero-cut normalizations | 69 |
| Principal prefix rank | 2 |
| Principal defect rank | 1 |
| Principal total-cost rank | 2 |
| Principal cut-invariant set | Plane `x=-1` |
| Principal fixed-point set | Empty |
| Figure states | 343 |
| Exact defect values | 7 |
| States in each displayed fibre | 49 |
| Zero-defect figure states | 49 |

`evidence/verification.json` contains the exact coefficient records. `evidence/figure.json` contains every displayed state, every transported cut total, and every defect vector.

The two paths use distinct constructions. The coefficient path composes summaries. The polynomial path executes the local maps and local costs. Each rotated word starts at the original symbolic prefix state. Equality is coefficient equality over the rationals, which proves equality for every real initial state of each specified word.

The general proofs were reviewed against the conditions listed in `evidence/PROOF_REVIEW.md`. Exact examples also cover an inconsistent cut-invariance system, a singular prefix map, and two quadratic cases with different minimum dimensions.

The final manuscript contains seven A4 pages. Every page was rendered and visually inspected. The title, author mark, equations, tables and both references are within the page area. XeLaTeX reports no missing characters or overfull or underfull boxes in the final build.

The completed figure was rendered in Blender 5.2.3 LTS with CPU Cycles, four threads and 32 samples per pixel. Its observed dimensions are 3840 × 2705. Visual inspection confirmed the seven scalar values, seven exact output triples, gold cut-invariant plane and contained labels.

The saved scene contains 1,632 objects, including all 343 state objects. Its embedded mathematical certificate equals `evidence/figure.json`. It has a relative render path and requires no external library or font. The canonical source scene is preserved. `evidence/render-receipt.json` and `evidence/scene-audit.json` record these observations.
