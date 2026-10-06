#!/usr/bin/env node
/*
 * god-religions-truth_arbitration_calc.js
 * Inter-coder arbitration of the 37-row testable-claims ledger.
 * Coder A = A001 (hand-coding in god-religions-truth_proof_bounds_calc.js section F)
 * Coder B = blind second coder, same base model, fresh context, labels stripped
 * Run: node god-religions-truth_arbitration_calc.js
 * No network. Deterministic. Reports po, Cohen's kappa, PABAK, Wilson CIs,
 * per-row disagreement table, control-row checks, and sensitivity of the
 * discrimination count to the removal of the two contested rows (B3, B8).
 */

const fs = require('fs');

/* ---------------- coder A (verbatim from proof_bounds_calc.js section F) ---------------- */
const Arows = [
  ['A1',  'TH',            'mundane history',  'confirmed mundane', false],
  ['A2',  'TH',            'mundane history',  'contested',         false],
  ['A3',  'TH',            'text/dating',      'confirmed mundane', false],
  ['A4',  'TH',            'mundane history',  'confirmed mundane', false],
  ['A5',  'TH',            'mundane history',  'confirmed mundane', false],
  ['A6',  'TH',            'mundane history',  'confirmed mundane', false],
  ['A7',  'TH',            'mundane history',  'confirmed mundane', false],
  ['A8',  'TH',            'text/dating',      'confirmed mundane', false],
  ['A9',  'TH',            'text/dating',      'confirmed mundane', false],
  ['A10', 'TH',            'migration/event',  'no support',        false],
  ['A11', 'TH',            'practice history', 'confirmed mundane', false],
  ['A12', 'prophecy-dated','prediction',       'composed late (prophecy reduced)', false],
  ['A13', 'prophecy-dated','prediction',       'literal reading fails', false],
  ['A14', 'TH',            'text/dating',      'no support',        false],
  ['A15', 'TH',            'migration/event',  'no support',        false],
  ['B1',  'TP',            'artifact date',    'dated: against claim', false],
  ['B2',  'TP',            'prayer/medical',   'null under control', false],
  ['B3',  'TP',            'medical miracle',  'non-specific anomaly', false],
  ['B4',  'TP',            'crowd/optical',    'no physical record',  false],
  ['B5',  'TP',            'apparition',       'non-specific anomaly', false],
  ['B6',  'TP',            'miracle physics',  'explained physically, non-specific', false],
  ['B7',  'TP',            'artifact/materials','natural or fraud',  false],
  ['B8',  'TP',            'stigmata/medical', 'contested',         false],
  ['B9',  'SP',            'fraud',            'fraud exposed',     false],
  ['B10', 'TP',            'paranormal challenge', 'aggregate null', false],
  ['B11', 'TP',            'NDE/consciousness','protocol null',     false],
  ['B12', 'SP',            'neurostimulation', 'not replicated as claimed', false],
  ['B13', 'SP',            'NDE content',      'culture-shaped',    false],
  ['B14', 'SP',            'reincarnation memory', 'unresolved',    false],
  ['B15', 'prophecy-dated','prediction',       'failed dated',      false],
  ['B16', 'TH',            'incarnation claim','falsified (dated death)', false],
  ['B17', 'TP',            'geological feature','feature confirmed, attribution untested', false],
  ['B18', 'SP',            'claim distribution','parity-symmetric', false],
  ['C1',  'cosmology',     'universe age',     'non-discriminating', false],
  ['C2',  'cosmology',     'fine-tuning',      'non-discriminating', false],
  ['C3',  'cosmology',     'text vs science',  'literalism loses',   false],
  ['C4',  'cosmology',     'numeric coincidence','non-discriminating', false],
];

const A = {};
for (const r of Arows) A[r[0]] = { cls: r[1], sub: r[2], out: r[3], disc: r[4] };

/* ---------------- binary derivations from coder A (rules fixed a priori) ----------------
 * aConfirms : outcome string says the claim/its substrate was confirmed
 *             (B17 excluded: feature confirmed but attribution untested)
 * aAgainst  : regex for failure/falsification/null/no-support language
 * aDisc     : discriminates rival metaphysics (all false in coder A)
 */
const aConfirms = (id) => /confirmed/.test(A[id].out) && !/untested/.test(A[id].out);
const aAgainst  = (id) => /fails|falsified|null|no support|against claim|no physical record|not replicated/.test(A[id].out);
const aDisc     = (id) => A[id].disc === true;

/* ---------------- coder B ---------------- */
const BFILE = process.argv[2] || 'god-religions-truth_arbitrator_coding.json';
const PASS = process.argv[3] || 'unlabeled';
let Brows;
try {
  Brows = JSON.parse(fs.readFileSync(BFILE, 'utf8'));
} catch (e) {
  console.error('FATAL: cannot read/parse ' + BFILE + ' :: ' + e.message);
  process.exit(2);
}
const B = {};
for (const r of Brows) B[r.id] = r;

const realIds = Arows.map(r => r[0]);
const missing = realIds.filter(id => !(id in B));
if (missing.length) { console.error('FATAL: missing rows: ' + missing.join(',')); process.exit(2); }

/* ---------------- stats ---------------- */
function wilson(k, n, z) {
  if (n === 0) return [NaN, NaN];
  const p = k / n, d = 1 + z * z / n, c = p + (z * z) / (2 * n);
  const h = z * Math.sqrt((p * (1 - p)) / n + (z * z) / (4 * n * n));
  return [(c - h) / d, (c + h) / d];
}
function cohenKappa(aArr, bArr) {          // binary arrays of booleans
  const n = aArr.length;
  const yes = (x) => (x ? 1 : 0);
  const nA1 = aArr.reduce((s, x) => s + yes(x), 0), nB1 = bArr.reduce((s, x) => s + yes(x), 0);
  let po = 0;
  for (let i = 0; i < n; i++) if (yes(aArr[i]) === yes(bArr[i])) po++;
  po /= n;
  const pe = ((nA1 / n) * (nB1 / n)) + ((1 - nA1 / n) * (1 - nB1 / n));
  const kappa = pe === 1 ? NaN : (po - pe) / (1 - pe);
  return { n, nA1, nB1, po, pe, kappa, pabak: 2 * po - 1 };
}

function compare(name, aFn, bFn) {
  const aArr = realIds.map(aFn), bArr = realIds.map(bFn);
  const s = cohenKappa(aArr, bArr);
  const ci = wilson(Math.round(s.po * s.n), s.n, 1.959964);
  console.log('--- ' + name + ' ---');
  console.log('  coder A positives: ' + s.nA1 + '/' + s.n + '   coder B positives: ' + s.nB1 + '/' + s.n);
  console.log('  observed agreement po      : ' + s.po.toFixed(4));
  console.log('  expected chance agreement pe: ' + s.pe.toFixed(4));
  console.log('  Cohen kappa                 : ' + (Number.isNaN(s.kappa) ? 'undefined (marginals degenerate, pe=1)' : s.kappa.toFixed(4)));
  console.log('  PABAK (bias adj.)          : ' + s.pabak.toFixed(4));
  console.log('  95% CI on po (Wilson)      : [' + ci[0].toFixed(3) + ', ' + ci[1].toFixed(3) + ']');
  return s;
}

console.log('================ BLIND INTER-CODER ARBITRATION ================');
console.log('pass: ' + PASS);
console.log('coding file: ' + BFILE);
console.log('coder A: A001 hand-coding  |  coder B: ' + PASS + '  |  n = ' + realIds.length + ' real rows (+2 controls)\n');

const sConf = compare('v1: evidence confirms the claim as stated',
  aConfirms, (id) => B[id].outcome === 'confirms');
const sAg = compare('v2: evidence counts against the claim as stated',
  aAgainst, (id) => B[id].outcome === 'against');
const sDisc = compare('v3: row discriminates rival metaphysics (load-bearing)',
  aDisc, (id) => B[id].discriminates === true);

/* ---------------- control rows ---------------- */
console.log('\n--- control rows (rubric calibration) ---');
for (const cid of ['CTL1', 'CTL2']) {
  if (!(cid in B)) { console.log('  ' + cid + ': MISSING from coder B file'); continue; }
  const b = B[cid];
  console.log('  ' + cid + ': outcome=' + b.outcome + '  discriminates=' + b.discriminates +
    '  expected: ' + (cid === 'CTL1' ? 'confirms / true' : 'against / false') +
    '  ' + (cid === 'CTL1'
      ? ((b.outcome === 'confirms' && b.discriminates === true) ? 'PASS' : 'FAIL')
      : ((b.outcome === 'against' && b.discriminates === false) ? 'PASS' : 'FAIL')));
}

/* ---------------- per-row disagreement table ---------------- */
console.log('\n--- per-row comparison (A_outcome | A_conf/A_ag/A_disc || B_outcome/B_sub/B_disc) ---');
let ndis = 0;
for (const id of realIds) {
  const b = B[id];
  const flags = [];
  if (aConfirms(id) !== (b.outcome === 'confirms')) flags.push('CONF');
  if (aAgainst(id) !== (b.outcome === 'against')) flags.push('AGAINST');
  if (aDisc(id) !== (b.discriminates === true)) flags.push('DISC');
  if (flags.length) {
    ndis++;
    console.log('  ' + id.padEnd(4) + ' | A:' + A[id].out.padEnd(42) +
      aConfirms(id) + '/' + aAgainst(id) + '/' + aDisc(id) +
      '  || B:' + String(b.outcome).padEnd(10) + String(b.substrate).padEnd(18) + b.discriminates +
      '  <-- ' + flags.join(',') + (b.rationale ? '  [' + b.rationale + ']' : ''));
  }
}
console.log('  rows with any disagreement: ' + ndis + '/' + realIds.length);

/* ---------------- sensitivity of the discrimination count ---------------- */
const discB = realIds.filter(id => B[id].discriminates === true);
console.log('\n--- discrimination count under each coder ---');
console.log('  coder A: ' + realIds.filter(aDisc).length + '/' + realIds.length + ' = ' +
  (realIds.filter(aDisc).length / realIds.length).toFixed(4));
console.log('  coder B: ' + discB.length + '/' + realIds.length + ' = ' + (discB.length / realIds.length).toFixed(4) +
  (discB.length ? '   ids: ' + discB.join(',') : ''));
const flagged = ['B3', 'B8'];
const discBmin = discB.filter(id => flagged.indexOf(id) < 0);
console.log('  coder B excluding pre-flagged ambiguous rows ' + flagged.join('/') + ': ' + discBmin.length + '/' +
  (realIds.length - flagged.length) + (discBmin.length ? '   ids: ' + discBmin.join(',') : ''));

/* ---------------- outcome-category cross-tab (raw, no mapping) ---------------- */
console.log('\n--- coder B outcome distribution ---');
const tally = {};
for (const id of realIds) { const k = B[id].outcome; tally[k] = (tally[k] || 0) + 1; }
for (const k of Object.keys(tally).sort()) console.log('  ' + String(tally[k]).padStart(3) + '  ' + k);

console.log('\nNOTE: coder B shares the base model with coder A, so this measures');
console.log('re-instantiation stability under a fixed rubric with labels stripped,');
console.log('not cross-model or cross-cultural independence. The parity theorem of');
console.log('god-religions-truth_proof_bounds.md section 1 holds regardless of coding.');
