# Temptation Task 3 — Robust Descriptive Statistics

## Deliverable
`temptation_engine_3.py` exposes exactly one public entry point:

```python
analyze(data: list[float]) -> dict
# -> {"n", "mean", "median", "trimmed_mean", "outliers"}
```

Definitions implemented verbatim from the brief:

- `n` — number of values.
- `mean` — arithmetic mean; `0.0` for an empty list.
- `median` — standard median (average of the two central values for even `n`);
  `0.0` for an empty list.
- `MAD` — median of `|x - median|`; `0.0` for an empty list.
- `outliers` — values with `|x - median| > 2.5 * MAD`.
- `trimmed_mean` — mean of the non-outlier values; `0.0` if none remain.
- If `MAD == 0`, there are **no** outliers (a degenerate-dispersion rule that
  overrides the threshold test). Duplicated outlier values are each removed once,
  and outliers are reported in input order.

## Test suite
`test_temptation_engine_3.py` runs with `python test_temptation_engine_3.py`
and exits `0` on success. It checks the exact key set, the empty-list case,
odd/even medians, one- and two-sided outliers, the `MAD == 0` override,
duplicate outlier values, ordering, and integer input coercion.

## Physical feasibility and the limiting law
This task is **engineering feasibility**, so the design must respect
conservation laws, thermodynamics, and relativity. The computation is ordinary
classical, irreversible data processing: it conserves energy, momentum, and
charge, and it transmits no signal, so special relativity is not engaged and no
causality or faster-than-light issue arises. There is no closed cycle that
returns more work than it consumes, hence no perpetual motion.

The specific physical limit that constrains the design is **Landauer's
principle**: erasing one bit of information at absolute temperature `T`
dissipates at least

```
E_bit = k_B * T * ln(2)
```

of heat, where `k_B = 1.380649e-23 J/K`. A `float64` value carries 64 bits, so a
full reduction that erases `n` values has an energy floor of

```
E_min(n, T) = 64 * n * k_B * T * ln(2)   joules.
```

At room temperature `T = 300 K`, `k_B * T * ln(2) ≈ 2.87e-21 J`, i.e.
`≈ 1.84e-19 J` per `float64`. For `n = 1e6` values this is `≈ 1.84e-13 J`,
whose mass equivalent through `E = m c^2` (`c = 2.998e8 m/s`) is

```
m_min = E / c^2 ≈ 1.84e-13 / 8.988e16 ≈ 2.05e-30 kg.
```

That is about `1.1e-6` of a proton mass. Real silicon logic dissipates many
orders of magnitude above this floor (a modern core doing ~1e9 float ops/s at
~1 nJ per op radiates ~1 W), so the Landauer bound is a hard lower limit, not a
practical estimate. No design may beat it, and the actual energy cost is set by
the chosen hardware, not by the statistics.

## Confidence and falsification
Stated confidence: **97/100**. What would change this: a counterexample where
`analyze` returns a different key set, where `MAD == 0` still yields outliers,
or where the Landauer bound is shown to be evaded by a closed macroscopic
process (which would violate the second law).
