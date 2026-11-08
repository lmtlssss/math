pragma circom 2.0.0;
include "../lib/circomlib/bitify.circom";
// UNDERCONSTRAINED: sum is range-checked to n bits, but carry is not forced
// into {0,1}. For a+b < 2^n the equation allows carry to absorb field wraps.
// Simpler classic bug: only constrain sum bits, leave carry free except equation.
template ModSumCarryFree(n) {
    signal input a;
    signal input b;
    signal output sum;
    signal output carry;
    // Witness computation (honest)
    var MOD = 1 << n;
    sum <-- (a + b) % MOD;
    carry <-- (a + b) \ MOD;
    // Only range-check sum; carry unconstrained as a bit
    component n2b = Num2Bits(n);
    n2b.in <== sum;
    a + b === sum + carry * MOD;
}
component main {public [a, b]} = ModSumCarryFree(4);
