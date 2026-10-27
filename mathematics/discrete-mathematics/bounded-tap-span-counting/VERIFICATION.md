# Verification

The main theorem is proved in `paper.tex`. Execution checks supplement the proof.

The native suffix solver matched complete direct histograms on 21,760 inverse queries. The canonical forward solver matched direct enumeration on 840 fixed queries covering every tap triple at widths 4 through 8. All 54 saved generalized-width cases matched three implementations, including the reference that keeps an explicit output carry.

The 256-bit example returns exactly 5,784,112,988,160 solutions. Its native solver visits 558,622 states and checks 1,115,268 transitions. The separate illustrative 24-bit instance has exactly 224 solutions and 496 forward state visits. Every edge in the figure is an accepted local transition from that instance.

The replay includes zero and all-one operands, empty fibers, cyclic index changes, shift truncation, discarded final carries, and consistent tail-carry closure. Counts use arbitrary precision. A resource cap is an incomplete run, not a zero count.

`evidence/verification.json` records the complete comparisons and source digests. This is internal cross-code verification, not an assertion of external peer review or formal verification of the compilers.
