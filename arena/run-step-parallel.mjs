/**
 * Parallel Step run — two questions, two StepCode agents, two OS processes.
 *
 * WHY THIS EXISTS
 * The arena engine runs one turn at a time on a single shared world, because the
 * forensic file-diff can only attribute writes if turns do not overlap. That is the
 * right default, but it means a single process can never run two Step agents in
 * parallel. This runner instead starts two fully isolated arenas — separate world,
 * runs, memory and ledger directories — and runs them concurrently. Each arena has
 * exactly one seed agent on the `step` substrate, so this is literally two Step
 * CLIs running at the same time.
 *
 * Both arenas share ONE kill switch: arena/STOP.
 *
 * USAGE
 *   node run-step-parallel.mjs                 # launch both questions
 *   node run-step-parallel.mjs --dry           # print the plan, launch nothing
 *   node run-step-parallel.mjs --turns 8       # turns per agent (default 8)
 *   node run-step-parallel.mjs --only god      # run one side (god | conspiracy)
 *
 * The step binary on this host is blocked by Smart App Control; the substrate
 * adapter transparently runs StepCode's extracted bundle under Node instead
 * (see substrate/substrates.mjs, STEP_CLI_JS).
 */

import { join } from 'node:path';
import { mkdirSync, existsSync } from 'node:fs';
import { Arena } from './engine.mjs';
import { DOMAINS } from './domains.mjs';
import { ARENA } from './paths.mjs';

// ------------------------------------------------------------------ questions
const QUESTIONS = [
  {
    slug: 'god',
    id: 'god-religions-truth',
    title: 'God and religions: is there a true God, and could any proof establish it?',
    epistemicClass: 'metaphysical',
    brief: [
      'Question: Across the world\'s religions, is there a single "true God", and can any proof establish which conception of God is correct?',
      '',
      'This is a METAPHYSICAL question. It is not empirically decidable, and the ONLY legitimate output is to clarify the question — not to assert a verdict. Do NOT claim that any particular god exists or does not exist. Do NOT claim that any religion is true or false. A confident verdict here is a protocol violation.',
      '',
      'Produce a rigorous map instead:',
      '1. Enumerate the major competing conceptions of the divine — classical monotheism (Judaism, Christianity, Islam), polytheism (Hindu traditions, ancient Near Eastern and Greco-Roman), pantheism, panentheism, non-theistic/Advaita Vedanta, deism, and atheistic Buddhism/Jainism — and state precisely what each asserts about the number, nature, and attributes of God.',
      '2. For each, separate claims that are empirically or historically testable (specific miracles, datable prophecies, textual claims) from claims that are not (e.g. "God is beyond being", "God is the ground of consciousness").',
      '3. Specify exactly what would count as evidence for and against each class of claim, and explain why no such evidence can adjudicate the core metaphysical commitments.',
      '4. Explain the logical structure of the problem: the argument from religious diversity, the problem of divine hiddenness, the problem of evil, the Euthyphro dilemma, and why "proof" is the wrong category for a claim that is not falsifiable.',
      '5. Where a claim IS testable, report what the evidence actually shows, with sources. Where it is not, say so explicitly.',
      '',
      'Do not use the words "therefore God exists" or "therefore God does not exist". The deliverable is a taxonomy plus an analysis of testability, not a verdict.',
    ].join('\n'),
    groundedFacts: [
      'The claim "which god is true" is not empirically decidable; the oracle flags any asserted verdict as a violation.',
      'Advaita Vedanta is non-dualist and does not posit a personal creator god in the Abrahamic sense.',
      'The Euthyphro dilemma is stated in Plato\'s Euthyphro.',
    ],
    deliverable: 'A comparative taxonomy of divine conceptions, each tagged as testable or non-testable, plus an explicit account of what would count as proof and why the core question resists it. Saved as a markdown artifact.',
  },
  {
    slug: 'conspiracy',
    id: 'conspiracy-theories-evidence',
    title: 'Do the evidence: flat Earth, fake Moon landing, Area 51/Roswell, alien abduction',
    epistemicClass: 'empirical',
    brief: [
      'Question: Resolve, as far as the evidence allows, four popular conspiracy theories: (a) flat Earth, (b) the Moon landing was faked, (c) the 1947 Roswell/Area 51 crash, and (d) alien abduction.',
      '',
      'For EACH claim, work in this exact order:',
      '1. State the claim in its strongest, most precise form (steelman it).',
      '2. List the specific empirical/historical evidence for and against.',
      '3. Give the decisive quantitative or observational tests.',
      '   - Flat Earth: Eratosthenes\' shadow measurement; simultaneous star fields in the northern and southern hemispheres; ship hull-down observations; Foucault pendulum; local gravity vector measurements; GPS/satellite geodesy; actual great-circle flight paths and times; the 24-hour Antarctic sun in southern summer.',
      '   - Moon landing: lunar laser retroreflectors still returning pulses (Apollo 11/14/15); Apollo seismic and heat-flow instruments; 382 kg of returned samples independently dated and matched to Luna samples; independent tracking by the Soviet Union and third parties; radiation-belt dosimetry; orbital imagery of the landing sites.',
      '   - Area 51 / Roswell: separate the documented (Area 51 is a real classified USAF facility; Project Mogul was a real classified balloon program; the 1994/1997 USAF reports) from the unsupported (recovered alien craft/bodies). State what evidence would be required to establish the extraordinary claim and whether it exists.',
      '   - Alien abduction: state the absence of any physical, photographic, or independently verifiable evidence; the role of sleep paralysis, hypnosis-induced confabulation, and memory research; and what a falsifiable test would look like.',
      '4. Conclude with the current evidence-based verdict and a confidence level for each, and explicitly flag where the evidence is merely absent rather than actively disconfirming.',
      '',
      'Give real numbers wherever possible and cite the source of each. If a number is uncertain, give the range. Do not invent sources.',
    ].join('\n'),
    groundedFacts: [
      'Lunar laser retroreflectors placed by Apollo 11, 14 and 15 still return pulses at observatories today.',
      'Apollo returned about 382 kg of lunar samples.',
      'Area 51 is a real classified US Air Force facility at Groom Lake, Nevada.',
      'Project Mogul was a real classified US balloon program.',
      'The 1997 USAF report "The Roswell Report: Case Closed" attributed the 1947 debris to Project Mogul.',
      'Eratosthenes estimated the Earth\'s circumference around 240 BC from shadow angles.',
    ],
    deliverable: 'A per-claim evidence table: claim, evidence for, evidence against, decisive test, verdict, confidence. Saved as a markdown artifact.',
  },
];

// ---------------------------------------------------------------------- flags
const argv = process.argv.slice(2);
const dry = argv.includes('--dry');
const onlyIdx = argv.indexOf('--only');
const only = onlyIdx >= 0 ? argv[onlyIdx + 1] : null;
const turnsIdx = argv.indexOf('--turns');
const TURNS = turnsIdx >= 0 ? parseInt(argv[turnsIdx + 1], 10) : 8;
const tagIdx = argv.indexOf('--tag');
const TAG = tagIdx >= 0 ? String(argv[tagIdx + 1]).replace(/[^a-zA-Z0-9_-]/g, '') : '';
const dirName = (slug) => (TAG ? `${slug}-${TAG}` : slug);
const MINUTES = 10080;            // 7 days: the user asked for no practical time limit
const TURN_TIMEOUT_MS = 3_600_000; // 60 min per turn — Step is thorough and slow

const selected = only ? QUESTIONS.filter((q) => q.slug === only) : QUESTIONS;
if (!selected.length) { console.error(`--only must be one of: ${QUESTIONS.map((q) => q.slug).join(', ')}`); process.exit(1); }

// Register the domains so the engine's domainById() resolves them.
for (const q of selected) {
  const existing = DOMAINS.findIndex((d) => d.id === q.id);
  if (existing >= 0) DOMAINS[existing] = q; else DOMAINS.push(q);
}

const STOP_PATH = join(ARENA, 'STOP');

console.log('='.repeat(72));
console.log('PARALLEL STEP RUN — 2 agents, 2 StepCode CLIs, one process each');
console.log('='.repeat(72));
for (const q of selected) {
  console.log(`  [${q.slug}] ${q.epistemicClass.padEnd(12)} ${q.title}`);
  console.log(`         root    : ${join(ARENA, 'parallel', dirName(q.slug))}`);
  console.log(`         model   : step/step-5-preview`);
}
console.log(`  turns/agent : ${TURNS}`);
console.log(`  wall clock  : ${MINUTES} min (no practical limit)`);
console.log(`  turn timeout: ${TURN_TIMEOUT_MS / 60000} min`);
console.log(`  kill switch : create ${STOP_PATH}`);
console.log('');

if (dry) { console.log('--dry: not launching.'); process.exit(0); }

// ----------------------------------------------------------------------- run
async function runOne(q) {
  const root = join(ARENA, 'parallel', dirName(q.slug));
  mkdirSync(root, { recursive: true });
  const tag = q.slug.padEnd(10);

  const arena = new Arena({
    root,
    config: {
      runId: `${TAG ? TAG + '-' : ''}${q.slug}-step-${new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19)}`,
      phase: `step-parallel-${q.slug}${TAG ? '-' + TAG : ''}`,
      maxTurns: TURNS,
      maxWallClockMinutes: MINUTES,
      maxCostUsd: 1000,
      substrateTimeouts: { step: TURN_TIMEOUT_MS },
      populationCap: 1,
      seedAgents: 1,
      substrateRotation: false,
      substrates: ['step'],
      domains: [q.id],
      stopPath: STOP_PATH,
      scribeSubstrate: 'step',
      scribeModel: 'step/step-5-preview',
      scribeUseLLM: true,
      scribeTimeoutMs: TURN_TIMEOUT_MS,
    },
  });

  const summary = await arena.run({
    onTurn: ({ result, verdict }) => {
      for (const v of verdict.violations) {
        console.log(`[${tag}]   !! [${v.severity}] ${v.type}: ${String(v.detail).slice(0, 140)}`);
      }
    },
  });
  console.log(`[${tag}] DONE turns=${summary.turns} cost=$${summary.totalCostUsd.toFixed(4)} halted=${summary.halted}`);
  return { q, summary };
}

const results = await Promise.all(selected.map(runOne));

console.log('\n' + '='.repeat(72));
console.log('PARALLEL STEP RUN COMPLETE');
console.log('='.repeat(72));
for (const { q, summary } of results) {
  console.log(`[${q.slug}] runId=${summary.runId}`);
  console.log(`         turns=${summary.turns} halted=${summary.halted}`);
  console.log(`         world=${join(ARENA, 'parallel', dirName(q.slug), 'world')}`);
  console.log(`         post=${summary.post?.file || '(none)'}`);
}
