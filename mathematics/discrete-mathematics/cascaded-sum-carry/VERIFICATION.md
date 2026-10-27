# Exact verification

The native Python execution completed the declared whole-function experiment
on 27 October 2026. `evidence/verification.json` records the observed results.

The independent oracle performs successive integer additions and extracts each
carry directly. It does not use the cumulative-profile formula, classification,
counting recurrence, or dense-code formulas.

The exhaustive part covers 54 radix/stage panels at radices 2 through 10. The
panels include 196,160 complete operand tuples and 5,005,590 incoming-bit
assignments. Each oracle truth table agrees with the profile descriptor. Both
directions of the descriptor-to-function correspondence agree. The possible
final residues of every carry function match the interval/singleton lemma.

All 13,191 distinct functions in those panels receive different dense labels.
Every label is occupied. Decoding each label gives a representative with the
same complete truth table. The panels include k < B-1, k = B-1, and k > B-1.

The direct two-stage codec passes 359,996 output comparisons at radices 2–24.
Additional checks cover 15,792 outputs at widths 8, 16, 32, 64, 128, 256 and
512 bits. The wider experiments use 24 operand tuples for each width and stage
count. They enumerate every carry assignment through four stages, and sample
32 assignments per tuple at seven and twelve stages. Boundary operands are
included deliberately. Separate dense-label checks cover the stable regime and
labels at both ends of their ranges.

The figure certificate records all 4096 radix-eight operand tuples, all 113
functions, and their complete eight-input truth tables. Its source-to-class
incidence is exact.

Finite checks support the implementation. The manuscript supplies the proof
for all integer radices and stage counts. These results are internal exact
verification, not independent laboratory replication or a formal proof-kernel
acceptance. The recorded execution time is a verification time, not a claimed
speed advantage.

The publication pass repeated the unchanged whole-function experiment.
`evidence/publication-verification.json` preserves this separate execution.
