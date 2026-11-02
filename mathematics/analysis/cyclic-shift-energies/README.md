# Cyclic-Shift Energies: Minimal State and Cyclotomic Gaps

**lmtlssss🜐 · 2 November 2026 · Version 1.0.0**
DOI: [10.5281/zenodo.23897127](https://doi.org/10.5281/zenodo.23897127)

A cyclotomic divisibility criterion decides equality in an integer-occupancy spectral bound. At prime periods, algebraic norms yield a quantitative positive gap for nonflat spectra. The bound is attained at exactly five occupancies in a complete 210-state example. Minimal linear state and retained-potential identities supply the representation framework.

## Principal contribution

The principal result is the quantitative cyclotomic spectral gap, its equality obstruction and the attained five-cycle certificate. The Fourier diagonalization, positive-semidefinite rank argument, cyclotomic irreducibility and field-norm integrality are established ingredients and receive attribution.

## Files

`paper.tex` is the mathematical manuscript. `verify.py` reconstructs the foundational examples; `verify_extension.py` reconstructs the principal discovery and its independent comparisons. `evidence/verification.json` and `evidence/discovery.json` contain the observed results; `evidence/figure.json` is the figure certificate. `visual/build_scene.py` and `visual/scene_common.py` construct the native mathematical diagram from that certificate.

The release includes `paper.pdf`, `00-cover.png` at native 3840-pixel width, `cyclic-shift-energies.blend`, and `source-and-proof.zip`. The saved scene and image embed the publication DOI. The figure follows the author's established mathematical visual series.

## Reproduce

Run `python3 verify.py --output evidence/verification.json`, then `python3 verify_extension.py`, from this directory. The second command writes the current figure certificate. Use Python 3.11 or later and the dependencies in `requirements.txt`. The exact checks are: 6822 direct coordinate evaluations; 1200 retained-potential updates; 19437 exact occupancies; 32 exact frequency-rank instances.

The principal-discovery checks are: 162 exact prime binary norm certificates; 7,172 supplementary primitive-root numerical cross-checks of exact polynomial divisibility; all 210 integer occupancies in the attained-gap example.

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
