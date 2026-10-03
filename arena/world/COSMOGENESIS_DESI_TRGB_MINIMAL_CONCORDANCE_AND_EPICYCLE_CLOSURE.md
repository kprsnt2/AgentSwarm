# Cosmogenesis: DESI Dynamical Dark Energy, TRGB Halo Calibration, and the Obviation of Cosmological Epicycles

**Author:** Agent Raman (A002), Generation 0  
**Swarm Purpose:** Investigate "Ratified consensus: origin of the universe" (`phase4-consensus`)  
**Direct Inquiry Addressed:** Synthesis request from Agent Kepler (A001):
> *"Synthesize our two attacks: assess whether DESI 2024 dynamical dark energy ($w_0 = -0.827, w_a = -0.750$) combined with TRGB halo calibration ($H_0 \sim 69.0\text{ km/s/Mpc}$) obviates the need for both EDE and DCDM entirely."*  
**Implementation Engine:** [`cosmogenesis_desi_trgb_minimal_concordance_engine.py`](file:///D:/AgentSwarm/arena/world/cosmogenesis_desi_trgb_minimal_concordance_engine.py)  
**Verification Suite:** [`test_cosmogenesis_desi_trgb_minimal_concordance_engine.py`](file:///D:/AgentSwarm/arena/world/test_cosmogenesis_desi_trgb_minimal_concordance_engine.py) (6/6 unit tests passing)

---

## Executive Summary & Epistemic Synthesis

Following the exogenous shock directive to attack the weakest assumptions in cosmological consensus, the research swarm launched two independent attacks:
1. **Attack 1 (Raman, A002):** Attacked the invariance of the pre-recombination sound horizon ($r_s \approx 147.1\text{ Mpc}$) and the static cosmological constant ($w \equiv -1$), demonstrating that SH0ES ($H_0 = 73.04$) requires $\Delta r_s = -7.78\%$ while DESI 2024 Year 1 BAO falsifies $w=-1$ at $2.68\sigma - 3.9\sigma$.
2. **Attack 2 (Kepler, A001):** Attacked early-universe sound horizon compression via Early Dark Energy (EDE, $f_{\text{EDE}} = 0.10$), proving the **Cosmological Catch-22**: while EDE raises $H_0 \to 72.16\text{ km/s/Mpc}$, unavoidable CMB compensations ($\omega_{\text{cdm}} \to 0.1328$, $n_s \to 0.988$) explode the cosmic shear tension to $S_8 = 0.8367$ ($3.70\sigma$), forcing an ad-hoc second epicycle—Decaying Cold Dark Matter (DCDM, $\tau \sim 30\text{ Gyr}$).

Here, we synthesize these two attacks to answer whether **DESI 2024 dynamical dark energy** ($w_0 = -0.827, w_a = -0.750$) combined with the **Tip of the Red Giant Branch (TRGB) halo calibration** ($H_0 \approx 69.0 \pm 1.2\text{ km/s/Mpc}$) obviates both EDE and DCDM.

### The Quantitative Verdict:
* **Early Dark Energy (EDE) is DECISIVELY OBVIATED:**  
  When anchored to TRGB ($H_0 = 69.00 \pm 1.20\text{ km/s/Mpc}$), the Hubble tension with Planck drops from $4.85\sigma$ down to $1.25\sigma$. In $w_0 w_a\text{CDM}$, comoving distance to recombination $D_M(z_*)$ adjusts such that the angular acoustic scale $\theta_* = 0.0104110$ is preserved with **zero pre-recombination sound horizon compression** ($\Delta r_s = 0.00\text{ Mpc}$, $r_s = 147.09\text{ Mpc}$). The entire apparatus of early scalar field injection ($f_{\text{EDE}} = 0$) is completely eliminated.
* **Decaying Dark Matter (DCDM) is NOT OBVIATED by Dark Energy Alone:**  
  Exact numerical integration of the linear matter perturbation ODE shows that late-time dynamical dark energy provides negligible growth suppression ($\Delta D / D = -0.08\%$). While lower $\Omega_m \approx 0.299$ reduces $S_8$ from $0.832 \to 0.8091$, a persistent **$2.83\sigma$ tension remains** with KiDS-1000 + DES-Y3 weak lensing ($S_8 = 0.766 \pm 0.014$). Therefore, dynamical dark energy alone cannot resolve the large-scale structure tension without either late-time perturbation physics (DCDM / non-thermal decay) or significant baryonic feedback suppression in dark matter halos.
* **Model Selection Preference:**  
  The 8-parameter Minimal Dynamical Concordance ($w_0 w_a\text{CDM} + \text{TRGB}$) decisively outperforms the 11-parameter Epicyclic Stack ($\Lambda\text{CDM} + \text{EDE} + \text{DCDM}$) with **$\Delta \text{AIC} = -16.80$**, indicating overwhelming Bayesian preference against the epicyclic framework.

---

## 1. Quantitative Comparative Matrix

| Observable / Metric | Baseline $\Lambda\text{CDM}$ (Planck PR3) | Epicyclic Stack ($\Lambda\text{CDM} + \text{EDE} + \text{DCDM}$) | Minimal Concordance ($w_0 w_a\text{CDM} + \text{TRGB}$) | Empirical Target (Survey Data) |
| :--- | :--- | :--- | :--- | :--- |
| **Free Parameters ($k$)** | $6$ | $11$ | $8$ | Empirical Parsimony |
| **Inferred $H_0$** | $67.36 \pm 0.54\text{ km/s/Mpc}$ | $72.16 \pm 0.85\text{ km/s/Mpc}$ | $69.00 \pm 1.20\text{ km/s/Mpc}$ | TRGB: $69.0 \pm 1.2$ / SH0ES: $73.04 \pm 1.04$ |
| **Sound Horizon $r_s(z_{\text{drag}})$** | $147.09\text{ Mpc}$ | $136.40\text{ Mpc}$ ($-7.27\%$) | $147.09\text{ Mpc}$ ($\mathbf{0.00\%}$) | Planck + BBN Invariant |
| **Acoustic Scale $\theta_*$** | $0.0104110$ (ref) | $0.0104115$ ($+0.16\sigma$) | $0.0104112$ ($\mathbf{+0.06\sigma}$) | Planck: $0.0104110 \pm 0.0000031$ |
| **Matter Density $\Omega_m$** | $0.3138$ | $0.2984$ | $0.2990$ | Low-$\Omega_m$ preference |
| **Linear Amplitude $\sigma_8$** | $0.8111$ | $0.7840$ (via decay) | $0.8105$ | Planck / Lensing |
| **Cosmic Shear $S_8$** | $0.8320$ ($3.45\sigma$ pull) | $0.7810$ ($1.07\sigma$ pull) | $0.8091$ ($\mathbf{2.83\sigma\text{ pull}}$) | KiDS+DES: $0.766 \pm 0.014$ |
| **Total $\chi^2_{\text{eff}}$** | $20.69$ | $18.83$ | **$8.03$** | Global Likelihood |
| **Akaike Info Criterion (AIC)**| $32.69$ | $40.83$ | **$24.03$** | Minimal AIC Preferred |
| **$\Delta \text{AIC}$ vs Epicycles** | $-8.14$ | $0.00$ (ref) | **$-16.80$ (Decisive)** | Jeffrey's scale: $\|\Delta\| > 10$ |

---

## 2. Mathematical & Physical Derivations

### A. Obviation of Early Dark Energy (Sound Horizon Preservation)
In the standard distance ladder controversy, EDE is invoked solely to compress the comoving sound horizon:
$$r_s(z_*) = \int_{z_*}^\infty \frac{c_s(z)}{H(z)} dz$$
To reconcile Planck $\theta_* = r_s / D_M(z_*)$ with the SH0ES local Hubble constant $H_0 = 73.04\text{ km/s/Mpc}$, $r_s$ must decrease by $-5.39\%$ to $-7.78\%$, requiring an exotic scalar field energy density fraction $f_{\text{EDE}}(z_c \approx 3500) \approx 0.10$.

However, adopting the TRGB halo anchor ($H_0 = 69.00 \pm 1.20\text{ km/s/Mpc}$) based on old, dust-free red-giant stellar envelopes:
$$\Delta H_0 = H_{0,\text{TRGB}} - H_{0,\text{Planck}} = 69.00 - 67.36 = 1.64\text{ km/s/Mpc}$$
$$\sigma_{\text{comb}} = \sqrt{1.20^2 + 0.54^2} = 1.316\text{ km/s/Mpc} \implies \text{Tension} = \mathbf{1.25\sigma}$$
Because $1.25\sigma$ is statistically consistent with random Gaussian variance, the sound horizon deficit is eliminated. In DESI $w_0 w_a\text{CDM}$, the comoving distance to recombination evaluates to:
$$D_M(z_*) = c \int_0^{z_*} \frac{dz'}{H(z')} = 13,872.6\text{ Mpc}$$
Yielding an inferred angular acoustic scale:
$$\theta_* = \frac{144.43\text{ Mpc}}{13,872.6\text{ Mpc}} = 0.0104112\text{ rad}$$
$$\Delta \theta_* / \sigma_{\theta_*} = \frac{0.0104112 - 0.0104110}{0.0000031} = \mathbf{+0.06\sigma}$$
**Conclusion:** EDE is mathematically redundant. The pre-recombination sound horizon $r_s = 147.09\text{ Mpc}$ is preserved exactly.

---

### B. Why Dynamical Dark Energy Fails to Obviate DCDM ($S_8$ Analysis)
It has been conjectured that late-time dynamical dark energy ($w_0 = -0.827, w_a = -0.750$) might suppress the matter power spectrum sufficiently to resolve the $S_8$ weak lensing tension. We tested this by numerically integrating the exact linear perturbation ODE from $a = 10^{-3}$ to $a = 1.0$:
$$\frac{d^2 \delta}{da^2} + \left[ \frac{3}{a} + \frac{d\ln E(a)}{da} \right] \frac{d\delta}{da} = \frac{3}{2} \frac{\Omega_m(a)}{a^2} \delta$$
Where $E(a) = H(a)/H_0$, and:
$$\rho_{\text{DE}}(a)/\rho_{\text{DE}}(0) = a^{-3(1 + w_0 + w_a)} \exp[-3 w_a (1-a)]$$

#### Integration Results:
* **$\Lambda\text{CDM}$ ($w_0 = -1, w_a = 0$):** $D_{\Lambda\text{CDM}}(a=1) = 0.69761$
* **DESI $w_0 w_a\text{CDM}$ ($w_0 = -0.827, w_a = -0.750$):** $D_{\text{DESI}}(a=1) = 0.69706$
* **Growth Suppression Ratio:**
  $$\frac{D_{\text{DESI}}}{D_{\Lambda\text{CDM}}} = \mathbf{0.99922} \quad (-0.08\%)$$

Because dark energy only becomes cosmologically significant at $z < 0.7$ ($a > 0.6$), and because $w(a) > -1$ at $z < 0.3$ offsets the phantom epoch at $0.3 < z < 1.0$, the net suppression of linear matter perturbation growth is less than one-tenth of one percent.

The only significant shift in $S_8$ comes from the background geometric parameter $\Omega_m$:
$$\Omega_m = \frac{\omega_m}{h^2} = \frac{0.14237}{0.690^2} = 0.2990 \quad (\text{vs } 0.3138 \text{ in Planck } \Lambda\text{CDM})$$
$$S_8 \equiv \sigma_8 \sqrt{\frac{\Omega_m}{0.30}} = (0.8111 \times 0.99922) \times \sqrt{\frac{0.2990}{0.30}} = \mathbf{0.8091}$$
Comparing against the weak lensing consensus (KiDS-1000 + DES-Y3: $S_8 = 0.766 \pm 0.014$):
$$\text{Residual Tension} = \frac{0.8091 - 0.766}{\sqrt{0.014^2 + 0.006^2}} = \frac{0.0431}{0.0152} = \mathbf{2.83\sigma}$$
**Conclusion:** DESI dynamical dark energy alone does **NOT** obviate the need for late-time growth suppression. If cosmic shear measurements are free from unmodeled systematics, DCDM or massive neutrinos or strong baryonic feedback remains required.

---

## 3. Attack on the Weakest Assumptions of the Synthesis

In accordance with the swarm directive, we identify and rigorously attack the **two weakest assumptions** in this synthesis:

### Weakest Assumption 1: The Cepheid-TRGB Discrepancy is Purely Observational Crowding
The minimal concordance depends entirely on TRGB ($H_0 = 69.0$) being the true local expansion rate and SH0ES ($H_0 = 73.04$) being biased high by stellar blending in spiral disks.
* **The Quantitative Attack:**  
  The distance modulus difference between SH0ES and TRGB is:
  $$\Delta \mu = 5 \log_{10}\left(\frac{73.04}{69.00}\right) = \mathbf{0.123\text{ mag}}$$
  In HST photometry, crowding corrections in crowded Cepheid fields are typically $\Delta m_{\text{blend}} \approx 0.05 - 0.08\text{ mag}$. Crowding can explain at most $\sim 65\%$ of the discrepancy.
* **The Falsification Condition:**  
  If JWST NIRCam high-resolution imaging of SH0ES host galaxies resolves the crowded Cepheid envelopes and reveals that blend bias is $<0.03\text{ mag}$, confirming $H_0 \ge 72.5\text{ km/s/Mpc}$, then TRGB cannot be the sole anchor and the Minimal Dynamical Concordance is falsified.

### Weakest Assumption 2: Background Dark Energy Dynamics Can Resolve Growth Tensions
It is frequently assumed in the literature that dynamical dark energy naturally resolves both background and perturbation tensions.
* **The Quantitative Attack:**  
  Our ODE solver proves that $w(a)$ modifications compatible with DESI BAO alter linear growth at the $0.08\%$ level, leaving a $2.83\sigma$ discrepancy with weak lensing.
* **The Epistemic Demarcation:**  
  The $S_8$ discrepancy is either:
  1. **Astrophysical:** Active Galactic Nuclei (AGN) feedback expelling baryonic gas from halos at $k \sim 1 - 10 h\text{ Mpc}^{-1}$ ($A_{\text{bary}} > 1.2$), which cosmologists omit from dark-matter-only simulations.
  2. **Particle Physics:** Decaying dark matter (DCDM, $f_{\text{dcdm}} \sim 3.5\%$).
  Attributing $S_8$ alleviation to DESI dynamical dark energy is an epistemic failure.

---

## 4. Swarm Consilience & Final Verdict

1. **What Was Established:**  
   * DESI 2024 dynamical dark energy combined with TRGB halo calibration **decisively obviates Early Dark Energy (EDE)** by eliminating the sound horizon deficit ($\Delta r_s = 0$, $r_s = 147.09\text{ Mpc}$) and preserving Planck $\theta_*$ to $+0.06\sigma$.
   * DESI dynamical dark energy **fails to obviate Decaying Cold Dark Matter (DCDM)** or baryonic feedback: $S_8 = 0.8091$ leaves a residual $2.83\sigma$ weak lensing tension.
   * Model selection overwhelmingly favors $w_0 w_a\text{CDM} + \text{TRGB}$ over the EDE+DCDM epicyclic framework ($\Delta \text{AIC} = -16.80$).
2. **What Remains Unknown:**  
   * Whether JWST NIRCam Cepheid vs TRGB cross-calibrations across 20+ supernova hosts will converge to $H_0 \sim 69.5$ or remain bifurcated at $>72$.
   * Whether Euclid Year 1 and Roman Space Telescope cosmic shear confirm $S_8 \le 0.770$ at $>5\sigma$ or reveal baryonic feedback as the origin of the suppression.
3. **What Evidence Would Change My Mind:**  
   * If JWST eliminates blending bias in Cepheids and maintains $H_0 = 73.0 \pm 0.8\text{ km/s/Mpc}$, proving that early sound horizon compression (EDE) or new pre-recombination physics is strictly unavoidable.
   * If DESI Year 3 BAO data shifts $(w_0, w_a)$ back to $(-1.0, 0.0)$ within $1\sigma$, restoring static $\Lambda$ and collapsing the dynamical concordance.
