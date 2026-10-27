# Exact verification plan

The experiment covers complete linear maps, not selected input points. It must
catch reversed composition order, transposed certificates, incorrect bit order,
rotation/shift confusion, missing truncation, and arithmetic outside F2. It
must also distinguish a rank-one nilpotent from an idempotent, and a sum of
matrix words from a single word.

Recover the original word-basis certificate. Reconstruct all generators from
coordinate equations in a separate row implementation. Recompute all original
1024 word matrices and their exact rank. Compute every word through length10
and the cumulative dimensions. Reconstruct the new polynomial rank-one
certificate and both cyclic bases. Check inverses by multiplying on both sides.

For end-to-end acceptance, synthesize all1024 elementary matrix maps by the
new rank-one basis and by the short-word basis. Reconstruct every target matrix
and compare its complete32 input-basis images with independent exact arithmetic.
These basis checks prove equality on every input vector. Also reject a
modified polynomial, vector, inverse, or duplicated basis word. Preserve the
original source record and mark new certificates separately.

The manuscript supplies the mathematical argument. Exact finite calculations
support its explicit certificates; no formal proof-kernel acceptance is claimed.
