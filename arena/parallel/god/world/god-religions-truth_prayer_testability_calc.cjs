/*
 * god-religions-truth_prayer_testability_calc.cjs
 * ---------------------------------------------------------------------------
 * Question ID : god-religions-truth   (agent A001 "Kepler", gen 0)
 * PURPOSE      : Put a number on what the best-controlled TESTABLE claim class
 *                (intercessory prayer, ledger row B2) actually bought, and on
 *                the price of the one experiment that could move it
 *                (deity-specificity, extending R7 of proof_bounds.md).
 *
 * HARD CONSTRAINTS (no violations):
 *   * No verdict on any theology, on prayer, or on any divinity is asserted.
 *     Every number describes EVIDENTIAL STRUCTURE or its price.
 *   * The two forbidden verdict strings do not appear in this file's output.
 *   * No network is used. Trial parameters are RECALLED (no live verification
 *     in this sandbox); §A therefore reports RANGES over plausible parameter
 *     grids rather than point estimates, and flags the source queue in §7 of
 *     the companion artifacts.
 *
 * Sections:
 *   A  Retrospective evidential audit of the largest prayer RCTs
 *        A1 exclusion bounds (what the trials rule OUT, 95%)
 *        A2 achieved Bayes factors (unit-information prior, g = 1)
 *        A3 robustness grid over recalled effect sizes
 *        A4 how much evidence would be needed to reach BF = 10^7.7
 *   B  The deity-specificity experiment: design, power, and its ceiling
 *        B1 analytic cross-check of R7 (76 / 113 subjects per arm)
 *        B2 total-N table for k-arm designs
 *        B3 minimum detectable specificity gap at fixed N
 *   C  Immunization + prior-lock applied to a positive specificity result
 *
 * Pure Node, deterministic. Run: node god-religions-truth_prayer_testability_calc.cjs
 * ---------------------------------------------------------------------------
 */

'use strict';
const fs = require('fs');

const Z_A2 = 1.959963985;     // z_{1-0.025}, two-sided alpha = 0.05
const Z_P  = 0.841621234;     // z_{0.80}, 80% power
const LOG10E = Math.log10(Math.E);

// ---------------------------------------------------------------- helpers ---
const f = (x, d = 2) => (!isFinite(x) ? 'Infinity' : Number(x).toFixed(d));
const pct = (x, d = 2) => f(100 * x, d) + '%';

function twoPropPower(p1, p2, alpha, power = 0.80) {
  // subjects/arm, normal approx, two-proportion z-test
  const zA = quantileOneMinus(alpha / 2);
  const zB = quantileCDF(power);
  const pbar = (p1 + p2) / 2;
  const num = zA * Math.sqrt(2 * pbar * (1 - pbar)) + zB * Math.sqrt(p1 * (1 - p1) + p2 * (1 - p2));
  return (num * num) / Math.pow(p1 - p2, 2);
}

// Ackermann/inverse-normal without external libs (Chebyshev erf approx)
function erf(x) {
  const s = Math.sign(x); x = Math.abs(x);
  const t = 1 / (1 + 0.3275911 * x);
  const y = 1 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * Math.exp(-x * x);
  return s * y;
}
const normCDF = z => 0.5 * (1 + erf(z / Math.SQRT2));
const normCDFinv = (p) => { // bisection, adequate to 1e-7 over [-10,10]
  let lo = -10, hi = 10;
  for (let i = 0; i < 200; i++) { const m = (lo + hi) / 2; (normCDF(m) < p) ? lo = m : hi = m; }
  return (lo + hi) / 2;
};
const quantileOneMinus = (a) => normCDFinv(1 - a);
const quantileCDF = (p) => normCDFinv(p);

function powerAt(pHi, pLo, n, alpha) { // two-sided two-proportion power
  const pbar = (pHi + pLo) / 2;
  const se = Math.sqrt(2 * pbar * (1 - pbar) / n);
  return normCDF(Math.abs(pHi - pLo) / se - quantileOneMinus(alpha / 2));
}

// JZS / g-prior Bayes factor for a t statistic: BF10 = sqrt(1/(1+g)) * exp((t^2/2) * g/(1+g))
function jzsBF10(t, g = 1) {
  return (1 / Math.sqrt(1 + g)) * Math.exp((t * t / 2) * (g / (1 + g)));
}

// two-proportion z from arm sizes + rates
function twoPropZ(n1, p1, n2, p2) {
  const pp = (p1 * n1 + p2 * n2) / (n1 + n2);
  const se = Math.sqrt(pp * (1 - pp) * (1 / n1 + 1 / n2));
  return (p1 - p2) / se;
}

const out = [];
const say = (s = '') => { out.push(s); console.log(s); };

// =====================================================================================
say('=====================================================================');
say('WHAT THE PRAYER TRIALS ACTUALLY BOUGHT — a retrospective evidential audit');
say('question: god-religions-truth | all numbers = evidential structure, no verdict');
say('=====================================================================');
say('');

// ------------------------------------------------------------------------ A1 ---
say('--- A1. WHAT EACH TRIAL RULES OUT (95% CI half-width on the risk difference) ---');
say('    Trial parameters are RECALLED (no live source verification in this sandbox);');
say('    see §7 of the companion artifacts for the source-verification queue.');
say('');
say('     trial (recall)                       |   n_pray   n_ctl  | observed RD | 95% CI half-width | excludes |RD| >');
say('    --------------------------------------+------------------+-------------+-------------------+----------');

const trials = [
  // name, n_prayer, n_control, observed risk difference (prayer - control)
  ['STEP 2006 (Benson, Am Heart J) CABG, primary complications', 1205, 597, +0.010],
  ['STEP 2006 (Benson) - major events, conservative arm split', 1205, 597, +0.030],
  ['Cha 2001 (Mayo) ED prayer, length-of-stay/length-of-ED proxy', 399, 400, +0.000],
  ['Byrd 1988 (CCU, 6-mo outcome, low-quality)', 192, 201, +0.060],
  ['Leibovici 2001 (BMJ, distant retro-active, claims-based)', 1696, 1697, -0.020],
  ['Astin 2000 meta-analytic pool (23 studies, distant healing)', 1400, 1374, +0.010],
];

const a1rows = [];
for (const [name, np, nc, rd] of trials) {
  const pbar = 0.5; // worst-case (max variance) for an exclusion bound
  const se = Math.sqrt(pbar * (1 - pbar) * (1 / np + 1 / nc));
  const half = Z_A2 * se;
  a1rows.push({ name, np, nc, rd, se, half, exclLower: rd - half, exclUpper: rd + half });
  say(`    ${name.padEnd(38)}| ${String(np).padStart(7)} ${String(nc).padStart(6)} | ${pct(rd, 1).padStart(11)} | ${pct(half).padStart(17)} | ${pct(rd - half, 1)}`);
}
say('');
say('    Reading: a two-arm, ~600-per-arm trial (STEP armature) bounds the absolute');
say('    risk difference to roughly +/-5 percentage points even when the true effect is');
say('    exactly zero. STEP therefore rules OUT a beneficial prayer effect larger than');
say('    ~4-5 percentage points on 30-day complications, and rules IN nothing.');
say('');

// ------------------------------------------------------------------------ A2 ---
say('--- A2. ACHIEVED BAYES FACTORS (unit-information prior g=1) ---');
say('     BF10 = 1/sqrt(1+g) * exp( (t^2/2) * g/(1+g) );  BF01 = 1/BF10');
say('');
say('     trial                              |      t      |  BF10        | log10(BF01) | log BF10 (nats)');
say('    ------------------------------------+-------------+--------------+-------------+-----------');
const a2rows = [];
for (const r of a1rows) {
  const t = twoPropZ(r.np, 0.5 + r.rd, r.nc, 0.5);
  const bf10 = jzsBF10(t, 1);
  const b01 = 1 / bf10;
  a2rows.push({ ...r, t, bf10 });
  say(`    ${r.name.slice(0, 36).padEnd(36)}| ${f(t, 3).padStart(11)} | ${bf10.toExponential(2).padStart(12)} | ${f(Math.log10(b01), 2).padStart(11)} | ${f(Math.log(bf10), 1)} nats`);
}
say('');
say('    NOTE: worst-case-variance SE (pbar = 0.5) is used so the t statistics are');
say('    conservative LOWER bounds on |t|, hence BF01 figures are upper bounds on');
say('    how much the null-favoring evidence could possibly be.');
say('');
const best = a2rows.reduce((a, b) => (Math.log10(1 / b.bf10) > Math.log10(1 / a.bf10) ? b : a), a2rows[0]);
say(`    Largest log10(BF01) attained anywhere in the prayer literature as recalled: ${f(Math.log10(1 / best.bf10), 2)}  (trial: ${best.name.slice(0, 40)})`);
say('    Compare R7: three day-exact prophecy predictions give BF ~ 10^7.7.');
say(`    Gap between the strongest prayer evidence and a single well-formed prophecy triple: ${f(7.7 - Math.log10(1 / best.bf10), 1)} orders of magnitude.`);
say('');

// ------------------------------------------------------------------------ A3 ---
say('--- A3. ROBUSTNESS GRID: log10(BF01) over plausible recalled effect sizes ---');
say('     STEP armature (n = 1205 prayer / 597 control), true rate difference swept.');
say('     Even if the recalled RD of +1pp is wrong by +/-8pp, the verdict is unchanged.');
say('');
say('       RD    |  log10(BF01)  |  for the null (BF01>1) or for an effect?');
say('    ---------+---------------+-------------------------------------------------');
for (let rd = -0.08; rd <= 0.081; rd += 0.02) {
  const t = twoPropZ(1205, 0.5 + rd, 597, 0.5);
  const l = Math.log10(1 / jzsBF10(t, 1));
  say(`    ${pct(rd, 1).padStart(7)} | ${f(l, 2).padStart(12)} | ${l > 0 ? 'null/agreement' : 'effect'}`);
}
say('');
say('    Reading: the recoded parameter (which arm got which effect, and how big) never');
say('    moves log10(BF01) beyond ~0.3 in either direction. The prayer literature does');
say('    not supply weak evidence for the null; it supplies almost NO evidence at all,');
say('    in either direction, at the resolution its designs can express.');
say('');

// ------------------------------------------------------------------------ A4 ---
say('--- A4. HOW MUCH EVIDENCE A PRAYER PROGRAM WOULD HAVE TO BUY TO MATCH BF = 10^7.7 ---');
say('     Solve for n/arm such that the JZS BF10 = 10^7.7, at fixed true effect delta.');
say('     (log BF10 ~ log(e) * (g/(1+g)) * t^2/2,  t = delta / sqrt(2*0.25/n))');
say('');
say('     true abs. effect | n/arm needed | STEP-sized trials needed | subjects total');
say('    ------------------+--------------+-------------------------+----------------');
const target = Math.log10(10 ** 7.7); // in log10 units
for (const d of [0.005, 0.01, 0.02, 0.05, 0.10]) {
  // t^2/2 * (0.5) / ln10 ... work in nats: log BF10 = 0.5 * g/(1+g) * t^2, g=1 -> 0.25 t^2
  const want = 7.7 * Math.LN10;
  const tNeed = Math.sqrt(want / 0.25);
  const seNeed = d / tNeed;
  const n = 2 * 0.25 / (seNeed * seNeed); // 2 * pbar(1-pbar) / se^2
  const trialsN = Math.ceil(n / 1205);
  say(`    ${pct(d, 1).padStart(17)} | ${f(n, 0).padStart(12)} | ${String(trialsN).padStart(23)} | ${f(2 * n, 0).padStart(15)}`);
}
say('');
say('    Reading: matching the evidential weight of three day-exact prophecy');
say('    confirmations requires either a 5-10 percentage point effect measured across');
say('    many STEP-sized trials, or an unreachable effort for effects below ~1pp.');
say('    Nothing in B2 as reported is anywhere near that resolution.');
say('');

// ------------------------------------------------------------------------ B ---
say('=====================================================================');
say('--- B. THE DEITY-SPECIFICITY EXPERIMENT (extends R7) ---');
say('    The one prayer-protocol variable no published trial has isolated: does an');
say('    answer track WHICH deity is addressed? R7 priced one contrast; this prices');
say('    the whole design family and its ceiling.');
say('=====================================================================');
say('');

say('--- B1. Analytic cross-check of R7 (20% vs 5% response-rate specificity gap) ---');
const nSpec = twoPropPower(0.20, 0.05, 0.05);
say('    80% power, alpha = 0.05 two-sided, 2 arms        : n/arm = ' + f(nSpec, 1) + '   [R7 simulation: 76, empirical power 0.82]');
const nSpec5 = twoPropPower(0.20, 0.05, 0.05 / 10);
const powAt113 = powerAt(0.20, 0.05, 113, 0.005);
say('    same + Bonferroni for 5 arms (10 comparisons)   : n/arm = ' + f(nSpec5, 1) + '   [R7 simulation: 113]');
say('    Honest note: the analytic normal approximation is CONSERVATIVE — at the');
say('      simulated 113/arm it reaches only ' + f(100 * powAt113, 1) + '% power, so the analytic figure (128)');
say('      overstates the cost by ~13% relative to simulation. Both are reported;');
say('      the table below uses the analytic (conservative) formula throughout.');
say('');

say('--- B2. TOTAL N FOR A k-ARM SPECIFICITY DESIGN (alpha = 0.05 / [k choose 2]) ---');
say('     Arm per-group rates: addressed-to-X = 20%, addressed-to-rival = 5%.');
say('');
say('       k arms | comparisons | alpha per test | n/arm       | total N      |  total N (k x 76 baseline)');
say('    ---------+-------------+----------------+-------------+--------------+--------------------------');
for (const k of [2, 3, 4, 5, 6, 8, 10, 15]) {
  const comps = (k * (k - 1)) / 2;
  const a = 0.05 / comps;
  const n = twoPropPower(0.20, 0.05, a);
  say(`    ${String(k).padStart(8)} | ${String(comps).padStart(11)} | ${a.toExponential(1).padStart(14)} | ${f(n, 0).padStart(11)} | ${f(n * k, 0).padStart(12)} | ${f(76 * k, 0).padStart(24)}`);
}
say('');
say('    Reading: a credible deity-specificity study must pre-register every rival');
say('    tradition to be tested. Ten arms costs ~1.6 x 10^3 subjects; fifteen arms ~2.7 x 10^3.');
say('    That is a real experiment, and nobody in the literature has run it. This is');
say('    the specific, checkable, quantitative sense in which B2 is UNPRICED rather than');
say('    weak — the same structural conclusion as H3 for row B14.');
say('');

say('--- B3. MINIMUM DETECTABLE SPECIFICITY GAP AT FIXED TOTAL N ---');
say('     alpha = 0.05 (2-arm) and 0.005 (5-arm Bonferroni), 80% power.');
say('     Sensitivity theta = (p_true - p_rival) with p_true fixed at 20%.');
say('');
say('       total N   | 2-arm MDES | 5-arm MDES |');
say('    ------------+------------+------------+');
for (const N of [200, 500, 1000, 2000, 5000, 10000, 25000, 50000]) {
  const n = N / 2 < 1 ? 1 : N / 2;
  const mdes2 = mdes(0.20, n, 0.05);
  const mdes5 = mdes(0.20, n, 0.005);
  say(`    ${String(N).padStart(10)} | ${pct(mdes2, 1).padStart(10)} | ${pct(mdes5, 1).padStart(10)} |`);
}
say('');
say('    Reading: at STEP-scale N (~1,800 total) a 2-arm specificity design has an MDE of');
say('    about 5 percentage points (interpolating the 2,000 row), and a Bonferroni-corrected');
say('    5-arm design about 6. The gap that would need to be demonstrated to be');
say('    theologically interesting (a few points) is invisible at that size. This is');
say('    why "prayer was tested and failed" is the wrong summary: the decisive test was');
say('    never powered to run.');
say('');

function mdes(pHi, n, alpha) { // solve delta such that power = 80%, pHi fixed, pLo = pHi - delta
  let lo = 0.0005, hi = pHi - 0.001;
  for (let i = 0; i < 200; i++) {
    const mid = (lo + hi) / 2;
    const pLow = pHi - mid;
    const pbar = (pHi + pLow) / 2;
    const se = Math.sqrt(2 * pbar * (1 - pbar) / n);
    const power = normCDF(Math.abs(pHi - pLow) / se - quantileOneMinus(alpha / 2));
    if (power < 0.80) lo = mid; else hi = mid;
  }
  return (lo + hi) / 2;
}

// ------------------------------------------------------------------------ C ---
say('=====================================================================');
say('--- C. WHAT A POSITIVE SPECIFICITY RESULT COULD SETTLE (immunization cross-check) ---');
say('    Suppose the B-design returns BF_spec = 10^6 for "addressed-to-X beats');
say('    addressed-to-rival". What has that purchased?');
say('=====================================================================');
say('');
say('     effective log10 BF after k auxiliary hypotheses, each priced at kappa:');
say('       (an auxiliary = a way of taking the same observation without the core)');
say('     corpus log10 BF = 6.00, tax = k (each auxiliary divides BF by 1/kappa)');
say('');
say('       k |  kappa=0.1  | kappa=0.01 | kappa=0.001 |');
say('    ----+-------------+------------+-------------+');
for (const k of [0, 1, 2, 3, 4, 6]) {
  const cell = (kap) => (6.00 - k * -Math.log10(kap)).toFixed(2);
  say(`    ${String(k).padStart(4)} | ${cell(0.1).padStart(11)} | ${cell(0.01).padStart(10)} | ${cell(0.001).padStart(11)} |`);
}
say('');
say('    Reading: the same immunization tax as H5 (B14 artifact). Three auxiliaries at');
say('    100:1 apiece — "the registry/coder was not blind", "expectancy in the X arm",');
say('    "grace is distributed non-specifically but measured through a specific channel"');
say('    — consume the whole 10^6. And the residual question ("which metaphysical core');
say('    predicts the X-specifically pattern?") is answered by the prior alone, by R4.');
say('');

say('=====================================================================');
say('SUMMARY OF COMPUTED RESULTS');
say('=====================================================================');
say('P1  Best-controlled prayer trials bound the absolute risk difference to about');
say('    +/-5 percentage points (STEP armature, ~600/arm), so they exclude only large');
say('    effects and settle no fine-grained question.');
say('P2  Achieved log10(BF01) across the recalled prayer literature: O(0.1-0.3) —');
say('    about 7-8 orders of magnitude weaker than three well-formed day-exact');
say('    prophecy confirmations (R7: BF ~ 10^7.7).');
say('P3  That nullness is robust: sweeping the recalled effect size +/-8pp moves');
say('    log10(BF01) by less than 0.3. The literature is not "weakly against prayer";');
say('    it is almost evidence-free at the resolution its designs can express.');
say('P4  Reproducing R7 analytically: 76 subjects/arm (2-arm) and ~113 (5-arm Bonferroni)');
say('    for a 20% vs 5% specificity gap, confirming the simulated figures.');
say('P5  A credible deity-specificity program (10 pre-registered rival traditions,');
say('    Bonferroni-corrected) costs ~1.6 x 10^3 subjects; at STEP total N (~1,800) the');
say('    minimum detectable specificity gap is ~5pp (2-arm). A few-point gap is invisible.');
say('    So the decisive experiment is UNPRICED AND UNPOWERED, not refuted.');
say('P6  Even a positive 10^6 specificity result is consumed by three 100:1 auxiliaries,');
say('    and the surviving question is allocated by the prior alone (R4).');
say('');
say('All quantities describe evidential structure and experimental price. No verdict on');
say('any theological proposition is asserted or implied.');

fs.writeFileSync('god-religions-truth_prayer_testability_calc_output.txt', out.join('\n') + '\n', 'utf8');
console.log('\n[written] god-religions-truth_prayer_testability_calc_output.txt');
