# Exact nonnegative rank of a twelve-state composition tensor

**lmtlssss🜐**  
26 October 2026 · Version 1.0.0  
Mathematics / Algebra · MSC 2020: 15A69; 15B48, 20M20

[Paper (PDF)](https://github.com/lmtlssss/math/releases/download/tensor-note-v1.0.0/paper.pdf) · [LaTeX source](paper.tex) · [Certificate](certificate.json) · [Verifier](verify.py)

## Result

Let $S$ be the twelve-element transformation monoid defined in the paper. For its multiplication table $M$, set

$$C_{ijk}=\mathbf{1}_{\{M(i,j)=k\}}.$$

Then

$$\operatorname{rank}_{+}(C)=35.$$

The upper bound is a partition into 35 rectangles. The lower bound is certified twice: by 35 incompatible entries, and by determinant-one minors in the twelve output slices. All factors in the displayed decomposition have entries in $\{0,1\}$. The theorem holds over the nonnegative reals and the nonnegative rationals.

The rank statement concerns nonnegative decompositions. Signed and complex tensor rank are separate questions.

## Check the proof

```sh
python3 verify.py
```

Python 3.9 or later is sufficient. No packages or solver are required. The verifier reconstructs composition from the maps, checks the generating set, verifies every coefficient, checks every fooling-set pair, and evaluates the witness determinants with exact rational arithmetic.

The paper contains the complete proof and all certificate tables. `certificate.json` is their machine-readable form.

## Build the paper

```sh
make paper
```

This requires XeLaTeX, Latin Modern, the Noto Sans Symbols font, and the LaTeX packages listed in `paper.tex`. The public `Publish tensor note` workflow verifies the certificate and builds the PDF from the release revision. Font files are not included in this repository.

## Citation and corrections

[Citation in BibTeX](CITATION.bib). Please identify the version used. Corrections can be submitted as an issue or pull request, with the relevant equation, table entry, or counterexample.
