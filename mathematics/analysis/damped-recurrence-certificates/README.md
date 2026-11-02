# Sharp Observation Bounds and Minimal Peak Horizons for Damped Recurrences

**lmtlssss🜐 · 2 November 2026 · Version 1.0.0**
DOI: [10.5281/zenodo.23897133](https://doi.org/10.5281/zenodo.23897133)

Exact coefficient inequalities classify the stable conjugate-root recurrences with minimal uniform peak horizon two or three. A symmetric observation hexagon supplies necessity and sufficiency. An explicit rational boundary example has shortest uniform horizon three. Sharp observation constants, rational adaptive certificates and exact Stein sums accompany the new coefficient-region result.

## Principal contribution

The principal result is the closed necessary-and-sufficient coefficient classification for minimal horizons two and three, including all boundary equalities. General finite determination, polar invariant sets and Stein identities are classical. The paper gives the exact second-order regions rather than presenting those general tools as new.

## Files

`paper.tex` is the mathematical manuscript. `verify.py` reconstructs the foundational examples; `verify_extension.py` reconstructs the principal discovery and its independent comparisons. `evidence/verification.json` and `evidence/discovery.json` contain the observed results; `evidence/figure.json` is the figure certificate. `visual/build_scene.py` and `visual/scene_common.py` construct the native mathematical diagram from that certificate.

The release includes `paper.pdf`, `00-cover.png` at native 3840-pixel width, `damped-recurrence-certificates.blend`, and `source-and-proof.zip`. The saved scene and image embed the publication DOI. The figure follows the author's established mathematical visual series.

## Reproduce

Run `python3 verify.py --output evidence/verification.json`, then `python3 verify_extension.py`, from this directory. The second command writes the current figure certificate. Use Python 3.11 or later and the dependencies in `requirements.txt`. The exact checks are: 507 observation inequalities; 5 two-sample equality witnesses; 2420 strip-polygon inequalities and 20 equality witnesses; 120 exact peak certificates; 720 finite energy sums.

The principal-discovery checks are: 8,478 exact rational coefficient pairs against an independently constructed convex hull: 2,869 horizon-two, 3,014 horizon-three and 2,595 requiring at least four samples; an explicit irredundancy witness and 101 observation rows for the rational example.

Typeset with `xelatex -interaction=nonstopmode -halt-on-error paper.tex` twice. The manuscript uses Latin Modern and Noto Sans Symbols, following earlier notes in the series. The release PDF was also built natively with `tectonic --keep-logs paper.tex` (Tectonic 0.17.0).

For the native figure, open the original public tensor-series style scene as the input file and run this paper's builder:

```sh
FIGURE_OUTPUT="$PWD/release" MATHEMATICS_FONT=/path/to/DejaVuSans.ttf \
  blender --background /path/to/twelve-state-tensor-rank35.blend \
  --python visual/build_scene.py
```

The style authority is the author's [tensor-note-v1.0.0 release](https://github.com/lmtlssss/math/releases/tag/tensor-note-v1.0.0). The builder preserves the source scene file, reuses its world and render/color settings, and records its SHA-256 in `render-receipt.json`. Text is converted to mesh geometry. The published package contains no font files.

## Citation and licence

Use `CITATION.cff` or `CITATION.bib`. Mathematical text, data and figure specification are CC BY 4.0. Code is MIT licensed. See `LICENSE.md`.
