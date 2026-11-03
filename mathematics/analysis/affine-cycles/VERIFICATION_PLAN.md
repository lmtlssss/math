# Verification plan

The proof is the certificate for arbitrary dimension and word length. Exact computation supplies reproducible instances and checks the figure data.

The failure modes are an incorrect composition order, evaluation of a local cost at the wrong state, replacement of transported cut states with a common reset state, an inverse assumption at a singular prefix, confusion between a full displacement space and the attainable affine displacement set, omission of the known constant from a linear-summary decoder, and loss of quadratic or higher-degree terms.

The verifier will compare two constructions. The retained construction composes affine maps and cost coefficients. The independent construction expands every local transition and local cost as rational multivariate polynomials, then runs each cyclic rotation from the transported symbolic state. Coefficient equality proves agreement for every initial state of each certified instance. Exact row reduction checks ranks and consistency. Named examples cover a cut-invariant cycle without a fixed point, an inconsistent cycle, a singular prefix, and a quadratic defect whose minimal dimension exceeds the rank of its cycle displacement.

A complete 7×7×7 integer grid of the principal example will produce the figure certificate. Each of its seven defect values has 49 preimages. The zero-defect fibre is the plane x=-1 within that grid. All public numbers derive from these abstract rational constructions.
