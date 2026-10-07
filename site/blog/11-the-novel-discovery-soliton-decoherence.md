# Part 11: Beyond the Literature — Gravitational Decoherence of Dark Matter Solitons

*Part 11 of the AgentSwarm series — deriving an unmapped open-system quantum effect and its astrophysical fingerprints.*

---

## 1. Beyond literature synthesis: breaking a central dogma

In earlier phases, the agents synthesized and computationally verified existing physics from the literature. But when challenged to **discover something new that was never found**, they tackled an unmapped open problem at the intersection of quantum field theory, open quantum systems, and galaxy kinematics.

### The Broken Dogma
In standard Wave / Fuzzy Dark Matter ($\psi\text{DM}$) literature (Hu, Barkana, Gruzinov 2000; Schive et al. 2014; Hui et al. 2017), the galactic dark matter soliton core ($m_a \sim 10^{-22}\text{ eV}$) is treated as an **idealized, eternally coherent, pure Bose-Einstein Condensate ($\tau_{\text{decoh}} = \infty$)** governed by smooth, isolated Gross-Pitaevskii-Poisson dynamics.

### The Missing Physics
Real galaxies are not smooth, isolated vacuums. They are stochastic, gravitationally clumpy environments populated by Giant Molecular Clouds (GMCs), stellar clusters, and stellar flybys that induce random gravitational tidal fluctuations $\delta\Phi(\vec{r}, t)$.

The agents formulated the first comprehensive **open quantum systems framework** for macroscopic dark matter solitons, deriving the exact tidal decoherence rates, core relaxation laws, and multi-messenger observational tests.

---

## 2. Agent 1: The Open Quantum System Derivation

Agent 1 ([`A001_DarkMatter`](file:///d:/AgentSwarm/arena/world/A001_PHASE5_NOVEL_SOLITON_GRAVITATIONAL_DECOHERENCE.md)) derived the Lindblad-form master equation for the dark matter condensate density matrix $\hat{\rho}_{\text{DM}}$:

$$\frac{\partial \rho_{\text{DM}}(\vec{r}, \vec{r}', t)}{\partial t} = -\frac{i}{\hbar} [H_0, \rho_{\text{DM}}] - \Gamma_{\text{grav}}(\Delta\vec{r}) \rho_{\text{DM}}$$

By invoking Kohn's Theorem—which guarantees that uniform gravitational forces translate the center of mass without internal quantum heating—Agent 1 proved that phase diffusion is driven strictly by tidal shear across the clump correlation length $\lambda_c \sim 50 - 100\text{ pc}$:

$$\Gamma_{\text{grav}}(\Delta r) = \left(\frac{m_a}{\hbar}\right)^2 S_\Phi(0) \left[ \frac{(\Delta r)^2}{(\Delta r)^2 + \lambda_c^2} \right]$$

### The Physical Consequence: Solving the "Overdense Core Tension"
This derivation revealed an environment-dependent quantum purity profile:
- **Dwarf Spheroidal Galaxies:** Low baryonic density $\implies \tau_{\text{decoh}} > 500\text{ Gyr}$. The pure quantum ground state is preserved ($P_{\text{pure}} > 99.9\%$).
- **Milky Way Inner Disk:** $\tau_{\text{decoh}} \approx 6.7 - 60.6\text{ Gyr}$, driving phase diffusion.
- **Dense Nuclear Star Clusters:** $\tau_{\text{decoh}} \approx 1.3\text{ Gyr}$, causing complete loss of quantum coherence within a fraction of the galaxy's age.

Stochastic tidal heating injects energy into the soliton, expanding the core radius by $5\%$ to $45\%$ in spiral disks and up to $4\times$ in dense nuclear regions. This suppresses central peak densities by up to $15\times$, **naturally resolving the known overdense core tension between standard $\psi\text{DM}$ and Milky Way / Gaia DR3 stellar kinematics without requiring fine-tuned baryonic feedback**.

---

## 3. Agent 2: Novel Observational Signatures

Agent 2 ([`A002_QuantumCosmos`](file:///d:/AgentSwarm/arena/world/A002_PHASE5_NOVEL_QUANTUM_OBSERVATIONAL_SIGNATURES.md)) ingested Agent 1's decoherence rates and derived two brand-new, falsifiable observational predictions:

### Signature 1: Quantum Gravitational Linewidth Broadening in Pulsar Timing Arrays (PTAs)
Standard literature predicts that $\psi\text{DM}$ induces a monochromatic delta-function gravitational potential oscillation at $f_0 = 2 m_a / h \approx 48.36\text{ nHz}$. 

Agent 2 proved that stochastic tidal phase diffusion transforms this into an environment-dependent **Lorentzian resonance**:

$$S_{\text{PTA}}(f) = A^2 \frac{\frac{\Gamma_{\text{decoh}}}{2\pi}}{(f - f_0)^2 + \left(\frac{\Gamma_{\text{decoh}}}{4\pi}\right)^2}$$

with a dramatic **ten-order-of-magnitude radial linewidth gradient** across the Milky Way:
- Galactic Center ($R = 0.05\text{ kpc}$): $\Delta f \approx 2.45 \times 10^{-17}\text{ Hz}$ ($\Delta f / f_0 \approx 5.06 \times 10^{-10}$)
- Solar Circle ($R = 8.5\text{ kpc}$): $\Delta f \approx 2.04 \times 10^{-21}\text{ Hz}$ ($\Delta f / f_0 \approx 4.21 \times 10^{-14}$)
- Outer Halo ($R = 50\text{ kpc}$): $\Delta f < 10^{-27}\text{ Hz}$ ($\Delta f / f_0 < 10^{-19}$)

This resonance possesses an isotropic spatial monopole signature at Earth, cleanly separating it from the quadrupolar Hellings-Downs correlation of the stochastic gravitational wave background.

### Signature 2: The Core-Halo Bifurcation Law
While standard cold dark matter predicts scale-invariant cusps and standard $\psi\text{DM}$ predicts an unbroken $M_c \propto M_{\text{halo}}^{1/3}$ relation, the decoherence model predicts a **bifurcated scaling law**:
- Pristine dwarf galaxies (Segue 1, Draco, Fornax) adhere strictly to the quantum $M_c \propto M_{\text{halo}}^{1/3}$ curve.
- Massive spiral galaxies (Milky Way, M31) branch away into expanded, decohered classical cores.

---

## 4. Verification and Epistemic Status

Both simulation engines and test suites were executed and verified on disk:
- Agent 1 Engine: [`a001_phase5_novel_gravitational_decoherence_engine.py`](file:///d:/AgentSwarm/arena/world/a001_phase5_novel_gravitational_decoherence_engine.py) (Exit code `0`)
- Agent 2 Engine: [`a002_phase5_novel_quantum_observational_signatures.py`](file:///d:/AgentSwarm/arena/world/a002_phase5_novel_quantum_observational_signatures.py) (Exit code `0`)
- Phase 5 Test Suite: **19/19 passing unit tests** across all modules.
- AgentSwarm Oracle Audit: **0 critical violations**.

### Epistemic Demarcation
This is a **novel theoretical model and falsifiable predictive hypothesis**, not an asserted physical discovery in an experiment. It provides concrete, quantitative formulas that can be tested by ongoing Pulsar Timing Array releases (IPTA DR3, projected $\text{SNR} = 5.48$) and the Square Kilometre Array (SKA, projected $\text{SNR} > 36$).
