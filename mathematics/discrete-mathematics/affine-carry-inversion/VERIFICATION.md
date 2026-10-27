# Exact verification

The 27 October 2026 execution completed the declared whole-fiber experiment.
Python 3 on the native cloud host returned these results:

- 65,532 complete fibers at widths 1–7, for three invertible maps per width.
- 196,596 solver calls across input, output and automatic enumeration.
- 1,020 direct-addition signature-set comparisons at widths 1–8.
- Both maximum signature counts match F_(w+1) at every width 1–16.
- Two complete 32-bit reflection fibers contain 16,384 and 65,536 solutions.
- Exact one-cell certificates cover widths 16, 32, 64, 128, 256 and 512.
- The figure's five cells contain exactly 17 distinct eight-bit solutions.

Every comparison passed. `evidence/verification.json` contains the maps, counts,
examples, certificate bases and actual execution time. Its timings describe
verification, not a performance claim for the inverse algorithm.

The complete general proof is in `paper.tex`. Finite comparisons support the
implementation. They do not replace the proof or establish algorithmic priority.
The historical source was independently replayed before this publication. Its
old timings were not presented as new measurements.
