# Executed verification

The actual `verify.py` run completed successfully. 2400 direct grid instances, including 1533 feasible cases; 200 exact independently propagated state-scaling steps; exact design reversal and empty-grid interval.

The verifier output is `evidence/verification.json`. Its exact figure inputs are `evidence/figure.json`. These examples test implementations of the proved statements; mathematical claims are established by the proofs in `paper.tex`.

`visual/build_scene.py` constructs its geometry from the same certificate. Native render, source-style preservation and release hashes are recorded in the accompanying render receipt and release manifest. PDF rendering is reviewed separately from mathematical verification.
