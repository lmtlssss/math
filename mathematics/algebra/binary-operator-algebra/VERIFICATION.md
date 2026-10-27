# Exact verification

The 27 October 2026 publication pass independently reconstructed the source
certificate and completed the declared full-map experiment.

The coordinate-row verifier and the column construction agree on the explicit
polynomial rank-one identity. The two cyclic bases have rank32. All four
inverse-matrix products equal identity. The rank-one matrix is nilpotent.

The retained short-word certificate has1024 different words and independent
matrix images. Full enumeration of2047 words through length10 gives cumulative
dimensions 1,3,7,15,31,63,127,255,510,991,1024. Each elementary matrix is
synthesized by the short-word basis and by the rank-one basis. Both methods
reconstruct all1024 elementary matrices and64 additional complete binary maps.
The experiment rejects five deliberately altered certificates.

The historical source basis was read and compared before this publication.
The explicit polynomial certificate is a separate derivation from this pass.
`evidence/verification.json` contains the observed results. The cloud build
produces a separate `evidence/cloud-verification.json` receipt. The general
proof and finite certificate interpretation are in the manuscript. The
execution is internal exact verification, not external replication or formal
proof-kernel acceptance. Execution time is a verifier time, not a speed claim.
