pragma circom 2.0.0;
// BitVM-style u4 8-limb add WITHOUT range checks. UNDERCONSTRAINED.
template U4AddBuggy(k) {
    signal input a[k];
    signal input b[k];
    signal output out[k + 1];
    signal carry[k];
    carry[0] <-- (a[0] + b[0]) \ 16;
    out[0] <-- (a[0] + b[0]) % 16;
    a[0] + b[0] === out[0] + carry[0] * 16;
    for (var i = 1; i < k; i++) {
        carry[i] <-- (a[i] + b[i] + carry[i - 1]) \ 16;
        out[i] <-- (a[i] + b[i] + carry[i - 1]) % 16;
        a[i] + b[i] + carry[i - 1] === out[i] + carry[i] * 16;
    }
    out[k] <== carry[k - 1];
}
component main {public [a, b]} = U4AddBuggy(8);
