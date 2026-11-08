# ᑕ. — Exact State Contraction

**lmtlssss🜐 · 8 November 2026 · terminology and notation proposal 1.0**

## Definition

**ᑕ.** (spoken **TAA**) denotes *exact state contraction*: a replacement of a computational representation by a retained state that preserves a declared observation contract for every admissible input. The operator includes the reduced transition rule and the map that recovers each declared observation.

The term names a specified contract and its checkable construction. It does not name every state reduction, every hash, or a signature algorithm.

Let an input-driven system be \(M=(S,U,F,Y,G)\). Its state is \(s\in S\), input is \(u\in U\), transition is \(F:S\times U\to S\), and observation is \(G:S\times U\to Y\). Let \(Q\) be a retained-state set. An **exact state contraction for \(G\)** is a surjection \(\pi:S\to Q\), a reduced transition \(\bar F:Q\times U\to Q\), and an observation map \(\bar G:Q\times U\to Y\) such that, for every \(s,u\),

\[
\pi(F(s,u))=\bar F(\pi(s),u),\qquad
G(s,u)=\bar G(\pi(s),u).
\]

Write \(\mathsf{TAA}_{G}(M)=(Q,\pi,\bar F,\bar G)\), with printed notation **ᑕ.**. The subscript identifies the preserved contract. Exactness always has this declared scope.

### Trace theorem

If the two identities hold, the original and retained systems give equal observation traces for every initial state and every finite input word. Proof: at step zero the observations agree by the second identity. If the retained state is the image of the original state at step \(k\), the first identity preserves that relation at step \(k+1\). The second identity then preserves the next observation. Induction completes the proof.

The same construction works with nondeterministic relations when the reduced relation preserves the specified set of observable traces in both directions. If a claim concerns the *number of witnesses*, the contraction must also preserve witness counts, or establish a bijection between the relevant witness fibers. Preservation of possible outputs alone cannot establish unique witnesses.

## Affine interval form

An execution interval carries a state map and a cost function:

\[
x'=Fx+b,\qquad J(x)=x^{\mathsf T}Qx+q^{\mathsf T}x+d.
\]

For interval \(A\) followed by interval \(B\), the retained summary is

\[
\begin{aligned}
F_{BA}&=F_BF_A,\\
b_{BA}&=F_Bb_A+b_B,\\
Q_{BA}&=Q_A+F_A^{\mathsf T}Q_BF_A,\\
q_{BA}&=q_A+F_A^{\mathsf T}(q_B+2Q_Bb_A),\\
d_{BA}&=d_A+d_B+q_B^{\mathsf T}b_A+b_A^{\mathsf T}Q_Bb_A.
\end{aligned}
\]

These equations come from substituting \(F_Ax+b_A\) into \(J_B\), then adding \(J_A\). They preserve the cross-terms. Function composition and cost addition make the operation associative. The stored coefficients describe the complete chronological result for the chosen input state.

### Exact example

Let \(A:x\mapsto2x+1\), with \(J_A=x^2+1\). Let \(B:y\mapsto3y-2\), with \(J_B=2y^2+3y+4\). Their retained composite is

\[
x\mapsto6x+1,\qquad J_{BA}(x)=9x^2+14x+10.
\]

At \(x=2\), the first interval ends at 5 and costs 5. The second costs 69. The total is 74, which equals the retained polynomial at 2. The verifier in this publication checks these identities over exact rational coefficients and several input sequences.

## Certificate contract

A **ᑕ. certificate** binds an artifact digest to a precise claim, input domain, observation contract, method and method version, result, verifier identity, and evidence digest. A certificate can state **Certified**, **Broken**, or **Unknown**. A signature authenticates the issuer's statement. A separate checker establishes whether the evidence supports the statement. A transparency receipt establishes registration, not mathematical correctness.

For a statement of output uniqueness, preserve the possible output set for each declared input. For a statement of witness uniqueness, preserve witness identity or multiplicity as well. A checker must reject a claim whose preservation conditions are missing.

The term **exact** refers to the observation contract over the stated domain. It does not claim that arbitrary programs admit small contractions or that every verification problem is efficiently decidable.

## Notation and origin

The printed operator is the two-character sequence **ᑕ.**: U+1455 CANADIAN SYLLABICS TA followed by U+002E FULL STOP. Its spoken name is **TAA**. U+1455 is an existing character in the Canadian Aboriginal Syllabics block. This proposal assigns it a *new mathematical use* and retains its established linguistic identity. Unicode does not assign academic meanings to mathematical applications of existing characters.

ASCII name: `taa`. Versioned identifier: `taa.exact-state-contraction.v1`.

## Relation to prior results

The author previously proved exact affine-cost composition, cut-defect identities and minimal retained linear dimensions under explicit recovery contracts in **Affine Cycles: Exact Cut Defects and Minimal Retained State** (DOI: [10.5281/zenodo.23931722](https://doi.org/10.5281/zenodo.23931722)). Other prior papers give exact arithmetic-frontier constructions and certificates. This note names the shared *preservation contract*, proves its basic trace consequence, and fixes the printed notation. Quotient systems, congruence relations, automata minimization, bisimulation, and affine composition are established concepts. This proposal does not assert priority over those foundations.

## References

1. lmtlssss🜐, *Affine Cycles: Exact Cut Defects and Minimal Retained State*, Zenodo, 2026, DOI: 10.5281/zenodo.23931722.
2. lmtlssss🜐, *Affine Fibers and a Fibonacci Bound for Boolean–Modular Inversion*, Zenodo, 2026, DOI: 10.5281/zenodo.23697726.
3. Unicode Consortium, *Unified Canadian Aboriginal Syllabics*, Unicode Character Database, U+1455.
4. IETF, *JSON Canonicalization Scheme*, RFC 8785, 2020.
5. IETF, *An Architecture for Trustworthy and Transparent Digital Supply Chains*, RFC 9943, 2026.

**License:** CC BY 4.0 for this note. Reference verifier: MIT.
