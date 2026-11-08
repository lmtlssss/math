pragma circom 2.0.0;
// UNDERCONSTRAINED 2-limb add: no Num2Bits on intermediate sums/carries.
// Models a broken BitVM-style u4 limb chain.
template LimbAddBuggy(n, k) {
    signal input a[k];
    signal input b[k];
    signal output out[k + 1];
    signal carry[k];
    var MOD = 1 << n;
    carry[0] <-- (a[0] + b[0]) \ MOD;
    out[0] <-- (a[0] + b[0]) % MOD;
    a[0] + b[0] === out[0] + carry[0] * MOD;
    for (var i = 1; i < k; i++) {
        carry[i] <-- (a[i] + b[i] + carry[i - 1]) \ MOD;
        out[i] <-- (a[i] + b[i] + carry[i - 1]) % MOD;
        a[i] + b[i] + carry[i - 1] === out[i] + carry[i] * MOD;
    }
    out[k] <== carry[k - 1];
}
component main {public [a, b]} = LimbAddBuggy(4, 2);
