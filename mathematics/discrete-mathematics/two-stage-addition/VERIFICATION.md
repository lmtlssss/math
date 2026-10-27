# Exact complete-function verification

The source proof was recovered from the 27 October 2026 arithmetic archive.
The publication independently reconstructs its normal forms and extends the
statement to every integer radix B >= 2. The complete response contains the
modular residue and both outgoing carries for all four incoming carry pairs.

Observed native-cloud results:

- All 44,099 operand triples for every radix from 2 through 20 match the
  independent arithmetic oracle at all four inputs: 176,396 responses.
- Every canonical label occurs and denotes one distinct full function.
- Every representative and every class multiplicity agrees with enumeration.
- The independent C++ census covers all binary operand triples at widths 1–8.
  At width eight it covers 16,777,216 triples, 1,276 classes, and carry-image
  counts 16,581,120 / 195,584 / 512 for image sizes one / two / three.
- 1,340 exact wide-operand examples cover word widths through 512 bits.
- 2,560 composed-response comparisons include binary and mixed-radix stages.

Every comparison passed. The general result follows from the case proof in
`paper.tex`. The finite experiments support the implementations. The 42-bit
stage-product bound requires independently recoverable local responses.
It is not asserted for an observer restricted to reachable whole-word traces.
