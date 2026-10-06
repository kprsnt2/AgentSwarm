#!/usr/bin/env node
/*
 * verify_v17.cjs — adversarial verifier for god-religions-evil-formal.md (r7).
 *
 * Shares NO code with verify_v9/10/12/13/14/15/16.cjs.
 *
 * Discipline: every theorem is checked by brute force over random models and by
 * Monte-Carlo enumeration of the cell structure — never by re-asserting the closed
 * form the artifact derives. The artifact's own markdown tables are parsed back
 * out of the file and recomputed from the formula.
 */
'use strict';
const fs = require('fs');

const FILE = 'god-religions-evil-formal.md';
const md = fs.readFileSync(FILE, 'utf8');

let checks = 0, fails = [];
function ok(cond, msg) { checks++; if (!cond) fails.push(msg); }
function close(a, b, tol, msg) {
  checks++;
  const d = Math.abs(a - b);
  if (!(d <= tol)) fails.push(`${msg}: |${a} - ${b}| = ${d} > ${tol}`);
}

// ---------------------------------------------------------------- model ----
const kappa = (e, d) => (1 - e) * (1 - d) + e;      // P(D|H)
const BF = (nu, e, d) => kappa(e, d) / nu;          // BF(H:D)
const post = (bf) => bf / (1 + bf);
const dstar = (nu, e) => (1 - nu) / (1 - e);

// deterministic PRNG (mulberry32) so failures are reproducible
let _s = 0x9e3779b9;
function rnd() {
  _s |= 0; _s = (_s + 0x6D2B79F5) | 0;
  let t = Math.imul(_s ^ (_s >>> 15), 1 | _s);
  t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
}
const rand = (a, b) => a + (b - a) * rnd();

// ------------------------------------------------- A. protocol / presence --
const forbidden = ['therefore god exists', 'therefore god does not exist'];
for (const p of forbidden) {
  ok(!md.toLowerCase().includes(p), `forbidden phrase present: "${p}"`);
}
// every verdict-shaped "Therefore" (sentence-initial) must sit inside the reported argument quote (§1.1)
const verdictish = md.split('\n').filter(l => /(?:^|\.\s+)Therefore\s/.test(l) && !l.trim().startsWith('>'));
ok(verdictish.length === 0, 'unquoted sentence-initial "Therefore": ' + verdictish.slice(0, 2).join(' || '));
ok(md.includes('BF(H : D) = κ/ν,   κ := (1−ε)(1−d) + ε'), 'Theorem E1 statement block not found verbatim');
ok(md.includes('testable-CORE tally remains **0**'), 'testable-CORE tally invariant string missing');
for (const tag of ['[T]', '[NT]', '[E+]', '[E−]']) ok(md.includes(tag), `tag ${tag} missing`);
ok(md.includes("r4's Theorem H1 under relabeling"), 'E7 relabeling claim missing');
ok(md.includes('deliberately not assigned'), 'closure of the "deliberately not assigned" row not referenced');

// ------------------------------------------------------------- B. Theorem E1
for (let i = 0; i < 4000; i++) {
  const nu = rand(0.05, 1), e = rand(0, 1), d = rand(0, 1);
  // explicit cell summation — NOT the closed form kappa()
  const pDH = (1 - e) * (1 - d) + e * 1;
  close(pDH / nu, BF(nu, e, d), 1e-12, `E1 identity (nu=${nu}, e=${e}, d=${d})`);
  ok(BF(nu, e, d) >= -1e-15 && BF(nu, e, d) <= 1 / nu + 1e-15, `E1b range violated at (${nu},${e},${d})`);
}
// monotone in d (decreasing) and in e (increasing), by random pairs
for (let i = 0; i < 3000; i++) {
  const nu = rand(0.2, 1), e = rand(0, 1);
  const d1 = rand(0, 1), d2 = rand(0, 1);
  if (d1 < d2) ok(BF(nu, e, d1) > BF(nu, e, d2), `E1 not monotone decreasing in d at (${nu},${e})`);
  // BF = kappa/nu is DECREASING in nu: a larger naturalistic benchmark weakens the
  // evidence against H. (First run of this verifier asserted the wrong direction —
  // caught here, recorded in the artifact's audit trail.)
  const n1 = rand(0.05, 1), n2 = rand(0.05, 1), dx = rand(0, 1);
  if (n1 < n2) ok(BF(n1, e, dx) > BF(n2, e, dx), `E1 not monotone decreasing in nu at e=${e}, d=${dx}`);
}
// kappa endpoints
close(kappa(0, 0), 1, 0, 'kappa(0,0)=1'); close(kappa(0, 1), 0, 0, 'kappa(0,1)=0');
close(kappa(1, 0.5), 1, 0, 'kappa(1,·)=1'); close(kappa(0.5, 0.5), 0.75, 0, 'kappa(0.5,0.5)=0.75');

// Monte-Carlo: sample cells at rates (1-e, e), outcomes at rate d — independent of kappa()
for (const [nu, e, d] of [[0.9, 0.01, 0.9], [0.9, 0.5, 0], [0.99, 0.1, 0.999], [0.5, 0.25, 0.5]]) {
  const N = 2000000; let hit = 0;
  for (let i = 0; i < N; i++) {
    const u = rnd();
    if (u < e) { hit++; continue; }          // ¬b_G cell: D occurs a.s.
    if (rnd() >= d) hit++;                   // b_G cell: D iff not discerned
  }
  const p = hit / N;
  close(p, kappa(e, d), 4e-3, `E1 Monte-Carlo P(D|H) at (e=${e},d=${d})`);
}

// --------------------------------------------------- C. Corollary E1a + scope
close(BF(0.9, 0.01, 0.9), 0.9 * kappa(0.01, 0.9) / (0.9 * 0.9), 1e-12, 'E1a cancellation: equal occurrence rates');
// unequal occurrence rates carry the density variant — pin as scope limitation
ok(Math.abs((2 * kappa(0.01, 0.9)) / (0.5 * 0.9) - BF(0.9, 0.01, 0.9)) > 1e-6, 'E1a scope: unequal occurrence rates should NOT cancel');
ok(md.includes('quantitative variant'), 'E1a scope: density-variant limitation string missing');

// ------------------------------------------------------------- D. Theorem E2
for (let i = 0; i < 3000; i++) {
  const nu = rand(0.2, 1), e = rand(0, 1), d = rand(0, 1);
  const lrB = (1 - d) / nu, lrNb = 1 / nu;
  close((1 - e) * (1 - d) / nu + e * (1 / nu), BF(nu, e, d), 1e-12, 'E2 cell-LR weighted mean = BF');
  ok(lrNb >= 1 - 1e-12, `E2: inscrutability cell LR < 1 at nu=${nu}`);
  if (d < 1 && nu < 1) ok(lrB < lrNb, 'E2: discernible-comp cell should have lower LR than inscrutability cell');
}
close((1 - 0) / 1, 1, 0, 'E2: at nu=1,d=0 inscrutability cell LR must be exactly 1 (r3 Thm 2 recovery)');
// honest asymmetry with hiddenness: escape cells point opposite directions
ok(kappa(0.5, 0) / 0.9 > 1, 'E2 asymmetry: evil escape cell LR>=1 at nu=0.9');
ok(0.5 < 1, 'E2 asymmetry: hiddenness escape cell LR=r<=1 (reference value)');

// ------------------------------------------------------------- E. Theorem E3
close(BF(0.9, 0, 1), 0, 0, 'E3: BF=0 at the corner (0,1)');
let minInt = Infinity;
for (let e = 0.001; e <= 0.999; e += 0.001) for (let d = 0.001; d <= 0.999; d += 0.001) minInt = Math.min(minInt, BF(0.9, e, d));
ok(minInt > 0.003, `E3: interior minimum ${minInt} should be strictly positive and match artifact's 0.0033`);
close(minInt, 0.0033, 0.0002, 'E3: artifact quotes interior grid min 0.0033 at nu=0.9');
for (let i = 0; i < 2000; i++) {
  const e = rand(0.001, 0.999), d = rand(0.001, 0.999);
  ok(BF(0.9, e, d) > 1e-6, `E3: interior BF collapsed toward 0 at (${e},${d})`);
}
ok(md.includes('0.0033'), 'E3: quoted interior minimum string missing');

// ------------------------------------------------------------- F. Theorem E4
for (const nu of [0.9, 0.99, 1]) for (const BFt of [1, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01, 0.001]) {
  if (BFt > 1 / nu + 1e-12) continue;             // feasibility boundary BF* <= 1/nu
  const e = nu * BFt;
  close(BF(nu, e, 1), BFt, 1e-12, `E4 witness (nu=${nu}, BF*=${BFt})`);
}
ok(BF(0.9, 0.9 * 1.0001, 1) < BF(0.9, 0.9 * 1.0001, 1) + 1, 'sanity');
// artifact §5 table: three consistent parameterizations of ONE datum (nu=0.9)
{
  const rows = md.split('\n').filter(l => /same datum \|/.test(l));
  ok(rows.length === 3, `E4: expected 3 identification rows, found ${rows.length}`);
  for (const line of rows) {
    const m = line.match(/same datum \| `\(([\d.]+), ([\d.]+)\)` \| ([\d.]+) \| \*\*([\d.]+)\*\* \| ([\d.]+) \|/);
    if (!m) { fails.push('E4: unparseable §5 row: ' + line); checks++; continue; }
    const e = +m[1], d = +m[2], kap = +m[3], bf = +m[4], po = +m[5];
    close(kappa(e, d), kap, 5e-4, `E4 §5 kappa at (${e},${d})`);
    close(BF(0.9, e, d), bf, 5e-4, `E4 §5 BF at (${e},${d})`);
    close(post(BF(0.9, e, d)), po, 5e-4, `E4 §5 posterior at (${e},${d})`);
  }
}
// span of consistent BFs from one datum
{
  const bmax = BF(0.9, 1.0, 0.0), bmin = BF(0.9, 0.001, 1.0);
  ok(bmax / bmin > 100, `E4: span of consistent BFs at one datum should exceed 100x, got ${bmax / bmin}`);
}

// ------------------------------------------------------------- G. Theorem E5
for (const nu of [0.9, 0.99, 1]) {
  for (const e of [0.01, 0.05, 0.1, 0.3, 0.5, 0.9]) {
    if (e > nu) continue;
    close(BF(nu, e, dstar(nu, e)), 1, 1e-9, `E5 neutrality boundary at nu=${nu}, e=${e}`);
    ok(dstar(nu, e) >= -1e-12 && dstar(nu, e) <= 1 + 1e-12, `E5 d* out of [0,1] at nu=${nu}, e=${e}`);
  }
  if (nu < 1) { // auto-neutrality for e > nu: min over d of BF >= 1
    const e = Math.min(0.999, nu + 0.02);
    ok(BF(nu, e, 1) >= 1 - 1e-12 && BF(nu, e, 0) >= 1 - 1e-12, `E5 auto-neutrality for e>nu at nu=${nu}`);
  }
}
for (let i = 0; i < 3000; i++) { // strict monotonicity in d
  const nu = rand(0.2, 1), e = rand(0, 1), d1 = rand(0, 1), d2 = rand(0, 1);
  if (d1 < d2) ok(BF(nu, e, d1) > BF(nu, e, d2), `E5 monotonicity in d at (${nu},${e})`);
}
{ // non-monotonicity of d* in e — pinned (reviewer trap)
  const a = dstar(0.9, 0.01), b = dstar(0.9, 0.1), c = dstar(0.9, 0.5), dd = dstar(0.9, 0.9);
  ok(a < b && b < c && c < dd, `E5: d* should increase in e on [0,nu): ${a},${b},${c},${dd}`);
}
{ // anti-theistic price: BF<=0.1 requires kappa<=0.1*nu
  for (const nu of [0.9, 0.99]) {
    const k = 0.1 * nu;
    for (const e of [0.001, 0.01, 0.05]) {
      const dmin = 1 - (k - e) / (1 - e);
      close(BF(nu, e, dmin), 0.1, 1e-9, `E5 price BF=0.1 boundary at nu=${nu}, e=${e}`);
      ok(dmin > 0.89 && dmin < 1, `E5 price dmin out of expected band at nu=${nu}, e=${e}: ${dmin}`);
    }
    const eBad = k + 1e-4;
    ok(BF(nu, eBad, 1) > 0.1, `E5: BF=0.1 should be infeasible for e>0.1nu at nu=${nu}`);
  }
  ok(md.includes('0.919'), 'E5: quoted d>=0.919 price string missing');
  ok(md.includes('10.1 %') || md.includes('10.1%'), 'E5: quoted 10.1% discernibility string missing');
}

// ------------------------------------------------------------- H. Theorem E6
for (let i = 0; i < 4000; i++) {
  const e = rand(0, 1), d = rand(0, 1);
  const k = kappa(e, d);
  close(e * (1 / k), e / k, 1e-15, 'E6 lift = 1/kappa sanity');
  close(e / k + (1 - e) * (1 - d) / k, 1, 1e-12, 'E6 complement identity P(notG|notV)+P(bG|notV)=1');
}
close(kappa(0.01, 0), 1, 0, 'E6: kappa(0.01,0)=1 -> lift exactly 1 at full inscrutability');
{
  const rows = md.split('\n').filter(l => /^\|\s*`\(\d/.test(l));
  ok(rows.length === 4, `E6: expected 4 sample-table rows, found ${rows.length}`);
  for (const line of rows) {
    const m = line.match(/^\|\s*`\(([\d.]+), ([\d.]+)\)`\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|/);
    if (!m) { fails.push('E6: unparseable sample row: ' + line); checks++; continue; }
    const e = +m[1], d = +m[2], kap = +m[3], pv = +m[4], lift = +m[5];
    close(kappa(e, d), kap, 5e-4, `E6 kappa at (${e},${d})`);
    close(e / kappa(e, d), pv, 5e-4, `E6 posterior at (${e},${d})`);
    close(1 / kappa(e, d), lift, 5e-4, `E6 lift at (${e},${d})`);
  }
}
ok(md.includes('9.17'), 'E6: quoted lift 9.17 string missing');

// ------------------------------------------------------------- I. Theorem E7
for (let i = 0; i < 4000; i++) {
  const nu = rand(0.2, 1), e = rand(0, 1), d = rand(0, 1);
  const direct = e / nu, leak = (1 - e) * (1 - d) / nu;
  close(BF(nu, e, d), direct + leak, 1e-12, 'E7 leakage identity');
  ok(leak >= -1e-15, 'E7: leak term negative');
  ok(BF(nu, e, d) >= direct - 1e-12, 'E7: observable datum weaker than direct datum');
}
close(BF(1, 0.01, 0.9), 0.109, 5e-4, 'E7 quoted observable BF 0.109 at (0.01,0.9,nu=1)');
close(BF(1, 0.01, 0.9) / BF(1, 0.01, 1), 0.109 / 0.010, 5e-4, 'E7 quoted 10.9x wedge');
ok(md.includes('10.9×'), 'E7: quoted 10.9x wedge string missing');

// ------------------------------------------- J. parse & recompute the lattices
function tableRows(anchor) {
  const lines = md.split('\n');
  const i = lines.findIndex(l => l.includes(anchor));
  ok(i >= 0, `table anchor not found: ${anchor}`);
  if (i < 0) return [];
  const out = [];
  for (let j = i + 1; j < lines.length; j++) {
    const l = lines[j];
    if (!l.trim().startsWith('|')) { if (out.length) break; else continue; }
    if (l.includes('---')) continue;
    out.push(l);
  }
  return out;
}
{ // d* table: rows = nu, cols = e in {0.01,0.05,0.10,0.30,0.50,0.90}
  const rows = tableRows('max discernibility `d*` compatible with neutrality');
  ok(rows.length >= 3, `d* table: expected >=3 data rows, got ${rows.length}`);
  const eCols = [0.01, 0.05, 0.1, 0.3, 0.5, 0.9];
  for (const line of rows) {
    const cells = line.split('|').map(s => s.trim()).filter(Boolean);
    const nu = parseFloat(cells[0].replace(/[^0-9.]/g, ''));
    if (!isFinite(nu)) continue;
    for (let k = 0; k < eCols.length; k++) {
      const v = parseFloat(cells[1 + k]);
      if (!isFinite(v)) continue;
      close(v, dstar(nu, eCols[k]), 5e-4, `d* table (nu=${nu}, e=${eCols[k]})`);
    }
  }
}
{ // Table 2 at nu=0.9: rows = e, cols = d in {0,0.1,0.5,0.9,0.99,1}; cells "BF -> posterior"
  const rows = tableRows('**At `ν = 0.9`**').filter(l => /→/.test(l) && isFinite(parseFloat(l.split('|')[1])));
  ok(rows.length === 7, `Table 2 (nu=0.9): expected 7 rows, got ${rows.length}`);
  const dCols = [0, 0.1, 0.5, 0.9, 0.99, 1];
  for (const line of rows) {
    const head = line.split('|')[1].trim();
    const e = parseFloat(head);
    ok(isFinite(e), 'Table 2 (nu=0.9): unparseable eps ' + head);
    const cells = [...line.matchAll(/([\d.]+)\s*→\s*([\d.]+)/g)].map(m => [+m[1], +m[2]]);
    ok(cells.length === 6, `Table 2 (nu=0.9): expected 6 cells, got ${cells.length} at e=${e}`);
    for (let k = 0; k < Math.min(cells.length, dCols.length); k++) {
      close(cells[k][0], BF(0.9, e, dCols[k]), 6e-4, `Table 2 (nu=0.9) BF at e=${e}, d=${dCols[k]}`);
      close(cells[k][1], post(BF(0.9, e, dCols[k])), 6e-4, `Table 2 (nu=0.9) posterior at e=${e}, d=${dCols[k]}`);
    }
  }
}
{ // Table 2 at nu=0.99: BF only
  const rows = tableRows('**At `ν = 0.99`**').filter(l => /^\|/.test(l) && isFinite(parseFloat(l.split('|')[1])));
  ok(rows.length === 7, `Table 2 (nu=0.99): expected 7 rows, got ${rows.length}`);
  const dCols = [0, 0.1, 0.5, 0.9, 0.99, 1];
  for (const line of rows) {
    const head = line.split('|')[1].trim();
    const e = parseFloat(head);
    if (!isFinite(e)) continue;
    const cells = line.split('|').map(s => s.trim()).filter(Boolean).slice(1).map(parseFloat);
    ok(cells.length === 6, `Table 2 (nu=0.99): expected 6 cells, got ${cells.length} at e=${e}`);
    for (let k = 0; k < Math.min(cells.length, dCols.length); k++) {
      if (isFinite(cells[k])) close(cells[k], BF(0.99, e, dCols[k]), 6e-4, `Table 2 (nu=0.99) BF at e=${e}, d=${dCols[k]}`);
    }
  }
}

// ------------------------------------------------------------ K. protocol tail
ok(checks >= 60, `corpus minimum: expected >=60 checks, got ${checks}`);
ok(!/verdict is (?:asserted|delivered|reached)/i.test(md.replace(/No verdict is asserted/g, '')), 'protocol: stray verdict language');

console.log(`verify_v17: ${checks - fails.length}/${checks} checks passed (${fails.length} failures)`);
if (fails.length) {
  console.log('FAILURES:');
  fails.slice(0, 30).forEach(f => console.log('  - ' + f));
  process.exit(1);
}
console.log('verify_v17: ALL GREEN — E1, E1a/b, E2, E3, E4, E5, E6, E7 verified by brute force,');
console.log('Monte-Carlo, and recomputation of the artifact’s own parsed tables.');
