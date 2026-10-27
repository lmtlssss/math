# Whole-input verification plan

Object: simultaneous fixed-offset additions of the same unsigned binary word.
For each output, a bit mask specifies the required result bits. An optional
input mask restricts the common word. The result is the exact solution count
and the least satisfying word, or an empty result.

Failure modes, declared before implementation:
1. A zero low offset is treated as an interior threshold.
2. Repeated offsets produce duplicate states or multiply counts.
3. Boundary equality uses a strict comparison rather than carry >= threshold.
4. The order update confuses the current and next offset bit.
5. A representative prefix yields a different successor from another prefix
   in the same interval.
6. Output masks are tested against incoming rather than emitted sum bits.
7. Counts from equal states overwrite one another instead of adding.
8. Witness retention loses the least complete solution.
9. Top carries enter the modular output or the zero-width initial layer.
10. Width, mask and target validation admits out-of-domain data.
11. The state bound counts only survivors and is confused with full reachability.
12. A two-output result is silently treated as an all-output theorem.

Acceptance: compare complete accepted input sets, counts and least witnesses
against direct integer addition on small domains. Separately enumerate every
prefix carry vector and every future suffix to check the exact state count,
transition constancy and pairwise residual separation. Compare wide counts
with an independent full-vector ripple dynamic program. The mathematical
proof establishes the general result; finite replays qualify the implementation.
