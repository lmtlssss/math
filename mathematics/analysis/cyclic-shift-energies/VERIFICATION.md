# Executed verification

The actual `verify.py` run completed successfully. 6822 direct coordinate evaluations; 1200 retained-potential updates; 19437 exact occupancies; 32 exact frequency-rank instances.

The verifier output is `evidence/verification.json`. Its exact figure inputs are `evidence/figure.json`. These examples test implementations of the proved statements; mathematical claims are established by the proofs in `paper.tex`.

`visual/build_scene.py` constructs its geometry from the same certificate. Native render, source-style preservation and release hashes are recorded in the accompanying render receipt and release manifest. PDF rendering is reviewed separately from mathematical verification.
