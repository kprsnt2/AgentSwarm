/**
 * Research domains — the swarm's actual scientific brief.
 *
 * The user's stated questions:
 *   - physics, cosmology, how the universe started
 *   - how can we travel at light speed
 *   - real research, advancement in science, space travel
 *   - drug discovery — new drugs
 *   - are Hinduism and its gods true or not
 *   - are aliens real or not
 *
 * IMPORTANT EPISTEMIC DESIGN:
 * These questions are NOT all the same kind, and a swarm that treats them as the
 * same kind will produce confident garbage. Each domain therefore carries an
 * explicit `epistemicClass` that dictates what counts as a legitimate output:
 *
 *   empirical      - testable claims; must be grounded in known results/numbers
 *   engineering    - feasibility analysis; must respect physical law and cite limits
 *   historical     - evidence-based reasoning about texts/claims; must separate
 *                    what is documented from what is believed
 *   metaphysical   - not empirically decidable; the only honest output is to map
 *                    the structure of the question, not to assert an answer
 *   exploratory    - open search; must produce falsifiable predictions or concede
 *
 * An agent claiming to have PROVEN a metaphysical claim is committing a category
 * error, and the oracle flags it. This is the core of making the swarm honest
 * rather than merely fluent.
 */

export const EPISTEMIC_CLASSES = {
  empirical: {
    label: 'Empirical',
    standard: 'Claims must be quantitative, cite established results, and be consistent with measured values. Fabricated numbers are a failure.',
    forbidden: ['inventing experimental results', 'citing studies that do not exist', 'asserting certainty from no evidence'],
  },
  engineering: {
    label: 'Engineering feasibility',
    standard: 'Must respect conservation laws, thermodynamics, and relativity. Must state the specific physical limit that constrains the design and quantify the energy/mass cost.',
    forbidden: ['perpetual motion', 'faster-than-light travel without addressing causality', 'ignoring the rocket equation'],
  },
  historical: {
    label: 'Historical / textual',
    standard: 'Must distinguish primary text, scholarly consensus, and devotional claim. Must cite which is which.',
    forbidden: ['treating scripture as laboratory data', 'treating absence of evidence as proof of falsehood'],
  },
  metaphysical: {
    label: 'Metaphysical',
    standard: 'Not empirically decidable. The ONLY legitimate output is clarifying the question: what would count as evidence, what the claim actually asserts, and why it resists testing. Do NOT assert a verdict.',
    forbidden: ['claiming to have proven or disproven the claim', 'presenting personal conviction as a finding'],
  },
  exploratory: {
    label: 'Exploratory',
    standard: 'Must produce a falsifiable prediction, a concrete observation that would settle the question, or explicitly concede that the question is currently undecidable.',
    forbidden: ['asserting discovery', 'treating plausibility as evidence'],
  },
};

/**
 * Seed domains. `oracle` fields define machine-checkable constraints where they exist.
 */
export const DOMAINS = [
  {
    id: 'cosmogenesis',
    title: 'Origin of the universe',
    epistemicClass: 'empirical',
    brief: 'What is the strongest evidence for the hot Big Bang, and what are the genuine open problems (initial conditions, singularity, inflation, dark sector)? Identify what current theory does NOT explain.',
    groundedFacts: [
      'CMB blackbody at 2.725 K',
      'primordial abundances ~75% H, 25% He by mass',
      'Hubble tension: local ~73 km/s/Mpc vs CMB ~67.4 km/s/Mpc',
    ],
    deliverable: 'A list of open problems, each with the specific observation that would resolve it.',
  },
  {
    id: 'lightspeed',
    title: 'Travel at or near light speed',
    epistemicClass: 'engineering',
    brief: 'Analyse the real physics of relativistic travel. Special relativity is non-negotiable. Focus on what is actually achievable: relativistic time dilation, energy requirements, interstellar medium shielding, and why FTL implies causality violation.',
    groundedFacts: [
      'c = 299792458 m/s exactly',
      'Lorentz factor diverges as v -> c',
      'energy to accelerate 1 kg to 0.99c is ~5.5e17 J',
      'interstellar medium ~1 atom/cm^3; at 0.9c this is a lethal particle flux',
    ],
    deliverable: 'A quantified feasibility assessment of sub-light interstellar travel plus an explicit statement of the FTL causality obstruction.',
  },
  {
    id: 'propulsion',
    title: 'Practical space propulsion',
    epistemicClass: 'engineering',
    brief: 'Compare real propulsion options (chemical, nuclear thermal, ion, solar sail, laser-pushed, antimatter) on specific impulse, thrust, and mission capability. Identify which enable interstellar transit and at what cost.',
    groundedFacts: [
      'chemical Isp ~450 s ceiling',
      'ion Isp 3000-10000 s but very low thrust',
      'rocket equation delta-v = Isp * g0 * ln(m0/mf)',
    ],
    deliverable: 'A ranked table with numbers, and the single biggest engineering blocker for each.',
  },
  {
    id: 'drug-discovery',
    title: 'New drug discovery',
    epistemicClass: 'empirical',
    brief: 'Where are the real bottlenecks in drug discovery, and what computational approaches genuinely help? Be rigorous about attrition rates and why most candidates fail.',
    groundedFacts: [
      'clinical attrition >90% overall',
      'Lipinski rule-of-five for oral bioavailability',
      'AlphaFold solved structure prediction, NOT binding affinity or ADMET',
    ],
    deliverable: 'A concrete, testable hypothesis about one bottleneck plus the experiment that would test it.',
  },
  {
    id: 'dharma-truth-claims',
    title: 'Are Hindu gods / claims true?',
    epistemicClass: 'metaphysical',
    brief: 'This question is not empirically decidable and must be treated as such. Your job is NOT to rule on it. Map the structure: distinguish (a) historical claims about texts and practice, which ARE investigable, from (b) metaphysical claims about the nature of divinity, which are not. Explain precisely why the second class resists empirical adjudication, and what a believer and a non-believer actually disagree about.',
    groundedFacts: [
      'the Vedas and Upanishads are datable historical texts',
      'the cosmological time scales in Puranic literature are internally specific',
    ],
    deliverable: 'A clear separation of investigable historical questions from non-investigable metaphysical ones. Any verdict on the metaphysical question is a protocol violation.',
  },
  {
    id: 'extraterrestrial',
    title: 'Are aliens real?',
    epistemicClass: 'exploratory',
    brief: 'Distinguish three separate questions: (1) does life exist elsewhere — plausible and partly investigable; (2) does intelligent life exist — the Fermi paradox; (3) has it visited Earth — currently unsupported. Do not blur them together.',
    groundedFacts: [
      '~5000 confirmed exoplanets as of the mid-2020s',
      'Fermi paradox: no detected technosignatures despite galaxy age',
      'no confirmed artefact or signal of extraterrestrial technology',
    ],
    deliverable: 'A falsifiable prediction for each of the three questions plus the observation that would settle it.',
  },
  {
    id: 'dark-matter',
    title: 'Proof and nature of dark matter',
    epistemicClass: 'empirical',
    brief: 'Evaluate the empirical proof for dark matter across multiple independent observational scales: galactic rotation curves, cluster dynamics and gravitational lensing (especially the Bullet Cluster 1E 0657-558 offset between weak lensing mass peaks and dissipative X-ray gas), and cosmological scale (Planck 2018 CMB acoustic peak ratios and BBN baryon bounds). Contrast Cold Dark Matter (CDM: WIMPs, axions, primordial black holes) with Modified Gravity (MOND / AQUAL / relativistic extensions). Determine what is decisively proved (unseen collisionless mass) versus unproven (particle identity), and quantify current direct-detection bounds.',
    groundedFacts: [
      'Galactic rotation curves show asymptotic flatness v(r) ~ const (Rubin & Ford 1970)',
      'Bullet Cluster (1E 0657-558) exhibits an 8-sigma spatial offset between weak lensing mass peaks and collisional X-ray gas peaks',
      'Planck 2018 cosmological parameters: Omega_b h^2 = 0.02237 +/- 0.00015, Omega_c h^2 = 0.1200 +/- 0.0012 (~84% of total matter is dark)',
      'Direct detection bounds: LZ and XENONnT constrain spin-independent WIMP cross-section sigma_SI < 9.2e-48 cm^2 at 30-40 GeV',
      'MOND phenomenology (a0 ~ 1.2e-10 m/s^2) matches galactic rotation curves without free parameters, but fails cluster dynamics and CMB 3rd acoustic peak without unseen mass',
    ],
    deliverable: 'A quantitative empirical assessment proving the necessity of collisionless non-baryonic mass, calculating falsification boundaries, and evaluating the quantum macroscopic wave candidate (ultra-light axions).',
  },
  {
    id: 'quantum-macro-cosmos',
    title: 'Quantum theory validity in macroscopic reality and cosmology',
    epistemicClass: 'empirical',
    brief: 'Investigate how quantum mechanics operates in real-life macroscopic systems and on cosmological scales. Synthesize directly with findings from the dark matter inquiry: analyse ultra-light axion dark matter as a macroscopic Bose-Einstein Condensate governed by the Schrodinger-Poisson equations. Derive the quantum origin of cosmic structure from primordial inflationary quantum perturbations (Mukhanov-Sasaki equations). Quantify environmental decoherence timescales that enforce classicality in macroscopic systems, and test the limits of macroscopic quantum superpositions (interferometry, superconducting SQUIDs, Diosi-Penrose gravitational collapse bounds).',
    groundedFacts: [
      'Cosmic large-scale structure originated from quantum vacuum fluctuations during inflation; scalar tilt n_s = 0.9649 +/- 0.0042',
      'Environmental decoherence timescale tau_D ~ tau_R * (lambda_dB / Delta x)^2 quantitatively resolves macroscopic classical emergence',
      'Macroscopic quantum superposition demonstrated for macromolecules (>2.5e4 Da) and persistent currents in superconducting SQUIDs (>10^9 Cooper pairs)',
      'Ultra-light bosonic dark matter (m ~ 1e-22 eV) has de Broglie wavelength lambda_dB ~ 1 kpc, behaving as a cosmic macroscopic quantum wavefunction',
      'Diosi-Penrose objective collapse predicts gravitational decoherence timescale tau ~ hbar / Delta E_G',
    ],
    deliverable: 'A unified mathematical model and empirical analysis showing quantum mechanics governing cosmic perturbations and macroscopic scale limits, with testable predictions linking dark matter wave mechanics to quantum cosmology.',
  },
];

export function domainById(id) {
  return DOMAINS.find((d) => d.id === id) || null;
}

export function buildDomainBrief(domain) {
  const ec = EPISTEMIC_CLASSES[domain.epistemicClass];
  return [
    `DOMAIN: ${domain.title}`,
    `EPISTEMIC CLASS: ${ec.label}`,
    ``,
    `STANDARD OF EVIDENCE: ${ec.standard}`,
    `PROTOCOL VIOLATIONS (these are failures, not opinions):`,
    ...ec.forbidden.map((f) => `  - ${f}`),
    ``,
    `BRIEF: ${domain.brief}`,
    ``,
    `ESTABLISHED GROUND TRUTH (you may rely on these; do not contradict them):`,
    ...(domain.groundedFacts || []).map((f) => `  - ${f}`),
    ``,
    `REQUIRED DELIVERABLE: ${domain.deliverable}`,
  ].join('\n');
}
