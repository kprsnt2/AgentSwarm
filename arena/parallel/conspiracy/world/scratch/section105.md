
### 10.5 Independent audit of this pass, and what it changed

The arithmetic in `derivation3.py` and the fidelity of §10–12 to it were then
audited by a separate read-only reviewer agent, which re-derived every chain
independently. Its findings, and the resulting changes:

**Confirmed correct:** the full LLR link budget (1.03 × 10⁹ photons
intercepted, 7.03 km return footprint, 4.86 × 10⁻⁸ collection fraction, 49.8
photons at the telescope, 2.49/4.98 detected); the sensitivity table actually
bracketing the observed 1–5; the linearity of detected photons in array
aperture and all twelve inversion values; the EME comparison; the 66.7 ps
timing requirement and the 3.04 m sagitta; all six solved *p*⁎ values; the
sleep-paralysis table; and the 2.4 × 10⁵ supply ratio.

**Two substantive defects found, both now fixed in the text above:**

1. **An overstated concession in §10.3.** The first version of this section
   said the detection-rate argument "carries only if the contested 5–6% survey
   figures are right". The table's own *n* = 1,700 row refutes that: at *p* =
   10⁻², P(no record) = 3.8 × 10⁻⁸, i.e. the silence *is* surprising on the
   documented claimant count alone. The argument is weak only for *p* ≲ 10⁻³.
   §10.3 and §5.5 have been rewritten to state the concession conditionally on
   *p* rather than categorically.
2. **An overstated framing of the timing exclusion in §10.1.** "≥300× too
   broad" was presented as a hard exclusion, but a pulse width does not by
   itself bound achievable timing precision — a clean symmetric pulse can be
   centroided well below its own width given enough photons. The *hard*
   exclusion is the 51–205× photon deficit; the ~300× width is a supporting
   point. §10.1 and the script now say exactly that.

**Three lesser notes, also incorporated:** the EME figure is the laser-spot
return, not a whole-disc full-phase flux (mislabelled as the latter); the
inversion table prints QE = 0.15, which is unrealistically high for a 694 nm
photomultiplier and is shown only as an arithmetic bound; and the
§10.2 supply/demand figure divides episodes per year by a cumulative claimant
count, so the like-for-like population-to-population comparison (4.05 × 10⁸
recurrent sufferers vs 1,700 claimants) is now given as the headline.

This is recorded because the point of the exercise is the auditing trail: the
first draft of this report contained two unsourced assertions, and this pass
introduced two overstatements of its own. All four were found by checking, not
by confidence.
