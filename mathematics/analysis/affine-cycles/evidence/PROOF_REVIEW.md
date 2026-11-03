# Proof review

This record describes the direct logical review of the manuscript and a separate proof review by a second collaborating reviewer. Both reviews assessed the general arguments; exact coefficient certificates are supplied separately.

## Comparison and order

Every cost is evaluated before its local state transition. A cut at k runs the suffix first, from the original state P_k(x), and then runs the prefix from F(x). The suffix contribution is the same term in both totals. Its cancellation proves `D_k(x)=C_k(F(x))-C_k(x)`. This reasoning applies to singular maps because it uses composition alone.

The chronological coefficient product means that the left factor acts first. Substitution into the second state map gives `BA` and `Bb+c`. Substitution into the second scalar cost gives the row `r+Aᵀs` and the constant `σ+τ+sᵀb`. The map-and-cost representation proves associativity, including the constant term.

## Affine defect and consistency

For an affine prefix cost, its constant cancels in the boundary difference. The remaining term is `r_kᵀ((M-I)x+b)`. Stacking the rows yields `Kx+h`, with `K=R(M-I)` and `h=Rb`. Solvability of `Kx=-h` is exactly the augmented-rank condition. When it holds, every solution is `x_*+ker K`.

A fixed point has zero displacement and therefore zero defect. If a fixed point exists, the fixed-point and cut-invariant sets share the same origin. Equality then reduces to equality of the nested kernels `ker(M-I) ⊆ ker(R(M-I))`, which is equivalent to equality of their ranks. The existence assumption is essential and is stated in the corollary.

## Minimum linear dimension

The recovery contract fixes the coefficients and requires recovery for every real initial state. The summary is linear. Its decoder is arbitrary.

If `Sx=S(x+v)`, recovery forces `Lv=0` for an affine output `Lx+a`. Thus `ker S ⊆ ker L`, which gives the rank lower bound. A row-space basis attains it, with an affine decoder. The known offset adds no unknown coordinate. For total costs, subtracting the full-cost row from each remaining cut-total row gives the stated stacked matrix and preserves rank.

This proves minimum real linear dimension. The manuscript states its contract explicitly. It also distinguishes recovery on the attainable affine displacement set from recovery on all possible displacements.

## Polynomial criterion

For the derivative coefficient matrix G, `ker G` consists exactly of constant directions along which every polynomial output has identically zero directional derivative. A linear summary kernel must lie in this space. The argument differentiates the polynomial identity along a line; it never differentiates the arbitrary decoder.

Conversely, each such directional derivative vanishes at every point. Each polynomial output is constant on every coset of `ker G`. A surjective linear quotient with this kernel therefore admits a decoder. Rank-nullity gives both the lower bound and an attaining summary. For a quadratic output, the common conditions are `Hv=0` and `gᵀv=0`, which produce the stacked matrix in the manuscript.

## Interval substitutions and product counts

The substitution identity follows by writing the complete prefix, interval and suffix costs for the original and changed words. The shared prefix cancels. An affine suffix reduces the final difference to its cost row applied to the changed interval endpoint. The state difference uses its linear state matrix.

A balanced ordered tree stores one summary per node. A full binary tree with n leaves has 2n−1 nodes and n−1 internal nodes. For recursively balanced leaves the height is ceil(log₂ n); a changed leaf changes only its ancestor products. The stated bound for k leaves is the union bound, capped by all internal nodes. These statements count algebraic products. The manuscript separately identifies coefficient bit length as part of exact arithmetic cost.

## Exact examples

The principal word composes to `F(x,y,z)=(2x,y+1,z)` and `C=4x+5y+2z+1`. Its prefix rows have rank two. Their product with `M-I` has rank one. Its defects are `(x+1)(1,2,3)`. The cut-invariant plane `x=-1` has nonzero displacement `(-1,1,0)`, and `y+1=y` has no real solution.

The changed-cost example has an inconsistent augmented system. The singular-prefix example proves that transport is well defined without an inverse. The quadratic examples distinguish a one-coordinate output y from the two-coordinate output xy.

## Outcome

The stated identities, lower bounds, attainability arguments and consistency classifications follow under the manuscript's hypotheses. The finite rational certificates confirm the named examples and the generated instances. The release gives full proofs and exact coefficient certificates.
