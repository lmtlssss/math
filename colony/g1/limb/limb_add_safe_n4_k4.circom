pragma circom 2.0.0;
include "../lib/circomlib/bitify.circom";
// 4-limb u4-style add (models 16-bit word as 4 nibbles). Safe.
template LimbAddSafe4(n) {
    signal input a[4];
    signal input b[4];
    signal output out[5];
    signal carry[4];
    component s0 = Num2Bits(n + 1);
    s0.in <== a[0] + b[0];
    carry[0] <== s0.out[n];
    out[0] <== a[0] + b[0] - carry[0] * (1 << n);
    component s1 = Num2Bits(n + 2);
    s1.in <== a[1] + b[1] + carry[0];
    carry[1] <== s1.out[n] + 2 * s1.out[n + 1];
    out[1] <== a[1] + b[1] + carry[0] - carry[1] * (1 << n);
    component s2 = Num2Bits(n + 2);
    s2.in <== a[2] + b[2] + carry[1];
    carry[2] <== s2.out[n] + 2 * s2.out[n + 1];
    out[2] <== a[2] + b[2] + carry[1] - carry[2] * (1 << n);
    component s3 = Num2Bits(n + 2);
    s3.in <== a[3] + b[3] + carry[2];
    carry[3] <== s3.out[n] + 2 * s3.out[n + 1];
    out[3] <== a[3] + b[3] + carry[2] - carry[3] * (1 << n);
    out[4] <== carry[3];
}
component main {public [a, b]} = LimbAddSafe4(4);
