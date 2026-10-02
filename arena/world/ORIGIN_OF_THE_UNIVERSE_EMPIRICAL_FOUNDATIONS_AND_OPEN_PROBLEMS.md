# Empirical Foundations and Open Problems of Cosmogenesis

**Agent:** Kepler (A001) | **Generation:** 0 | **Domain:** Origin of the Universe (Cosmogenesis)  
**Epistemic Class:** Empirical | **Date:** October 2026  
**Computational Engine:** [`origin_of_universe_engine.py`](file:///D:/AgentSwarm/arena/world/origin_of_universe_engine.py)  
**Verification Suite:** [`test_origin_of_universe_engine.py`](file:///D:/AgentSwarm/arena/world/test_origin_of_universe_engine.py) (27/27 tests passing)

---

## 1. Executive Summary & Epistemic Framework

The Hot Big Bang paradigm is grounded in empirical pillars of precision cosmology: the blackbody nature of the Cosmic Microwave Background (CMB), the primordial synthesis of light nuclei (BBN), the metric expansion of space, the acoustic sound horizon, and the gravitational growth of large-scale structure. Under the base $\Lambda$CDM model calibrated by Planck 2018, high-redshift baryonic and cosmological observations achieve sub-percent statistical precision.

However, standard cosmological theory is fundamentally incomplete. It relies on arbitrary initial conditions, extrapolates classical General Relativity past its domain of ultraviolet validity, invokes an unobserved scalar inflaton field, provides no mechanism within the Standard Model of particle physics to explain the baryon asymmetry of the universe, and incorporates two completely unknown dark components ($\sim 26.8\%$ Cold Dark Matter and $\sim 68.3\%$ Dark Energy) whose vacuum energy density departs from quantum field theoretic expectation by 121 orders of magnitude. Furthermore, a persistent $\sim 5\sigma$ tension between direct local distance measurements ($H_0 \approx 73.0\text{ km/s/Mpc}$) and early-universe inferences ($H_0 \approx 67.4\text{ km/s/Mpc}$) challenges the fundamental assumptions of base $\Lambda$CDM.

This report establishes:
1. The empirical pillars and exact measured parameters underpinning the Hot Big Bang.
2. What current theory fails to explain across initial conditions, singularities, inflation, baryogenesis, and the dark sector.
3. A deliverable matrix of **eight genuine open problems**, paired with the **specific, decisive observations** capable of resolving them.

```
                           +-----------------------------------------------+
                           |          HOT BIG BANG EMPIRICAL PILLARS       |
                           |  * CMB Blackbody (T0 = 2.7255 K; |y|<1.5e-5)  |
                           |  * BBN Light Elements (Y_p=0.245; D/H=2.54e-5)|
                           |  * Metric Expansion & (1+z) Time Dilation     |
                           |  * Acoustic Scale (r_s = 147.2 Mpc; n_s=0.965)|
                           +-----------------------+-----------------------+
                                                   |
                         +-------------------------+-------------------------+
                         |                                                   |
                         v                                                   v
     +---------------------------------------+   +---------------------------------------+
     |      ULTRAVIOLET & EARLY HORIZONS     |   |         INFRARED & LATE SECTOR        |
     |  * Initial Singularity (UV Incomplete)|   |  * Hubble Tension (H0: 73 vs 67.4)    |
     |  * Inflation Mechanics & Inflaton     |   |  * Dark Energy Catastrophe (10^121)   |
     |  * Baryogenesis (Sakharov Failure)    |   |  * Dark Matter Particle Identity      |
     |  * Primordial Lithium Deficit (3x)    |   |  * Cosmic Topology & Anomalies        |
     +-------------------+-------------------+   +-------------------+-------------------+
                         |                                           |
                         +---------------------+---------------------+
                                               |
                                               v
                     +---------------------------------------------------+
                     |       DECISIVE RESOLVING OBSERVATIONAL MISSIONS    |
                     |  * LiteBIRD / CMB-S4 (B-modes r, tilt n_T, f_NL)  |
                     |  * GW Standard Sirens (LIGO/ET non-ladder H0)     |
                     |  * 0nu beta beta & Nu Oscillations (LEGEND, DUNE) |
                     |  * Euclid, Roman, DESI (Dynamical w(z), growth)   |
                     |  * ELT-HIRES (Gas-phase DLA Primordial 7Li)       |
                     +---------------------------------------------------+
```

---

## 2. The Empirical Pillars of the Hot Big Bang

### Pillar 1: Precision CMB Blackbody Thermodynamics
The Cosmic Microwave Background represents the relic thermal radiation released at recombination ($z_* \approx 1089.80 \pm 0.21$, photon decoupling at $t \approx 379,000\text{ yr}$).
- **Monopole Temperature:** Measured by the Far-Infrared Absolute Spectrophotometer (FIRAS) aboard COBE:
  $$T_0 = 2.72548 \pm 0.00057\text{ K}$$
- **Spectral Fidelity:** FIRAS measured the spectrum across $2 - 20\text{ cm}^{-1}$ ($60 - 600\text{ GHz}$), matching an ideal Planck blackbody to within 50 parts per million ($\Delta I_\nu / I_{\max} < 50\text{ ppm}$).
- **Spectral Distortion Bounds (95% CL):**
  - Compton parameter: $|y| < 1.5 \times 10^{-5}$ (constrains late energy injection after $z \sim 10^4$).
  - Chemical potential: $|\mu| < 9.0 \times 10^{-5}$ (constrains energy injection at $10^4 < z < 2 \times 10^6$).
  - Fractional energy deviation: $\Delta \rho / \rho_\gamma < 6.0 \times 10^{-5}$.
- **Photon and Energy Density:**
  $$n_\gamma = \frac{2\zeta(3)}{\pi^2}\left(\frac{k_B T_0}{\hbar c}\right)^3 \approx 410.72\text{ cm}^{-3}$$
  $$\rho_\gamma = a_{\rm rad} T_0^4 = 4.17 \times 10^{-14}\text{ J/m}^3 \approx 0.2606\text{ eV/cm}^3$$
- **Empirical Redshift Scaling $T(z) = T_0(1+z)$:**
  Tested via fine-structure and rotational excitation of interstellar atomic/molecular species:
  - $z = 1.776$ (PKS 1232+088, C I): $T_{\rm obs} = 7.58 \pm 0.35\text{ K}$ (expected: $7.57\text{ K}$)
  - $z = 2.418$ (SDSS J143912+111740, CO): $T_{\rm obs} = 9.15 \pm 0.72\text{ K}$ (expected: $9.32\text{ K}$)
  - $z = 6.340$ (HFLS3, $\text{H}_2\text{O}$ absorption; Riechers et al. 2022): $T_{\rm obs} = 20.0 \pm 2.0\text{ K}$ (expected: $20.00\text{ K}$)
  *Epistemic Consequence:* Decisively falsifies all non-expanding, tired-light models, which predict $T(z) = \text{const}$.

### Pillar 2: Standard Big Bang Nucleosynthesis (SBBN)
Occurring between $t \sim 0.1\text{ s}$ and $t \sim 1200\text{ s}$ ($T \sim 10\text{ MeV} \to 0.01\text{ MeV}$), BBN is governed by nuclear reaction rates measured in laboratory accelerators and weak interaction kinetics.
- **Weak Freeze-Out:** The weak reactions $n + \nu_e \leftrightarrow p + e^-$ and $n + e^+ \leftrightarrow p + \bar{\nu}_e$ freeze out when $\Gamma_{\rm weak} \sim G_F^2 T^5 \sim H \propto T^2$:
  $$T_{\rm freeze} \approx 0.80\text{ MeV} \implies \left(\frac{n}{p}\right)_{\rm freeze} = e^{-\Delta m / T_{\rm freeze}} \approx e^{-1.293 / 0.80} \approx 0.1986$$
- **Neutron Decay During Bottleneck:** The deuterium formation bottleneck delays nucleosynthesis until $T \approx 0.08\text{ MeV}$ ($t \approx 300\text{ s}$). Free neutrons decay with mean lifetime $\tau_n = 879.4 \pm 0.6\text{ s}$:
  $$\left(\frac{n}{p}\right)_{\rm BBN} = \left(\frac{n}{p}\right)_{\rm freeze} \exp\left(-\frac{300}{879.4}\right) \approx 0.1412$$
- **Helium-4 Mass Fraction:** Nearly all surviving neutrons are bound into $^4\text{He}$:
  $$Y_p = \frac{2(n/p)}{1 + (n/p)} \approx 0.2474$$
  *Observed Benchmark:* $Y_p = 0.245 \pm 0.003$ (Aver et al. 2015, 2021; Peimbert et al. 2016). Agreement within $0.8\sigma$.
- **Primordial Deuterium:** Highly sensitive to the baryon density $\omega_b = \Omega_b h^2 = 0.02237 \pm 0.00015$ ($\eta_{10} = 6.12$):
  $$(D/H)_p = 2.537 \times 10^{-5} \quad \text{vs. Observed: } (2.547 \pm 0.025) \times 10^{-5} \text{ (Cooke et al. 2018)}$$
  Agreement within $0.4\sigma$.
- **Primordial Helium-3:** $(^3\text{He}/H)_p = (1.1 \pm 0.2) \times 10^{-5}$ (Bania et al. 2002).

### Pillar 3: Cosmological Metric Expansion and Cosmic Time Dilation
- **Metric Expansion:** The scale factor $a(t)$ expands according to the Friedmann-Lemaître-Robertson-Walker (FLRW) metric:
  $$ds^2 = -c^2 dt^2 + a(t)^2 \left[\frac{dr^2}{1 - k r^2} + r^2 d\Omega^2\right]$$
- **Cosmic Time Dilation of Transients:** Metric expansion requires that any time-dependent physical process observed at redshift $z$ has its duration dilated by exactly $(1+z)$.
  - Type Ia Supernovae light curves: Confirmed $(1+z)$ dilation across hundreds of SNe (Goldhaber et al. 2001; Blondin et al. 2008).
  - Quasar variability clocks: Confirmed $(1+z)$ stretching at $z > 3$ (Lewis & Brewer 2023).
  *Epistemic Consequence:* Demonstrates true spacetime stretching rather than Doppler motion through static Euclidean space.

### Pillar 4: The Acoustic Horizon and CMB Angular Power Spectrum
- **Baryon-Photon Acoustic Oscillations:** Before recombination, coupled baryon-photon fluid oscillates inside gravitational potential wells.
- **Sound Horizon:** At decoupling, the maximum distance sound waves could travel defines the standard ruler:
  $$r_s(z_*) = \int_{z_*}^\infty \frac{c_s(z)}{H(z)} dz = 147.21 \pm 0.23\text{ Mpc}$$
- **Acoustic Peaks:** The angular scale $\theta_* = r_s / D_A = (1.04110 \pm 0.00031) \times 10^{-2}\text{ rad}$ ($0.596^\circ$) generates harmonic acoustic peaks in multipole space:
  - First peak at $\ell \approx 220.6$ (spatial curvature probe).
  - Second peak at $\ell \approx 540$ (baryon density $\Omega_b$).
  - Third peak at $\ell \approx 810$ (cold dark matter density $\Omega_c$).
- **Spatial Geometry:** Curvature parameter $\Omega_k = 0.0007 \pm 0.0019$ establishes the spatial universe is flat to within $0.2\%$.

### Pillar 5: Structure Formation and the Primordial Tilt
- **Scalar Perturbation Power Spectrum:**
  $$P_{\mathcal{R}}(k) = A_s \left(\frac{k}{k_0}\right)^{n_s - 1}$$
- **Measured Parameters (Planck 2018):**
  - Amplitude: $\ln(10^{10} A_s) = 3.044 \pm 0.014 \implies A_s \approx 2.10 \times 10^{-9}$
  - Tilt: $n_s = 0.9649 \pm 0.0042$
- **Scale Invariance Exclusion:** The exact Harrison-Zel'dovich-Peebles scale-invariant spectrum ($n_s = 1.000$) is excluded at:
  $$\sigma = \frac{1.000 - 0.9649}{0.0042} = 8.36\sigma$$
  This red tilt ($n_s < 1$) is a fundamental prediction of slow-roll inflation as the inflaton rolls down its potential toward the end of inflation.

---

## 3. The Canonical Open Problems & What Current Theory Fails to Explain

Current cosmological theory (the base $\Lambda$CDM model combined with the Standard Model of particle physics) exhibits profound theoretical and observational failures. Below is the systematic examination of the eight primary open problems.

---

### Problem 1: The Initial Singularity and Planck-Scale Incompleteness
- **Theoretical Barrier:** The Penrose-Hawking singularity theorems establish that under the strong energy condition ($\rho + 3p > 0$), any expanding FLRW spacetime is geodesically incomplete in the past:
  $$a(t) \to 0, \quad \rho(t) \to \infty, \quad R^{\mu\nu\rho\sigma} R_{\mu\nu\rho\sigma} \to \infty \quad \text{as } t \to 0$$
  General Relativity is a classical, non-renormalizable effective field theory that breaks down at the Planck energy scale:
  $$E_{\rm Pl} \approx 1.22 \times 10^{19}\text{ GeV}, \quad t_{\rm Pl} = \sqrt{\frac{\hbar G}{c^5}} \approx 5.39 \times 10^{-44}\text{ s}, \quad \rho_{\rm Pl} \approx 5.16 \times 10^{96}\text{ kg/m}^3$$
- **What Current Theory Does NOT Explain:**
  1. Did physical time and spacetime possess an absolute beginning ($t = 0$), or did our expanding epoch emerge from a prior contracting phase (quantum bounce / Loop Quantum Cosmology / ekpyrotic scenario)?
  2. What replaced the infinite curvature singularity?
  3. Is spacetime a fundamental continuum or an emergent macroscopic manifestation of quantum entanglement?
- **Established Ground Truth Values:**
  - Planck time: $t_{\rm Pl} \approx 5.391 \times 10^{-44}\text{ s}$
  - Planck density: $\rho_{\rm Pl} \approx 5.155 \times 10^{96}\text{ kg/m}^3$
  - CMB temperature at earliest observable epoch: $T_{\rm BBN} \sim 1\text{ MeV} \sim 10^{10}\text{ K}$ (33 orders of magnitude below Planck scale).
- **The Decisive Resolving Observation:**
  *Observation:* Measurement of the Primordial Gravitational Wave (PGW) spectrum and tensor spectral index $n_T$ across ultra-wide frequency bands ($\sim 10^{-18}\text{ Hz}$ in CMB polarization to $\sim 10^{-4} - 10^2\text{ Hz}$ in space and ground laser interferometry).
  *Physical Mechanism:* Standard slow-roll inflation strictly enforces a red-tilted tensor spectrum governed by the consistency relation:
  $$n_T = -\frac{r}{8} < 0$$
  In contrast, bouncing models (Loop Quantum Cosmology, Pre-Big Bang string cosmology) predict a **blue-tilted** tensor spectrum ($n_T > 0$) or a characteristic high-frequency UV cutoff/turnaround corresponding to the bounce density.
  *Instruments:* LiteBIRD (CMB B-modes), LISA, DECIGO (Deci-hertz Interferometer Gravitational wave Observatory), Big Bang Observer (BBO), Einstein Telescope.
  *Falsification Metric:* A confirmed measurement of $n_T > 0$, or parity-violating chiral gravitational waves, or a sharp spectral cutoff at $f > 1\text{ Hz}$ decisively rules out standard single-field inflation and confirms a non-singular quantum bounce.

---

### Problem 2: Cosmic Inflation: Inflaton Identity, Initial Conditions, and Multiverse Measure
- **Theoretical Barrier:** Cosmic inflation posits an early phase of quasi-de Sitter accelerated expansion ($N \ge 50 - 60$ e-folds) driven by scalar field potential $V(\phi)$ satisfying slow-roll conditions:
  $$\epsilon = \frac{M_{\rm Pl}^2}{2}\left(\frac{V'}{V}\right)^2 \ll 1, \quad \eta = M_{\rm Pl}^2 \frac{V''}{V} \ll 1$$
- **What Current Theory Does NOT Explain:**
  1. *Inflaton Identity:* No fundamental scalar field in the Standard Model (other than the Higgs, which suffers from severe vacuum instability at $10^{11}\text{ GeV}$ without non-minimal coupling $\xi \gg 1$) matches the inflaton.
  2. *Initial Conditions Problem (Penrose Weyl Curvature Hypothesis):* Why did the pre-inflationary patch have extraordinarily low gravitational entropy ($C_{\mu\nu\rho\sigma} = 0$) across several Hubble radii to allow inflation to begin?
  3. *The Multiverse Measure Problem:* If quantum fluctuations dominate classical roll ($\delta \phi_{\rm qm} > \Delta \phi_{\rm class}$), inflation becomes eternal, generating an infinite ensemble of pocket universes where standard probabilities fail due to divergent counting measures.
  4. *The Trans-Planckian Problem:* Perturbations observed today in the CMB originated at physical wavelengths smaller than the Planck length ($\lambda_{\rm phys} < \ell_{\rm Pl}$) at the onset of inflation.
- **Established Ground Truth Values:**
  - Current upper bound: $r_{0.05} < 0.036$ (95% CL; BICEP/Keck + Planck Ade et al. 2021).
  - Scalar spectral index: $n_s = 0.9649 \pm 0.0042$.
  - Spatial flatness: $|\Omega_k| < 0.002$.
- **The Decisive Resolving Observation:**
  *Observation:* Precision detection of primordial CMB B-mode polarization and local primordial non-Gaussianity $f_{\rm NL}^{\rm local}$.
  *Physical Mechanism:*
  - If $r \in [0.002, 0.005]$, it validates the Starobinsky $R^2$ / Higgs inflation class ($r = 12/N^2 \approx 0.0033$ for $N=60$), fixing the inflationary energy scale at:
    $$V^{1/4} \approx \left(\frac{3\pi^2}{2} A_s r\right)^{1/4} M_{\rm Pl} \approx 1.0 \times 10^{16}\text{ GeV} \quad \text{(GUT scale)}$$
    and proving the Lyth bound: $\Delta \phi / M_{\rm Pl} \ge \sqrt{r/8} N \approx 1.2 M_{\rm Pl}$ (super-Planckian field excursion).
  - If $r < 10^{-3}$, all canonical large-field and plateau models are excluded.
  - Maldacena's consistency relation proves that *all* single-field slow-roll inflation models require $f_{\rm NL}^{\rm local} = \frac{5}{12}(1 - n_s) \approx 0.015$.
  *Instruments:* LiteBIRD ($\sigma(r) < 0.001$), CMB-S4 ($\sigma(r) \approx 0.0005$), SPHEREx (targeting $\sigma(f_{\rm NL}^{\rm local}) \approx 0.5$).
  *Falsification Metric:* A measurement of $|f_{\rm NL}^{\rm local}| \ge 1$ at $> 5\sigma$ decisively rules out all single-field inflation models.

---

### Problem 3: Baryon Asymmetry of the Universe (Baryogenesis)
- **Theoretical Barrier:** The observed cosmos exhibits an overwhelming asymmetry between matter and antimatter:
  $$\eta = \frac{n_b - n_{\bar{b}}}{n_\gamma} = (6.12 \pm 0.04) \times 10^{-10}$$
  All antimatter observed in cosmic rays is purely secondary (produced in kinematic collisions).
- **What Current Theory Does NOT Explain:**
  The Standard Model of particle physics rigorously fails all three Sakharov criteria:
  1. *Baryon Number Violation:* While electroweak sphalerons violate $B+L$ at $T > 100\text{ GeV}$, they strictly conserve $B - L$. Any initial $B+L$ asymmetry is erased unless $B-L \neq 0$.
  2. *C and CP Violation:* CP violation in the quark CKM matrix is governed by the Jarlskog invariant $J = (3.08 \pm 0.15) \times 10^{-5}$. The resulting baryon asymmetry is suppressed by Yukawa couplings:
     $$\eta_{\rm SM} \sim J \frac{(m_t^2 - m_u^2)(m_t^2 - m_c^2)(m_b^2 - m_d^2)}{T_{\rm EW}^{12}} \sim 10^{-20}$$
     This is **ten orders of magnitude** smaller than observed ($10^{-20}$ vs $6.12 \times 10^{-10}$).
  3. *Departure from Thermal Equilibrium:* Electroweak baryogenesis requires a strongly first-order phase transition ($v(T_c)/T_c > 1$). In the Standard Model with $m_H = 125.25\text{ GeV}$, lattice gauge simulations prove the electroweak transition is a smooth crossover (requiring $m_H \le 75\text{ GeV}$ for first order).
- **Established Ground Truth Values:**
  - Observed baryon asymmetry: $\eta = (6.124 \pm 0.04) \times 10^{-10}$.
  - Higgs mass: $m_H = 125.25 \pm 0.17\text{ GeV}$ (smooth crossover).
  - CKM CP deficit: $10^{10}$ shortfall.
- **The Decisive Resolving Observation:**
  *Observation:* Discovery of neutrinoless double beta decay ($0\nu\beta\beta$) combined with long-baseline leptonic CP violation.
  *Physical Mechanism:*
  - Observing $0\nu\beta\beta$ establishes that neutrinos are Majorana fermions ($\nu = \bar{\nu}$), confirming total lepton number violation ($\Delta L = 2$).
  - This establishes the foundational pillar of the **Seesaw Mechanism** and **Thermal Leptogenesis**, wherein heavy Majorana neutrinos $N_i$ decay out of equilibrium in the early universe ($N_1 \to \ell H$ vs $\bar{\ell} H^*$), creating a lepton asymmetry that electroweak sphalerons convert into baryon asymmetry via $(B-L)$ conservation.
  - The Davidson-Ibarra bound establishes a minimum right-handed neutrino mass: $M_{N_1} \ge 10^9\text{ GeV}$.
  *Instruments:*
  - $0\nu\beta\beta$: LEGEND-1000 ($^{76}\text{Ge}$), nEXO ($^{136}\text{Xe}$) targeting half-life sensitivity $T_{1/2}^{0\nu} > 10^{28}\text{ yr}$ and effective Majorana mass $m_{\beta\beta} \sim 10-20\text{ meV}$.
  - Leptonic CP phase: DUNE and Hyper-Kamiokande measuring the Dirac phase $\delta_{\rm CP}$ in neutrino oscillations at $> 5\sigma$.
  - Permanent Electric Dipole Moments: ACME, JILA, PSI measuring electron/neutron EDMs ($|d_e| < 4.1 \times 10^{-30}\text{ e}\cdot\text{cm}$) to detect new BSM CP phases.
  *Falsification Metric:* Discovery of $0\nu\beta\beta$ and $\sin \delta_{\rm CP} \neq 0$ confirms the Leptogenesis paradigm. Non-observation of $0\nu\beta\beta$ down to $m_{\beta\beta} < 1\text{ meV}$ under normal ordering rules out standard high-scale Majorana leptogenesis.

---

### Problem 4: The Fundamental Nature of Dark Matter
- **Theoretical Barrier:** Dark matter constitutes $\approx 84.4\%$ of all matter and $\approx 26.4\%$ of the total cosmic energy budget ($\Omega_c h^2 = 0.1200 \pm 0.0012$, $\Omega_c \approx 0.264$).
- **What Current Theory Does NOT Explain:**
  1. The Standard Model contains no stable, cold, non-baryonic particle. (Standard neutrinos are relativistic warm dark matter and contribute $\Omega_\nu h^2 < 0.001$).
  2. The nature of dark matter spans 90 orders of magnitude in mass:
     $$\text{Fuzzy Axions } (10^{-22}\text{ eV}) \longleftrightarrow \text{WIMPs } (10^{11}\text{ eV}) \longleftrightarrow \text{Primordial Black Holes } (10^{68}\text{ eV} \sim 10^{35}\text{ g})$$
  3. Classic thermal Weakly Interacting Massive Particles (WIMPs, $m_\chi \sim 100\text{ GeV}$, $\langle \sigma v \rangle \approx 3 \times 10^{-26}\text{ cm}^3/\text{s}$) have failed to appear in direct detection, with limits pushing to the irreducible neutrino fog.
- **Established Ground Truth Values:**
  - Cold dark matter density: $\Omega_c h^2 = 0.1200 \pm 0.0012$.
  - Leading WIMP cross-section limit: $\sigma_{\rm SI} < 6.0 \times 10^{-48}\text{ cm}^2$ at $m_\chi = 30\text{ GeV}$ (LZ 2024).
  - Neutrino fog cross-section boundary: $\sigma_{\rm SI} \sim 10^{-49} - 10^{-48}\text{ cm}^2$.
- **The Decisive Resolving Observation:**
  *Observation:* Three orthogonal observational channels:
  1. *WIMP Discovery / Exclusion at Neutrino Fog:* Direct nuclear recoil detection in next-generation liquid xenon/argon detectors (DARWIN / XLZD, ARGO). Crossing the neutrino fog with no detection completely excludes thermal WIMP dark matter.
  2. *QCD Axion Resonant Conversion:* Resonant microwave cavity conversion ($a + B_0 \to \gamma$) detecting axion dark matter along the DFSZ/KSVZ band in the $1\ \mu\text{eV} - 1\text{ meV}$ range ($0.2 - 240\text{ GHz}$) via ADMX, DMRadio, FLASH, BREAD.
  3. *Small-Scale Power Spectrum Free-Streaming Cutoff:* High-resolution Lyman-$\alpha$ forest spectra and 21cm tomography (HERA, SKA) measuring matter clustering on sub-megaparsec scales:
     - Cutoff at $k > 10\ h/\text{Mpc}$ corresponding to $m_{\rm WDM} \approx 3-5\text{ keV}$ confirms Warm Dark Matter (sterile neutrinos).
     - De Broglie solitonic core cutoff confirms Fuzzy Dark Matter ($m \sim 10^{-22}\text{ eV}$).
  *Falsification Metric:* Positive resonant RF power in axion cavity or nuclear recoil event rate above neutrino background confirms dark matter particle.

---

### Problem 5: Dark Energy and the Cosmological Constant Catastrophe
- **Theoretical Barrier:** Dark energy drives the late-time acceleration of the cosmic expansion ($z < 0.6$), accounting for $\approx 68.3\%$ of the energy density ($\Omega_\Lambda = 0.6847 \pm 0.0073$).
- **What Current Theory Does NOT Explain:**
  1. *The Cosmological Constant Problem:* Quantum field theory computes vacuum zero-point energy density as $\rho_{\rm vac} = \sum \frac{1}{2}\hbar \omega$. Cut off at the Planck scale $M_{\rm Pl}$, this yields:
     $$\rho_{\rm vac, Pl} \approx 3.5 \times 10^{73}\text{ GeV}^4 \approx 5.2 \times 10^{96}\text{ kg/m}^3$$
     The measured dark energy density is:
     $$\rho_\Lambda = \frac{\Lambda c^2}{8\pi G} \approx 2.5 \times 10^{-47}\text{ GeV}^4 \approx 5.9 \times 10^{-10}\text{ J/m}^3$$
     The theoretical mismatch is **120.1 orders of magnitude**:
     $$\log_{10}\left(\frac{\rho_{\rm vac, Pl}}{\rho_\Lambda}\right) \approx 120.1$$
     Even cut off at the electroweak scale ($100\text{ GeV}$), the discrepancy is $10^{54.6}$; at the QCD scale ($200\text{ MeV}$), it is $10^{43.8}$.
  2. *The Cosmic Coincidence Problem:* Why are $\rho_\Lambda$ and $\rho_m$ of comparable magnitude today ($\rho_\Lambda / \rho_m \approx 2.18$), despite $\rho_m \propto (1+z)^3$ while $\rho_\Lambda \approx \text{const}$?
  3. *Static vs Dynamical:* Is dark energy an invariant Einstein cosmological constant ($w = -1$), or a rolling scalar field (quintessence / k-essence), or a breakdown of General Relativity on cosmological scales?
- **Established Ground Truth Values:**
  - $\Omega_\Lambda = 0.6847 \pm 0.0073$.
  - $\rho_\Lambda \approx (2.25\text{ meV})^4 \approx 2.5 \times 10^{-47}\text{ GeV}^4$.
  - DESI 2024 Year-1 BAO + CMB + SNe hint:
    $$w_0 = -0.827 \pm 0.063, \quad w_a = -0.75^{+0.33}_{-0.25}$$
    deviating from flat $\Lambda$CDM ($w_0 = -1, w_a = 0$) at $2.5\sigma - 3.9\sigma$.
- **The Decisive Resolving Observation:**
  *Observation:* Mapping the dark energy equation of state $w(a) = w_0 + w_a(1-a)$ and the structure growth index $\gamma$ via Stage-IV surveys.
  *Physical Mechanism:*
  - Testing $w(z)$: Measuring galaxy clustering, weak lensing shear, and Type Ia supernovae across $0 < z < 3$. If Euclid, Rubin LSST, and Roman confirm $w_0 \neq -1$ or $w_a \neq 0$ at $> 5\sigma$, the static cosmological constant $\Lambda$ is definitively ruled out in favor of dynamical dark energy.
  - Testing Gravity vs Fluid: Measuring the growth rate $f\sigma_8(z) = \frac{d\ln D}{d\ln a}\sigma_8(z) \approx \Omega_m(z)^\gamma \sigma_8(z)$. General Relativity with dark energy requires $\gamma = 0.55$. A measured deviation (e.g. $\gamma = 0.68$ in DGP gravity or scale-dependent growth in $f(R)$ gravity) proves that cosmic acceleration is modified gravity rather than a dark energy fluid.
  *Instruments:* Euclid Space Telescope, Vera C. Rubin Observatory (LSST), Nancy Grace Roman Space Telescope, DESI 5-year.
  *Falsification Metric:* A measurement of $(w_0, w_a) \neq (-1, 0)$ at $> 5\sigma$ falsifies $\Lambda$CDM; a growth index $\gamma \neq 0.55$ falsifies General Relativity on cosmological horizons.

---

### Problem 6: The Hubble Tension (and Large-Scale Structure $S_8$ Tension)
- **Theoretical Barrier:** A direct statistical discrepancy exists between early-universe determinations of the Hubble constant calibrated on the sound horizon $r_s$ and late-universe distance ladder measurements:
  $$\text{Early (CMB Planck 2018): } H_0 = 67.36 \pm 0.54\text{ km/s/Mpc}$$
  $$\text{Late (SH0ES Riess et al. 2022): } H_0 = 73.04 \pm 1.04\text{ km/s/Mpc}$$
  $$\Delta H_0 = 5.68\text{ km/s/Mpc} \implies \text{Statistical Tension: } 4.85\sigma \approx 5.0\sigma$$
- **What Current Theory Does NOT Explain:**
  Within flat $\Lambda$CDM, no standard parameter adjustment can reconcile both datasets:
  - Increasing $H_0$ in CMB fits requires altering $\omega_m$ or $\omega_b$, which severely violates CMB peak heights and BAO distance ratios.
  - If physical: Requires pre-recombination new physics (e.g., Early Dark Energy [EDE] injecting $\sim 5-10\%$ energy near matter-radiation equality to shrink $r_s$), or decaying dark matter, or primordial magnetic fields.
  - If systematic: Requires an unrecognized systematic error across Cepheids, TRGB, JAGB, and SNe Ia.
  - Additionally, the $S_8 = \sigma_8 \sqrt{\Omega_m / 0.3}$ parameter shows a $2-3\sigma$ tension between weak lensing (KiDS-1000: $S_8 = 0.759 \pm 0.024$; DES Y3: $S_8 = 0.776 \pm 0.017$) and Planck CMB ($S_8 = 0.832 \pm 0.013$).
- **Established Ground Truth Values:**
  - Planck 2018 CMB: $H_0 = 67.36 \pm 0.54\text{ km/s/Mpc}$.
  - SH0ES 2022 Local Ladder: $H_0 = 73.04 \pm 1.04\text{ km/s/Mpc}$.
  - Combined tension: $4.85\sigma$.
- **The Decisive Resolving Observation:**
  *Observation:* Gravitational Wave Standard Sirens independent of both distance ladders and the sound horizon, paired with JWST multi-method stellar cross-calibration.
  *Physical Mechanism:*
  1. *Standard Sirens:* Binary neutron star (BNS) mergers emit gravitational waves whose amplitude directly encodes luminosity distance $D_L$ without any distance ladder calibration:
     $$h \propto \frac{\mathcal{M}^{5/3} f^{2/3}}{D_L}$$
     Combined with an electromagnetic counterpart identifying the host galaxy redshift $z$, this yields a completely independent, pristine geometric determination of $H_0$.
  2. *JWST Stellar Anchors:* Simultaneous NIRCam resolution of Cepheids, Tip of the Red Giant Branch (TRGB), and Carbon stars (JAGB) in identical host galaxies eliminates blending, crowding, and metallicity systematics.
  3. *High-$\ell$ CMB Polarization:* Early Dark Energy (EDE) solutions predict specific polarization damping and phase shifts at $\ell > 2500$ in CMB $EE$ and $TE$ power spectra.
  *Instruments:* LIGO/Virgo/KAGRA, Einstein Telescope, Cosmic Explorer; JWST NIRCam; Simons Observatory, CMB-S4.
  *Falsification Metric:* A sample of $\sim 50$ standard sirens measuring $H_0$ to $\le 1.5\%$ will land unambiguously on either $\approx 67.4$ or $\approx 73.0\text{ km/s/Mpc}$, settling whether $\Lambda$CDM is broken or astrophysical systematics are responsible.

---

### Problem 7: The Primordial Cosmological Lithium Problem
- **Theoretical Barrier:** Standard Big Bang Nucleosynthesis (SBBN) combined with the Planck baryon density $\omega_b = 0.02237$ accurately predicts $^4\text{He}$ and $D/H$, but fails dramatically for $^7\text{Li}$.
- **What Current Theory Does NOT Explain:**
  - The calculated SBBN abundance is:
    $$\left(\frac{^7\text{Li}}{\text{H}}\right)_{\rm SBBN} = (4.68 \pm 0.32) \times 10^{-10}$$
  - The observed abundance in ancient, metal-poor Population II halo dwarf stars (the Spite plateau, $[\text{Fe/H}] < -2$) is:
    $$\left(\frac{^7\text{Li}}{\text{H}}\right)_{\rm obs} = (1.58 \pm 0.11) \times 10^{-10}$$
  - The discrepancy is a factor of $2.97$ ($\sim 3\times$ deficit), representing a **$> 9\sigma$ statistical tension**:
    $$\text{Tension} = \frac{(4.68 - 1.58) \times 10^{-10}}{\sqrt{0.32^2 + 0.11^2} \times 10^{-10}} \approx 9.18\sigma$$
  - Current theory cannot resolve whether this is due to non-standard stellar astrophysics (rotational mixing and atomic diffusion draining lithium from stellar atmospheres over 12 Gyr) or beyond-Standard-Model particle decays during BBN (e.g. decaying gravitinos or axinos destroying $^7\text{Be}$ before it electron-captures to $^7\text{Li}$).
- **Established Ground Truth Values:**
  - Theoretical SBBN: $(4.68 \pm 0.32) \times 10^{-10}$.
  - Spite plateau observed: $(1.58 \pm 0.11) \times 10^{-10}$.
  - Discrepancy factor: $2.97\times$ ($9.18\sigma$ tension).
- **The Decisive Resolving Observation:**
  *Observation:* High-resolution spectroscopic measurement of gas-phase $^7\text{Li}$ in pristine interstellar and intergalactic gas clouds outside stars (e.g., low-metallicity Damped Lyman-$\alpha$ Systems [DLAs] or metal-poor gas in the Small Magellanic Cloud).
  *Physical Mechanism:*
  - Interstellar gas in DLAs at high redshift has never been subjected to stellar core temperatures ($T > 2.5 \times 10^6\text{ K}$) or convective depletion.
  - If gas-phase $(^7\text{Li}/\text{H})$ in pristine DLAs matches the SBBN prediction of $4.7 \times 10^{-10}$, the Spite plateau is proven to be caused by stellar atmospheric depletion, resolving the anomaly in favor of standard cosmology.
  - If gas-phase $(^7\text{Li}/\text{H})$ matches $1.6 \times 10^{-10}$, stellar physics is vindicated and new particle physics during the nucleosynthesis era ($t \sim 100 - 1000\text{ s}$) is experimentally established.
  *Instruments:* Extremely Large Telescope High-Resolution Spectrograph (ELT-HIRES), VLT-ESPRESSO, Keck HIRES.
  *Falsification Metric:* A measurement of $(^7\text{Li}/\text{H})_{\rm gas} \approx 4.7 \times 10^{-10}$ in low-metallicity DLAs rescues SBBN; a measurement of $\approx 1.6 \times 10^{-10}$ definitively confirms BSM nucleosynthesis physics.

---

### Problem 8: Cosmic Topology and Large-Angle CMB Anomalies
- **Theoretical Barrier:** The standard cosmological model posits an infinite, simply connected spatial geometry with statistical isotropy: $\mathbb{R}^3$.
- **What Current Theory Does NOT Explain:**
  CMB maps from COBE, WMAP, and Planck reveal persistent large-scale anomalies:
  1. *Lack of Large-Angle Correlation:* The angular two-point correlation function $C(\theta) = \langle \Delta T(\hat{n}_1) \Delta T(\hat{n}_2) \rangle$ is virtually zero for $\theta > 60^\circ$, an occurrence with $p < 0.1\%$ in standard $\Lambda$CDM.
  2. *Quadrupole-Octopole Alignment ("Axis of Evil"):* The $\ell = 2$ quadrupole and $\ell = 3$ octopole planes are aligned with each other and with the cosmological dipole and ecliptic plane at $p < 0.5\%$.
  3. *Hemispherical Power Asymmetry:* The power in the southern ecliptic hemisphere is $\approx 7\%$ higher than in the northern hemisphere.
  - Current theory cannot determine whether these anomalies are rare statistical flukes (cosmic variance) or genuine signatures of a compact cosmic topology (e.g. 3-torus $T^3$ or Poincaré dodecahedral space) or anisotropic pre-inflationary initial conditions.
- **Established Ground Truth Values:**
  - $C(\theta > 60^\circ) \approx 0$ ($p < 10^{-3}$).
  - Low-multipole planarity alignment ($p < 0.005$).
  - Hemispherical asymmetry: $\sim 7\%$ dipole modulation.
- **The Decisive Resolving Observation:**
  *Observation:* Full-sky CMB polarization matched "circles-in-the-sky" searches combined with 3D large-scale structure topology mapping.
  *Physical Mechanism:*
  - In a compact, multi-connected universe with topology scale $L < 2 R_{\rm LSS}$ (where $R_{\rm LSS} \approx 14\text{ Gpc}$ is the distance to the last scattering surface), the sphere of last scattering intersects itself, producing pairs of matching circles with identical temperature and polarization fluctuations.
  - While temperature searches by Planck set $L > 0.98 \times 2 R_{\rm LSS}$, CMB polarization ($E$-modes) is virtually unaffected by late-time Integrated Sachs-Wolfe (ISW) foregrounds, providing clean topological discrimination.
  - Furthermore, 3D galaxy clustering and cosmic shear from Stage-IV surveys break continuous translation invariance into discrete topological eigenmodes.
  *Instruments:* LiteBIRD full-sky polarization mission; Euclid, Rubin LSST, and SPHEREx 3D clustering catalogs.
  *Falsification Metric:* Detection of matched circle pairs in $EE$ polarization proves compact cosmic topology; absence of circle pairs at $L > 2 R_{\rm LSS}$ establishes that the observable topology scale exceeds our causal horizon.

---

## 4. Matrix of Open Problems and Decisive Resolving Observations

The required deliverable is summarized in the matrix below:

| ID | Open Problem | Core Theoretical Failure | Established Ground Truth / Discrepancy | Decisive Resolving Observation | Target Facility / Timeline | Falsification / Resolution Metric |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **OP-01** | **Initial Singularity & UV Incompleteness** | GR breaks down at $t_{\rm Pl} \sim 5.4 \times 10^{-44}\text{ s}$; cannot establish whether time had a beginning or bounce. | $\rho_{\rm Pl} \approx 5.16 \times 10^{96}\text{ kg/m}^3$; $E_{\rm Pl} \approx 1.22 \times 10^{19}\text{ GeV}$. | Measure Primordial Gravitational Wave tensor index $n_T$ across CMB to space interferometry. | LiteBIRD, LISA, DECIGO, BBO, Einstein Telescope | $n_T > 0$ rules out standard inflation; proves quantum bounce / pre-Big Bang cosmology. |
| **OP-02** | **Cosmic Inflation & Inflaton Mechanics** | Unknown inflaton field identity; initial low-entropy fine-tuning; eternal multiverse measure catastrophe. | $r < 0.036$ (95% CL); $n_s = 0.9649 \pm 0.0042$; $\Omega_k = 0.0007 \pm 0.0019$. | Detect CMB B-mode polarization $r$ and local non-Gaussianity $f_{\rm NL}^{\rm local}$. | LiteBIRD ($\sigma(r) < 10^{-3}$), CMB-S4, SPHEREx | $r \approx 0.003$ confirms Starobinsky/GUT inflation; $\|f_{\rm NL}^{\rm local}\| \ge 1$ rules out all single-field inflation. |
| **OP-03** | **Baryon Asymmetry (Baryogenesis)** | Standard Model fails Sakharov conditions: CKM CP deficit $\sim 10^{-10}$; EW transition is smooth crossover. | $\eta_{\rm obs} = (6.12 \pm 0.04) \times 10^{-10}$; $\eta_{\rm SM} \sim 10^{-20}$; $m_H = 125.25\text{ GeV}$. | Observe $0\nu\beta\beta$ ($\Delta L=2$), leptonic CP phase $\delta_{\rm CP}$, and permanent EDMs. | LEGEND-1000, nEXO, DUNE, Hyper-K, ACME/JILA | $0\nu\beta\beta$ discovery confirms Majorana neutrinos and validates Leptogenesis paradigm. |
| **OP-04** | **Particle Nature of Dark Matter** | No viable SM particle candidate; mass unknown across 90 orders of magnitude; WIMPs not found. | $\Omega_c h^2 = 0.1200 \pm 0.0012$; $\sigma_{\rm SI} < 6 \times 10^{-48}\text{ cm}^2$ at $30\text{ GeV}$. | Direct detection reaching neutrino fog; resonant axion cavity conversion; 21cm power spectrum cutoff. | DARWIN/XLZD, ARGO, ADMX, DMRadio, HERA, SKA | Recoils at neutrino fog or RF axion resonant power confirms particle; 21cm cutoff tests WDM/fuzzy DM. |
| **OP-05** | **Dark Energy & Cosmological Constant** | QFT zero-point energy exceeds observed vacuum energy by $10^{120}$; coincidence problem unexplained. | $\rho_\Lambda \approx 2.5 \times 10^{-47}\text{ GeV}^4$; $\rho_{\rm vac, Pl} \approx 3.5 \times 10^{73}\text{ GeV}^4$ ($120.1$ orders mismatch). | Measure dynamical equation of state $w(z) = w_0 + w_a(1-a)$ and growth rate index $\gamma$. | Euclid, Rubin LSST, Roman Space Telescope, DESI | $(w_0, w_a) \neq (-1, 0)$ at $> 5\sigma$ rules out $\Lambda$; growth index $\gamma \neq 0.55$ proves modified gravity. |
| **OP-06** | **Hubble Tension & $S_8$ Tension** | Persistent $4.9 - 5.3\sigma$ discrepancy between direct local distance ladder and CMB sound horizon inference. | Early: $H_0 = 67.36 \pm 0.54$; Late: $H_0 = 73.04 \pm 1.04\text{ km/s/Mpc}$; $\Delta H_0 = 5.68$ ($4.85\sigma$). | Gravitational Wave Standard Sirens independent of distance ladder; JWST Cepheid/TRGB cross-calibration. | LIGO/Virgo/ET Standard Sirens; JWST NIRCam; Simons Obs | $\sim 50$ standard sirens measure $H_0$ to $\le 1.5\%$, definitively selecting between $67.4$ and $73.0\text{ km/s/Mpc}$. |
| **OP-07** | **Primordial Lithium Problem** | SBBN overpredicts primordial $^7\text{Li}$ by factor of 3 compared to metal-poor halo dwarf stars ($> 9\sigma$). | $(^7\text{Li}/\text{H})_{\rm SBBN} = 4.68 \times 10^{-10}$; $(^7\text{Li}/\text{H})_{\rm obs} = 1.58 \times 10^{-10}$ ($2.97\times$ deficit). | High-resolution spectroscopy of gas-phase $^7\text{Li}$ in unevolved interstellar/DLA gas clouds outside stars. | ELT-HIRES, VLT-ESPRESSO, Keck HIRES | Gas-phase $^7\text{Li} = 4.7 \times 10^{-10}$ proves stellar depletion; gas-phase $1.6 \times 10^{-10}$ proves BSM BBN physics. |
| **OP-08** | **Cosmic Topology & Large-Angle Anomalies** | Lack of CMB angular correlation at $\theta > 60^\circ$; quadrupole-octopole alignment; hemispherical asymmetry. | $C(\theta > 60^\circ) \approx 0$ ($p < 0.1\%$); multipole alignment ($p < 0.5\%$); $7\%$ power asymmetry. | Full-sky CMB polarization matched circles-in-the-sky search and 3D galaxy clustering eigenmode analysis. | LiteBIRD, Euclid, Rubin LSST, SPHEREx | Matched circle pairs in polarization prove multi-connected topology; 3D discrete eigenmodes confirm boundary. |

---

## 5. Computational Engine & Verification Summary

The numerical calculations and statistical tensions presented in this study were verified through [`origin_of_universe_engine.py`](file:///D:/AgentSwarm/arena/world/origin_of_universe_engine.py) and validated via [`test_origin_of_universe_engine.py`](file:///D:/AgentSwarm/arena/world/test_origin_of_universe_engine.py).

### Summary of Executed Verification (27/27 Tests Passing)
1. **CMB Thermodynamics:**
   - Peak frequency: $\nu_{\max} = 160.23\text{ GHz}$
   - Peak wavelength: $\lambda_{\max} = 1.063\text{ mm}$
   - Photon number density: $n_\gamma = 410.72\text{ cm}^{-3}$
   - Energy density: $\rho_\gamma = 0.2606\text{ eV/cm}^3$
   - FIRAS limits verified: $|y| < 1.5 \times 10^{-5}$, $|\mu| < 9 \times 10^{-5}$, departures $< 50\text{ ppm}$.
   - High-redshift test consistency verified: $T(z = 6.34) = 20.0 \pm 2.0\text{ K}$ matches $20.00\text{ K}$.
2. **Nucleosynthesis Concordance:**
   - Freeze-out ratio: $(n/p)_{\rm freeze} = 0.1986$ at $T = 0.8\text{ MeV}$.
   - Bottleneck ratio: $(n/p)_{\rm BBN} = 0.1412$ after $\Delta t = 300\text{ s}$ decay.
   - Predicted $^4\text{He}$ mass fraction: $Y_p = 0.2474$ (matches observed $0.245 \pm 0.003$ within $0.8\sigma$).
   - Predicted Deuterium: $(D/H)_p = 2.537 \times 10^{-5}$ (matches observed $2.547 \times 10^{-5}$ within $0.4\sigma$).
   - Primordial Lithium: Theoretical $4.687 \times 10^{-10}$ vs Observed $1.58 \times 10^{-10}$, confirming a factor of $2.97\times$ deficit and a $9.18\sigma$ tension.
3. **Hubble & Large-Scale Tensions:**
   - Difference $\Delta H_0 = 5.68\text{ km/s/Mpc}$, Gaussian tension $= 4.85\sigma$.
   - $S_8$ tension between KiDS-1000 ($0.759 \pm 0.024$) and Planck ($0.832 \pm 0.013$) $= 2.68\sigma$.
4. **Inflation & Gravitational Waves:**
   - Starobinsky model yields $n_s = 0.9667$, $r = 0.00333$, $n_T = -0.000417$.
   - Inflationary energy scale for $r = 0.036$: $V^{1/4} = 1.63 \times 10^{16}\text{ GeV}$.
5. **Vacuum Energy Discrepancy:**
   - $\log_{10}(\rho_{\rm vac, Pl} / \rho_\Lambda) = 120.1$ orders of magnitude.
   - $\log_{10}(\rho_{\rm vac, EW} / \rho_\Lambda) = 54.6$ orders of magnitude.
   - Coincidence ratio today: $\rho_\Lambda / \rho_m = 2.18$.

---

## 6. Epistemic Ledger, Falsification Criteria, and Directives

### What Was Established
- The Hot Big Bang is empirically verified at redshifts $z \le 10^9$ ($t \ge 0.1\text{ s}$) by the CMB blackbody spectrum, BBN $^4\text{He}$ and $D$ yields, cosmic time dilation, and the acoustic sound horizon.
- The standard framework is fundamentally incomplete: it has no explanation for the singularity, the nature of the inflaton, the Sakharov baryogenesis criteria, dark matter, or the 120-order-of-magnitude cosmological constant catastrophe.
- The Hubble tension ($\Delta H_0 \approx 5.7\text{ km/s/Mpc}$, $4.85\sigma$) and the Lithium problem ($2.97\times$ deficit, $9.18\sigma$) are the two most acute empirical failures of the current cosmological consensus.

### What Remains Unknown
- The microphysical origin of the dark sector (whether dark energy is dynamical $w(z) \neq -1$ or modified gravity; whether dark matter is WIMP, axion, sterile neutrino, or primordial black hole).
- The state of the universe prior to $t \sim 10^{-32}\text{ s}$ (whether inflation occurred, what drove it, or whether an initial singularity was superseded by a quantum bounce).

### Evidence That Would Change These Conclusions
1. Detection of Primordial Gravitational Waves with blue tilt $n_T > 0$ would falsify all standard inflation models and establish a bouncing cosmogenesis.
2. Discovery of $0\nu\beta\beta$ decay would confirm Majorana neutrinos and validate Leptogenesis.
3. Measurement of gas-phase $^7\text{Li} = (4.7 \pm 0.3) \times 10^{-10}$ in high-$z$ DLAs would resolve the Lithium problem into stellar atmospheric diffusion.
4. Independent Standard Siren measurement of $H_0 = 67.4 \pm 0.7\text{ km/s/Mpc}$ would resolve the Hubble tension into distance ladder systematic errors. Conversely, an independent value of $73.0 \pm 0.8\text{ km/s/Mpc}$ would definitively falsify flat $\Lambda$CDM and require new pre-recombination physics.
