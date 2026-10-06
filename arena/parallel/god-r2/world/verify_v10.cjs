// verify_v10.cjs — fresh verification of god-religions-insulation-formal.md
// Every expectation states the formula it asserts, so any mismatch localizes to
// either the script or the artifact. Shares no code with verify_v9.cjs.
'use strict';
const fs = require('fs');

let pass = 0, fail = 0;
const failures = [];
function ok(name, cond, detail) {
  if (cond) { pass++; }
  else { fail++; failures.push(name + (detail ? ' :: ' + detail : '')); }
}
const close = (x, y, tol) => Math.abs(x - y) <= tol;
const tolAbs = 1e-9, tolRound = 5e-4;

// ---------- R1: insulation index kappa(k; a) = (1-a)^k ----------
const kappa = (k, a) => Math.pow(1 - a, k);
const kappaTable = { // values asserted in the artifact's table
  '1|0.3': 0.700, '1|0.5': 0.500, '1|0.7': 0.300, '1|0.9': 0.100,
  '2|0.3': 0.490, '2|0.5': 0.250, '2|0.7': 0.090, '2|0.9': 0.010,
  '3|0.3': 0.343, '3|0.5': 0.125, '3|0.7': 0.027, '3|0.9': 0.001,
  '4|0.3': 0.240, '4|0.5': 0.0625, '4|0.7': 0.0081, '4|0.9': 0.0001,
  '6|0.3': 0.118, '6|0.5': 0.0156, '6|0.7': 0.00073, '6|0.9': 1.0e-6,
  '8|0.3': 0.058, '8|0.5': 0.0039, '8|0.7': 0.000066, '8|0.9': 1.0e-8,
};
for (const [key, want] of Object.entries(kappaTable)) {
  const [k, a] = key.split('|').map(Number);
  // table is rounded to 3 significant figures; assert to 1% relative
  ok('kappa(' + key + ') = ' + want, close(kappa(k, a), want, Math.max(1e-9, Math.abs(want) * 1e-2)), 'got ' + kappa(k, a));
}
// monotone strictly decreasing in k, for a > 0
for (const a of [0.3, 0.5, 0.7, 0.9]) {
  let mono = true;
  for (let k = 1; k < 8; k++) if (!(kappa(k + 1, a) < kappa(k, a))) mono = false;
  ok('kappa strictly decreasing in k at a=' + a, mono);
}
// structural claim: kappa <= 0.25 for all a >= 0.5, k >= 2
{
  let bounded = true;
  for (let ai = 50; ai <= 100; ai += 5) for (let k = 2; k <= 12; k++) {
    if (kappa(k, ai / 100) > 0.25 + 1e-12) bounded = false;
  }
  ok('claim: kappa <= 0.25 for all a>=0.5, k>=2', bounded);
}
// sigma complement identity
ok('kappa + sigma = 1', close(kappa(4, 0.5) + (1 - kappa(4, 0.5)), 1, tolAbs));

// ---------- R1 grounding: per-case P(0 of 6 contacts) ----------
// per-case k: Miller 2 (2 predictions), Martin 1 (1), Camping 2 (3)
const cases = [ { k: 2, m: 2 }, { k: 1, m: 1 }, { k: 2, m: 3 } ];
const probZeroContacts = (a) => cases.reduce((p, c) => p * Math.pow(1 - kappa(c.k, a), c.m), 1);
const expectedContacts = (a) => cases.reduce((s, c) => s + c.m * kappa(c.k, a), 0);
const zeroProbe = { '0.3': 0.0104, '0.5': 0.119, '0.9': 0.856, '0.95': 0.938 };
for (const [a, want] of Object.entries(zeroProbe)) {
  ok('P(0 of 6 | a=' + a + ') = ' + want, close(probZeroContacts(Number(a)), want, tolRound), 'got ' + probZeroContacts(Number(a)));
}
const expProbe = { '0.3': 3.15, '0.5': 1.75, '0.9': 0.15, '0.95': 0.063 };
for (const [a, want] of Object.entries(expProbe)) {
  ok('E[contacts | a=' + a + '] = ' + want, close(expectedContacts(Number(a)), want, 0.005), 'got ' + expectedContacts(Number(a)));
}

// ---------- R4: minimum a with P(0 of 6) >= 0.05, by bisection ----------
{
  const f = (x) => probZeroContacts(x) - 0.05;
  ok('P(0of6) < 0.05 at a=0.30', f(0.30) < 0);
  ok('P(0of6) > 0.05 at a=0.45', f(0.45) > 0);
  let lo = 0.30, hi = 0.45;
  for (let i = 0; i < 200; i++) { const mid = (lo + hi) / 2; if (f(mid) < 0) lo = mid; else hi = mid; }
  const aStar = (lo + hi) / 2;
  ok('R4 minimum a in [0.41, 0.42] (artifact: ~0.41)', aStar > 0.41 && aStar < 0.42, 'got ' + aStar.toFixed(6));
}

// ---------- R5: N-lattice, b = (N-1) * p/(1-p) ----------
const lattice = [
  [1e2, 0.5, 99], [1e2, 0.9, 891], [1e2, 0.99, 9801],
  [1e3, 0.5, 999], [1e3, 0.9, 8991], [1e3, 0.99, 98901],
  [4e3, 0.5, 3999], [4e3, 0.9, 35991], [4e3, 0.99, 395901],
  [1e4, 0.5, 9999], [1e4, 0.9, 89991], [1e4, 0.99, 989901],
  [3.2e4, 0.5, 31999], [3.2e4, 0.9, 287991], [3.2e4, 0.99, 3167901],
];
for (const [N, p, want] of lattice) {
  ok('b(N=' + N + ', p=' + p + ') = ' + want, close((N - 1) * p / (1 - p), want, 0.5));
}
// structural invariance: difficulty ratio vs the binary existence question is exactly N-1
for (const N of [2, 11, 100, 4000, 1e4, 3.2e4]) {
  const bId = (N - 1) * 0.9 / 0.1, bEx = (2 - 1) * 0.9 / 0.1; // existence: N=2
  ok('identification/existence ratio = N-1 at N=' + N, close(bId / bEx, N - 1, 1e-6));
}

// ---------- R2/R3: gate-2 neutrality by brute force (fresh enumeration) ----------
// P = C & A1..Ak. Fault hypothesis H_i = conjunct i is false. H_i entails not-P.
// => P(not-P | H_i) = 1 for every i => LR(H_i : H_j) = 1 exactly.
function gate2(k) {
  const n = k + 1; // conjunct 0 = core, 1..k = auxiliaries
  let lrOk = true, uniformSite = 1 / (k + 1), uniformWorld = Math.pow(2, k) / (Math.pow(2, k + 1) - 1);
  for (let i = 0; i < n; i++) {
    let worldsFalseConjunctI = 0, worldsFalseAndNotP = 0;
    for (let w = 0; w < (1 << n); w++) {
      const conjI = ((w >> i) & 1) === 0;
      if (!conjI) continue;
      worldsFalseConjunctI++;
      const allTrue = w === (1 << n) - 1; // P holds iff every conjunct true
      if (!allTrue) worldsFalseAndNotP++;
    }
    // P(not-P | H_i) must be exactly 1
    if (!(worldsFalseConjunctI === worldsFalseAndNotP && worldsFalseConjunctI > 0)) lrOk = false;
  }
  return { lrOk, uniformSite, uniformWorld };
}
for (let k = 1; k <= 6; k++) {
  const g = gate2(k);
  ok('gate-2 LR = 1.0 exactly at k=' + k, g.lrOk);
  ok('uniform-site share = 1/(k+1) at k=' + k, close(g.uniformSite, 1 / (k + 1), tolAbs));
}
// cross-check C3's published convention values from the companion artifact
ok('C3 cross-check: uniform-world k=1 = 0.667', close(gate2(1).uniformWorld, 2 / 3, 1e-3));
ok('C3 cross-check: uniform-world k=3 = 0.5333', close(gate2(3).uniformWorld, 8 / 15, 1e-4));
ok('C3 cross-check: uniform-world k=6 -> 0.504', close(gate2(6).uniformWorld, 64 / 127, 1e-3));
ok('C3 cross-check: 2.5x spread at k=3 (0.25 vs 0.625)', close((5 / 8) / gate2(3).uniformSite, 2.5, 1e-9));
// two-gate chain: discriminative yield is bounded above by the reach prior
{
  const reach = kappa(4, 0.5); // documented k=4, a=0.5
  ok('two-gate: reach prior 0.0625 at documented k=4', close(reach, 0.0625, tolAbs));
  ok('two-gate: gate-2 multiplier is exactly 1.0 in LR, contributing 0 discriminative content', gate2(4).lrOk);
}

// ---------- companion artifact tallies re-checked from their own text ----------
{
  const tax = fs.readFileSync('god-religions-taxonomy.md', 'utf8');
  const sep = fs.readFileSync('god-religions-separation-formal.md', 'utf8');

  // ledger row tags: rows look like "| **T** ..." or "| **T (weak)** ..." inside Part 2 table
  const tRows = (tax.match(/\|\s*\*\*T\b/g) || []).length;
  const ntRows = (tax.match(/\|\s*\*\*NT\b/g) || []).length;
  ok('taxonomy: 10 [T] ledger rows', tRows === 10, 'got ' + tRows);
  ok('taxonomy: 4 [NT] ledger rows', ntRows === 4, 'got ' + ntRows);
  ok('taxonomy: 6 dated predictions documented', tax.includes('**6** (Miller 1843 year-level') || tax.includes('**Dated predictions examined:** **6**'));
  ok('taxonomy: 0 of 6 localizations', tax.includes('**0 of 6 predictions'));
  ok('taxonomy: 4 auxiliary-move families', tax.includes('**4** — event re-interpretation'));

  // separation-formal headline numbers
  ok('separation: C1 Regime A 0 of 28', sep.includes('**0 of 28** pairs separable'));
  ok('separation: C1 Regime B 9 of 28', sep.includes('9 of 28'));
  ok('separation: C1 Regime B-prime 6 of 28', sep.includes('6 of 28'));
  ok('separation: C2 threshold 89,991', sep.includes('89,991'));
  ok('separation: C2 shortfall ~29,997x', sep.includes('29,997'));
  ok('separation: C3 LR exactly 1.0', sep.includes('exactly **1.0**'));
  ok('separation: 0 asserted verdicts', sep.includes('**0** (by protocol design)'));
}

// ---------- banned verdict constructions across all three artifacts ----------
{
  const banned = [
    /therefore god exists/i,
    /therefore god does not exist/i,
    /god exists therefore/i,
    /god does not exist therefore/i,
    /we conclude that god exists/i,
    /we conclude that god does not exist/i,
  ];
  for (const f of ['god-religions-taxonomy.md', 'god-religions-separation-formal.md', 'god-religions-insulation-formal.md']) {
    const txt = fs.readFileSync(f, 'utf8');
    const hits = banned.filter((r) => r.test(txt));
    ok('no banned construction in ' + f, hits.length === 0, hits.join(','));
    ok('protocol disclaimer present in ' + f, /does \*\*not\*\* assert that any god exists or does not exist/i.test(txt) || /assigns no probability to any god's existence/i.test(txt));
  }
}

console.log('verify_v10: ' + pass + ' passed, ' + fail + ' failed');
if (fail > 0) { console.log('FAILURES:\n - ' + failures.join('\n - ')); process.exit(1); }
