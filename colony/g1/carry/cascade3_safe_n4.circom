pragma circom 2.0.0;
include "../lib/circomlib/bitify.circom";
// Three-stage cascaded addition with bitified carries.
// Applies cascaded-sum-carry / two-stage-addition exact state counts.
template Cascade3(n) {
    signal input x0;
    signal input x1;
    signal input x2;
    signal input x3;
    signal input a0; // incoming bit stage 0
    signal input a1;
    signal input a2;
    signal output r;  // final residue
    signal output c0;
    signal output c1;
    signal output c2;
    a0 * (a0 - 1) === 0;
    a1 * (a1 - 1) === 0;
    a2 * (a2 - 1) === 0;
    component s0 = Num2Bits(n + 1);
    s0.in <== x0 + a0; // first operand alone + incoming; simplify: use x0 as base residue path
    // Proper cascade: stage i adds xi and ai to preceding residue
    // Stage 0: res0 = (x0 + a0) mod 2^n, c0 = carry
    c0 <== s0.out[n];
    signal res0;
    res0 <== x0 + a0 - c0 * (1 << n);
    component s1 = Num2Bits(n + 2);
    s1.in <== res0 + x1 + a1;
    c1 <== s1.out[n] + 2 * s1.out[n + 1];
    signal res1;
    res1 <== res0 + x1 + a1 - c1 * (1 << n);
    component s2 = Num2Bits(n + 2);
    s2.in <== res1 + x2 + a2;
    c2 <== s2.out[n] + 2 * s2.out[n + 1];
    r <== res1 + x2 + a2 - c2 * (1 << n);
    // x3 unused placeholder to mirror 4-operand cascade API — constrain it trivially
    signal dummy;
    dummy <== x3 * x3;
}
component main {public [x0, x1, x2, x3, a0, a1, a2]} = Cascade3(4);
