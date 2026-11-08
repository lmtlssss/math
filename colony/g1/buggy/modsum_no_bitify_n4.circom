pragma circom 2.0.0;
// UNDERCONSTRAINED: equation alone does not pin (sum,carry) uniquely in F_p.
// Many (sum,carry) pairs satisfy a+b = sum + carry*2^n.
template ModSumBuggy(n) {
    signal input a;
    signal input b;
    signal output sum;
    signal output carry;
    var MOD = 1 << n;
    sum <-- (a + b) % MOD;
    carry <-- (a + b) \ MOD;
    a + b === sum + carry * MOD;
}
component main {public [a, b]} = ModSumBuggy(4);
