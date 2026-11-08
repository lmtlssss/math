pragma circom 2.0.0;
template Cascade3Buggy(n) {
    signal input x0;
    signal input x1;
    signal input x2;
    signal input a0;
    signal input a1;
    signal input a2;
    signal output r;
    signal output c0;
    signal output c1;
    signal output c2;
    var MOD = 1 << n;
    signal res0;
    signal res1;
    c0 <-- (x0 + a0) \ MOD;
    res0 <-- (x0 + a0) % MOD;
    x0 + a0 === res0 + c0 * MOD;
    c1 <-- (res0 + x1 + a1) \ MOD;
    res1 <-- (res0 + x1 + a1) % MOD;
    res0 + x1 + a1 === res1 + c1 * MOD;
    c2 <-- (res1 + x2 + a2) \ MOD;
    r <-- (res1 + x2 + a2) % MOD;
    res1 + x2 + a2 === r + c2 * MOD;
}
component main {public [x0, x1, x2, a0, a1, a2]} = Cascade3Buggy(4);
