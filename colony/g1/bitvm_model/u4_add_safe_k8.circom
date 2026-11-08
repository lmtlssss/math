pragma circom 2.0.0;
include "../lib/circomlib/bitify.circom";
// BitVM u4 (nibble) 8-limb add = 32-bit word. Safe with Num2Bits per stage.
template U4AddSafe(k) {
    signal input a[k];
    signal input b[k];
    signal output out[k + 1];
    signal carry[k];
    component s0 = Num2Bits(5);
    s0.in <== a[0] + b[0];
    carry[0] <== s0.out[4];
    out[0] <== a[0] + b[0] - carry[0] * 16;
    component s[k - 1];
    for (var i = 1; i < k; i++) {
        s[i - 1] = Num2Bits(6);
        s[i - 1].in <== a[i] + b[i] + carry[i - 1];
        carry[i] <== s[i - 1].out[4] + 2 * s[i - 1].out[5];
        out[i] <== a[i] + b[i] + carry[i - 1] - carry[i] * 16;
    }
    out[k] <== carry[k - 1];
}
component main {public [a, b]} = U4AddSafe(8);
