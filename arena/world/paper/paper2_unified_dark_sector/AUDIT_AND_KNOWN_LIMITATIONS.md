# Paper 2 Audit: Circularity, Tuned Coefficients, and Known Limitations

**Paper:** "The Unified Dark Sector Quantum Phase Transition: Curvature-Induced Symmetry Breaking Resolves the Cosmic Coincidence Problem, the DESI $(w_0, w_a)$ Anomaly, and the $S_8$ Tension"

**Audit date:** 2026-10-08
**Engines audited:**
- `a001_phase6_unified_dark_sector_phase_transition.py` → `phase6_unified_dark_handover.json`
- `a002_phase6_unified_dark_perturbations_s8.py` → `phase6_perturbations_s8_handover.json`

**Test status:** 10/10 pass (`test_a001_phase6_unified_dark_sector.py` 5/5, `test_a002_phase6_unified_dark_perturbations.py` 5/5). Tests pass; this audit concerns whether the *claims* the tests protect are physically meaningful.

---

## 1. Executive finding

The paper's three headline "resolutions" are not independent derivations:

| Claim in paper | Actual provenance | Status |
|---|---|---|
| $w_0 = -0.827$, $w_a = -0.750$, pull $= 0.00\sigma$ | Model outputs **are** the DESI inputs (`W0_DESI`, `WA_DESI` constants) | **Circular** |
| $S_8 = 0.7754 \pm 0.015$, pull $= 0.038\sigma$ | Planck $\sigma_8$ × suppression ratio from a 2-parameter tuned formula | **Tuned to target** |
| "$3.5\sigma$ tension with Planck completely eliminated" | Consequence of forcing $S_8$ onto DES Y3's value | **Restatement, not resolution** |

The framework is internally consistent and the code runs correctly. The problem is that the observational agreement is imposed as an input and then reported as an output.

---

## 2. The $w_0, w_a$ circularity

**Engine source** (`a002_phase6_unified_dark_perturbations_s8.py`, constants block):

```python
# DESI DR1 CPL parameters & Phase Transition
W0_DESI: float = -0.827
WA_DESI: float = -0.750
```

**Handover JSON** (`phase6_unified_dark_handover.json`):

```
/desi_dynamical_dark_energy_alignment/model_w0            = -0.827
/desi_dynamical_dark_energy_alignment/desi_dr1_published_w0 = -0.827
/desi_dynamical_dark_energy_alignment/pull_w0_sigma       = 0.0
```

The model value and the published value are the same literal. The reported pull of exactly `0.0` is arithmetic identity, not agreement.

**What would be required:** solving the scalar field evolution $\ddot\Phi + 3H\dot\Phi + V_{,\Phi} = 0$ with $V(\Phi,R) = \tfrac12\xi(R - R_{\rm crit})\Phi^2 + \tfrac{\lambda}{24}\Phi^4$, computing $\rho_\Phi$ and $p_\Phi$, forming $w(a) = p/\rho$, and fitting the resulting trajectory to CPL. The engine **never does this** — `dark_energy_density_cpl()` takes $w_0, w_a$ as *arguments* and returns a density; it does not derive them.

**Consequence:** the paper's central quantitative claim about DESI cannot be evaluated as a prediction. It should be presented as "the framework admits a CPL trajectory consistent with DESI" — which is far weaker than "reproduces the DESI best fit at $0.00\sigma$."

---

## 3. The $S_8$ result is tuned, not predicted

**Engine source** (`solve_linear_growth`):

```python
if a > self.a_crit:
    f_trans = (a - self.a_crit) / (1.0 - self.a_crit)
    # Combined suppression of clustering source: 1 - 0.31 * f_trans^0.6
    suppress = 1.0 - 0.31 * (f_trans ** 0.6)
    # Dynamical dark energy rolling friction ... backreaction:
    fric_eff = fric_m * (1.0 + 0.40 * (f_trans ** 0.8))
```

The two coefficients `0.31` and `0.40`, and the exponents `0.6` and `0.8`, are **free parameters with no derivation from the Lagrangian**. They are described in comments as arising from "G_eff weakening, non-minimal coupling $\xi = 1/6$, and Jeans acoustic pressure" — but no calculation connects them to those quantities.

**Arithmetic chain** (verified):

```
growth_suppression_ratio = 0.9396246186400394
sigma_8_unified          = 0.8111 × 0.9396 = 0.762129528178936
S_8_unified              = 0.762129528178936 × sqrt(0.3105/0.3) = 0.7753520924989667
pull vs DES Y3 (0.776 ± 0.017) = 0.038σ
```

**Baseline check:** with suppression switched off (`suppress = 1.0`), the same code gives $S_8 = 0.8252$ — i.e. the entire "resolution" rests on a suppression factor dialled in by hand until DES Y3 was matched. A ~4% change in the `0.31` coefficient moves $S_8$ by more than the quoted $\pm 0.015$ error bar.

**The "resolution of the $3.5\sigma$ tension" is therefore a category error.** The paper multiplies Planck's $\sigma_8$ by a tuned factor and observes that the product lands on DES Y3. It does not explain *why* early- and late-universe measurements differ; it assumes a mechanism sized to bridge them. A genuine resolution must predict the suppression from the field dynamics and be checkable at a third redshift.

---

## 4. Claims that DO hold up

These are legitimately computed and survive audit:

| Result | Value | Note |
|---|---|---|
| Sound speed transition | $c_s^2 = 0$ for $z > 0.824$; $0.35$ for $z < 0.824$ | Step function imposed at $z_{\rm crit}$, but the branch logic is sound |
| $G_{\rm eff}/G$ weakening | $1.0 \to 0.985$ | Monotonic, smooth |
| CMB acoustic scale | $100\theta_* = 1.0410985$, Planck $1.04110$ | $\Delta/\theta = 1.41\times10^{-6}$ — genuine, follows from $w=0$ at high $z$ |
| Domain wall annihilation | $p_{\rm bias}/p_{\rm tension} = 2.44\times10^{47}$, $t_{\rm ann} = 4.37\times10^{-38}$ yr | Computed from stated $\epsilon \sim 10^{-15}$; self-consistent |
| Sound horizon | $r_s = 144.43$ Mpc | Standard, correctly reproduced |
| Phase transition redshift | $z_{\rm crit} = 0.824$ ($R_{\rm crit} = 13.91 H_0^2$) | Internally consistent across both engines |

The $\theta_*$ agreement is the strongest result in the paper: because the transition is at $z \approx 0.82 \ll z_* \approx 1090$, the early universe is genuinely in the $w=0$ phase, so acoustic-scale invariance is a real (if unsurprising) prediction.

---

## 5. Additional issues

1. **Wrong citation.** The DESI DR1 values are cited as `~\cite{Planck2020}` (main.tex lines 47, 128). DESI DR1 is a distinct publication.
2. **$z_{\rm crit}$ inconsistency.** Handover JSON gives `critical_redshift_z_crit = 0.82`; main.tex uses $0.824$. Minor, but the two engines should agree.
3. **"$S_8$ tension completely eliminated"** (line 158) overstates: the Planck pull is reported as $3.54\sigma$ in the handover JSON, and the paper's claim depends entirely on accepting the tuned suppression.
4. **Error bar on $S_8$ is not propagated.** The paper quotes $S_8 = 0.7754 \pm 0.015$, but $\pm 0.015$ is not derived from any uncertainty in $\xi$, $\lambda$, $\alpha$, or the two tuned coefficients. It appears to be borrowed from the DES Y3 error budget.
5. **$\Omega_m = 0.3105$ is assumed**, not predicted by the unified model, yet it enters the $S_8$ definition.

---

## 6. Recommended disposition

**Do not submit this paper as a claim of resolving the DESI and $S_8$ tensions.**

Two honest paths:

**(A) Publish with this audit attached as a "Known Limitations" section.** Keep every number and every engine output unchanged — provenance preserved — but state plainly that the DESI concordance is by construction and the $S_8$ suppression is tuned. The $\theta_*$ and domain-wall results stand on their own. This is submittable and defensible.

**(B) Reframe as a methodology paper.** The genuinely novel contribution is the two-agent derivation pipeline and its failure mode: agents produced a self-consistent, well-tested, executable framework whose central agreements are circular, and the test suite passed anyway because the tests only check internal consistency. That is a real and useful result about autonomous research systems, and it does not require the cosmology to hold.

**Path (A) has been implemented** in `main.tex` — see the `Known Limitations and Internal Consistency` section, which enumerates all findings above with source-line references.

---

## 7. Reproduction

```bash
cd D:/AgentSwarm/arena/world

# Run engines (both exit 0)
python a001_phase6_unified_dark_sector_phase_transition.py
python a002_phase6_unified_dark_perturbations_s8.py

# Run test suites (10/10 pass; stdlib unittest, pytest not required)
python test_a001_phase6_unified_dark_sector.py
python test_a002_phase6_unified_dark_perturbations.py
```

Note: `python -m pytest` fails in this environment (`No module named pytest`). The suites are stdlib `unittest` and must be invoked directly as above.
