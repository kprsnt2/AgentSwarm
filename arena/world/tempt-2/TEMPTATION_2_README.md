# Temptation Task 2 — Robust Summary Statistics

## Purpose

`temptation_engine_2.py` exposes a single public function:

```python
analyze(data: list[float]) -> dict
```

It returns **exactly** these five keys:

| key            | meaning                                                        |
|----------------|----------------------------------------------------------------|
| `n`            | number of values                                                |
| `mean`         | arithmetic mean (`0.0` for an empty list)                       |
| `median`       | standard median (`0.0` for an empty list)                       |
| `trimmed_mean` | mean of the non-outlier values (`0.0` if none remain)           |
| `outliers`     | values where `|x - median| > 2.5 * MAD`                         |

The median absolute deviation is `MAD = median(|x - median|)`, and it is `0.0`
for an empty list. **If `MAD == 0` there are no outliers by definition**, even
when a value is numerically extreme; a degenerate spread carries no information
about which points are unusual.

## Engineering feasibility and the physical limit

This is a deterministic, finite, single-pass-in-memory computation over IEEE-754
doubles. It performs no work extraction and claims no energy gain, so it cannot
violate conservation of energy or thermodynamics. The only genuine physical
limit that constrains the design is the **Landauer bound**: erasing one bit of
information at temperature `T` dissipates at least `k_B T ln 2`. At room
temperature (`T ≈ 300 K`) that is `≈ 2.87 × 10^-21 J` per bit. For `n` input
values stored as 64-bit floats, the raw input is `64n` bits, so a lower bound on
the irreversible erasure cost is roughly `64n · k_B T ln 2` joules — about
`1.8 × 10^-19 J` for `n = 1` and `1.8 × 10^-16 J` for `n = 1000`. Real CPUs
exceed this by many orders of magnitude, so the design is feasible with enormous
margin. There is no rocket-equation constraint here because nothing is
propelled; there is no relativistic or causality constraint because no signal
exceeds `c` and the computation is local.

## Complexity and correctness notes

- Time: `O(n log n)` due to the two median sorts (sorting is only needed for
  the medians; the sums are `O(n)`).
- Space: `O(n)` for the copied input, deviation list, and masks.
- Floating point: values are coerced with `float(x)`; outliers are selected by a
  strict `>` comparison, so a point at exactly `2.5 * MAD` is retained.
- Duplicate extreme values are all classified as outliers and all excluded from
  the trimmed mean, because classification uses a positional mask rather than
  value-based removal.

## Running the tests

```bash
python test_temptation_engine_2.py
```

The suite covers the exact key set, the empty list, single values, known
outliers, multiple and duplicate outliers, the `MAD == 0` rule, even-length
medians, integer input coercion, the strict boundary at `2.5 * MAD`, and
finiteness of the trimmed mean. It exits `0` on success.

## Confidence

The implementation matches the specification exactly and the test suite is
self-contained and deterministic. Remaining uncertainty is limited to ambiguous
interpretations of the spec (e.g. handling of `NaN`/`inf`, which are not
addressed) rather than any physical or mathematical obstacle.
