# Robust Amplitude Elimination and Exact Lattice-Phase Selection

**lmtlssss🜐 · 2 November 2026 · Version 1.0.0**
DOI: [10.5281/zenodo.23897131](https://doi.org/10.5281/zenodo.23897131)

A complete exact selection law for a translating common lattice reduces finite robust designs to residue cells and affine envelopes. It gives rational selection probabilities, expected optima and boundary decisions. A four-design example separates the continuous winner from the phase-selection probabilities. A second theorem proves persistent reversal under arbitrarily fine lattice refinement.

## Principal contribution

The principal contributions are the common-lattice phase-selection law, its exact probability and expectation formula, and the persistent-refinement reversal theorem. Scalar monotonicity, interval elimination, homogeneity and line-envelope geometry are established foundations, not separate originality claims.

## Files

`paper.tex` is the mathematical manuscript. `verify.py` reconstructs the foundational examples; `verify_extension.py` reconstructs the principal discovery and its independent comparisons. `evidence/verification.json` and `evidence/discovery.json` contain the observed results; `evidence/figure.json` is the figure certificate. `visual/build_scene.py` and `visual/scene_common.py` construct the native mathematical diagram from that certificate.

The release includes `paper.pdf`, `00-cover.png` at native 3840-pixel width, `homogeneous-amplitude-elimination.blend`, and `source-and-proof.zip`. The saved scene and image embed the publication DOI. The figure follows the author's established mathematical visual series.

## Reproduce

Run `python3 verify.py --output evidence/verification.json`, then `python3 verify_extension.py`, from this directory. The second command writes the current figure certificate. Use Python 3.11 or later and the dependencies in `requirements.txt`. The exact checks are: 2400 direct grid instances, including 1533 feasible cases; 200 exact independently propagated state-scaling steps; exact design reversal and empty-grid interval.

The principal-discovery checks are: An exact four-design phase diagram, independent origin comparisons and 400 direct grid enumerations; 425 strict refinement-reversal comparisons; exact boundary ties and one-sided feasibility events.

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
