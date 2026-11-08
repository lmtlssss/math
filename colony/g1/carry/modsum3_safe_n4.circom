pragma circom 2.0.0;
include "../lib/circomlib/bitify.circom";
// a+b+c with c a carry bit. Models BitVM-style cascaded limb stage.
template ModSumThreeSafe(n) {
    signal input a;
    signal input b;
    signal input c;
    signal output sum;
    signal output carry;
    c * (c - 1) === 0;
    component n2b = Num2Bits(n + 2);
    n2b.in <== a + b + c;
    carry <== n2b.out[n] + 2 * n2b.out[n + 1];
    sum <== a + b + c - carry * (1 << n);
}
component main {public [a, b, c]} = ModSumThreeSafe(4);
