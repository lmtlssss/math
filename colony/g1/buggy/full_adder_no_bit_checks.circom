pragma circom 2.0.0;
include "../lib/circomlib/bitify.circom";
// UNDERCONSTRAINED: missing bit constraints on inputs.
template FullAdderLoose() {
    signal input b1;
    signal input b2;
    signal input carry_in;
    signal output v;
    signal output carry_out;
    component n2b = Num2Bits(2);
    n2b.in <== b1 + b2 + carry_in;
    v <== n2b.out[0];
    carry_out <== n2b.out[1];
}
component main {public [b1, b2, carry_in]} = FullAdderLoose();
