# Whole-fiber verification plan

Before implementation: check final-carry truncation, residue halving, word-width
complements, inverse-matrix direction, omitted signatures, duplicate cells,
inconsistent equations, dependent basis vectors, and complete output coverage.

Use independently computed full forward fibers as the oracle. Compare sets,
not only planted witnesses. Check both enumeration directions. Validate cell
bases and directions as certificates. Check exact carry-signature sets and
maximal counts against direct small-word additions. Retain a worked figure
certificate and wide reflection families with closed-form cardinalities.

The original archived replay remains a separate provenance check. Its historical
timings are not new measurements. The manuscript's theorem is proved directly;
finite verification supports the implementation.
