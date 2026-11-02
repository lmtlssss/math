# Executed verification

The actual `verify.py` run completed successfully. 507 observation inequalities; 5 two-sample equality witnesses; 2420 strip-polygon inequalities and 20 equality witnesses; 120 exact peak certificates; 720 finite energy sums.

The verifier output is `evidence/verification.json`. Its exact figure inputs are `evidence/figure.json`. These examples test implementations of the proved statements; mathematical claims are established by the proofs in `paper.tex`.

`visual/build_scene.py` constructs its geometry from the same certificate. Native render, source-style preservation and release hashes are recorded in the accompanying render receipt and release manifest. PDF rendering is reviewed separately from mathematical verification.
