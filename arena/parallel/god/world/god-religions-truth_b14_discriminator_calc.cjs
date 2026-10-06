/*
 * god-religions-truth_b14_discriminator_calc.cjs
 * Quantitative decision rule for the ledger's strongest discriminator candidate:
 * B14 (past-life-memory veridicality), flagged by the blind-arbitration audit as the
 * only row where evidence could, in principle, move rebirth-family vs naturalist core odds.
 *
 * This script computes:
 *   A. per-case likelihood ratio under a Stevenson-style protocol, parameterized by the
 *      blind-recorded fraction and the "flexibility inflation" of non-blind matching
 *   B. corpus requirement for a target Bayes factor (numerology is never the constraint)
 *   C. pilot sizing: the price of MEASURING the confounder channel (the decisive result)
 *   D. cultural-clustering Bayes factor and its ambiguous band
 *   E. immunization tax: auxiliary hypotheses erode a corpus Bayes factor
 *   F. family-level attribution invariance: a confirmed corpus re-runs the prior-lock
 *      problem inside the rebirth-accepting classes
 *   G. prior-lock: the prior odds needed to absorb a corpus via one auxiliary
 *
 * Pure arithmetic; no network; no Monte Carlo needed (all closed forms). Deterministic.
 * Every quantity is a fact about evidential structure; none is a probability of any
 * theological proposition. No verdict is asserted anywhere in this file.
 */
'use strict';

const line = (s) => console.log(s === undefined ? '' : s);
const pad = (s, n) => String(s).padStart(n);
function fmt(x, d) {
  if (d === undefined) d = 3;
  if (!isFinite(x)) return 'Infinity';
  if (x === 0) return '0';
  const a = Math.abs(x);
  if (a >= 1e6 || a < 1e-4) return x.toExponential(2);
  return x.toFixed(d);
}
function l10(x) { return Math.log10(x); }

line('=== B14 DISCRIMINATOR RULE: computed sections A-G ===');

/* ------------------------------------------------------------------
 * A. Per-case likelihood ratio
 *    LR = P(S/S checkable statements verified as matching | rebirth)
 *       / P(S/S checkable statements verified as matching | naturalistic channel)
 *
 *    model: LR = 1 / (K * sigma^(b*S) * phi)
 *      S    = statements that were checkable and all matched
 *      sigma= P(a random deceased candidate matches one statement)
 *      K    = number of deceased candidates searched per case
 *      b    = blind-recorded fraction (statements recorded before any candidate known)
 *      phi  = flexibility inflation of guided (post-hoc) elicitation & matching
 * ------------------------------------------------------------------ */
function perCaseLR(S, sigma, K, b, phi) {
  return 1 / (K * Math.pow(sigma, b * S) * phi);
}

line('');
line('--- A1. log10(per-case LR): sigma x blind-fraction b   (S=10, K=100, phi=1) ---');
const sigmas = [1e-1, 1e-2, 1e-3];
const bs = [1.0, 0.5, 0.2];
line('   b  |' + sigmas.map(s => pad('sig=' + s.toExponential(0), 16)).join(''));
for (const b of bs) {
  const cells = sigmas.map(s => pad(l10(perCaseLR(10, s, 100, b, 1)).toFixed(2), 16));
  line(pad(b.toFixed(1), 6) + ' |' + cells.join(''));
}

line('');
line('--- A2. log10(per-case LR): blind-fraction b x flexibility inflation phi   (S=10, sigma=1e-3, K=100) ---');
const phis = [1, 3, 10, 30, 100];
line('   b  |' + phis.map(p => pad('phi=' + p, 12)).join(''));
for (const b of bs) {
  const cells = phis.map(p => pad(l10(perCaseLR(10, 1e-3, 100, b, p)).toFixed(2), 12));
  line(pad(b.toFixed(1), 6) + ' |' + cells.join(''));
}

line('');
line('--- A3. Break-even phi*: flexibility inflation at which per-case LR = 1 ---');
line('    (a non-blind protocol must inflate false matches by MORE than this before the');
line('     evidence content of a case vanishes; phi > phi* => corpus can never discriminate)');
line('    S=10, K=100:');
const K = 100;
line('   sigma  |  b=1.0        b=0.5        b=0.2');
for (const s of [1e-1, 1e-2, 1e-3]) {
  const cells = bs.map(b => {
    const phiStar = K * Math.pow(s, b * 10); // LR=1  <=>  phi* = K sigma^(bS)
    return pad(fmt(phiStar, 2), 12);
  });
  line(pad(s.toExponential(0), 9) + ' |' + cells.join('  '));
}

/* ------------------------------------------------------------------
 * B. Corpus requirement: n = ceil( threshold_log10 / log10(LR_per_case) )
 * ------------------------------------------------------------------ */
line('');
line('--- B. Corpus size needed for a target corpus Bayes factor ---');
line('    (independent cases multiply: log10 BF_corpus = n * log10 LR_case)');
line('    log10 LR/case |  n for BF=1e3  |  n for BF=1e6  |  BF at n=2500 (current-corpus scale)');
for (const l of [0.5, 1, 2, 3, 6, 12, 24, 30]) {
  const n3 = Math.ceil(3 / l);
  const n6 = Math.ceil(6 / l);
  const bf2500 = Math.pow(10, 2500 * l);
  line('    ' + pad(l, 13) + ' |' + pad(n3, 14) + ' |' + pad(n6, 14) + ' |' + pad(fmt(bf2500), 30));
}
line('    Reading: at ANY nonzero per-case LR the corpus arithmetic is trivially satisfiable —');
line('    so the numerology is never the binding constraint. The binding constraint is whether');
line('    per-case LR exceeds 1 at all (section A3), which is the phi/b question.');

/* ------------------------------------------------------------------
 * C. The missing measurement: price of estimating the H2 per-attempt
 *    false-match probability p to relative precision r.
 *    n ~= z^2 (1-p) / (r^2 p)  ~= 3.84 / (r^2 p)   for small p (z=1.96)
 * ------------------------------------------------------------------ */
line('');
line('--- C. Pilot sizing: blinded match attempts needed to measure the confounder channel ---');
line('    n ~= z^2 (1-p)/(r^2 p), z=1.96; p = P(random candidate matches one statement | naturalistic)');
const rs = [0.5, 0.25, 0.1];
const ps = [1e-1, 1e-2, 1e-3, 1e-4, 1e-5];
line('      p     |' + rs.map(r => pad('r=' + r, 16)).join(''));
for (const p of ps) {
  const cells = rs.map(r => pad(Math.ceil(3.8416 * (1 - p) / (r * r * p)), 16));
  line(pad(p.toExponential(0), 12) + ' |' + cells.join(''));
}
line('');
line('    In case units (S=10 checkable statements per case):');
line('      p     |  r=0.25 attempts |  cases');
for (const p of ps) {
  const att = Math.ceil(3.8416 / (0.0625 * p));
  line(pad(p.toExponential(0), 12) + ' |' + pad(att, 16) + ' |' + pad(Math.ceil(att / 10), 8));
}
line('    Reading: estimating the false-match rate at p=1e-3 to +/-25% needs ~6.1e4 blinded');
line('    match attempts (~6.1e3 blinded case-verifications) — an experiment nobody has run.');
line('    Until it is run, per-case LR (and hence the whole B14 program) is UNSCORABLE, not weak.');

/* ------------------------------------------------------------------
 * D. Cultural clustering. R = population belief-prevalence ratio
 *    (believing cultures : secular cultures). Constructed-memory (H2)
 *    predicts case incidence scales with belief: rho_hat ~ R.
 *    Rebirth-real with belief-independent incidence (H1a): rho_hat ~ 1.
 *    Rebirth-real with near-home rebinding (H1b): rho_hat ~ R too (muddy).
 * ------------------------------------------------------------------ */
line('');
line('--- D. Cultural clustering: log10 BF for "constructed" over "rebirth-real" ---');
line('    observed rho = case-incidence ratio (believing : secular cultures); Poisson approx.');
const Rhos = [10, 100];
line('    R=10:   rho |   log10 BF (vs belief-independent rebirth)');
for (const rho of [1, 2, 5, 10, 20, 50]) {
  // BF = P(rho|H2)/P(rho|H1a), Poisson means R vs 1, log BF = R - 1 + rho*ln(1/R)
  const logBF = (Rhos[0] - 1) + rho * Math.log(1 / Rhos[0]);
  line('    ' + pad(rho, 11) + ' |' + pad((logBF / Math.LN10).toFixed(3), 18));
}
line('    R=100:  rho |   log10 BF (vs belief-independent rebirth)');
for (const rho of [1, 2, 5, 10, 20, 50]) {
  const logBF = (Rhos[1] - 1) + rho * Math.log(1 / Rhos[1]);
  line('    ' + pad(rho, 11) + ' |' + pad((logBF / Math.LN10).toFixed(3), 18));
}
line('    Ambiguous band: |log10 BF| < 1 => neither hypothesis preferred 10:1.');
line('    Band check: log10 BF crosses +/-1 at rho = (R-1)/ln R +/- 2.303/ln R.');
line('      R=10 : rho in (2.9, 4.9)      | R=100: rho in (20.8, 22.0)  — knife-edges.');
line('    So IF rebirth-real meant belief-independent incidence, the clustering datum would');
line('    be strongly discriminating (any rho <= 20 favors "constructed" by >10:1 when R=100).');
line('    But the near-home rebinding defence predicts rho ~ R under rebirth-real as well,');
line('    collapsing H1 onto H2. The datum is therefore a CONTESTED candidate, not a');
line('    discriminator: its force depends on which rebirth prediction is stipulated.');

/* ------------------------------------------------------------------
 * E. Immunization tax: each ad-hoc auxiliary costs kappa (parsimony factor).
 *    effective corpus BF = BF * kappa^k
 * ------------------------------------------------------------------ */
line('');
line('--- E. Immunization tax: corpus BF after k auxiliaries, each costing kappa ---');
line('    corpus BF=1e6 (a strong B14): effective log10 BF');
const kappas = [1e-1, 1e-2, 1e-3];
line('    k |' + kappas.map(k => pad('kappa=' + k.toExponential(0), 16)).join(''));
for (const k of [0, 1, 2, 3, 4, 6]) {
  const cells = kappas.map(kp => pad((6 + k * l10(kp)).toFixed(2), 16));
  line(pad(k, 5) + ' |' + cells.join(''));
}
line('    Reading: three auxiliaries at kappa=1e-2 (each a 100:1 parsimony price — modest for');
line('    "memories are constructed by an unknown mechanism" style deflections) fully consume');
line('    a 1e6 corpus BF. The tax is symmetric: the same arithmetic applies to any core.');

/* ------------------------------------------------------------------
 * F. Family-level attribution invariance.
 *    Grant the corpus at BF=1e6: it multiplies all rebirth-accepting classes
 *    equally, so the split among them is unchanged. Compute exactly.
 * ------------------------------------------------------------------ */
line('');
line('--- F. Attribution invariance INSIDE the rebirth-accepting family ---');
const fam = [
  ['hindu-theism', 1170],   // ~1.17B adherents, Pew-style 2020 figures (M confidence)
  ['advaita', 292],         // treated as ~25% of Hindu mass; school, not separate population
  ['buddhism', 510],        // rebirth without atman
  ['sikhism', 30],
  ['jainism', 5]
];
const tot = fam.reduce((a, x) => a + x[1], 0);
const priorsPop = fam.map(x => x[1] / tot);
const priorsUni = fam.map(() => 1 / fam.length);

function splitReport(name, priors, BF) {
  // evidence E multiplies every member's likelihood by BF equally (rebirth-family signature)
  const post = priors.map(p => p * BF);
  const Z = post.reduce((a, b) => a + b, 0);
  const q = post.map(p => p / Z);
  const drift = priors.map((p, i) => Math.abs(Math.log2(q[i] / p))).reduce((a, b) => Math.max(a, b), 0);
  line('    ' + name + ' (BF=' + BF.toExponential(0) + '):');
  fam.forEach((x, i) => line('       ' + pad(x[0], 14) + ' prior=' + priors[i].toFixed(4) +
                             '  posterior=' + q[i].toFixed(4)));
  line('       max drift vs prior: ' + drift.toFixed(6) + ' bits');
}
splitReport('population-weighted priors', priorsPop, 1e6);
splitReport('uniform priors', priorsUni, 1e6);
line('    Reading: a confirmed corpus would lift the whole family against no-rebirth cores,');
line('    but allocate WITHIN the family by prior alone — R4 reruns one level down. "Which');
line('    rebirth metaphysics?" would be exactly as evidence-invariant as "which god?".');

/* ------------------------------------------------------------------
 * G. Prior-lock: prior odds needed for a core to absorb a corpus BF
 *    via one auxiliary of cost kappa and still reach posterior >= 0.5.
 * ------------------------------------------------------------------ */
line('');
line('--- G. Prior-lock: prior odds needed to survive a corpus ---');
line('    (posterior P(H) >= 0.5 requires prior odds >= BF_effective against the corpus)');
line('    corpus BF |  kappa=1 (raw)  |  kappa=1e-2 (one auxiliary)  |  kappa=1e-4 (two)');
for (const BF of [1e3, 1e6, 1e12]) {
  line('    ' + pad(BF.toExponential(0), 10) + ' |' + pad(BF.toExponential(0), 15) + ' |' +
      pad((BF * 1e-2).toExponential(0), 28) + ' |' + pad((BF * 1e-4).toExponential(0), 22));
}
line('    Reading: a core can absorb even a 1e12 corpus by already holding ~1e8:1 prior');
line('    odds plus two modest auxiliaries. Evidence reallocates only among the movable.');

/* ------------------------------------------------------------------
 * H. Summary
 * ------------------------------------------------------------------ */
line('');
line('=== H. SUMMARY OF COMPUTED RESULTS ===');
line('H1  Per-case LR for a Stevenson-style case at S=10, K=100 ranges from 1e28 (fully');
line('    blind, sigma=1e-3) down to 1e-2 (b=0.2, guided elicitation, sigma=1e-1): a');
line('    30-order-of-magnitude swing carried entirely by two unmeasured protocol');
line('    parameters. No existing corpus measures either one.');
line('H2  Corpus arithmetic is never binding: at any per-case LR >= 10^0.5, n=2500 cases');
line('    gives a corpus BF beyond 10^1000. The numerology is not the weak point.');
line('H3  The weak point is measurement, not strength: estimating the naturalistic');
line('    false-match rate p=1e-3 to +/-25% needs ~6.1e4 blinded match attempts');
line('    (~6.1e3 blinded case-verifications). No such measurement exists; the corpus is');
line('    therefore UNSCORABLE rather than weak.');
line('H4  Cultural clustering is knife-edge ambiguous under belief-independent rebirth');
line('    (R=100: ambiguous only for rho in (20.8,22.0)) and is predicted by BOTH readings');
line('    under near-home rebinding. Its force depends on which rebirth prediction is');
line('    stipulated, so it is a contested candidate, not a discriminator.');
line('H5  A 1e6 corpus BF is fully consumed by three kappa=1e-2 auxiliaries; the tax is');
line('    symmetric across all cores.');
line('H6  Even a confirmed corpus re-runs attribution invariance inside the rebirth-accepting');
line('    family: max drift from priors = 0.000000 bits at BF=1e6.');
line('H7  Prior-lock: a core can absorb a 1e12 corpus with ~1e8:1 prior odds plus two');
line('    auxiliaries.');
line('');
line('All quantities describe evidential structure. No probability of any theological');
line('proposition is asserted, and no verdict is expressed.');
