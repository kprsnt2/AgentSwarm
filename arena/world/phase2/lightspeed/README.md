# Relativistic Interstellar Flight & FTL Causality Engine (`lightspeed`)

**Agent**: Kepler (A001, Generation 0)  
**Domain**: Travel at or near light speed (`lightspeed`)  
**Epistemic Class**: Engineering feasibility under Special Relativity, Thermodynamics, and Conservation Laws.

---

## 1. Overview

The `lightspeed` engine (`lightspeed_engine.py`) provides a machine-checkable, quantitative feasibility assessment of sub-light relativistic interstellar flight and a rigorous mathematical proof of the Faster-Than-Light (FTL) causality obstruction.

The module exposes the standard contract function:
```python
def analyze() -> dict:
    ...
```
returning a dictionary containing:
- `domain`: `"lightspeed"`
- `claims`: list of quantitative scientific findings and physical bounds.
- `confidence`: float in `[0.0, 1.0]` (quantified at `0.99`).
- `evidence`: list of auditable evidence records with `kind`, `value`, and `source`.

---

## 2. Core Physical Findings and Governing Laws

### A. Special Relativity Mechanics & Ground Truth
- **Speed of Light**: $c = 299,792,458\text{ m/s}$ (exact SI definition).
- **Lorentz Factor**: $\gamma = 1 / \sqrt{1 - \beta^2}$ diverges asymptotically as $\beta \to 1$.
- **Kinetic Energy Ground Truth**:
  $$E_k = (\gamma - 1) m c^2$$
  Accelerating $1\text{ kg}$ of payload to $\beta = 0.99$ ($\gamma \approx 7.0888$) requires:
  $$E_k \approx 5.474 \times 10^{17}\text{ J} \approx 5.5 \times 10^{17}\text{ J}$$
  This matches established empirical and theoretical ground truth, exceeding the entire annual primary electrical generation of industrial nations for even a modest probe.

### B. Relativistic Rocket Equation & Mass Ratio Prohibition
For onboard rocket systems, momentum conservation in special relativity dictates:
$$R = \frac{m_0}{m_f} = \left(\frac{1 + \beta}{1 - \beta}\right)^{\frac{c}{2 u_{ex}}}$$
- **D-T Fusion ($u_{ex} = 0.05c$)**:
  - Reaching $\beta = 0.1c$: $R \approx 7.44$.
  - Reaching $\beta = 0.9c$ (one-way): $R \approx 6.13 \times 10^{12}\text{ kg fuel / kg payload}$.
  - Reaching $\beta = 0.9c$ with deceleration: $R_{total} = R^2 \approx 3.76 \times 10^{25}\text{ kg fuel / kg payload}$, exceeding the mass of the Earth ($5.97 \times 10^{24}\text{ kg}$).
- **Conclusion**: Onboard chemical, fission, and fusion systems are strictly excluded from relativistic velocities ($\beta > 0.1c$). High sub-light travel ($\beta \sim 0.1\text{--}0.2c$) is physically viable *only* via beamed momentum systems (directed laser lightsails) where reaction mass is not carried onboard.

### C. Thermal Radiator Acceleration Clamping
Onboard antimatter and nuclear engines generate intense waste heat:
$$\frac{P_{waste}}{F} = \frac{f_{waste} c^2}{w_{exhaust}} \approx 41.64\text{ MW / N}$$
Radiative heat rejection governed by the Stefan-Boltzmann law ($q = 2 \epsilon \sigma T_{rad}^4$) at $T_{rad} = 1800\text{ K}$ with $\sigma_{panel} = 5.0\text{ kg/m}^2$ requires a radiator mass of:
$$\frac{M_{rad}}{F} \approx 194.3\text{ kg / N}$$
This clamps the maximum possible engine acceleration (even with zero payload and structural mass) to:
$$a_{max} = \frac{F}{M_{rad}} \approx 0.00515\text{ m/s}^2 \approx 5.25 \times 10^{-4}\text{ g}_0$$
At this acceleration, reaching $\beta = 0.2c$ requires **380 years** of continuous burn over **38 light-years**, ruling out onboard antimatter rocketry for human-timescale exploration.

### D. Interstellar Medium (ISM) Lethal Particle Flux
The interstellar medium ($n_{ISM} \approx 10^6\text{ protons/m}^3$):
- At $\beta = 0.9c$:
  - Incoming proton kinetic energy: $E_p \approx 1.214\text{ GeV}$.
  - Proton flux: $\Phi \approx 2.70 \times 10^{14}\text{ protons / (m}^2\text{ s)}$.
  - Continuous energy flux: $P_{flux} \approx 52.5\text{ kW / m}^2$.
- At $\beta = 0.99c$, power flux reaches $\approx 271.7\text{ kW / m}^2$ with $5.7\text{ GeV}$ protons, causing devastating spallation, atomic lattice displacement, and lethal ionization penetrating several meters of solid material.

### E. FTL Causality Obstruction (Tachyonic Antitelephone)
In Minkowski spacetime, the Lorentz transformation of a temporal interval between space-like separated events ($x = v_{FTL} t$) under boost velocity $v_{boost}$ is:
$$t' = \gamma_{boost} \left(t - \frac{v_{boost} x}{c^2}\right) = \gamma_{boost} t \left(1 - \frac{v_{boost} v_{FTL}}{c^2}\right)$$
- If $v_{boost} v_{FTL} > c^2$, then $t' < 0$.
- In frame $S'$, the signal arrives before it is emitted. By reflecting the signal via a symmetric FTL link in frame $S'$, the return signal arrives in frame $S$ at coordinate time $\Delta t_{total} < 0$, creating closed timelike curves (CTCs) and enabling grandfather paradoxes.
- Therefore, within Lorentz-invariant physics, faster-than-light travel or signaling is mathematically equivalent to time travel into the past, violating causality.

---

## 3. Test Suite Verification

The engine is paired with `test_lightspeed_engine.py`, containing 8 distinct verification methods:
1. `test_analyze_contract_schema`: Validates schema structure, dictionary keys, confidence bounds, and types.
2. `test_special_relativity_lorentz_gamma`: Validates $\gamma(\beta)$ asymptotic behavior and boundary domain restrictions.
3. `test_relativistic_kinetic_energy_ground_truth`: Validates $5.474 \times 10^{17}\text{ J/kg}$ at $0.99c$ matching ground truth, plus low-velocity Newtonian correspondence.
4. `test_relativistic_rocket_equation_mass_ratios`: Validates exponential mass ratios ($R > 10^{12}$ and $R^2 > 3.7 \times 10^{25}$ for fusion).
5. `test_interstellar_medium_lethal_flux`: Validates ISM proton energy ($1.21\text{ GeV}$) and power flux ($52.5\text{ kW/m}^2$) at $0.9c$.
6. `test_thermal_radiator_acceleration_limits`: Validates Raman's $41.64\text{ MW/N}$ waste heat and $194.3\text{ kg/N}$ radiator mass clamping $a_{max} < 0.0006\text{ g}_0$.
7. `test_ftl_tachyonic_antitelephone_causality_obstruction`: Validates negative time coordinates ($t' < 0$) and CTC formation when $v_{boost} v_{FTL} > c^2$.
8. `test_time_dilation_and_momentum_consistency`: Validates relativistic momentum and time dilation consistency.

---

## 4. Execution & Verification

Run the test suite:
```bash
python test_lightspeed_engine.py
```

Run the engine module:
```bash
python lightspeed_engine.py
```
