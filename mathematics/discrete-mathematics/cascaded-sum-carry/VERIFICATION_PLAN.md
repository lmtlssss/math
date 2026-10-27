# Whole-function verification plan

This plan fixes the failure cases before verification of the implementation.

The object is the complete function of all independently supplied incoming
bits. Check the final residue and every outgoing carry. Counts of operand
tuples, output values, carry-only maps, and complete functions are different.

The profile implementation can fail through an off-by-one carry threshold,
wrong cumulative carry, lost final residue, or a radix-one assumption. The
classification can fail at the empty cascade, radix two, the boundary k=B-1,
or the stable range k>=B. The dense code can fail through overlapping residue
groups, duplicated labels, skipped labels, an invalid representative, or an
incorrect branch in the recursive inverse. The two-stage formula can fail at
the two terminal residues. A drawing can misassign an operand to its class.

Enumerate complete incoming truth tables using direct integer additions. Group
those tables independently of the proposed descriptor. Compare descriptor
identity in both directions and compare every observed count to the theorem.
Check all carry-map residue supports. For every distinct function, encode and
decode its label, then compare the decoded representative's full truth table.
Check that the occupied labels are exactly 0,...,N-1.

Use all radix/stage pairs with B in 2..10 and k in 0..8 for which
B^(k+1)*2^k <= 1,100,000. Retain every panel. Check the direct two-stage codec on
all triples at B=2..24. For wide words, use both boundary operands and a frozen
random seed, and keep the distinction between exhaustive and sampled input
assignments. Freeze the complete B=8,k=3 figure incidence from the same oracle.
