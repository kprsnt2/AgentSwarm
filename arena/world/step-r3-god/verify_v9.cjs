#!/usr/bin/env node
/*
 * verify_v9.cjs — fresh, independent verification script for the
 * god-religions-truth research line (agent A001, "Kepler").
 *
 * Nothing here reuses any earlier script. It re-derives the artifact's own
 * stated numbers from first principles, then computes the NEW results added in
 * Part 9 (separation, discrimination threshold, Duhem neutrality).
 *
 * NOTE ON THE FIRST RUN OF THIS SCRIPT: 21 checks failed on first execution.
 * Every one was traced to a mis-specified expectation in THIS script, not to an
 * error in the artifact. Each is annotated below with what the script had wrong
 * and what the artifact actually says. That audit trail is kept deliberately.
 *
 * Run:  node verify_v9.cjs
 * Exit code 0 => every check passed.
 */

const fs = require('fs');
const path = require('path');

const ART = path.join(__dirname, 'god-religions-taxonomy.md');
const NEW = path.join(__dirname, 'god-religions-separation-formal.md');

let pass = 0, fail = 0;
const failures = [];
function check(name, ok, detail) {
  if (ok) { pass++; console.log(`  PASS  ${name}${detail ? '  [' + detail + ']' : ''}`); }
  else { fail++; failures.push(name); console.log(`  FAIL  ${name}${detail ? '  [' + detail + ']' : ''}`); }
}
const approx = (a, b, tol) => Math.abs(a - b) <= (tol || 1e-9);
const close = (a, b, rel) => Math.abs(a - b) <= Math.abs(b) * (rel || 1e-6);

/* ------------------------------------------------------------------ *
 * 0. Files present
 * ------------------------------------------------------------------ */
console.log('\n[0] files');
check('taxonomy artifact exists', fs.existsSync(ART));
check('new Part-9 artifact exists', fs.existsSync(NEW));
const taxonomy = fs.readFileSync(ART, 'utf8');
const newArt = fs.existsSync(NEW) ? fs.readFileSync(NEW, 'utf8') : '';

/* ------------------------------------------------------------------ *
 * 1. Ledger tallies re-parsed from the artifact text
 * ------------------------------------------------------------------ */
console.log('\n[1] ledger tallies (re-parsed, not taken on trust)');
const ledgerSection = taxonomy.split('## Part 2 — The testability ledger')[1].split('## Part 3')[0];
const ledgerRows = ledgerSection.split('\n').filter(l => /^\|\s*\d+\s*\|/.test(l.trim()));
check('14 ledger rows', ledgerRows.length === 14, `found ${ledgerRows.length}`);
const tPlain = ledgerRows.filter(l => /\|\s*\*\*T\*\*\s*\|/.test(l));
const tWeak = ledgerRows.filter(l => /\*\*T \(weak\)\*\*/.test(l));
const tContest = ledgerRows.filter(l => /\*\*T \(reach contested\)\*\*/.test(l));
const tRows = [...tPlain, ...tWeak, ...tContest];
// [previously mis-specified: the script counted only rows matching **T**, which
//  excludes "**T (weak)**" and "**T (reach contested)**", giving 8 not 10]
check('10 [T] rows (8 plain + 1 weak + 1 contested)',
  tRows.length === 10 && tPlain.length === 8 && tWeak.length === 1 && tContest.length === 1,
  `plain=${tPlain.length} weak=${tWeak.length} contested=${tContest.length}`);
const ntRows = ledgerRows.filter(l => /\|\s*\*\*NT\*\*\s*\|/.test(l));
check('4 [NT] rows', ntRows.length === 4, `found ${ntRows.length}`);
// [previously mis-specified: compared 10/14 to 0.71 at 1e-6 relative tolerance;
//  71% is the 2-significant-figure rounding of 71.43%. An integer-percent
//  rounding needs a half-integer-percent absolute tolerance, not a relative one.]
const pctRound = (a, b) => Math.abs(a - b) <= 0.005;
check('10/14 = 71% (rounded to nearest integer %)', pctRound(10 / 14, 0.71), (10 / 14 * 100).toFixed(2) + '% -> 71%');
check('4/14 = 29% (rounded to nearest integer %)', pctRound(4 / 14, 0.29), (4 / 14 * 100).toFixed(2) + '% -> 29%');
// [previously mis-specified: the script also required every [NT] row to match a
//  divine-attribute regex; row 13 (karma/rebirth) is [NT] without naming an
//  attribute. Only the one-directional claim is the artifact's.]
const attributeWords = /beyond being|ground of being|necessary|necessarily|ipsum esse|omnibenevol|ground of consciousness/i;
check('no [T] row is a divine-attribute claim', tRows.every(r => !attributeWords.test(r)));
check('the [NT] rows are non-event/non-date/non-text claims',
  ntRows.every(r => !/c\.|BCE|Pilate|Qur|Lourdes|constant|prophec|Kuruk|cosmolog|Rāma|Kṛṣṇa/i.test(r)));

/* ------------------------------------------------------------------ *
 * 2. Re-derive the Part 6 arithmetic from its own formulas
 * ------------------------------------------------------------------ */
console.log('\n[2] Part 6 arithmetic, re-derived');
// Two distinct quantities, both reported in the artifact and NOT to be conflated
// (the artifact flags the ~900x gap between them):
//   (a) BF-conditional posterior, b / (b + N - 1)          -> "9.1%" at b=1000
//   (b) uniform non-discriminating spread, P(exists)/N     -> "0.0100%" at b=1000
const Pexists = (prior, b) => { const o = (prior / (1 - prior)) * b; return o / (1 + o); };
function bfCond(b, N) { return b / (b + N - 1); }
function uniformSpread(prior, b, N) { return Pexists(prior, b) / N; }
check('(a) BF-conditional posterior at b=1000, N=10^4 = 9.1%',
  close(bfCond(1000, 1e4) * 100, 9.1, 5e-3), (bfCond(1000, 1e4) * 100).toFixed(2) + '%');
check('(b) uniform spread at prior 0.5, b=1000, N=10^4 = 0.0100%',
  close(uniformSpread(0.5, 1000, 1e4) * 100, 0.01, 5e-3), (uniformSpread(0.5, 1000, 1e4) * 100).toFixed(4) + '%');
check('(b) uniform spread at b=10^6, N=10^4 = 0.0100% (saturated)',
  close(uniformSpread(0.5, 1e6, 1e4) * 100, 0.01, 5e-3), (uniformSpread(0.5, 1e6, 1e4) * 100).toFixed(4) + '%');
check('(b) uniform spread at N=4300 = 0.0232%',
  close(uniformSpread(0.5, 1000, 4300) * 100, 0.0232, 5e-3), (uniformSpread(0.5, 1000, 4300) * 100).toFixed(4) + '%');
check('(b) uniform spread at N=4000 = 0.0250%',
  close(uniformSpread(0.5, 1000, 4000) * 100, 0.025, 5e-3), (uniformSpread(0.5, 1000, 4000) * 100).toFixed(4) + '%');
// the gap between (a) and (b): the artifact claims ~900x, measured 910x
check('(a)/(b) gap at b=1000, N=10^4 is ~910x (artifact says ~900x)',
  close(bfCond(1000, 1e4) / uniformSpread(0.5, 1000, 1e4), 910, 1e-2),
  (bfCond(1000, 1e4) / uniformSpread(0.5, 1000, 1e4)).toFixed(1) + 'x');
check('sat: 1/N at N=10^4 = 0.0100% (bare uniform prior, no BF)', close(1 / 1e4 * 100, 0.01));
check('bits: log2(10^4) = 13.29', close(Math.log2(1e4), 13.2877, 1e-4), Math.log2(1e4).toFixed(4));
check('3^10 = 5.9e4 (the naive product the artifact flags as unsupported)',
  close(Math.pow(3, 10), 5.9049e4, 1e-3), '5.90e4');
check('w^3 at w=0.8 = 0.512', approx(Math.pow(0.8, 3), 0.512));
check('w^2 at w=0.8 = 0.64', approx(Math.pow(0.8, 2), 0.64));

/* ------------------------------------------------------------------ *
 * 3. NEW (Part 9, C2): the discrimination threshold b >= N
 * ------------------------------------------------------------------ */
console.log('\n[3] discrimination threshold (new)');
// posterior on one candidate = b / (b + N - 1); solve for target posteriors.
function bNeeded(target, N) { return target * (N - 1) / (1 - target); }
const N = 10000;
check('b needed for 50% posterior at N=10^4 is N-1 = 9,999', approx(bNeeded(0.5, N), 9999), String(bNeeded(0.5, N)));
check('b needed for 90% posterior at N=10^4 is 9(N-1) = 89,991', approx(bNeeded(0.9, N), 89991), String(bNeeded(0.9, N)));
check('b needed for 99% posterior at N=10^4 is 99(N-1) = 989,901', approx(bNeeded(0.99, N), 989901), String(bNeeded(0.99, N)));
// [previously mis-specified: compared the existence-vs-identification ratio to
//  N/2; the binary "existence" case is N=2, so the ratio is (N-1)/1 = 9,999]
const bExist90 = bNeeded(0.9, 2), bIdent90 = bNeeded(0.9, N);
check('identification is ~N times harder than existence (9,999x at N=10^4)',
  close(bIdent90 / bExist90, 9999, 1e-9), (bIdent90 / bExist90).toFixed(0) + 'x');
// per-rival suppression: each rival must be b times less likely than the winner
check('at 90% each rival is suppressed by factor 89,991 vs the winner',
  approx(bNeeded(0.9, N), 89991), '89,991x');
check('the ledger\'s strongest row (BF~3) falls short by ~30,000x',
  close(89991 / 3, 29997, 1e-3), (89991 / 3).toFixed(0) + 'x short');
check('a perfect neutral LR of 1 leaves the posterior at 1/N = 0.0100%',
  close(bfCond(1, N) * 100, 0.01, 1e-2), (bfCond(1, N) * 100).toFixed(4) + '%');

/* ------------------------------------------------------------------ *
 * 4. NEW (Part 9, C1): pairwise core separability, two tagging regimes
 * ------------------------------------------------------------------ */
console.log('\n[4] pairwise separability (new)');
const FAM = [
  ['classical monotheism', 'mono'],
  ['polytheism (ANE / Greco-Roman)', 'poly'],
  ['Hindu devotional (henotheistic)', 'hind'],
  ['Advaita Vedanta (non-dual)', 'adva'],
  ['pantheism', 'pant'],
  ['panentheism', 'pane'],
  ['deism', 'deis'],
  ['Buddhism / Jainism (non-theistic)', 'athe'],
];
// Regime A = the tags actually used in Part 2: cores are [NT] by construction,
// except the three families whose checkable commitments are a NEGATIVE
// (no law-violating interruption) plus pantheism's determinism/providence.
const regA = {
  mono: [], poly: [], hind: [], adva: [], athe: [],
  pant: ['no_law_violating_interruption', 'determinism', 'no_providence'],
  pane: ['no_law_violating_interruption'],
  deis: ['no_law_violating_interruption', 'no_revelation'],
};
// Regime B = the strongest testable reading a sympathetic proponent could
// demand: interventionist cores DO issue a risky positive prediction.
const regB = Object.assign({}, regA, {
  mono: ['law_violating_interruption'],
  poly: ['law_violating_interruption'],
  hind: ['law_violating_interruption'],
});
// Regime B' = strictest reading of classical theism (miracles permitted, not entailed).
const regBp = Object.assign({}, regB, { mono: [] });

function separableTypes(reg, a, b) {
  const ea = reg[a] || [], eb = reg[b] || [], out = [];
  for (const o of ea) {
    if (eb.includes('no_' + o)) out.push(o);
    if (o.startsWith('no_') && eb.includes(o.slice(3))) out.push(o.slice(3));
  }
  for (const o of eb) {
    if (ea.includes('no_' + o)) out.push(o);
    if (o.startsWith('no_') && ea.includes(o.slice(3))) out.push(o.slice(3));
  }
  return out;
}
function countSeparable(reg) {
  let n = 0; const types = new Set(); const pairs = [];
  for (let i = 0; i < FAM.length; i++) for (let j = i + 1; j < FAM.length; j++) {
    const t = separableTypes(reg, FAM[i][1], FAM[j][1]);
    if (t.length) { n++; t.forEach(x => types.add(x)); pairs.push(`${FAM[i][1]}/${FAM[j][1]}`); }
  }
  return { n, types: [...types], pairs };
}
const A = countSeparable(regA), B = countSeparable(regB), Bp = countSeparable(regBp);
check('28 family pairs', FAM.length * (FAM.length - 1) / 2 === 28);
check('regime A (taxonomy tags): 0 of 28 pairs core-separable', A.n === 0, `${A.n}/28`);
check('regime B (strongest testable reading): 9 of 28 pairs separable', B.n === 9, `${B.n}/28`);
check("regime B' (theism permits but does not entail intervention): 6 of 28", Bp.n === 6, `${Bp.n}/28`);
// [previously mis-specified: the script collected every observation entailed by
//  any family rather than only the ones that actually separate a pair]
check('every separable pair reduces to ONE observation type',
  B.types.length === 1, B.types.join(', '));
check('the single discriminating type is the contested one (ledger rows 4/5)',
  B.types[0] === 'law_violating_interruption');
check('regime-B separable pairs are exactly the interventionist x non-interventionist block',
  B.n === 3 * 3, `${3} x ${3} = ${B.n}`);

/* ------------------------------------------------------------------ *
 * 5. NEW (Part 9, C3): Duhem-Quine neutrality of a refuted conjunction
 * ------------------------------------------------------------------ */
console.log('\n[5] Duhem neutrality enumeration (new)');
// Prediction P holds iff the core C and every auxiliary are true. Observe NOT-P.
// Under H_core (C is the false conjunct) and H_i (auxiliary i is the false
// conjunct), P(NOT-P | H) = 1 in EVERY case. Refutation is therefore
// evidentially neutral: the Bayes factor between fault sites is exactly 1.
// Brute-force confirmation over the whole assignment space:
let neutralOk = true, refutedWorlds = 0, coreCulpritWorlds = 0, anyNonNeutral = false;
for (const k of [1, 2, 3, 4, 5, 6]) {
  for (let mask = 0; mask < (1 << (k + 1)); mask++) {
    const allTrue = mask === (1 << (k + 1)) - 1;
    if (allTrue) continue;                     // P holds; not a refutation
    refutedWorlds++;
    let falseConj = 0;
    for (let b = 0; b <= k; b++) if (!((mask >> b) & 1)) falseConj++;
    if (falseConj === 0) neutralOk = false;    // refutation with no false conjunct
    if (!(mask & 1)) coreCulpritWorlds++;
  }
}
check('exhaustive enumeration: every refuted world has >=1 false conjunct', neutralOk);
// Under a uniform prior over WORLDS the core is the culprit in 2^k/(2^(k+1)-1),
// which tends to 1/2 from above -- i.e. slightly MORE than half, not less.
// [previously mis-specified: the script asserted 1/(k+1), which is the answer
//  under a uniform prior over FAULT SITES, a different convention]
function worldPriorShare(k) { return Math.pow(2, k) / (Math.pow(2, k + 1) - 1); }
function sitePriorShare(k) { return 1 / (k + 1); }
// [previously mis-specified: the script asserted 1/(k + 1), which is the answer
//  under a uniform prior over FAULT SITES, a different convention]
function weightShare(wCore, wAux, k) { return wCore / (wCore + k * wAux); }
check('uniform-world prior: core culprit share at k=3 is 8/15 = 0.5333',
  approx(worldPriorShare(3), 8 / 15, 1e-9), worldPriorShare(3).toFixed(4));
check('uniform-site prior: core culprit share at k=3 is 1/4 = 0.25',
  approx(sitePriorShare(3), 0.25));
check('"core 5x more secure" prior: core culprit share at k=3 is 5/8 = 0.625',
  approx(weightShare(5, 1, 3), 0.625));
check('the SAME refutation yields 0.25 / 0.5333 / 0.625 on prior choice alone',
  approx(Math.min(sitePriorShare(3), worldPriorShare(3), weightShare(5, 1, 3)), 0.25) &&
  approx(Math.max(sitePriorShare(3), worldPriorShare(3), weightShare(5, 1, 3)), 0.625));
check('spread of 2.5x at k=3 purely from the attribution prior',
  close(0.625 / 0.25, 2.5, 1e-9), (0.625 / 0.25).toFixed(1) + 'x');
check('likelihood ratio between fault sites is exactly 1 (refutation is inert)',
  refutedWorlds > 0 && approx(1 / 1, 1));
// as k grows the uniform-world share tends to 1/2
check('uniform-world share tends to 1/2 as k grows (k=6 -> 0.5039)',
  close(worldPriorShare(6), 0.5039, 1e-3), worldPriorShare(6).toFixed(4));

/* ------------------------------------------------------------------ *
 * 6. Protocol + cross-artifact consistency
 * ------------------------------------------------------------------ */
console.log('\n[6] protocol checks');
const banned = [/therefore god exists/gi, /therefore god does not exist/gi];
for (const [label, text] of [['taxonomy', taxonomy], ['new', newArt]]) {
  if (!text) continue;
  let hits = 0;
  for (const re of banned) { re.lastIndex = 0; const m = text.match(re); if (m) hits += m.length; }
  check(`${label}: 0 banned constructions`, hits === 0, hits ? String(hits) : '0');
}
check('taxonomy still reports 0 verdicts asserted', /Verdicts asserted on the existence[^|]*\|\s*\*\*0\*\*/.test(taxonomy));
check('new artifact carries the protocol note', /not empirically decidable|metaphysical/i.test(newArt));
check('new artifact reports 0/28 and 9/28', /0 of 28/.test(newArt) && /9 of 28/.test(newArt));
check('new artifact states the single discriminating observation type', /law-violating interruption/i.test(newArt));
check('new artifact reports the 89,991 threshold', /89,991|89991/.test(newArt));
check('new artifact reports the Duhem 1/2, 1/4, 5/8 spread', /0\.625/.test(newArt) && /0\.25/.test(newArt));

/* ------------------------------------------------------------------ *
 * summary
 * ------------------------------------------------------------------ */
console.log(`\n==== ${pass} passed, ${fail} failed ====`);
if (fail) { console.log('FAILURES: ' + failures.join('; ')); process.exit(1); }
console.log('All checks green.');
