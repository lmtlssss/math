# Exact verification

The declared whole-input experiment completed on 27 October 2026.
All comparisons passed.

The prefix census covers 30,792 panels and
211,326 actual prefixes. It checks the exact
threshold class count and chain order. All 41,560
checked pairs of nonterminal states produce distinct first-suffix outputs.

The masked-counter comparison covers 3,840
complete queries and 785,664 direct input evaluations.
Counts and least witnesses agree with integer addition and a separately
written full-vector carry counter. The wide comparison includes
168 queries through 1,024 bits and up to 64 offsets.

The 256-bit, 32-offset example has exactly
291507445114675457594661599285981859699083240676748846694400
solutions. Both implementations return the same count and least witness.
The ordered implementation constructs 8,290 nonterminal source states and
attempts 16,580 transitions. Its maximum layer width is 33.

The native verification time was 19.852 seconds. It describes the
complete verification run and is not a performance comparison.
The paper supplies the proofs for all widths, offsets and masks.
No external replication or formal proof-kernel acceptance is claimed.

The publication pass repeated the unchanged whole-input experiment successfully.
`evidence/publication-verification.json` records that execution.
