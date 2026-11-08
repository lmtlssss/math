pragma circom 2.0.0;
include "../lib/circomlib/bitify.circom";
// Shared word x added to 3 constant offsets; each sum ModSum-decomposed.
// Applies shared-input-carry-frontiers (DOI 10.5281/zenodo.23702847):
// joint carry state count <= m+1 = 4.
template SharedInputParallel(w) {
    signal input x;
    signal output y0;
    signal output y1;
    signal output y2;
    signal output c0;
    signal output c1;
    signal output c2;
    component nx = Num2Bits(w);
    nx.in <== x;
    component s0 = Num2Bits(w + 1);
    s0.in <== x + 13;
    c0 <== s0.out[w];
    y0 <== x + 13 - c0 * (1 << w);
    component s1 = Num2Bits(w + 1);
    s1.in <== x + 45;
    c1 <== s1.out[w];
    y1 <== x + 45 - c1 * (1 << w);
    component s2 = Num2Bits(w + 1);
    s2.in <== x + 93;
    c2 <== s2.out[w];
    y2 <== x + 93 - c2 * (1 << w);
}
component main {public [x]} = SharedInputParallel(8);
