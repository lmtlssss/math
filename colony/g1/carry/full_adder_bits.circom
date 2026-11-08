pragma circom 2.0.0;
include "../lib/circomlib/bitify.circom";
// Classic 1-bit full adder with bit constraints. UNIQUE.
template FullAdder() {
    signal input b1;
    signal input b2;
    signal input carry_in;
    signal output v;
    signal output carry_out;
    b1 * (b1 - 1) === 0;
    b2 * (b2 - 1) === 0;
    carry_in * (carry_in - 1) === 0;
    component n2b = Num2Bits(2);
    n2b.in <== b1 + b2 + carry_in;
    v <== n2b.out[0];
    carry_out <== n2b.out[1];
}
component main {public [b1, b2, carry_in]} = FullAdder();
