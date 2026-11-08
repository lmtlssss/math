# Colony G1 · public circuit fixtures

The 18 original Circom circuits in Colony's 21-case G1 comparison are published here, byte-for-byte from the measured source corpus. The other three cases are upstream Picus benchmark circuits. Each clip's original `speedrunpapi@0.3.2` command remains reproducible. The current CLI is `0.5.1`.

Clone once:

```sh
git clone https://github.com/lmtlssss/math.git
cd math
npx --yes speedrunpapi@0.3.2 scan colony/g1/carry/modsum_safe_n4.circom --json
```

For a single case, download the linked .circom file, then scan its local pathname. `Certified` returns exit code 0; `Broken` returns 2 by design. The scope and original result are displayed in the CLI output. A Broken verdict can be a deliberate negative fixture, as indicated below.

| Circuit | Expected verdict | Rerun file |
| --- | --- | --- |
| [`modsum_safe_n4`](carry/modsum_safe_n4.circom) | Certified | `colony/g1/carry/modsum_safe_n4.circom` |
| [`modsum_safe_n8`](carry/modsum_safe_n8.circom) | Certified | `colony/g1/carry/modsum_safe_n8.circom` |
| [`modsum_safe_n16`](carry/modsum_safe_n16.circom) | Certified | `colony/g1/carry/modsum_safe_n16.circom` |
| [`modsum3_safe_n4`](carry/modsum3_safe_n4.circom) | Certified | `colony/g1/carry/modsum3_safe_n4.circom` |
| [`full_adder_bits`](carry/full_adder_bits.circom) | Certified | `colony/g1/carry/full_adder_bits.circom` |
| [`shared_input_parallel_m3_w8`](carry/shared_input_parallel_m3_w8.circom) | Certified | `colony/g1/carry/shared_input_parallel_m3_w8.circom` |
| [`cascade3_safe_n4`](carry/cascade3_safe_n4.circom) | Certified | `colony/g1/carry/cascade3_safe_n4.circom` |
| [`limb_add_safe_n4_k2`](limb/limb_add_safe_n4_k2.circom) | Certified | `colony/g1/limb/limb_add_safe_n4_k2.circom` |
| [`limb_add_safe_n4_k4`](limb/limb_add_safe_n4_k4.circom) | Certified | `colony/g1/limb/limb_add_safe_n4_k4.circom` |
| [`limb_add_safe_n8_k4`](limb/limb_add_safe_n8_k4.circom) | Certified | `colony/g1/limb/limb_add_safe_n8_k4.circom` |
| [`u4_add_safe_k8`](bitvm_model/u4_add_safe_k8.circom) | Certified | `colony/g1/bitvm_model/u4_add_safe_k8.circom` |
| [`modsum_no_bitify_n4`](buggy/modsum_no_bitify_n4.circom) | Broken | `colony/g1/buggy/modsum_no_bitify_n4.circom` |
| [`modsum_carry_not_bit_n4`](buggy/modsum_carry_not_bit_n4.circom) | Broken | `colony/g1/buggy/modsum_carry_not_bit_n4.circom` |
| [`full_adder_no_bit_checks`](buggy/full_adder_no_bit_checks.circom) | Certified | `colony/g1/buggy/full_adder_no_bit_checks.circom` |
| [`limb_add_missing_range_n4_k2`](buggy/limb_add_missing_range_n4_k2.circom) | Broken | `colony/g1/buggy/limb_add_missing_range_n4_k2.circom` |
| [`u4_add_buggy_k8`](bitvm_model/u4_add_buggy_k8.circom) | Broken | `colony/g1/bitvm_model/u4_add_buggy_k8.circom` |
| [`shared_input_no_bitify_m3_w8`](buggy/shared_input_no_bitify_m3_w8.circom) | Broken | `colony/g1/buggy/shared_input_no_bitify_m3_w8.circom` |
| [`cascade3_no_bitify_n4`](buggy/cascade3_no_bitify_n4.circom) | Broken | `colony/g1/buggy/cascade3_no_bitify_n4.circom` |

The 18 circuits use standard relative Circom includes. The required `lib/circomlib/` files are vendored with their original notices and license files so a Circom compiler can follow the imports. These are third-party sources by 0KIMS/circomlib, separate from the original Colony fixtures.

The remaining three G1 sources are publicly maintained with Picus: `test_bigadd_15.circom`, `test_bigadd_23.circom` and `BinSum@binsum.circom`. The SHA-256 compression lead clip is a separate circomlib benchmark. The full 21-case comparison is on [Colony's leaderboard](https://colony.technology/leaderboard); the live checker is [here](https://colony.technology/checker).

To repeat a source-bound check with today's published package, substitute `speedrunpapi@0.5.1` in the same command. The source paths are unchanged.
