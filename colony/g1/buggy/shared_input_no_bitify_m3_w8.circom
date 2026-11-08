pragma circom 2.0.0;
// UNDERCONSTRAINED shared-input parallel adds: equation only.
template SharedInputBuggy(w) {
    signal input x;
    signal output y0;
    signal output y1;
    signal output y2;
    signal output c0;
    signal output c1;
    signal output c2;
    var MOD = 1 << w;
    y0 <-- (x + 13) % MOD; c0 <-- (x + 13) \ MOD;
    y1 <-- (x + 45) % MOD; c1 <-- (x + 45) \ MOD;
    y2 <-- (x + 93) % MOD; c2 <-- (x + 93) \ MOD;
    x + 13 === y0 + c0 * MOD;
    x + 45 === y1 + c1 * MOD;
    x + 93 === y2 + c2 * MOD;
}
component main {public [x]} = SharedInputBuggy(8);
