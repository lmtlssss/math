pragma circom 2.0.0;
include "../lib/circomlib/bitify.circom";
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
component main {public [a, b]} = ModSumSafe(16);
