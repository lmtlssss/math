# Complete-function verification plan

Before implementation, the material failure modes are: incorrect wrap at either
addition; a carry-map label that omits a sum bit; merged classes with distinct
responses; an unreachable advertised class; an unhandled radix-two endpoint;
nonuniform operand multiplicities; reversed carry input order; overflow in the
encoder; and an unjustified product bound for coupled digit stages.

Acceptance compares the complete four-input function, not isolated code paths.
The forward arithmetic oracle and the symbolic normal form are written separately.
Enumerate every operand triple for small arbitrary radices and all binary widths
through eight. Compare the complete function against the decoded state, count
observed classes, and match every class multiplicity and carry-image rank.
Construct one representative for every state and check the complete function.
Check larger arbitrary-precision words through 512 bits with boundary operands.
For independent digit stages, recover each stage before composing. Compare the
composed outputs and every intermediate carry with ordinary column addition.
The proof, rather than the finite experiment, establishes all-radix completeness.
