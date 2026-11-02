# Sharp Two-Sample Bounds and Finite Peak Certificates for Damped Recurrences

**lmtlssss🜐 · 2 November 2026 · Version 1.0.0**  
DOI: [10.5281/zenodo.23897133](https://doi.org/10.5281/zenodo.23897133)

A sharp two-sample inequality yields a finite prefix for the infinite absolute peak of stable conjugate-root recurrences. An exact strip-polygon formulation handles larger observation sets; rational adaptive certificates and finite Stein sums give complete worked examples.

## Files

`paper.tex` is the mathematical manuscript. `verify.py` reconstructs the exact examples and independent comparisons. `evidence/verification.json` contains its observed results; `evidence/figure.json` is the figure certificate. `visual/build_scene.py` and `visual/scene_common.py` construct the native mathematical diagram from that certificate.

The release includes `paper.pdf`, `00-cover.png` at native 3840-pixel width, `damped-recurrence-certificates.blend`, and `source-and-proof.zip`. The saved scene and image embed the publication DOI. The figure follows the author's established mathematical visual series.

## Reproduce

Run `python3 verify.py --output evidence/verification.json` from this directory. Python 3.11 or later is sufficient; the cyclic-shift verifier also requires SymPy as listed in `requirements.txt`. The exact checks are: 507 observation inequalities; 5 two-sample equality witnesses; 2420 strip-polygon inequalities and 20 equality witnesses; 120 exact peak certificates; 720 finite energy sums.

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
