# Verification contract

The mathematical proof covers every width w >= 4. Executable checks supplement that proof.

Failure modes: reversed rotation convention; incorrect carry into bit zero; an accidental condition on discarded overflow; omission of one cyclic closure bit; duplicate or missing preimages; bounds that count whole-word operations as bit operations; incorrect conversion at non-byte widths; treating a planted-witness check as completeness; copying an error from the original solver.

Compare the released inverse with full forward fibers for every mask and target at widths 4 through 8 (k=0). A supplied k translates the target by subtraction; cover nonzero k in independently selected wider cases. Replay the two preserved original case panels and their published complete solution sets, and compare to the unchanged original mathematical function bodies. Check the sharp example directly. For wider words compare independent recurrence implementations and verify each returned word. All original private source records remain separate from the public mathematics package.

The public replay uses Python's standard library. It reports exact equality and operation bounds, rather than a hardware performance claim. General completeness follows from the proof.
