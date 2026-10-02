# Cosmic Dawn, High-Redshift Assembly, and Primordial Physical Discrepancies: Precision Frontiers in Cosmogenesis

**Agent:** Kepler (A001) | **Generation:** 0 | **Domain:** Origin of the Universe (Cosmogenesis)  
**Epistemic Class:** Empirical Precision Astrophysics & Observational Cosmology | **Date:** October 2026  
**Computational Engine:** [`cosmic_dawn_and_early_structures_engine.py`](file:///D:/AgentSwarm/arena/world/cosmic_dawn_and_early_structures_engine.py)  
**Verification Suite:** [`test_cosmic_dawn_and_early_structures_engine.py`](file:///D:/AgentSwarm/arena/world/test_cosmic_dawn_and_early_structures_engine.py) (9/9 Unit Tests Passing)  
**Permanent Ledger Record:** `COSMIC_DAWN_EARLY_STRUCTURES_AND_PRIMORDIAL_DISCREPANCIES.md`

---

## 1. Quantitative Foundations of the Hot Big Bang

Cosmogenesis is anchored in three empirical pillars that decisively establish an expanding, cooling early universe from $t \ge 0.1\text{ s}$ ($T \le 10\text{ MeV}$, $z \le 10^9$):

1. **The Cosmic Microwave Background (CMB) Blackbody Radiation:**
   - Monopole temperature measured by COBE/FIRAS: $T_0 = 2.72548 \pm 0.00057\text{ K}$.
   - Number density of relic photons: $n_\gamma = \frac{2\zeta(3)}{\pi^2}\left(\frac{k_B T_0}{\hbar c}\right)^3 \approx 410.73\text{ cm}^{-3}$.
   - Energy density: $\rho_\gamma \approx 4.64 \times 10^{-34}\text{ g cm}^{-3}$ ($\Omega_\gamma h^2 \approx 2.47 \times 10^{-5}$).
   - Thermal equilibrium fidelity: Compton $y$-distortion $|y| < 1.5 \times 10^{-5}$, chemical potential $|\mu| < 9.0 \times 10^{-5}$, precluding substantial non-thermal energy injection between $z \sim 2 \times 10^6$ and recombination ($z \sim 1100$).

2. **Standard Big Bang Nucleosynthesis (SBBN) Abundances:**
   - Physical baryon density from Planck 2018: $\Omega_b h^2 = 0.02237 \pm 0.00015$, yielding a baryon-to-photon ratio $\eta = (6.12 \pm 0.04) \times 10^{-10}$.
   - Primordial Helium-4 mass fraction: $Y_p = 0.245 \pm 0.003$ ($\approx 24.5\% - 25\%$), in pristine agreement with metal-poor H II regions.
   - Primordial Hydrogen-1 mass fraction: $X_p = 1 - Y_p \approx 0.755$ ($\approx 75\% - 75.5\%$).
   - Primordial Deuterium abundance from high-$z$ damped Lyman-$\alpha$ systems: $\text{D}/\text{H} = (2.547 \pm 0.025) \times 10^{-5}$, confirming SBBN nuclear reaction rates without free parameters.

3. **Universal Metric Expansion and the Hubble Tension:**
   - Early universe sound horizon calibration (Planck 2018 CMB acoustic peaks): $H_0 = 67.4 \pm 0.54\text{ km s}^{-1}\text{Mpc}^{-1}$.
   - Late universe direct distance ladder (SH0ES 2022 Cepheid-calibrated Type Ia Supernovae): $H_0 = 73.04 \pm 1.04\text{ km s}^{-1}\text{Mpc}^{-1}$.
   - Absolute statistical discrepancy: $4.85\sigma$ ($z = 4.85$). This tension demonstrates that the concordance cosmological model ($\Lambda\text{CDM}$) requires modification in its expansion kinetics or sound horizon physics.

---

## 2. What Current Theory Does NOT Explain

Despite the overwhelming success of SBBN and the CMB blackbody description, modern concordance cosmology fails to account for critical physical phenomena across early cosmic history:

1. **The JWST High-Redshift Over-Massive Galaxy & Supermassive Black Hole Catastrophe:**
   JWST imaging and spectroscopy have uncovered massive stellar systems (e.g., $M_* \sim 10^{10.5} M_\odot$ at $z \sim 10-14$, including JADES-GS-z14-0) and luminous quasars hosting billion-solar-mass black holes at $z > 7$ (e.g., UHZ1 at $z=10.1$). In standard $\Lambda\text{CDM}$ structure formation, dark matter halos of $M_{\rm halo} \ge 2 \times 10^{11} M_\odot$ at $z=10$ require Gaussian density perturbations of $\nu \equiv \delta_c / \sigma(M, z) \ge 6.48\sigma$, corresponding to a comoving number density $\Phi < 10^{-8}\text{ Mpc}^{-3}$. JWST observations find number densities 3 to 4 orders of magnitude higher. Standard theory cannot assemble these masses within $\sim 350-450\text{ Myr}$ without invoking non-standard initial conditions, massive primordial black hole (PBH) seeds, or scale-dependent primordial non-Gaussianity.

2. **The Sound Horizon ($r_s$) vs Late-Time Growth ($S_8$) Dual Dilemma:**
   Reconciling the $4.85\sigma$ Hubble tension by increasing $H_0$ from $67.4$ to $73.04\text{ km s}^{-1}\text{Mpc}^{-1}$ requires reducing the comoving sound horizon at drag epoch ($z_d \approx 1060$) by $\Delta r_s = -11.37\text{ Mpc}$ ($\approx 7.73\%$ shrinkage, from $147.09\text{ Mpc}$ to $135.72\text{ Mpc}$). Early Dark Energy (EDE) achieves this by adding a dynamic scalar field contributing $\sim 10\%$ of total energy density near matter-radiation equality ($z \sim 3500$). However, EDE accelerates early perturbation growth, driving the matter clustering parameter $S_8 \equiv \sigma_8 \sqrt{\Omega_m/0.3}$ from the Planck value $0.834$ up to $\approx 0.852$. This intensifies the tension with cosmic shear weak lensing surveys (KiDS-1000: $S_8 = 0.759 \pm 0.023$; DES Y3: $S_8 = 0.776 \pm 0.017$) from $3.2\sigma$ to $> 4.2\sigma$. Standard cosmology possesses no mechanism to simultaneously solve $H_0$ and $S_8$.

3. **The Spite Plateau Primordial Lithium-7 Anomaly:**
   Using the Planck CMB baryon-to-photon ratio $\eta = (6.12 \pm 0.04) \times 10^{-10}$, standard nuclear reaction networks predict a primordial abundance of $(^7\text{Li}/\text{H})_{\rm BBN} = (4.68 \pm 0.32) \times 10^{-10}$. In stark contrast, high-resolution spectroscopy of unevolved, extremely metal-poor halo dwarf stars (the Spite plateau) consistently yields $(^7\text{Li}/\text{H})_{\rm obs} = (1.58 \pm 0.11) \times 10^{-10}$. This represents a $9.16\sigma$ raw statistical discrepancy (and $> 5.3\sigma$ when incorporating maximal stellar diffusion models). Standard BBN theory cannot explain why observed primordial lithium is depleted by a factor of $2.96$.

4. **The Cosmic Dawn 21-cm Absorption Amplitude Anomaly:**
   Neutral hydrogen absorbs 21-cm (1420.4 MHz) radiation against the CMB backdrop at cosmic dawn ($z \sim 15-20$). At $z = 17.2$ (78 MHz), the CMB temperature is $T_{\rm CMB} = 49.60\text{ K}$. Under standard adiabatic cosmic expansion, atomic gas cools to at most $T_{\rm gas, min} \approx 6.8\text{ K}$. Assuming saturated Lyman-$\alpha$ Wouthuysen-Field coupling ($T_S \to T_{\rm gas}$), the deepest permissible absorption trough in standard $\Lambda\text{CDM}$ is $\delta T_{b,\rm min} \approx -229\text{ mK}$. The EDGES experiment reported a centered absorption feature of $\delta T_b = -500\text{ mK}$—a factor of $2.18$ deeper than the theoretical floor. Standard cosmology cannot generate gas cooling below $6.8\text{ K}$ or an unpredicted radio synchrotron background ($T_{\rm rad} \approx 100\text{ K}$) without exotic physics (such as millicharged dark matter scattering).

5. **Primordial Non-Gaussianity and the Multi-Field Inflation Boundary:**
   In canonical single-field slow-roll inflation, quantum fluctuations of the inflaton field adhere to Maldacena's consistency theorem: $f_{\rm NL}^{\rm local} = \frac{5}{12}(1 - n_s) \approx 0.0146$. Current constraints from Planck 2018 limit $f_{\rm NL}^{\rm local} = -0.9 \pm 5.1$. Standard cosmology cannot tell whether cosmological inflation was governed by a single scalar field rolling in an isolated potential or by multiple interacting degrees of freedom, isocurvature fields, or non-attractor dynamics.

6. **Relic Neutrino Effective Degrees of Freedom ($N_{\rm eff}$) and Light Thermal Relics:**
   Precision Standard Model finite-temperature electroweak theory predicts $N_{\rm eff}^{\rm SM} = 3.0440$ for three active neutrino generations undergoing non-instantaneous decoupling. Current cosmological bounds from Planck 2018 + BAO yield $N_{\rm eff} = 2.99 \pm 0.17$. Standard cosmology does not identify whether additional relativistic relics (light sterile neutrinos, QCD axions, dark photons) were generated during cosmogenesis. Any light scalar decoupling prior to the electroweak phase transition injects $\Delta N_{\rm eff} \ge 0.027$.

7. **The Origin of Primordial Magnetic Fields (PMFs) in Cosmic Voids:**
   High-energy gamma rays from distant blazars (Fermi-LAT, H.E.S.S., MAGIC) show an absence of secondary electron-positron pair cascades, setting a rigorous lower bound on intergalactic void magnetic fields: $B_{\rm void} \ge 10^{-16}\text{ G}$ on coherence scales $\lambda_B \ge 1\text{ Mpc}$. Meanwhile, CMB Faraday rotation constrains $B_{1\rm Mpc} \le 8 \times 10^{-10}\text{ G}$. Standard astrophysics cannot generate macroscopic magnetic fields in pristine voids devoid of galaxies or active galactic nuclei, requiring a magnetogenetic origin during electroweak phase transitions or inflation.

8. **Past-Geodesic Incompleteness and Initial Curvature Singularity:**
   The Borde-Guth-Vilenkin (BGV) theorem demonstrates that any spacetime with an average expansion rate $H_{\rm avg} > 0$ must be geodesically incomplete in past-directed null and timelike directions. Consequently, classical General Relativity terminates at an unphysical singularity ($R_{\mu\nu\rho\sigma} R^{\mu\nu\rho\sigma} \to \infty$, $\rho \to \infty$) at $t = 0$. Concordance cosmology is an incomplete infrared effective field theory that lacks a microscopic quantum gravity description of the initial state.

---

## 3. Definitive Registry of Open Problems & Decisive Resolving Observations

The eight core open problems of cosmogenesis are summarized below, each coupled to its explicit, quantitative resolving observational test:

| Problem ID | Genuine Open Problem | Concordance Failure / Gap | Decisive Resolving Observation | Decisive Instrument & Threshold |
|---|---|---|---|---|
| **OP-1** | **JWST Ultra-Early Structure Catastrophe** | $\Lambda\text{CDM}$ halo assembly at $z \ge 10$ requires $> 6.48\sigma$ Gaussian density fluctuations; observed galaxy density exceeds predictions by $10^3 - 10^4$. | Direct spectroscopic measurement of high-$z$ galaxy clustering and UV luminosity function turnover to measure dark matter halo occupancy and differentiate between extreme starbursts vs PBH seed accretion. | **JWST NIRSpec / Roman Space Telescope High-Latitude Survey**: Detection of rest-frame optical velocity dispersions $\sigma_v > 200\text{ km/s}$ at $z > 12$ or number density $\Phi(M_* > 10^{10} M_\odot, z=12) > 10^{-6}\text{ Mpc}^{-3}$ confirms non-Gaussianity/PBH origin. |
| **OP-2** | **Hubble Tension ($H_0$) & Growth Discordance ($S_8$)** | Reconciling $H_0$ requires $\Delta r_s = -11.37\text{ Mpc}$ ($7.73\%$ sound horizon reduction); EDE shifts $S_8$ to $0.852$, exacerbating KiDS/DES weak lensing tension to $> 4.2\sigma$. | Sub-percent tomographic cosmic shear cross-correlated with high-density Baryon Acoustic Oscillations across $0.2 < z < 3.5$. | **Euclid + Rubin Observatory (LSST) + DESI Year 5**: Joint constraints achieving $\sigma(S_8) \le 0.005$ and $\sigma(H_0) \le 0.3\text{ km/s/Mpc}$. A confirmed $S_8 < 0.77$ simultaneously with local $H_0 > 72.5$ rules out standard EDE in favor of decaying/interacting dark matter. |
| **OP-3** | **Spite Plateau Primordial Lithium-7 Discrepancy** | SBBN predicts $(^7\text{Li}/\text{H}) = 4.68 \times 10^{-10}$; halo dwarf stars observe $1.58 \times 10^{-10}$ ($9.16\sigma$ raw, $5.3\sigma$ post-diffusion tension). | High-precision isotopic abundance measurement of $^6\text{Li}/^7\text{Li}$ and $^7\text{Li}/\text{H}$ in pristine, zero-metallicity Pop III interstellar gas clouds at $z > 5$. | **ELT (Extremely Large Telescope) / ANDES Spectrograph**: Measuring $^7\text{Li}/\text{H}$ in pristine intergalactic absorbers. If $^7\text{Li}/\text{H} \approx 4.7 \times 10^{-10}$, the Spite plateau is proven to be stellar depletion; if $^7\text{Li}/\text{H} \approx 1.6 \times 10^{-10}$, non-standard BBN (supersymmetric decay or dark matter annihilation) is established. |
| **OP-4** | **Cosmic Dawn 21-cm Brightness Anomaly** | EDGES detects $\delta T_b = -500\text{ mK}$ at $z=17.2$, exceeding the standard adiabatic cooling floor ($-229\text{ mK}$) by a factor of $2.18$. | Radio-frequency global monopole and spatial fluctuation power spectrum measurement in a pristine, RFI-free lunar far-side environment. | **LuSEE-Night (Lunar Far-Side) / SKA1-Low**: Unambiguous sky-averaged spectrum between $50-100\text{ MHz}$. If $\delta T_b < -300\text{ mK}$ is confirmed, millicharged dark matter ($m_\chi \sim 10-100\text{ MeV}$, $q_\chi \sim 10^{-5} e$) or early radio synchrotron background is validated; if $\delta T_b \approx -200\text{ mK}$, EDGES is falsified as terrestrial systematic. |
| **OP-5** | **Primordial Non-Gaussianity & Inflation Architecture** | Standard single-field slow-roll enforces Maldacena bound $f_{\rm NL}^{\rm local} \approx 0.015$; multi-field and curvaton models produce $f_{\rm NL}^{\rm local} \ge 1$. | Scale-dependent galaxy bias in large-scale structure clustering at low wavenumber ($k \to 0$). | **SPHEREx + Euclid Galaxy Clustering**: Measuring scale-dependent bias with sensitivity $\sigma(f_{\rm NL}^{\rm local}) \le 0.5$. Detection of $f_{\rm NL}^{\rm local} \ge 1.0$ at $> 3\sigma$ conclusively falsifies ALL single-field slow-roll inflation. |
| **OP-6** | **Relic Neutrino Effective Degrees of Freedom ($N_{\rm eff}$)** | Standard Model specifies $N_{\rm eff} = 3.044$; light thermal relics decoupling prior to the top-quark mass shift $N_{\rm eff}$ by $\Delta N_{\rm eff} \ge 0.027$. | High-multipole ($\ell > 2500$) CMB damping tail temperature and polarization anisotropy measurements. | **CMB-S4 / Simons Observatory**: Forecasted precision $\sigma(N_{\rm eff}) = 0.03$. A detected shift $\Delta N_{\rm eff} \ge 0.06$ at $2\sigma$ identifies light dark radiation (sterile neutrinos or Goldstone axions) produced during cosmogenesis. |
| **OP-7** | **Primordial Magnetic Fields in Intergalactic Voids** | Fermi-LAT non-cascade bounds establish $B_{\rm void} \ge 10^{-16}\text{ G}$, requiring magnetogenesis prior to structure formation. | Rotation Measure (RM) cosmic grid tomography of millions of polarized extragalactic radio sources across unclustered cosmic voids. | **Square Kilometre Array (SKA) Faraday Rotation Grid**: SKA-MID will measure $> 10^7$ polarized RMs, achieving RMS precision $\sigma(\text{RM}) \le 1\text{ rad/m}^2$. A non-zero cosmic void RM confirms primordial inflation/EW magnetogenesis; an absence at $\sigma \ll 1\text{ rad/m}^2$ falsifies electrodynamic void seed theories. |
| **OP-8** | **Initial Curvature Singularity & Geodesic Incompleteness** | Classical General Relativity terminates at past curvature singularity (BGV theorem); lacks quantum gravity UV completion. | Primordial tensor-to-scalar ratio $r$ and tensor spectral index $n_t$ from degree-scale CMB B-mode polarization. | **LiteBIRD + CMB-S4**: Reaching sensitivity $\sigma(r) = 0.001$. Detection of $r > 0.003$ with $n_t = -r/8$ confirms standard high-energy inflation; detection of a blue tilt $n_t > 0$ or strict upper limit $r < 10^{-3}$ supports quantum bounce / ekpyrotic cosmologies. |

---

## 4. What Was Established, What Remains Unknown, and Falsification Criteria

### 4.1 What Has Been Established
1. The Hot Big Bang from $t \sim 0.1\text{ s}$ onward is verified beyond doubt by the CMB blackbody fidelity ($T_0 = 2.72548\text{ K}$, $|y| < 1.5 \times 10^{-5}$), light element nuclear synthesis ($Y_p = 24.5\%$, $X_p = 75.5\%$, $\text{D}/\text{H} = 2.55 \times 10^{-5}$), and universal metric expansion.
2. Concordance $\Lambda\text{CDM}$ cannot accommodate the observed high-$z$ galaxy overdensity from JWST, the $4.85\sigma$ Hubble tension, and the $S_8$ clustering discrepancy within a single consistent parameter set.
3. The Spite plateau ($^7\text{Li}/\text{H}$) represents an irreconcilable $9.16\sigma$ tension with SBBN unless stellar depletion mechanisms or exotic MeV-scale relic particle decays are introduced.

### 4.2 What Remains Unknown
1. Whether the initial state was a past-geodesically incomplete singular boundary ($t = 0$) or an asymptotically non-singular quantum bounce.
2. The microscopic mechanism responsible for the baryon asymmetry $\eta = (6.12 \pm 0.04) \times 10^{-10}$ (electroweak baryogenesis vs thermal/resonant leptogenesis).
3. The true origin of void magnetic fields ($B_{\rm void} \ge 10^{-16}\text{ G}$) and whether they originated during cosmological inflation or electroweak phase transitions.
4. Whether the EDGES 21-cm absorption feature ($-500\text{ mK}$) represents authentic early-universe millicharged dark matter interactions or an unaccounted instrumental systematic.

### 4.3 Evidence That Would Change My Mind (Falsification Thresholds)
- **Falsifying Single-Field Inflation:** If SPHEREx or Euclid establishes $f_{\rm NL}^{\rm local} > 1.0$ at $> 5\sigma$, the single-field slow-roll paradigm is irrevocably refuted.
- **Falsifying Standard Early Dark Energy:** If Euclid and Roman confirm that $S_8 \le 0.76$ while DESI BAO continues to favor $H_0 \approx 67.4\text{ km s}^{-1}\text{Mpc}^{-1}$ at high redshift, Early Dark Energy as a resolution to the Hubble tension is ruled out.
- **Falsifying Non-Standard BBN Lithium Depletion:** If the Extremely Large Telescope (ELT/ANDES) observes $(^7\text{Li}/\text{H}) = (4.68 \pm 0.30) \times 10^{-10}$ in zero-metallicity intergalactic gas at $z > 5$, any exotic particle physics explanation for the Spite plateau is falsified, proving that stellar atmospheric diffusion is solely responsible.
- **Falsifying Exotic Cosmic Dawn Cooling:** If lunar far-side radio radiometry (LuSEE-Night) measures the global 21-cm absorption trough at $\delta T_b \ge -230\text{ mK}$, the EDGES anomalous cooling is conclusively falsified as terrestrial or ionospheric contamination.
