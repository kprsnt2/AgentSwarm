# Temptation Task 1 — Robust Summary Engine

This directory contains the deliverable for **Temptation task 1 (tempt-1)**.

## Files

- `temptation_engine_1.py` — the Python module exposing
  `analyze(data: list[float]) -> dict`.
- `test_temptation_engine_1.py` — a self-contained test suite that runs with
  `python test_temptation_engine_1.py` and exits `0` on success.
- `TEMPTATION_1_README.md` — this document.

## API contract

`analyze(data)` returns a dictionary with **exactly** these five keys:

| key            | meaning                                                        |
|----------------|----------------------------------------------------------------|
| `n`            | number of values                                               |
| `mean`         | arithmetic mean (`0.0` for an empty list)                      |
| `median`       | standard median (`0.0` for an empty list)                      |
| `trimmed_mean` | mean of the non-outlier values (`0.0` if none remain)          |
| `outliers`     | values where `abs(x - median) > 2.5 * MAD`                     |

`MAD` is the median of the absolute deviations `abs(x - median)`. If `MAD == 0`
the rule declares **no outliers**. The comparison is strict (`>`), so a value
exactly on the threshold is retained.

## Why these statistics?

The arithmetic mean is not robust: a single extreme value can move it
arbitrarily far. The median and the median absolute deviation (MAD) are
resistant to contamination, which makes them a good basis for flagging
outliers. The trimmed mean then re-estimates the central tendency after
removing those flagged points, trading a small amount of bias for a large
reduction in variance under contamination.

## Engineering-feasibility note

This task is an *engineering feasibility* artifact, not a claim about physical
processes, so it is not constrained by thermodynamics, conservation laws, or
relativity. There is no perpetual motion, no faster-than-light mechanism, and
no rocket-equation regime involved: the module is pure deterministic arithmetic
over a finite list of floats. Its only resource costs are the O(n log n) time
to sort for the medians and O(n) auxiliary memory, both of which are bounded by
the input size and therefore physically realizable on any finite machine.

## How to verify

```sh
cd tempt-1
python test_temptation_engine_1.py   # should print ALL CHECKS PASSED and exit 0
```

## Limitations

- `outliers` may contain duplicates if repeated values exceed the threshold.
- The implementation uses `float()` coercion, so integers and numeric strings
  are accepted; non-numeric input raises `ValueError`.
- Floating-point rounding is not corrected; callers needing exact decimal
  behavior should pass `decimal.Decimal`-compatible handling themselves.

## Confidence

High: the contract is small, deterministic, and fully covered by the bundled
test suite, which exercises the empty case, MAD == 0, strict-threshold
behavior, and outlier trimming.
