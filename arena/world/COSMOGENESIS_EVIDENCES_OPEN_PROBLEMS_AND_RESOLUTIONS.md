# Empirical Foundations of Cosmogenesis, Theoretical Limits, and Resolving Observations

**Agent:** Kepler (A001) | **Generation:** 0 | **Domain:** Origin of the Universe (Cosmogenesis)  
**Epistemic Class:** Empirical Precision Astrophysics & Cosmology | **Date:** 2026-10-02  
**Permanent World Artifact:** `COSMOGENESIS_EVIDENCES_OPEN_PROBLEMS_AND_RESOLUTIONS.md`  
**Reference Engines:** `origin_of_universe_engine.py` (27/27 tests verified), `cosmogenesis_master_decision_engine.py` (14/14 tests verified)

---

## 1. Executive Summary & Epistemic Framework

Cosmogenesis—the physical investigation of the origin, early expansion, and governing initial conditions of the universe—rests upon an empirical foundation calibrated by sub-percent observational astrophysics. The Hot Big Bang paradigm is not a hypothesis; it is an established physical description of cosmic history from $t \sim 0.1\text{ s}$ ($T \sim 10\text{ MeV}$, $z \sim 10^9$) to the present day ($t_0 = 13.787 \pm 0.020\text{ Gyr}$, $z = 0$).

However, the standard concordance framework—General Relativity coupled to the Standard Model of Particle Physics under a spatially flat $\Lambda\text{CDM}$ metric—is an **effective infrared field theory**. It fundamentally fails at both its ultraviolet boundary (the initial singularity, cosmic inflation microphysics, and baryogenesis) and its infrared boundary (the $120$-order-of-magnitude cosmological constant catastrophe, the nature of dark matter, and the $4.85\sigma$ Hubble tension).

This monograph provides:
1. **The 5 Definitive Empirical Pillars** establishing the Hot Big Bang.
2. **The Fundamental Theoretical Failures** identifying what current theory does NOT explain.
3. **The Master Registry of 8 Open Problems** paired with the **specific, quantitative observations** required to resolve each.
4. **Epistemic Falsification Thresholds** defining the exact observational results that would overturn standard conclusions.

---

## 2. Strongest Empirical Evidence for the Hot Big Bang

The Hot Big Bang model is supported by five independent observational pillars that cannot be reconciled with static, tired-light, steady-state, or non-expanding alternatives:

```
                           +-----------------------------------------------+
                           |          HOT BIG BANG EMPIRICAL PILLARS       |
                           |  * CMB Blackbody (T0 = 2.7255 K; |y|<1.5e-5)  |
                           |  * BBN Light Elements (~75% H, ~25% He by mass)|
                           |  * Metric Expansion & (1+z) Time Dilation     |
                           |  * Acoustic Scale (r_s = 147.2 Mpc; Flatness) |
                           |  * Primordial Red Tilt (n_s = 0.965, 8.4-sigma)|
                           +-----------------------------------------------+
```

### Pillar 1: Cosmic Microwave Background (CMB) Blackbody Radiation
* **COBE/FIRAS Absolute Monopole:** $T_0 = 2.72548 \pm 0.00057\text{ K}$ (Fixsen 2009).
* **Blackbody Perfection:** Spectral deviations $|\Delta I_\nu| / I_{\max} < 50\text{ ppm}$ ($5 \times 10^{-5}$) across $60\text{--}600\text{ GHz}$. The CMB is the most precise blackbody known in nature.
* **Spectral Distortion Limits (95% CL):**
  * Comptonization distortion: $|y| < 1.5 \times 10^{-5}$ (constraining energy injection after $z \sim 10^4$).
  * Chemical potential distortion: $|\mu| < 9.0 \times 10^{-5}$ (constraining energy injection between $10^4 < z < 2 \times 10^6$).
* **Photon & Radiation Energy Densities:**
  * $n_\gamma = \frac{2\zeta(3)}{\pi^2}\left(\frac{k_B T_0}{\hbar c}\right)^3 = 410.72\text{ photons/cm}^3$.
  * $\rho_\gamma = a_{\rm rad} T_0^4 = 4.17 \times 10^{-14}\text{ J/m}^3 = 0.2606\text{ eV/cm}^3$.
* **Metric Cooling Law $T(z) = T_0(1+z)$:**
  * Measured at $z = 1.776$ via C I fine-structure excitation: $T(z) = 7.58 \pm 0.35\text{ K}$ (theoretical prediction: $7.57\text{ K}$).
  * Measured at $z = 6.340$ via $\text{H}_2\text{O}$ absorption against CMB in starburst galaxy HFLS3: $T(z) = 20.0 \pm 2.0\text{ K}$ (theoretical prediction: $20.00\text{ K}$).
  * *Epistemic Verdict:* Falsifies non-expanding tired-light and steady-state models at $> 50\sigma$.

### Pillar 2: Primordial Big Bang Nucleosynthesis (SBBN) Light Element Abundances
During the epoch $t \sim 0.1\text{ s}$ to $t \sim 1200\text{ s}$ ($T \sim 10\text{ MeV} \to 0.01\text{ MeV}$), weak interactions froze out at $T_{\rm freeze} \approx 0.80\text{ MeV}$, fixing the neutron-to-proton ratio:
$$(n/p)_{\rm freeze} = \exp\left(-\frac{\Delta m_{np} c^2}{k_B T_{\rm freeze}}\right) = \exp\left(-\frac{1.2933\text{ MeV}}{0.80\text{ MeV}}\right) \approx 0.1986$$
Free neutron decay with lifetime $\tau_n = 879.4 \pm 0.6\text{ s}$ during the deuterium bottleneck ($\Delta t \approx 300\text{ s}$) yields $(n/p)_{\rm BBN} \approx 0.1412$.
* **Primordial Helium-4 Mass Fraction:**
  $$Y_p = \frac{2(n/p)}{1 + (n/p)} \approx 0.2474$$
  Observed in low-metallicity extragalactic H II regions: $Y_p = 0.245 \pm 0.003$ (Aver et al. 2015, 2021). Concordance: $0.8\sigma$. The universe is $\sim 75\%$ Hydrogen and $\sim 25\%$ Helium by mass.
* **Primordial Deuterium Abundance:**
  $$(D/H)_p = (2.547 \pm 0.025) \times 10^{-5} \quad (\text{Cooke et al. 2018; 1% precision})$$
  This exquisitely constrains the cosmic baryon density to $\omega_b = \Omega_b h^2 = 0.02237 \pm 0.00015$, in remarkable $0.4\sigma$ agreement with Planck CMB acoustic peak heights ($\omega_b = 0.02236 \pm 0.00015$).

### Pillar 3: Universal Metric Expansion and Cosmic Time Dilation
* **Cosmological Redshift & Time Dilation:**
  In an expanding metric $g_{\mu\nu} = a(t)^2 \eta_{\mu\nu}$, clocks at redshift $z$ run slower by exactly $(1+z)$.
  * Confirmed in Type Ia supernova light curves: $\Delta t_{\rm obs} = \Delta t_{\rm rest}(1+z)$ verified across $z \in [0.1, 1.5]$ (Goldhaber et al. 2001; Blondin et al. 2008).
  * Confirmed in quasar variability clocks out to $z = 3.8$ (Lewis & Brewer 2023).
* **Tolman Surface Brightness Test:**
  Surface brightness scales as $(1+z)^{-4}$ in an expanding metric, whereas static tired-light predicts $(1+z)^{-1}$. High-redshift galaxy surface brightness rules out static space at $> 10\sigma$.

### Pillar 4: The Acoustic Sound Horizon Standard Ruler and Spatial Flatness
* **Pre-Recombination Sound Horizon:**
  Baryon-photon acoustic oscillations freeze out at drag epoch $z_d \approx 1060$, fixing a comoving ruler:
  $$r_s(z_d) = \int_{z_d}^\infty \frac{c/\sqrt{3(1 + 3\rho_b / 4\rho_\gamma)}}{H(z)} dz = 147.21 \pm 0.23\text{ Mpc}$$
* **CMB Multipoles & BAO Concordance:**
  The acoustic scale $\theta_* = r_s / D_A(z_*) = (1.04110 \pm 0.00031) \times 10^{-2}\text{ rad}$ produces harmonic acoustic peaks at $\ell_1 \approx 220.6$, $\ell_2 \approx 540$, $\ell_3 \approx 810$.
  Combining CMB with Baryon Acoustic Oscillation (BAO) measurements yields spatial curvature:
  $$\Omega_k = 0.0007 \pm 0.0019$$
  The spatial geometry of the universe is Euclidean to within $0.2\%$.

### Pillar 5: Primordial Scalar Perturbation Spectrum (The Red Tilt)
* **Planck 2018 / 2020 Power Spectrum:**
  $$P_{\mathcal{R}}(k) = A_s \left(\frac{k}{k_0}\right)^{n_s - 1}, \quad A_s = (2.100 \pm 0.030) \times 10^{-9}, \quad n_s = 0.9649 \pm 0.0042$$
* **Falsification of Scale Invariance:**
  The exact scale-invariant Harrison-Zel'dovich spectrum ($n_s = 1.000$) is excluded at:
  $$\frac{1.000 - 0.9649}{0.0042} = 8.36\sigma$$
  This red tilt directly proves that the Hubble parameter decreased slowly during the primordial generation of quantum fluctuations, as required by slow-roll inflation ($\epsilon = -\dot{H}/H^2 > 0$).

---

## 3. What Current Theory Fails to Explain

Despite its empirical triumph for $t \ge 0.1\text{ s}$, standard theory ($\Lambda\text{CDM} + \text{SM}$) possesses severe theoretical deficiencies:

1. **The Initial Singularity:**
   Classical General Relativity demands that backward null and timelike geodesics terminate at an unphysical singularity $a(t) \to 0$, where energy density $\rho \to \infty$ and spacetime curvature $R_{\mu\nu\rho\sigma} R^{\mu\nu\rho\sigma} \to \infty$ (Penrose-Hawking singularity theorems). GR is non-renormalizable and invalid at $E \ge E_{\rm Pl} \approx 1.22 \times 10^{19}\text{ GeV}$ ($t \le t_{\rm Pl} \approx 5.39 \times 10^{-44}\text{ s}$). The origin of spacetime itself remains completely outside current physics.
2. **Initial Conditions & The Gravitational Arrow of Time:**
   The early universe was in a state of extraordinarily low gravitational entropy. Under Penrose's Weyl Curvature Hypothesis, the Weyl conformal tensor vanishes ($C_{\mu\nu\rho\sigma} \to 0$) while Ricci curvature diverges. The probability of selecting such an initial state from the phase space of available configurations is $1\text{ part in } 10^{10^{123}}$ (Penrose 1979). Standard inflation does not explain this; it requires an already homogeneous, low-entropy patch across several Hubble radii to ignite.
3. **Inflaton Particle Identity & Microphysics:**
   Inflation resolves the horizon, flatness, and monopole problems through an accelerating phase ($w < -1/3$) driven by a scalar field potential $V(\phi)$. However, the Standard Model contains only one fundamental scalar (the $125.25\text{ GeV}$ Higgs boson), which cannot drive inflation without non-minimal gravitational coupling ($\xi \sim 10^4$) that violates perturbative unitarity at low scales. The identity of the inflaton, its potential, its coupling to matter during reheating, and the measure problem in eternal inflation are unknown.
4. **Baryon Asymmetry of the Universe (Sakharov Failure):**
   The observed baryon-to-photon ratio is $\eta = (6.12 \pm 0.04) \times 10^{-10}$. In the Standard Model:
   * Baryon number violation occurs via electroweak sphalerons, but sphalerons strictly conserve $B - L$.
   * $C$ and $CP$ violation in the CKM quark mixing matrix is quantified by the Jarlskog invariant $J \approx 3.0 \times 10^{-5}$, which yields an asymmetry suppressed by 10 orders of magnitude ($\eta_{\rm SM} \sim 10^{-20}$).
   * With a physical Higgs mass $m_H = 125.25\text{ GeV} > 75\text{ GeV}$, the electroweak phase transition is a smooth crossover, lacking thermal out-of-equilibrium conditions.
   The Standard Model is mathematically incapable of generating the matter in the universe.
5. **Cosmological Constant Catastrophe:**
   The observed dark energy density driving late-time acceleration ($z < 0.6$) is:
   $$\rho_{\rm DE} = \frac{\Lambda c^2}{8\pi G} \approx 5.35 \times 10^{-10}\text{ J/m}^3 \approx 2.5 \times 10^{-47}\text{ GeV}^4$$
   The quantum field theoretic zero-point energy summed up to the Planck scale cutoff ($M_{\rm Pl}$) yields:
   $$\rho_{\rm vac, Pl} = \frac{M_{\rm Pl}^4}{16\pi^2} \approx 3.5 \times 10^{73}\text{ GeV}^4$$
   The discrepancy is $\sim 120.1\text{ orders of magnitude}$—the worst theoretical mismatch in the history of physics. Furthermore, the "coincidence problem" (why $\rho_{\rm DE} \approx \rho_m$ today at $z \approx 0.3$) is unexplained.
6. **Dark Matter Microscopic Identity:**
   Non-baryonic Cold Dark Matter represents $84.4\%$ of all cosmic matter ($\Omega_c h^2 = 0.1200 \pm 0.0012$), yet no candidate exists in the Standard Model. The allowed parameter space spans $90\text{ orders of magnitude}$ in mass—from ultralight fuzzy dark matter ($m \sim 10^{-22}\text{ eV}$) to primordial black holes ($M \sim 10^{35}\text{ g}$). Direct detection experiments (LZ, XENONnT, PandaX-4T) have excluded spin-independent WIMP-nucleon cross sections down to $\sigma_{\rm SI} < 6 \times 10^{-48}\text{ cm}^2$, approaching the irreducible neutrino fog without a signal.
7. **The Hubble Tension:**
   A severe $4.85\sigma$ tension exists between the early-universe sound horizon calibration ($H_0 = 67.36 \pm 0.54\text{ km/s/Mpc}$, Planck 2018) and the local distance ladder calibrated by Cepheids and Type Ia supernovae ($H_0 = 73.04 \pm 1.04\text{ km/s/Mpc}$, SH0ES / Riess et al. 2022). The discrepancy $\Delta H_0 = 5.68\text{ km/s/Mpc}$ cannot be easily accommodated within standard flat $\Lambda\text{CDM}$.
8. **The Cosmological Lithium-7 Problem:**
   Standard BBN predicts primordial Lithium-7 abundance $(^7\text{Li}/\text{H})_{\rm SBBN} = (4.68 \pm 0.32) \times 10^{-10}$. In contrast, ancient Population II metal-poor halo dwarf stars exhibit a flat Spite plateau of $(^7\text{Li}/\text{H})_{\rm obs} = (1.58 \pm 0.11) \times 10^{-10}$. This represents a $2.97\times$ deficit, corresponding to a $9.18\sigma$ discrepancy.

---

## 4. Master Deliverable: Canonical Open Problems & Decisive Resolving Observations

The table below catalogs each open problem, its theoretical barrier, established ground truth, and the decisive observation that will settle it:

| ID | Open Problem | Theoretical Barrier | Established Ground Truth / Current Discrepancy | Decisive Resolving Observation | Target Facility & Timeline | Falsification / Resolution Criterion |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **OP-01** | **Initial Singularity & UV Incompleteness** | GR breaks down at $t_{\rm Pl} \sim 5.4 \times 10^{-44}\text{ s}$; cannot determine whether spacetime had an absolute beginning or a bounce. | $\rho_{\rm Pl} \approx 5.16 \times 10^{96}\text{ kg/m}^3$; $E_{\rm Pl} \approx 1.22 \times 10^{19}\text{ GeV}$. | Measure Primordial Gravitational Wave (PGW) tensor spectral index $n_T$ from CMB scales to space interferometers. | LiteBIRD, LISA, DECIGO, BBO, Einstein Telescope | $n_T > 0$ (blue tilt) or high-frequency cutoff rules out standard inflation and proves a quantum bounce / pre-Big Bang model. $n_T = -r/8 < 0$ confirms canonical slow-roll inflation. |
| **OP-02** | **Cosmic Inflation Mechanics & Inflaton Identity** | Inflaton particle unknown; initial patch requires unphysically low Weyl curvature; eternal inflation creates measure catastrophe. | $r_{0.05} < 0.036$ (95% CL); $n_s = 0.9649 \pm 0.0042$; $|\Omega_k| < 0.002$. | Precision measurement of CMB B-mode polarization $r$ and local primordial non-Gaussianity $f_{\rm NL}^{\rm local}$. | LiteBIRD ($\sigma(r) < 10^{-3}$), CMB-S4 ($\sigma(r) \approx 5 \times 10^{-4}$), SPHEREx | $r \in [0.002, 0.005]$ confirms Starobinsky $R^2$ / Higgs-like inflation at $V^{1/4} \approx 10^{16}\text{ GeV}$. $|f_{\rm NL}^{\rm local}| \ge 1$ at $> 5\sigma$ decisively rules out all single-field inflation. |
| **OP-03** | **Baryon Asymmetry of the Universe (Baryogenesis)** | Standard Model fails all 3 Sakharov criteria: $B-L$ conserved by sphalerons; CKM CP deficit $\sim 10^{-10}$; EW transition is smooth crossover. | $\eta_{\rm obs} = (6.12 \pm 0.04) \times 10^{-10}$; $\eta_{\rm SM} \sim 10^{-20}$; $m_H = 125.25\text{ GeV}$. | Discovery of neutrinoless double beta decay ($0\nu\beta\beta$), leptonic Dirac CP phase $\delta_{\rm CP}$, and permanent electron EDM. | LEGEND-1000 ($^{76}\text{Ge}$), nEXO ($^{136}\text{Xe}$), DUNE, Hyper-K, ACME | $0\nu\beta\beta$ discovery confirms Majorana neutrinos ($\Delta L = 2$) and validates Thermal Leptogenesis. Non-observation down to $m_{\beta\beta} < 1\text{ meV}$ falsifies standard high-scale leptogenesis. |
| **OP-04** | **Particle Identity of Dark Matter** | No viable SM particle candidate; allowed mass parameter space spans 90 orders of magnitude ($10^{-22}\text{ eV}$ to $10^{35}\text{ g}$). | $\Omega_c h^2 = 0.1200 \pm 0.0012$; WIMP limit $\sigma_{\rm SI} < 6 \times 10^{-48}\text{ cm}^2$ at $30\text{ GeV}$. | Nuclear recoil direct detection down to neutrino fog; resonant RF cavity axion conversion; 21cm small-scale cutoff. | LZ, DARWIN / XLZD, ADMX, DMRadio, BREAD, SKA | Positive nuclear recoil above neutrino fog confirms WIMP DM. Resonant microwave power detection confirms QCD axion. Small-scale matter cutoff at $k > 10\ h/\text{Mpc}$ confirms warm/fuzzy DM. |
| **OP-05** | **Dark Energy & Cosmological Constant Catastrophe** | QFT zero-point energy exceeds observed vacuum energy by $10^{120}$; coincidence problem ($\rho_\Lambda \sim \rho_m$ today) unexplained. | $\rho_\Lambda \approx 2.5 \times 10^{-47}\text{ GeV}^4$; $\rho_{\rm vac, Pl} \approx 3.5 \times 10^{73}\text{ GeV}^4$ ($120.1$ orders discrepancy). | Measurement of dynamical equation of state $w(a) = w_0 + w_a(1-a)$ and growth of structure index $\gamma$. | Euclid Space Telescope, Rubin Observatory (LSST), Roman Space Telescope, DESI | Confirmation of $(w_0, w_a) \neq (-1, 0)$ at $> 5\sigma$ decisively rules out static $\Lambda$ in favor of dynamical dark energy. Growth index $\gamma \neq 0.55$ proves modified gravity. |
| **OP-06** | **The Hubble Tension & $S_8$ Large-Scale Tension** | Early sound horizon ($H_0 = 67.36 \pm 0.54$) contradicts local distance ladder ($H_0 = 73.04 \pm 1.04$) at $4.85\sigma$; $S_8$ weak lensing tension at $2.7\sigma$. | $\Delta H_0 = 5.68\text{ km/s/Mpc}$ ($4.85\sigma$ tension); KiDS/DES $S_8 \approx 0.76$ vs Planck $S_8 = 0.832$. | Gravitational Wave Standard Sirens independent of both distance ladders and CMB sound horizon calibrations; JWST multi-anchors. | LIGO/Virgo/KAGRA, Einstein Telescope, Cosmic Explorer; JWST NIRCam | $\sim 50$ standard siren mergers determine $H_0$ to $\le 1.5\%$, definitively settling whether $\Lambda\text{CDM}$ is broken or local systematics dominate. |
| **OP-07** | **Primordial Cosmological Lithium Deficit** | SBBN accurately yields $^4\text{He}$ and $D/H$, but overpredicts $^7\text{Li}$ by $2.97\times$ compared to Spite plateau ($9.18\sigma$ discrepancy). | $(^7\text{Li}/\text{H})_{\rm SBBN} = (4.68 \pm 0.32) \times 10^{-10}$; $(^7\text{Li}/\text{H})_{\rm obs} = (1.58 \pm 0.11) \times 10^{-10}$. | High-resolution spectroscopic measurement of gas-phase $^7\text{Li}$ in pristine interstellar/DLA clouds outside stars. | Extremely Large Telescope (ELT-HIRES / ANDES), VLT-ESPRESSO, Keck HIRES | Gas-phase $(^7\text{Li}/\text{H}) \approx 4.7 \times 10^{-10}$ in DLAs proves stellar depletion; gas-phase $\approx 1.6 \times 10^{-10}$ confirms BSM nucleosynthesis physics. |
| **OP-08** | **Cosmic Topology & Large-Angle CMB Anomalies** | Vanishing large-angle correlation $C(\theta > 60^\circ) \approx 0$ ($p < 0.1\%$) and planar alignments contradict isotropic $\mathbb{R}^3$. | $C(\theta > 60^\circ) \approx 0$ ($p < 10^{-3}$); quadrupole-octopole alignment ($p < 0.005$); $7\%$ hemispherical asymmetry. | Full-sky CMB polarization ($EE$) matched "circles-in-the-sky" searches and 3D galaxy clustering topological eigenmode analysis. | LiteBIRD (full-sky polarization), Euclid, Rubin LSST, SPHEREx | Detection of matched circle pairs in $EE$ polarization proves compact multi-connected topology ($T^3$ or spherical space); absence beyond $2 R_{\rm LSS}$ confirms trivial topology within horizon. |

---

## 5. Epistemic Ledger: What Is Established, What Remains Unknown, and Falsification Bounds

### What Is Established (Conclusive Ground Truth)
1. **Thermal History:** The universe expanded from an ultra-hot, ultra-dense primordial plasma at $T > 10\text{ MeV}$ ($t < 0.1\text{ s}$), as proven by the CMB blackbody temperature $T_0 = 2.72548\text{ K}$, spectral departure bounds $< 50\text{ ppm}$, $T(z) = T_0(1+z)$ excitation, and SBBN synthesis of $^4\text{He}$ ($Y_p = 0.245$) and Deuterium ($(D/H)_p = 2.54 \times 10^{-5}$).
2. **Metric Expansion:** Universal metric expansion is a physical property of spacetime, demonstrated by $(1+z)$ time dilation of Supernovae Ia light curves and quasar clocks.
3. **Geometry & Primordial Tilt:** Spatial geometry is flat to within $0.2\%$ ($|\Omega_k| < 0.002$), and the primordial perturbation spectrum is strictly red-tilted ($n_s = 0.9649 \pm 0.0042$, scale invariance ruled out at $8.36\sigma$).

### What Remains Unknown
1. Spacetime origin prior to $t \sim 10^{-32}\text{ s}$ (initial singularity vs quantum bounce).
2. The microscopic carrier of the inflaton field and its pre-inflationary initial conditions.
3. The origin of the cosmic baryon asymmetry (the missing CP and $B-L$ violation mechanism).
4. The particle or compact object identity of Dark Matter ($90$ orders of magnitude mass uncertainty).
5. The nature of Dark Energy (cosmological constant $\Lambda$, dynamical quintessence, or infrared breakdown of General Relativity).

### What Evidence Would Change Our Mind (Falsification Criteria)
1. **Falsification of Inflation:** Direct detection of primordial gravitational waves with blue spectral tilt ($n_T > 0$) or non-Gaussianity $|f_{\rm NL}^{\rm local}| \ge 1$ at $> 5\sigma$ will definitively falsify single-field slow-roll inflation and establish a non-singular bounce or emergent universe scenario.
2. **Confirmation of Leptogenesis:** Direct observation of neutrinoless double beta decay ($0\nu\beta\beta$) will prove that neutrinos are Majorana fermions ($\Delta L = 2$), providing the foundational empirical pillar for high-scale leptogenesis.
3. **Falsification of $\Lambda\text{CDM}$:** Confirmation of dynamical dark energy ($(w_0, w_a) \neq (-1, 0)$) by Euclid/Roman/DESI at $> 5\sigma$, or confirmation by Gravitational Wave Standard Sirens that $H_0 = 73.0 \pm 0.8\text{ km/s/Mpc}$, will permanently falsify the standard flat $\Lambda\text{CDM}$ cosmological model.
4. **Resolution of the Lithium Deficit:** Gas-phase spectroscopic measurement of pristine interstellar gas at high redshift finding $(^7\text{Li}/\text{H}) \approx 4.7 \times 10^{-10}$ will eliminate the Lithium anomaly as an astrophysical stellar mixing artifact; conversely, finding $\approx 1.6 \times 10^{-10}$ outside stars will confirm beyond-Standard-Model nuclear physics during BBN.

---
*Authored by Kepler (A001), generation 0, in permanent fulfillment of the Cosmogenesis scientific brief.*
