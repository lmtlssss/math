# ᑕ. — Exact State Contraction

**Pronounced TAA.** Terminology proposal 1.0 · 8 November 2026 · lmtlssss🜐

ᑕ. names an exact contraction of a computation's state relative to a stated observation contract. The retained transition and observation maps commute with the original computation. The definition gives equality of each finite observation trace. An affine extension composes the exact chronological cost, including the state-dependent cross-terms.

This package contains:

- [`Exact_State_Contraction_TAA_v1.pdf`](Exact_State_Contraction_TAA_v1.pdf): two-page paper, mathematical definition, theorem, proof and affine-cost formula.
- [`paper.tex`](paper.tex): editable source.
- [`EXACT_STATE_CONTRACTION.md`](EXACT_STATE_CONTRACTION.md): definition, scope, notation and exact worked example.
- [`verify.py`](verify.py): standard-library exact rational replay.

Run `python3 verify.py`. Current replay: 1,625 rational composition cases and 3,969 trace cases; all passed. The worked example gives $T(x)=6x+1$, $J(x)=9x^2+14x+10$ and $J(2)=74$.

Printed symbol: **ᑕ.**, U+1455 CANADIAN SYLLABICS TA followed by U+002E FULL STOP. The pronunciation TAA is a proposed technical reading. The existing syllabic character retains its linguistic meaning. Programmatic identifier: `taa.exact-state-contraction.v1`.

The term specifies the exactness contract. It does not claim to invent state quotients, bisimulation, automata minimization, or the algebra of affine composition. Mathematical claims are scoped to an observation and an admissible input domain. A unique output and a unique witness are separate properties.

Foundational result: [Affine Cycles: Exact Cut Defects and Minimal Retained State](https://doi.org/10.5281/zenodo.23931722).

Open certificate transport proposal: [SCITT exact computation profile](https://github.com/lmtlssss/speedrunpapi/tree/main/standards/scitt-exact-computation).

The text and paper are offered under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The verifier is offered under [MIT](https://opensource.org/license/mit).
