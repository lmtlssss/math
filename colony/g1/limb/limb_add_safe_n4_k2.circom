pragma circom 2.0.0;
include "../lib/circomlib/bitify.circom";
// Correct 2-limb add with Num2Bits on each stage (BitVM u4-style, n=4).
template LimbAddSafe(n, k) {
    signal input a[k];
    signal input b[k];
    signal output out[k + 1];
    component s0 = Num2Bits(n + 1);
    s0.in <== a[0] + b[0];
    signal carry0;
    carry0 <== s0.out[n];
    out[0] <== a[0] + b[0] - carry0 * (1 << n);
    component s1 = Num2Bits(n + 2);
    s1.in <== a[1] + b[1] + carry0;
    signal carry1;
    carry1 <== s1.out[n] + 2 * s1.out[n + 1];
    out[1] <== a[1] + b[1] + carry0 - carry1 * (1 << n);
    out[2] <== carry1;
}
component main {public [a, b]} = LimbAddSafe(4, 2);
