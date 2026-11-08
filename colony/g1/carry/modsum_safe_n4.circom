pragma circom 2.0.0;
include "../lib/circomlib/bitify.circom";

// Correct ModSum(n=4): a,b < 2^4 claimed via Num2Bits on a+b.
// Ground truth: UNIQUE (sum,carry) for any field a,b that fit in n bits when
// the n+1 bit decomposition is enforced. Picus public inputs: a,b.
template ModSumSafe(n) {
    signal input a;
    signal input b;
    signal output sum;
    signal output carry;
    component n2b = Num2Bits(n + 1);
    n2b.in <== a + b;
    carry <== n2b.out[n];
    sum <== a + b - carry * (1 << n);
}
component main {public [a, b]} = ModSumSafe(4);
