# Empirical Foundations of Cosmogenesis and Master Taxonomy of Open Problems

**Agent**: Raman (A002, Generation 0)  
**Domain**: Origin of the universe (`cosmogenesis`)  
**Epistemic Class**: Empirical  
**Verification Date**: 2026-10-02  
**Module Artifact**: `phase2/cosmogenesis/cosmogenesis_engine.py`  
**Test Suite**: `phase2/cosmogenesis/test_cosmogenesis_engine.py` (8/8 tests pass, 100% verified)

---

## 1. Strongest Empirical Evidence for the Hot Big Bang

The Hot Big Bang is established by four non-negotiable quantitative observational pillars:

1. **CMB Blackbody Spectrum**:
   - Monopole temperature $T_0 = 2.72548 \pm 0.00057\text{ K}$ measured by COBE/FIRAS (Fixsen 2009).
   - Peak frequency $\nu_{peak} = 160.23\text{ GHz}$; energy density $u_{rad} = 4.17 \times 10^{-14}\text{ J/m}^3$; photon density $n_\gamma = 410.7\text{ cm}^{-3}$.
   - Rigorous spectral distortion upper limits ($|\mu| < 9 \times 10^{-5}$, $|y| < 1.5 \times 10^{-5}$) rule out any energy injection $> 10^{-4} \rho_{rad}$ between $z \sim 2 \times 10^6$ and recombination.

2. **Primordial Big Bang Nucleosynthesis (BBN)**:
   - Evaluated at baryon-to-photon ratio $\eta = (6.12 \pm 0.04) \times 10^{-10}$ ($\Omega_b h^2 = 0.02237 \pm 0.00015$).
   - Primordial He-4 mass fraction: $Y_p = 0.2450$, in perfect agreement with observed $Y_p = 0.245 \pm 0.003$ in metal-poor H II regions.
   - Primordial Deuterium abundance: $D/H = (2.54 \pm 0.04) \times 10^{-5}$ (Cooke et al. 2018).

3. **Universal Cosmic Expansion**:
   - Linear expansion $v = H_0 d$, confirmed across 13 billion years through Type Ia supernova light-curve time dilation ($\Delta t_{obs} = \Delta t_{emit}(1+z)$) and Tolman surface brightness $(1+z)^{-4}$ dimming.

4. **Acoustic Horizon and Geometric Flatness**:
   - CMB temperature and polarization acoustic peak spectrum ($\ell_1 \approx 220$), acoustic scale $\theta_* = (1.04110 \pm 0.00031) \times 10^{-2}\text{ rad}$, confirming $|\Omega_K| < 0.002$ (flat universe).

---

## 2. Master Taxonomy: Genuine Open Problems & Resolving Observations

Current cosmological theory breaks down or fails to explain eight fundamental phenomena:

### OP-01: Initial Spacetime Singularity
- **Unexplained**: General Relativity predicts geodesics terminate at infinite curvature and density at $t=0$ (Penrose-Hawking singularity theorems). Cosmology lacks an empirically verified quantum theory of gravity for $t < t_{Planck}$.
- **Resolving Observation**: Detection of the high-frequency primordial gravitational wave background spectrum ($10^8\text{--}10^{10}\text{ Hz}$) or ultra-high precision CMB B-mode tensor tilt $n_T$. Distinguishing quantum bounce models (Loop Quantum Cosmology: $n_T > 0$) from singular inflation ($n_T = -r/8 < 0$).
- **Target Facility**: LiteBIRD, CMB-S4, and ultra-high-frequency resonant cavity GW detectors.
- **Quantitative Threshold**: Tensor spectral index uncertainty $\sigma(n_T) < 0.01$ and tensor-to-scalar ratio sensitivity down to $r = 0.001$.

### OP-02: Baryon Asymmetry of the Universe (BAU)
- **Unexplained**: The observable universe has $\eta_B = (6.12 \pm 0.04) \times 10^{-10}$. Standard Model CP violation (Jarlskog $J \approx 3 \times 10^{-5}$) produces at most $\eta_B \le 10^{-18}$ ($> 10^8$ deficit). Furthermore, with $m_H = 125.10\text{ GeV} > 75\text{ GeV}$, the electroweak transition is a smooth crossover, failing Sakharov conditions.
- **Resolving Observation**: Measurement of the Higgs trilinear self-coupling $\lambda_{hhh}$ confirming a strongly first-order phase transition ($\delta\kappa_\lambda > 20\%$), detection of stochastic GWs from bubble collisions at mHz frequencies, or discovery of neutrinoless double beta decay ($0\nu\beta\beta$) confirming Majorana neutrinos and leptogenesis.
- **Target Facility**: HL-LHC / FCC-ee, LISA, and LEGEND-1000 / nEXO.
- **Quantitative Threshold**: $\delta\kappa_\lambda > 0.20$ at $>5\sigma$; LISA stochastic GW energy density $\Omega_{GW} h^2 \sim 10^{-11}$ at $1\text{ mHz}$; or $0\nu\beta\beta$ half-life $T_{1/2} > 10^{27}\text{ yr}$ with $m_{\beta\beta} \in [15, 50]\text{ meV}$.

### OP-03: Inflationary Mechanism & Inflaton Identification
- **Unexplained**: Inflation resolves the horizon, flatness, and magnetic monopole problems and predicts nearly scale-invariant perturbations ($n_s = 0.965$), but the underlying scalar field, potential, reheating coupling, and UV completion remain unidentified.
- **Resolving Observation**: Detection of primordial B-mode polarization in the CMB, fixing the inflation energy scale $V^{1/4} = 1.04 \times 10^{16} (r / 0.01)^{1/4}\text{ GeV}$ and testing the single-field consistency relation $r = -8 n_T$.
- **Target Facility**: LiteBIRD, CMB-S4, and Simons Observatory.
- **Quantitative Threshold**: Detection of $r \ge 0.003$ at $>5\sigma$, or an upper limit $r < 0.001$ ruling out canonical $R^2$ Starobinsky and plateau models.

### OP-04: Nature and Particle Identity of Cold Dark Matter
- **Unexplained**: Dark matter accounts for $\Omega_c h^2 = 0.1200 \pm 0.0012$ (~84% of matter). No Standard Model particle has the required neutral, stable, cold collisionless properties.
- **Resolving Observation**: Direct detection of WIMP nuclear recoils to the neutrino floor, resonant microwave cavity detection of QCD axions ($a \to \gamma\gamma$), or 21-cm matter power spectrum cutoff measuring free-streaming length.
- **Target Facility**: LZ, DARWIN (WIMPs); ADMX, MADMAX (Axions); SKA (21-cm tomography).
- **Quantitative Threshold**: WIMP-nucleon cross section $\sigma_{SI} \sim 10^{-49}\text{ cm}^2$ at $m_\chi \sim 50\text{ GeV}$; or axion-photon coupling $g_{a\gamma\gamma} \in [10^{-15}, 10^{-12}]\text{ GeV}^{-1}$ for $m_a \in [10^{-6}, 10^{-3}]\text{ eV}$.

### OP-05: Cosmological Constant Problem and Dark Energy
- **Unexplained**: Observed $\rho_{DE} \approx 2.3 \times 10^{-47}\text{ GeV}^4 \approx 5.35 \times 10^{-10}\text{ J/m}^3$ differs from QFT Planck-cutoff zero-point vacuum energy ($\rho_{vac} \sim 10^{76}\text{ GeV}^4$) by 120 orders of magnitude. Standard theory cannot explain why $\Lambda$ is non-zero yet canceled to 120 decimal places.
- **Resolving Observation**: Precision measurement of dark energy equation of state $w(z) = w_0 + w_a(1-a)$ through large-scale galaxy clustering, BAO, and SNe Ia.
- **Target Facility**: Euclid Space Telescope, Vera C. Rubin Observatory (LSST), and Roman Space Telescope.
- **Quantitative Threshold**: Measurement of $w_0$ to $\sigma(w_0) < 0.01$ and $w_a$ to $\sigma(w_a) < 0.08$. Detecting $w \ne -1$ or $w_a \ne 0$ at $>3\sigma$ falsifies static vacuum energy.

### OP-06: The Hubble Tension
- **Unexplained**: Early-universe sound horizon calibration under $\Lambda$CDM ($H_0 = 67.36 \pm 0.54\text{ km/s/Mpc}$) conflicts with late-universe Cepheid-SN distance ladder ($H_0 = 73.04 \pm 1.04\text{ km/s/Mpc}$) at $4.85\sigma$ ($5.0\sigma$).
- **Resolving Observation**: Calibration-free gravitational wave standard sirens from binary neutron star mergers with electromagnetic counterparts, combined with JWST multi-method distance recalibration.
- **Target Facility**: LIGO-Virgo-KAGRA / Einstein Telescope and JWST NIRCam.
- **Quantitative Threshold**: Determination of $H_0$ to $< 1.0\%$ precision ($< 0.7\text{ km/s/Mpc}$) using $N \ge 50$ sirens, determining whether the tension is instrumental/systematic or requires early dark energy / new physics.

### OP-07: Primordial Lithium-7 Depletion Anomaly
- **Unexplained**: Standard BBN predicts primordial $^7\text{Li}/H = (4.68 \pm 0.32) \times 10^{-10}$, whereas metal-poor halo dwarf stars consistently show $^7\text{Li}/H = (1.58 \pm 0.11) \times 10^{-10}$, a $9.2\sigma$ deficit ($2.96\times$) unresolvable by standard stellar diffusion without burning $^6\text{Li}$.
- **Resolving Observation**: High-dispersion optical absorption spectroscopy of pristine, non-stellar intergalactic gas clouds at $z > 2$.
- **Target Facility**: Extremely Large Telescope (ELT / ANDES spectrograph).
- **Quantitative Threshold**: Pristine IGM $^7\text{Li}$ measurement to $< 15\%$ uncertainty. If IGM shows $1.58 \times 10^{-10}$, BBN nuclear reaction rates are falsified; if it shows $4.68 \times 10^{-10}$, stellar depletion is confirmed.

### OP-08: Low Initial Gravitational Entropy & Arrow of Time
- **Unexplained**: Initial state had extraordinarily low gravitational entropy ($S_{init} \sim 10^{88}\text{ k}_B$) compared to a maximal thermalized black hole state ($S_{max} \sim 10^{123}\text{ k}_B$). Under Penrose's Weyl Curvature Hypothesis, $C_{\mu\nu\rho\sigma} \to 0$ at the initial hypersurface, requiring fine-tuning of 1 part in $10^{10^{123}}$.
- **Resolving Observation**: Precision measurement of primordial non-Gaussianity bispectrum shapes ($f_{NL}^{loc}, f_{NL}^{equil}$) and tensor tilt to constrain initial hypersurface quantum boundary conditions.
- **Target Facility**: SPHEREx, Euclid, and CMB-S4.
- **Quantitative Threshold**: Measurement of non-Gaussianity to $\sigma(f_{NL}) < 1.0$, discriminating single-field from multi-field and non-Bunch-Davies initial states.
