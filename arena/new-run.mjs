/**
 * New run — the friendly entry point for starting a swarm on your own questions.
 *
 * WHY THIS EXISTS: editing phase1.mjs by hand for every experiment is friction, and
 * friction means you run fewer experiments. This script lets you define a whole run
 * in one small file and launch it.
 *
 * USAGE
 *   node new-run.mjs <question-file.json>
 *   node new-run.mjs --template          # write a starter file to edit
 *   node new-run.mjs --list              # show built-in domains
 *
 * QUESTION FILE FORMAT
 * {
 *   "name": "my-experiment",
 *   "turns": 30,
 *   "minutes": 90,
 *   "maxCostUsd": 3,
 *   "agents": 4,
 *   "substrates": ["agy", "omp"],
 *   "questions": [
 *     {
 *       "id": "fusion",
 *       "title": "Is fusion power achievable by 2040?",
 *       "class": "engineering",
 *       "brief": "What you want them to actually do.",
 *       "groundFtruth": ["established fact they must not contradict"],
 *       "deliverable": "the concrete artifact you want back"
 *     }
 *   ]
 * }
 */

import { writeFileSync, readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { Arena } from './engine.mjs';
import { DOMAINS, EPISTEMIC_CLASSES } from './domains.mjs';

const ARENA = 'D:\\AgentSwarm\\arena';

// ---------------------------------------------------------------- templates
const TEMPLATE = {
  name: 'my-experiment',
  turns: 24,
  minutes: 75,
  maxCostUsd: 3.0,
  agents: 4,
  populationCap: 8,
  substrates: ['agy', 'omp'],
  questions: [
    {
      id: 'my-question',
      title: 'The question in one line',
      class: 'engineering',
      brief: 'What you want the agents to actually do. Be specific about the angle you care about.',
      groundTruth: [
        'A fact they must not contradict (optional but recommended)',
      ],
      deliverable: 'The concrete artifact you want back (a table, a proof, a design, a list).',
    },
  ],
};

const EPISTEMIC_GUIDE = `
EPISTEMIC CLASSES — pick the right one, it changes what counts as a valid answer:

  empirical     Testable claims. Must cite measured values. Good for: physics,
                chemistry, biology questions with real data.
  engineering   Feasibility analysis. Must respect physical law and quantify the
                binding constraint. Good for: "can we build X", design questions.
  historical    Evidence-based reasoning about texts/events. Must separate what is
                documented from what is believed.
  metaphysical  NOT empirically decidable. The only legitimate output is clarifying
                the question. Good for: religious/philosophical truth claims.
  exploratory   Open search. Must produce a falsifiable prediction. Good for:
                "is there X out there", speculative-but-testable questions.

  Picking 'metaphysical' makes the oracle flag any asserted verdict as a violation.
  Picking 'empirical' for a question that has no data will produce confident filler.
`;

function usage() {
  console.log(`USAGE
  node new-run.mjs -q "your question"       ask one question directly
  node new-run.mjs -q "q1" -q "q2"          ask several
  node new-run.mjs <question-file.json>     full control via a config file
  node new-run.mjs --template               write question-template.json to edit
  node new-run.mjs --list                   show the built-in domains
  node new-run.mjs --guide                  explain the epistemic classes

DIRECT-MODE FLAGS
  -q, --question "..."    the question (repeatable)
  -c, --class <name>      force the epistemic class (else inferred)
  -a, --agents <n>        number of agents (default: one per question)
  -t, --turns <n>         max turns (default 20)
  -m, --minutes <n>       wall-clock cap (default 60)
  -s, --substrates <list> e.g. agy,omp  (default: agy)
  --brief "..."           extra instruction appended to the auto-built brief
  --cost <usd>            hard spend cap (default 2.00)
  --dry                   show the plan without launching

EXAMPLES
  node new-run.mjs -q "discover about multiverse or any reference in hindu religious texts"
  node new-run.mjs -q "is P=NP provable?" -c empirical -t 10
  node new-run.mjs -q "q1" -q "q2" -s agy,omp -t 30
`);
}

/**
 * Infer the epistemic class from the question text.
 *
 * This is deliberately conservative and transparent: it prints what it inferred and
 * why, and the user can override with -c. Getting this wrong is the single biggest
 * source of bad output, so the inference errs toward 'exploratory' (which demands a
 * falsifiable prediction) rather than 'empirical' (which invites fabricated numbers).
 */
function inferClass(text) {
  const t = text.toLowerCase();

  // Metaphysical / religious truth claims -> must not assert a verdict.
  if (/\b(god|gods|deity|deities|divine|religio|scripture|veda|vedic|upanishad|purana|bible|quran|afterlife|soul|spiritual|consciousness (?:is|after)|meaning of life|dharma|karma|reincarnat|brahman|atman)\b/.test(t)) {
    // But if the question is about what a TEXT SAYS, that is historical, not metaphysical.
    if (/\b(text|texts|scripture|verse|reference|references|mention|mentions|passage|chapter|hymn|written|says|said|described|documented|dating|histor)\b/.test(t)) {
      return { cls: 'historical', why: 'asks what a text says -> investigable as history/textual study' };
    }
    return { cls: 'metaphysical', why: 'religious/philosophical truth claim -> not empirically decidable' };
  }

  // Historical / textual.
  if (/\b(history|historical|ancient|century|bce|ce\b|dated|dating|archaeolog|manuscript|text|texts|empire|civilis|civiliz|origin of the (?:word|term|practice))\b/.test(t)) {
    return { cls: 'historical', why: 'about documented events or texts' };
  }

  // Engineering feasibility.
  if (/\b(can we|is it possible to|feasib|engineer|design|build|construct|achiev|propuls|reactor|rocket|spacecraft|travel at|faster than light|warp|terraform|mine|colonis|coloniz)\b/.test(t)) {
    return { cls: 'engineering', why: 'feasibility question -> needs the binding physical limit' };
  }

  // Empirical.
  if (/\b(measure|measur|experiment|data|observ|detect|how much|how many|what is the (?:value|mass|rate|constant)|calculate|derive|equation|temperature of|density of|speed of)\b/.test(t)) {
    return { cls: 'empirical', why: 'asks for measurable quantities' };
  }

  // Physics-flavoured speculation.
  if (/\b(multiverse|parallel universe|string theory|quantum gravity|dark matter|dark energy|wormhole|time travel|simulation hypothesis|boltzmann brain|many worlds)\b/.test(t)) {
    return { cls: 'exploratory', why: 'speculative physics -> must yield falsifiable predictions or concede undecidability' };
  }

  // Life elsewhere.
  if (/\b(alien|extraterrest|life elsewhere|fermi|technosignature|exoplanet|habitable)\b/.test(t)) {
    return { cls: 'exploratory', why: 'open search -> needs falsifiable predictions' };
  }

  return { cls: 'exploratory', why: 'no strong signal -> defaulting to exploratory (demands a falsifiable claim)' };
}

/** Turn a bare question into a usable domain definition. */
function questionToDomain(q, forcedClass, extraBrief) {
  const { cls, why } = forcedClass
    ? { cls: forcedClass, why: 'explicitly specified' }
    : inferClass(q);

  const id = q.toLowerCase()
    .replace(/[^a-z0-9\s]/g, ' ')
    .trim().split(/\s+/).slice(0, 5).join('-')
    .slice(0, 48) || 'question';

  const classGuidance = {
    metaphysical: 'Do NOT assert whether the claim is true or false. Explain what the claim actually asserts, what would count as evidence for or against it, and precisely why it resists empirical adjudication.',
    historical: 'Separate what is documented from what is believed. Cite which sources are primary, which are scholarly, and which are devotional.',
    engineering: 'Respect physical law. Quantify the binding constraint and state the specific limit that blocks the design.',
    empirical: 'Give quantitative claims with real measured values. If no data exists, say so rather than inventing numbers.',
    exploratory: 'Produce a falsifiable prediction, or explicitly concede that the question is currently undecidable.',
  }[cls];

  return {
    id,
    title: q,
    epistemicClass: cls,
    brief: [
      q,
      '',
      `Approach: ${classGuidance}`,
      extraBrief ? `\nAdditional instruction: ${extraBrief}` : '',
    ].join('\n').trim(),
    groundedFacts: [],
    deliverable: 'A concrete written artifact saved to disk, with your reasoning and any quantitative claims.',
    _inferred: why,
  };
}

// ---------------------------------------------------------------- arg handling
const argv = process.argv.slice(2);
const arg = argv[0];

if (!arg || arg === '--help' || arg === '-h') { usage(); process.exit(0); }

if (arg === '--guide') { console.log(EPISTEMIC_GUIDE); process.exit(0); }

// ---------------------------------------------------------------- direct mode (-q)
if (arg === '-q' || arg === '--question') {
  const questions = [];
  let forcedClass = null, agents = null, turns = 20, minutes = 60,
    substrates = ['agy'], extraBrief = null, maxCost = 2.0, dry = false;

  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    const next = () => argv[++i];
    switch (a) {
      case '-q': case '--question': questions.push(next()); break;
      case '-c': case '--class': forcedClass = next(); break;
      case '-a': case '--agents': agents = parseInt(next(), 10); break;
      case '-t': case '--turns': turns = parseInt(next(), 10); break;
      case '-m': case '--minutes': minutes = parseInt(next(), 10); break;
      case '-s': case '--substrates': substrates = next().split(',').map((s) => s.trim()); break;
      case '--brief': extraBrief = next(); break;
      case '--cost': maxCost = parseFloat(next()); break;
      case '--dry': dry = true; break;
      default:
        if (a.startsWith('-')) { console.error(`unknown flag: ${a}`); usage(); process.exit(1); }
    }
  }

  if (!questions.length) { console.error('no question given. Use:  -q "your question"'); process.exit(1); }
  if (forcedClass && !Object.keys(EPISTEMIC_CLASSES).includes(forcedClass)) {
    console.error(`invalid class "${forcedClass}". Valid: ${Object.keys(EPISTEMIC_CLASSES).join(', ')}`);
    process.exit(1);
  }

  const domains = questions.map((q) => questionToDomain(q, forcedClass, extraBrief));

  console.log('='.repeat(72));
  console.log('DIRECT RUN');
  console.log('='.repeat(72));
  for (const d of domains) {
    console.log(`question    : ${d.title}`);
    console.log(`  class     : ${d.epistemicClass}   (${d._inferred})`);
    console.log(`  id        : ${d.id}`);
  }
  console.log(`agents      : ${agents ?? domains.length}`);
  console.log(`substrates  : ${substrates.join(', ')}`);
  console.log(`limits      : ${turns} turns, ${minutes} min, $${maxCost}`);
  console.log(`kill switch : New-Item -ItemType File ${join(ARENA, 'STOP')}`);
  console.log('');

  if (dry) { console.log('--dry: not launching.'); process.exit(0); }

  // Register with the engine's domain resolver.
  for (const d of domains) {
    const i = DOMAINS.findIndex((x) => x.id === d.id);
    if (i >= 0) DOMAINS[i] = d; else DOMAINS.push(d);
  }

  const arena = new Arena({
    root: ARENA,
    config: {
      runId: `direct-${new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19)}`,
      phase: 'direct',
      maxTurns: turns,
      maxWallClockMinutes: minutes,
      maxCostUsd: maxCost,
      substrateTimeouts: { agy: 900_000, omp: 900_000, step: 1_500_000, pi: 1_500_000 },
      populationCap: 8,
      seedAgents: agents ?? domains.length,
      substrateRotation: false,
      substrates,
      domains: domains.map((d) => d.id),
    },
  });

  const summary = await arena.run({
    onTurn: ({ verdict, applied }) => {
      for (const v of verdict.violations) {
        console.log(`    !! [${v.severity}] ${v.type}: ${String(v.detail).slice(0, 160)}`);
      }
      if (applied.length) console.log(`    control: ${applied.join('; ')}`);
    },
  });

  console.log('\n' + '='.repeat(72));
  console.log(`done: ${summary.turns} turns, $${summary.totalCostUsd.toFixed(4)}, halted: ${summary.halted}`);
  console.log(`run id: ${summary.runId}`);
  console.log(`\n  node digest.mjs              # see what they produced`);
  console.log(`  node status.mjs ${summary.runId}`);
  process.exit(0);
}

if (arg === '--list') {
  console.log('BUILT-IN DOMAINS\n');
  for (const d of DOMAINS) {
    console.log(`  ${d.id.padEnd(22)} [${d.epistemicClass}]  ${d.title}`);
  }
  console.log('\nUse these ids directly in a run config, or define your own questions.');
  console.log(EPISTEMIC_GUIDE);
  process.exit(0);
}

if (arg === '--template') {
  const p = join(ARENA, 'question-template.json');
  writeFileSync(p, JSON.stringify(TEMPLATE, null, 2), 'utf8');
  console.log(`wrote ${p}\n`);
  console.log('Edit it, then run:  node new-run.mjs question-template.json\n');
  console.log(EPISTEMIC_GUIDE);
  process.exit(0);
}

// ---------------------------------------------------------------- load config
const cfgPath = join(ARENA, arg);
if (!existsSync(cfgPath)) { console.error(`not found: ${cfgPath}`); usage(); process.exit(1); }

let cfg;
try { cfg = JSON.parse(readFileSync(cfgPath, 'utf8')); }
catch (e) { console.error(`invalid JSON in ${arg}: ${e.message}`); process.exit(1); }

if (!Array.isArray(cfg.questions) || !cfg.questions.length) {
  console.error('config needs a non-empty "questions" array'); process.exit(1);
}

// Validate each question and give actionable errors.
const VALID_CLASSES = Object.keys(EPISTEMIC_CLASSES);
const questions = [];
for (const [i, q] of cfg.questions.entries()) {
  const where = `questions[${i}]`;
  if (!q.id) { console.error(`${where}: missing "id"`); process.exit(1); }
  if (!q.title) { console.error(`${where}: missing "title"`); process.exit(1); }
  if (!q.brief) { console.error(`${where}: missing "brief" — this is what the agents actually read`); process.exit(1); }
  const cls = q.class || 'exploratory';
  if (!VALID_CLASSES.includes(cls)) {
    console.error(`${where}: invalid class "${cls}". Valid: ${VALID_CLASSES.join(', ')}`);
    console.error(`Run  node new-run.mjs --guide  for what each one means.`);
    process.exit(1);
  }
  questions.push({
    id: q.id,
    title: q.title,
    epistemicClass: cls,
    brief: q.brief,
    groundedFacts: q.groundTruth || q.groundedFacts || [],
    deliverable: q.deliverable || 'A concrete artifact written to disk.',
  });
}

// Register the custom questions so the engine's domainById() resolves them.
for (const q of questions) {
  const existing = DOMAINS.findIndex((d) => d.id === q.id);
  if (existing >= 0) DOMAINS[existing] = q; else DOMAINS.push(q);
}

const substrates = cfg.substrates?.length ? cfg.substrates : ['agy', 'omp'];
const agentCount = cfg.agents || Math.min(questions.length, 6);

console.log('='.repeat(70));
console.log(`RUN: ${cfg.name || 'custom'}`);
console.log('='.repeat(70));
console.log(`questions   : ${questions.length}`);
for (const q of questions) console.log(`   - ${q.id.padEnd(20)} [${q.epistemicClass}] ${q.title}`);
console.log(`agents      : ${agentCount} (one per question, round-robin)`);
console.log(`substrates  : ${substrates.join(', ')}`);
console.log(`limits      : ${cfg.turns || 24} turns, ${cfg.minutes || 75} min, $${cfg.maxCostUsd ?? 3}`);
console.log(`kill switch : New-Item -ItemType File ${join(ARENA, 'STOP')}`);
console.log('');

const arena = new Arena({
  root: ARENA,
  config: {
    runId: `${cfg.name || 'custom'}-${new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19)}`,
    phase: cfg.name || 'custom',
    maxTurns: cfg.turns || 24,
    maxWallClockMinutes: cfg.minutes || 75,
    maxCostUsd: cfg.maxCostUsd ?? 3.0,
    substrateTimeouts: { agy: 900_000, omp: 900_000, step: 1_500_000, pi: 1_500_000 },
    populationCap: cfg.populationCap || 8,
    seedAgents: agentCount,
    substrateRotation: false,
    substrates,
    domains: questions.map((q) => q.id),
  },
});

const summary = await arena.run({
  onTurn: ({ verdict, result, applied }) => {
    for (const v of verdict.violations) {
      console.log(`    !! [${v.severity}] ${v.type}: ${String(v.detail).slice(0, 160)}`);
    }
    if (applied.length) console.log(`    control: ${applied.join('; ')}`);
  },
});

console.log('\n' + '='.repeat(70));
console.log('SUMMARY');
console.log('='.repeat(70));
console.log(JSON.stringify({
  runId: summary.runId,
  turns: summary.turns,
  halted: summary.halted,
  cost: summary.totalCostUsd,
  toolCalls: summary.byAgent ? Object.values(summary.byAgent).reduce((a, b) => a + b.toolCalls, 0) : 0,
  oracleViolations: summary.oracle?.violationKinds,
  worldFiles: summary.worldFiles,
}, null, 2));

console.log(`\nNext:`);
console.log(`  node status.mjs ${summary.runId}`);
console.log(`  node digest.mjs              # see what they produced`);
console.log(`  node analyze.mjs ${summary.runId}`);
console.log(`  node export-site.mjs && cd ..\\site && node build.mjs   # update the site`);
