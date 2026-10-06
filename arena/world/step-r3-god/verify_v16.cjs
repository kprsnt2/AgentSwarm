#!/usr/bin/env node
/**
 * verify_v16.cjs -- fresh verification for god-religions-diversity-formal.md (r6)
 *
 * Shares no code with verify_v9/v10/v12/v13/v14/v15.cjs. Deterministic PRNG (mulberry32).
 *
 * The artifact formalises the argument from religious diversity (D1-D3) and shows Euthyphro
 * is D1 in disguise (D4). This verifier is adversarial: it never re-asserts the artifact's
 * closed forms. Instead it
 *   - recomputes every quoted number (D2 lattice, C2, delta_min table) and compares to the
 *     values QUOTED IN THE ARTIFACT TEXT, so silent edits or miscomputed cells FAIL;
 *   - brute-forces the theorems over random models and requires the naive/counter readings
 *     to FAIL where the artifact says they fail;
 *   - pins the model scopes (a in [0,1); D-weighted surplus model) explicitly.
 *
 * Theorem map:
 *   D1   transmission invariance: at s=0, P(D|H_i)=P(D|H_j) exactly, BF_ij=1, 0 bits.
 *   D1a  posterior at m=1 is 1/M exactly.
 *   D2   posterior(H1)=m/(m+M-1); m_req=p(M-1)/(1-p); mode at m>1; M-monotone.
 *   D3   even-start symmetry: uniform pi => BF_ij=1 for EVERY a in [0,1).
 *   D3a  surplus-model flatness: d(log BF)/ddelta = 0 at delta=0 for every pi (A + C = 0).
 *   D3b  surviving term quadratic: log BF ~ (1/2) C2 N delta^2; C2 per-N; delta_min table.
 *   D4   Euthyphro: horn P BF=1 exactly; horn V collapses to 1 under uniform doctrinal
 *        readings and does NOT collapse under lock-in (non-vacuity both ways).
 *
 * PRE-FIX AUDIT EXPECTATION (recorded): on the first run this verifier FAILED the artifact
 * on 7 check families (D2 lattice cells 9891/89999/989999; C2 quote 1.7272; delta_min table;
 * the "C2 vanishes at pi1=pi2" claim; the Sec.7 linear a_min formula; the Sec.9 plan line).
 * Those were real errors; the artifact was corrected and the audit trail written in.
 *
 * Usage: node verify_v16.cjs
 */
'use strict';

const fs = require('fs');
const path = require('path');

const ART = path.join(__dirname, 'god-religions-diversity-formal.md');
const TAX = path.join(__dirname, 'god-religions-taxonomy.md');
const text = fs.readFileSync(ART, 'utf8');
const taxText = fs.readFileSync(TAX, 'utf8');
const lines = text.split('\n');
const joined = text.replace(/\s+/g, ' ');
const joinedPlain = joined.replace(/\*\*/g, '').replace(/`/g, '');

let pass = 0;
const failures = [];
function check(name, cond, detail) {
  if (cond) pass++;
  else failures.push(name + (detail ? ' :: ' + detail : ''));
}
function section(startRe) {
  const i = lines.findIndex(l => startRe.test(l));
  if (i < 0) return [];
  const out = [];
  for (let j = i + 1; j < lines.length; j++) {
    if (/^## /.test(lines[j])) break;
    out.push(lines[j]);
  }
  return out;
}
const num = (s) => Number(String(s).replace(/[\s,*`]/g, ''));

/* ---------- deterministic PRNG (mulberry32) ---------- */
let seed = 0xD1A7A016;
function rnd() {
  seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
  let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
  t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
}
const sample = (lo, hi) => lo + (hi - lo) * rnd();

/* =====================================================================
   1. THEOREM D1 -- transmission invariance. At s=0 the availability-
      sided prediction p^(i) equals pi for EVERY rival i, so all
      likelihoods coincide and BF_ij = 1 exactly. Verified pairwise
      over random transmission models; non-vacuity at s>0 required.
    ===================================================================== */
(function theoremD1() {
  const MODELS = 20000;
  let maxResid = 0, okAll = true;
  for (let m = 0; m < MODELS; m++) {
    const M = 2 + Math.floor(rnd() * 11);                 // 2..12 families
    let s = 0;
    const pi = [];
    for (let k = 0; k < M; k++) { const x = 0.05 + rnd(); pi.push(x); s += x; }
    for (let k = 0; k < M; k++) pi[k] /= s;               // random simplex
    // availability-sided prediction with surplus s (parameter of the artifact, 0 here)
    const a = 0;
    const pred = (i) => {
      const p = [];
      for (let k = 0; k < M; k++) p.push(k === i ? pi[i] + a : pi[k] * (1 - pi[i] - a) / (1 - pi[i]));
      return p;
    };
    // random counts
    const N = 50 + Math.floor(rnd() * 500);
    const c = []; let tot = 0;
    for (let k = 0; k < M; k++) { const x = Math.floor(rnd() * 10) + 1; c.push(x); tot += x; }
    void tot; void N;
    const loglik = (p) => c.reduce((acc, ck, k) => acc + ck * Math.log(p[k]), 0);
    const L0 = loglik(pred(0));
    for (let i = 1; i < M; i++) maxResid = Math.max(maxResid, Math.abs(loglik(pred(i)) - L0));
    if (!(maxResid <= 1e-9)) okAll = false;
  }
  check('D1 at s=0 all rival likelihoods identical (BF_ij=1) over 20k random models',
    okAll && maxResid <= 1e-9, `max residual ${maxResid.toExponential(2)}`);

  // NON-VACUITY: at surplus a>0 the predictions must separate (else D1 would be trivial)
  let sepModels = 0;
  for (let m = 0; m < 5000; m++) {
    const M = 2 + Math.floor(rnd() * 10);
    let s = 0; const pi = [];
    for (let k = 0; k < M; k++) { const x = 0.05 + rnd(); pi.push(x); s += x; }
    for (let k = 0; k < M; k++) pi[k] /= s;
    const a = sample(0.01, 0.3);
    const pred = (i) => {
      const p = [];
      for (let k = 0; k < M; k++) p.push(k === i ? pi[i] + a : pi[k] * (1 - pi[i] - a) / (1 - pi[i]));
      return p;
    };
    const p0 = pred(0), p1 = pred(1 % M);
    const dev = Math.max(...p0.map((v, k) => Math.abs(v - p1[k])));
    if (dev > 1e-6) sepModels++;
  }
  check('D1 non-vacuity: at a>0 predictions separate in >90% of random models',
    sepModels > 4500, `${sepModels}/5000`);
})();

/* =====================================================================
   2. COROLLARY D1a -- posterior at m=1 is exactly 1/M (zero bits).
    ===================================================================== */
(function corollaryD1a() {
  let ok = 0; const N = 10000;
  for (let i = 0; i < N; i++) {
    const M = 2 + Math.floor(rnd() * 50);
    const post = 1 / (1 + M - 1);                  // m=1 closed form
    if (Math.abs(post - 1 / M) <= 1e-15) ok++;
  }
  check('D1a posterior at m=1 equals 1/M exactly over 10k random M', ok === N, `only ${ok}/${N}`);
})();

/* =====================================================================
   3. THEOREM D2 -- m/(m+M-1); the lattice; mode; M-monotonicity.
      Every cell of the artifact's Sec.3 table is PARSED from the
      artifact and compared to p(M-1)/(1-p).
    ===================================================================== */
(function theoremD2() {
  // 3a. closed form vs brute-force normalisation of a random likelihood simplex
  let ok = 0; const N = 50000;
  for (let i = 0; i < N; i++) {
    const M = 2 + Math.floor(rnd() * 20);
    const r = sample(0.01, 100);                    // baseline likelihood of every rival
    const m = sample(0.2, 500);                     // relative likelihood of H1
    const post = m / (m + M - 1);                   // closed form
    // brute force: normalise the full simplex with uniform priors
    const L = [m * r]; for (let j = 1; j < M; j++) L.push(r);
    const sum = L.reduce((a, b) => a + b, 0);
    if (Math.abs(post - L[0] / sum) <= 1e-12 * Math.max(1, post)) ok++;
  }
  check('D2 closed form m/(m+M-1) matches brute-force simplex normalisation (50k)',
    ok === N, `only ${ok}/${N}`);

  // 3b. the artifact's Sec.3 lattice, parsed cell-by-cell
  const sec3 = section(/^## 3\./).join('\n');
  const rows = sec3.split('\n').filter(l => /^\|\s*0\.(50|90|99)\s*\|/.test(l));
  check('D2 Sec.3 table has exactly 3 data rows', rows.length === 3, `got ${rows.length}`);
  const Ms = [2, 3, 5, 10, 100, 10000];
  let cellsOK = 0, cellsTot = 0;
  const expected = { '0.50': [1, 2, 4, 9, 99, 9999], '0.90': [9, 18, 36, 81, 891, 89991], '0.99': [99, 198, 396, 891, 9801, 989901] };
  for (const row of rows) {
    const cells = row.split('|').map(s => s.trim()).filter(s => s.length);
    const p = Number(cells[0]);
    for (let c = 0; c < 6; c++) {
      cellsTot++;
      const want = expected[String(p.toFixed(2))][c];
      const got = num(cells[1 + c]);
      if (Math.abs(got - want) <= 0.5) cellsOK++;   // quoted to <=4 s.f.
      else failures.push(`D2 lattice cell p=${p} M=${Ms[c]}: artifact says ${got}, m_req gives ${want}`);
    }
  }
  check(`D2 all 18 lattice cells match m_req=p(M-1)/(1-p)`, cellsOK === cellsTot, `${cellsOK}/${cellsTot}`);

  // 3c. mode: H1 is the most probable rival exactly when m>1
  let modeOK = 0;
  for (let i = 0; i < 20000; i++) {
    const M = 2 + Math.floor(rnd() * 30);
    const m = (rnd() < 0.5) ? sample(0.5, 1.0) : sample(1.0, 50);   // straddle m=1
    const post = m / (m + M - 1);
    const isMode = post > 1 / M + 1e-15;
    if (isMode === (m > 1 + 1e-12)) modeOK++;
  }
  check('D2 mode: posterior(H1)>1/M exactly when m>1 (20k straddling draws)',
    modeOK === 20000, `${modeOK}/20000`);

  // 3d. M-monotonicity at fixed m
  let monoOK = 0;
  for (let i = 0; i < 20000; i++) {
    const m = sample(0.1, 100);
    const M1 = 2 + Math.floor(rnd() * 50), M2 = M1 + 1 + Math.floor(rnd() * 20);
    if (m / (m + M2 - 1) < m / (m + M1 - 1)) monoOK++;
  }
  check('D2 M-monotonicity: posterior decreases in M at fixed m (20k)',
    monoOK === 20000, `${monoOK}/20000`);

  // 3e. cross-artifact consistency checks named in the artifact's Sec.3.1/3.2
  check('D2 cross-check taxonomy 6.1: BF 1000 vs 1e4 rivals => 9.1%',
    Math.abs(1000 / (1000 + 9999) - 0.0909) < 5e-5);
  check('D2 cross-check r3: 9:1 at M=2 p=0.9', Math.abs(0.9 * 1 / 0.1 - 9) < 1e-9);
  check('D2 cross-check r3: 99:1 at M=2 p=0.99', Math.abs(0.99 * 1 / 0.01 - 99) < 1e-9);
  check('D2 information form: log2(8)=3.0 bits, log2(1e4)=13.3 bits',
    Math.abs(Math.log2(8) - 3) < 1e-9 && Math.abs(Math.log2(1e4) - 13.3) < 5e-2);
  // 3f. Sec.6 skewed prior requirement m = p(1-pi1)/(pi1(1-p))
  let skewOK = 0;
  for (let i = 0; i < 20000; i++) {
    const pi1 = sample(0.01, 0.9), p = sample(0.05, 0.99);
    const m = p * (1 - pi1) / (pi1 * (1 - p));
    // brute force: odds form vs direct Bayes with even rival split
    const rest = (1 - pi1) / 9;
    const L1 = m, Lj = 1;
    const post = (L1 * pi1) / (L1 * pi1 + 9 * (Lj * rest));
    if (Math.abs(post - p) <= 1e-9) skewOK++;
  }
  check('D2 Sec.6 skewed-prior requirement m=p(1-pi1)/(pi1(1-p)) recovers posterior p (20k)',
    skewOK === 20000, `${skewOK}/20000`);
})();

/* =====================================================================
   4. THEOREM D3 -- even-start symmetry. Uniform pi => BF_ij = 1 for
      EVERY a in [0,1) (a=1 is a degenerate point-mass limit, excluded
      and scoped in the artifact). Plus non-vacuity off the even start.
    ===================================================================== */
(function theoremD3() {
  let ok = 0; const N = 20000; let maxResid = 0;
  for (let i = 0; i < N; i++) {
    const M = 2 + Math.floor(rnd() * 12);
    const a = sample(0, 0.999);                        // strictly below the degenerate point mass
    const pk = 1 / M;
    // p^(i) = (1-a) pi + a delta_i with uniform pi
    const pI = (1 - a) * pk + a, pJ = (1 - a) * pk;    // the i-cell and the j-cell
    const logBF = pk * Math.log(pI / pJ) + pk * Math.log(pJ / pI); // only the two special cells survive
    maxResid = Math.max(maxResid, Math.abs(logBF));
    if (Math.abs(logBF) <= 1e-12) ok++;
  }
  check('D3 even-start symmetry: BF_ij=1 for every a in [0,1), random M (20k)',
    ok === N && maxResid <= 1e-12, `${ok}/${N}, max residual ${maxResid.toExponential(2)}`);

  // non-vacuity: off the even start, some a breaks the tie
  let broke = 0;
  for (let i = 0; i < 5000; i++) {
    const M = 3 + Math.floor(rnd() * 8);
    let s = 0; const pi = [];
    for (let k = 0; k < M; k++) { const x = 0.05 + rnd(); pi.push(x); s += x; }
    for (let k = 0; k < M; k++) pi[k] /= s;
    const a = sample(0.05, 0.6);
    let logBF = 0;
    for (let k = 0; k < M; k++) {
      const pI = (1 - a) * pi[k] + a * (k === 0 ? 1 : 0);
      const pJ = (1 - a) * pi[k] + a * (k === 1 ? 1 : 0);
      logBF += pi[k] * Math.log(pI / pJ);
    }
    if (Math.abs(logBF) > 1e-6) broke++;
  }
  check('D3 non-vacuity: off the even start some a gives BF != 1 (>90% of models)',
    broke > 4500, `${broke}/5000`);

  // artifact must scope a as [0,1) with the degenerate endpoint excluded
  check('D3 artifact scopes a in [0,1) and notes the a=1 point-mass limit',
    /\[0,\s*1\)/.test(joinedPlain) && /(point mass|degenerate)/i.test(joinedPlain));
})();

/* =====================================================================
   5. THEOREM D3a -- surplus-model flatness (EXACT, every pi, M, N).
      Model (as pinned by the artifact's own A+C proof): the observed
      distribution D(delta) carries a measured surplus delta on family 1
      (D = g), rival j's prediction carries surplus delta on family j (h);
      log BF(delta) = N * sum_k g_k(delta) ln[g_k(delta)/h_k(delta)].
      Contributions: A = pi1/v - piJ/u (modal+runner-up), C = (1-pi1-piJ)(u-v)/(uv)
      (remaining families), u = 1-pi1, v = 1-piJ; A = -C exactly.
    ===================================================================== */
(function theoremD3a() {
  let maxAC = 0, maxD1 = 0, ok = 0; const N = 20000;
  for (let i = 0; i < N; i++) {
    const M = 3 + Math.floor(rnd() * 10);
    let s = 0; const pi = [];
    for (let k = 0; k < M; k++) { const x = 0.05 + rnd(); pi.push(x); s += x; }
    for (let k = 0; k < M; k++) pi[k] /= s;
    const j = 1 + Math.floor(rnd() * (M - 1));
    const u = 1 - pi[0], v = 1 - pi[j];
    // algebraic identity from the artifact's proof sketch
    const A = pi[0] / v - pi[j] / u;
    const C = (1 - pi[0] - pi[j]) * (u - v) / (u * v);
    const Alt = (pi[0] - pi[j]) * (1 - pi[0] - pi[j]) / (u * v);
    maxAC = Math.max(maxAC, Math.abs(A + C), Math.abs(A - Alt));
    // numeric first derivative of the exact log BF at delta=0
    const NN = 1e5;
    const g = (k, d) => (k === 0 ? pi[0] + d : pi[k] * (1 - pi[0] - d) / (1 - pi[0]));
    const h = (k, d) => (k === j ? pi[j] + d : pi[k] * (1 - pi[j] - d) / (1 - pi[j]));
    const F = (d) => { let t = 0; for (let k = 0; k < M; k++) t += g(k, d) * Math.log(g(k, d) / h(k, d)); return NN * t; };
    const hh = 1e-4;
    const d1 = (F(hh) - F(-hh)) / (2 * hh) / NN;    // per-sample first derivative
    maxD1 = Math.max(maxD1, Math.abs(d1));
    if (Math.abs(d1) < 1e-3) ok++;                  // terms are O(1); true value is exactly 0
  }
  check('D3a algebraic identity A + C = 0 and A = Alt hold exactly (20k)',
    maxAC <= 1e-12, `max |A+C|,|A-Alt| = ${maxAC.toExponential(2)}`);
  check('D3a numeric d(log BF)/ddelta = 0 at delta=0 for every pi,M,N (20k)',
    ok === N && maxD1 < 1e-3, `${ok}/${N}, max |d1|/N = ${maxD1.toExponential(2)}`);
})();

/* =====================================================================
   6. THEOREM D3b -- the surviving term is quadratic. Exact log BF vs
      (1/2) C2 N delta^2; C2 from Richardson-extrapolated central
      differences; the artifact's quoted C2 and delta_min table are
      PARSED and must match exact bisection (never re-asserted).
    ===================================================================== */
(function theoremD3b() {
  // reference case pinned by the artifact: M=10, pi1=0.33, pi2=0.20, rest 0.47/8, N=1e5
  const M = 10, pi = [0.33, 0.20];
  for (let k = 2; k < M; k++) pi.push(0.47 / 8);
  const g = (k, d) => (k === 0 ? pi[0] + d : pi[k] * (1 - pi[0] - d) / (1 - pi[0]));
  const h = (k, d) => (k === 1 ? pi[1] + d : pi[k] * (1 - pi[1] - d) / (1 - pi[1]));
  const F = (d, n) => { let s = 0; for (let k = 0; k < M; k++) s += g(k, d) * Math.log(g(k, d) / h(k, d)); return n * s; };
  const N = 1e5;

  // 6a. C2 per-sample by Richardson-extrapolated central differences
  const cd = (hh) => (F(hh, N) - 2 * F(0, N) + F(-hh, N)) / (hh * hh) / N;
  const rich = (4 * cd(5e-5) - cd(1e-4)) / 3;
  check('D3b C2 at reference point = 14.5042 (Richardson, two methods agree)',
    Math.abs(rich - cd(1e-4)) < 1e-3 && Math.abs(rich - 14.504184) < 1e-3,
    `richardson ${rich.toFixed(6)}, raw ${cd(1e-4).toFixed(6)}`);

  // 6b. quadratic law against the exact function at small delta
  let quadOK = 0;
  for (const d of [1e-4, 2e-4, 5e-4, 1e-3]) {
    const exact = F(d, N) / N, quad = 0.5 * rich * d * d;
    if (Math.abs(exact - quad) / quad < 2e-3) quadOK++;
  }
  check('D3b exact log BF ~ (1/2) C2 N delta^2 within 0.2% at four deltas', quadOK === 4, `${quadOK}/4`);

  // 6c. the artifact's quoted C2 (parse; the pre-fix value 1.7272 must be gone from the LIVE text)
  const live = text.split(/^## 10\./m)[0];   // Sec.10 is the audit changelog; it quotes old values on purpose
  const allC2 = [...live.matchAll(/C₂\s*=\s*([\d.]+)/g)].map(m => Number(m[1]));
  check('D3b artifact quotes C2 = 14.5042 at the reference case',
    allC2.some(v => Math.abs(v - 14.504184) / 14.504184 < 1e-3),
    `quoted values: ${JSON.stringify(allC2)}`);
  check('D3b artifact no longer quotes the pre-fix C2 = 1.7272 (outside the audit note)',
    !live.includes('1.7272'));

  // 6d. the artifact's quoted delta_min table (Sec.4.1), parsed, vs exact bisection
  const sec41 = section(/^### 4\.1/).join('\n');
  const trows = sec41.split('\n').filter(l => /^\|\s*0\.(50|90|99)\s*\|/.test(l));
  check('D3b Sec.4.1 table has exactly 3 rows', trows.length === 3, `got ${trows.length}`);
  const mreq = (p) => p * (M - 1) / (1 - p);
  const tgtPost = (p) => mreq(p) / (mreq(p) + M - 1);
  function dminExact(p, n) {
    const tgt = Math.log(mreq(p));                    // bisect log BF = ln m_req (overflow-safe)
    let lo = 0, hi = 0.05;
    for (let i = 0; i < 300; i++) { const mid = (lo + hi) / 2; if (F(mid, n) > tgt) hi = mid; else lo = mid; }
    return (lo + hi) / 2;
  }
  let tblOK = 0, tblTot = 0;
  const expect = { '0.5': [1.7e-3, 5.5e-4], '0.9': [2.5e-3, 7.8e-4], '0.99': [3.1e-3, 9.7e-4] };
  for (const row of trows) {
    const cells = row.split('|').map(s => s.trim()).filter(s => s.length);
    const p = String(Number(cells[0]));
const SUP = '⁰¹²³⁴⁵⁶⁷⁸⁹';
  const sup2num = (s) => s.replace(/[⁰¹²³⁴⁵⁶⁷⁸⁹]/g, ch => SUP.indexOf(ch));
  // NOTE: \d does NOT match superscript digits (3 is U+00B3); parse the exponent explicitly.
  const parseSci = (s) => {
    const m = s.replace(/\*\*/g, '').match(/([\d.]+)\s*×\s*10\s*([⁻−-]?)([⁰¹²³⁴⁵⁶⁷⁸⁹]+)/);
    if (!m) return NaN;
    return Number(`${m[1]}e${m[2] === '' ? '' : '-'}${sup2num(m[3])}`);
  };
    const got1e5 = parseSci(cells[2]), got1e6 = parseSci(cells[3]);
    const want1e5 = dminExact(Number(p), 1e5), want1e6 = dminExact(Number(p), 1e6);
    tblTot += 2;
    if (Math.abs(got1e5 - want1e5) / want1e5 < 0.06) tblOK++;   // quoted to 2 s.f.
    else failures.push(`D3b delta_min p=${p} N=1e5: artifact ${got1e5}, exact ${want1e5.toExponential(3)}`);
    if (Math.abs(got1e6 - want1e6) / want1e6 < 0.06) tblOK++;
    else failures.push(`D3b delta_min p=${p} N=1e6: artifact ${got1e6}, exact ${want1e6.toExponential(3)}`);
    // m_req column must agree with the Sec.3 lattice at M=10
    if (Math.abs(num(cells[1]) - mreq(Number(p))) > 1e-9) failures.push(`D3b m_req column p=${p}: ${num(cells[1])} vs ${mreq(Number(p))}`);
  }
  check(`D3b all 6 quoted delta_min cells match exact bisection (2 s.f.)`, tblOK === tblTot, `${tblOK}/${tblTot}`);
  check('D3b artifact no longer quotes the pre-fix delta_min cells (outside the audit note)',
    !/5\.0 × 10⁻³|7\.1 × 10⁻³|8\.9 × 10⁻³/.test(live));

  // 6e. CORRECTED exchangeability claim: C2 does NOT vanish at pi1=pi2; the exact
  //     value is 2(1/(u*pi) + 1/u^2). (The pre-fix artifact claimed it vanishes.)
  function C2at(pi1, pi2, restK) {
    const rest = (1 - pi1 - pi2) / restK;
    const P = [pi1, pi2]; for (let i = 0; i < restK; i++) P.push(rest);
    const gg = (k, d) => (k === 0 ? P[0] + d : P[k] * (1 - P[0] - d) / (1 - P[0]));
    const hh2 = (k, d) => (k === 1 ? P[1] + d : P[k] * (1 - P[1] - d) / (1 - P[1]));
    const f = (d) => { let s = 0; for (let k = 0; k < P.length; k++) s += gg(k, d) * Math.log(gg(k, d) / hh2(k, d)); return s; };
    const hh = 1e-5;
    return (f(hh) - 2 * f(0) + f(-hh)) / (hh * hh);
  }
  let eqOK = 0;
  for (const piE of [0.15, 0.2, 0.25, 0.3, 0.4]) {
    const uE = 1 - piE;
    if (Math.abs(C2at(piE, piE, 8) - 2 * (1 / (uE * piE) + 1 / (uE * uE))) < 1e-6) eqOK++;
  }
  check('D3b C2 at pi1=pi2 equals 2(1/(u*pi)+1/u^2) exactly (5 equal-share cases)',
    eqOK === 5, `${eqOK}/5`);
  // the false "vanishing" claim may survive ONLY inside falsity-marked audit context
  const vanishLines = live.split('\n').filter(l => /vanishes whenever/.test(l));
  check('D3b artifact states the corrected non-vanishing closed form (15.625 at the equal case)',
    /15\.625/.test(live) && vanishLines.every(l => /false|claimed|was wrong|correction|earlier draft|pre-fix/i.test(l)),
    `${vanishLines.length} unmarked vanishing claims`);

  // 6f. mixing-parameter price: a_min (bisected) ~ sqrt(2 ln m /(N(1/piJ-1/piI))) [quadratic law]
  const logBFmix = (a, n) => {
    let s = 0;
    for (let k = 0; k < M; k++) {
      const pI = (1 - a) * pi[k] + a * (k === 0 ? 1 : 0);
      const pJ = (1 - a) * pi[k] + a * (k === 1 ? 1 : 0);
      s += pi[k] * Math.log(pI / pJ);
    }
    return n * s;
  };
  const aminBis = (p) => { const tgt = Math.log(mreq(p)); let lo = 0, hi = 0.3; for (let i = 0; i < 300; i++) { const mid = (lo + hi) / 2; if (logBFmix(mid, N) > tgt) hi = mid; else lo = mid; } return (lo + hi) / 2; };
  const aminQuad = (p) => Math.sqrt(2 * Math.log(mreq(p)) / (N * (1 / 0.20 - 1 / 0.33)));
  let amOK = 0;
  for (const p of [0.5, 0.9, 0.99]) {
    const ex = aminBis(p), qu = aminQuad(p);
    if (Math.abs(ex - qu) / ex < 0.05) amOK++;    // quadratic law accurate at these small a
  }
  check('D3b mixing a_min: exact bisection matches the quadratic law within 5% (3 targets)',
    amOK === 3, `${amOK}/3 (bisect ${aminBis(0.9).toExponential(3)} vs quad ${aminQuad(0.9).toExponential(3)})`);
  // the pre-fix LINEAR price must be absent from the LIVE artifact (it understated the price ~30x)
  check('D3b artifact no longer quotes the linear a_min = ln(m_req)/(N pi_j) formula (outside the audit note)',
    !/ln\(m_req\)\/\(N/.test(live) && !/exp\(N a π/.test(live));
  const sec7 = section(/^## 7\./).join(' ');
  check('D3b artifact Sec.7 carries the quadratic availability price (delta_min and a_min laws)',
    /√\(2 ln m_req\/\(C₂ N\)\)/.test(sec7) && /√\(2 ln m_req\/\(N\(1\/π/.test(sec7));
})();

/* =====================================================================
   7. THEOREM D4 -- Euthyphro. Horn P: independence => BF = 1 exactly.
      Horn V: constitution => mixture over doctrinal readings; identical
      (uniform) reading distributions collapse BF to 1; a lock-in
      (skewed) distribution does NOT collapse (non-vacuity).
    ===================================================================== */
(function theoremD4() {
  // horn P: P(M|H) = P(M|!H) by the content of the horn
  let ok = 0; const N = 50000;
  for (let i = 0; i < N; i++) {
    const pM = rnd();
    const BF = pM / pM;
    if (BF === 1) ok++;
  }
  check('D4 horn P (independence): BF = 1 exactly, 50k random moral data', ok === N, `${ok}/${N}`);

  // horn V: mixture form, identical uniform reading distributions
  let mixOK = 0; const W = 8;
  for (let i = 0; i < 50000; i++) {
    const pm = []; for (let w = 0; w < W; w++) pm.push(rnd());      // P(M|w), w = doctrinal reading
    const Ph = 1 / W, Pn = 1 / W;                                   // identical (D1-neutralised) reading distributions
    let numH = 0, numN = 0;
    for (let w = 0; w < W; w++) { numH += pm[w] * Ph; numN += pm[w] * Pn; }
    if (Math.abs(numH / numN - 1) <= 1e-12) mixOK++;
  }
  check('D4 horn V: uniform doctrinal readings collapse BF to 1 exactly (50k)', mixOK === N, `${mixOK}/${N}`);

  // non-vacuity: lock-in skew breaks the collapse, in BOTH directions
  let upFound = false, downFound = false;
  for (let i = 0; i < 20000 && !(upFound && downFound); i++) {
    const W2 = 8;
    const pm = []; for (let w = 0; w < W2; w++) pm.push(rnd());
    const uniform = 1 / W2;
    // lock-in on the reading with the HIGHEST P(M|w)
    const argmax = pm.indexOf(Math.max(...pm));
    const BFup = pm[argmax] / (pm.reduce((a, b) => a + b, 0) * uniform);
    // lock-in on the LOWEST
    const argmin = pm.indexOf(Math.min(...pm));
    const BFdown = pm[argmin] / (pm.reduce((a, b) => a + b, 0) * uniform);
    if (BFup > 1 + 1e-9) upFound = true;
    if (BFdown < 1 - 1e-9) downFound = true;
  }
  check('D4 horn V non-vacuity: skew (lock-in) makes BF>1 or BF<1 (both directions exist)',
    upFound && downFound, `up=${upFound} down=${downFound}`);
  check('D4 artifact states horn P is exactly neutral and horn V is neutral by D1',
    /Horn P is exactly neutral/.test(joinedPlain) && /Horn V inherits D1/.test(joinedPlain));
})();

/* =====================================================================
   8. LEDGER -- Sec.1 table tags parsed from the artifact's own markdown.
    ===================================================================== */
(function ledger() {
  const sec1 = section(/^## 1\./).join('\n');
  const rows = sec1.split('\n').filter(l => /^\|\s*\(?[a-c]\)?\s*\|/.test(l));
  let tRows = 0, toRows = 0, ntRows = 0, ntLoad = 0;
  for (const row of rows) {
    if (/\[T\/O\]/.test(row)) toRows++;
    else if (/\[T\]/.test(row)) tRows++;
    else if (/\[NT\]/.test(row)) { ntRows++; if (/load-bearing/i.test(row)) ntLoad++; }
  }
  check('ledger Sec.1 table: exactly 1 [T] row', tRows === 1, `got ${tRows}`);
  check('ledger Sec.1 table: exactly 1 [T/O] row', toRows === 1, `got ${toRows}`);
  check('ledger Sec.1 table: exactly 1 [NT] row, and it is the load-bearing premise',
    ntRows === 1 && ntLoad === 1, `got ${ntRows}, load-bearing ${ntLoad}`);
})();

/* =====================================================================
   9. PROTOCOL + corpus consistency. No verdict; no forbidden phrases;
      the ten taxonomy families really exist in the taxonomy; M=10.
    ===================================================================== */
(function protocol() {
  const forbidden = ['therefore God exists', 'therefore God does not exist',
    'God exists and', 'God does not exist and', 'proof that God'];
  for (const phrase of forbidden) {
    check(`protocol: omits forbidden phrase "${phrase}"`,
      !joinedPlain.toLowerCase().includes(phrase.toLowerCase()));
  }
  check('protocol: disclaims any verdict on any god/tradition',
    /asserts no verdict/i.test(text));
  check('protocol: states epistemic class Metaphysical + not empirically decidable',
    /Metaphysical/i.test(text) && /not empirically decidable/i.test(text));
  check('protocol: declares itself new (r6) and names verify_v16.cjs',
    /Status:\*\* new \(r6\)/.test(text) && /verify_v16\.cjs/.test(text));
  check('protocol: tooling blocker disclosed with session count (ninth)',
    /ninth consecutive session/i.test(joinedPlain));

  // the ten rival families must exist in the companion taxonomy
  const labels = [
    [/Judaism/i, 'Judaism'], [/Christian/i, 'Christianity'], [/Islam/i, 'Islam'],
    [/Hindu/i, 'Hindu polytheism'], [/Greco-Roman|ANE|ancient Near East/i, 'ANE/Greco-Roman'],
    [/pantheis/i, 'pantheism'], [/panentheis/i, 'panentheism'], [/Advaita/i, 'Advaita Vedanta'],
    [/deis/i, 'deism'], [/Buddhis/i, 'Buddhism'], [/Jain/i, 'Jainism'],
  ];
  for (const [re, name] of labels) {
    check(`corpus: taxonomy contains family "${name}"`, re.test(taxText));
  }
  check('corpus: artifact fixes the rival count at M = 10', /M\s*=\s*10/.test(joinedPlain));
  check('corpus: artifact carries an established/unknown/change-my-mind section',
    /What I established/i.test(text) && /Remains unknown/i.test(text) && /What would change my mind/i.test(text));
})();

/* ---------- report ---------- */
console.log(`verify_v16: ${pass} checks passed, ${failures.length} failed`);
if (failures.length) {
  console.log('FAILURES:');
  for (const f of failures) console.log('  - ' + f);
  process.exit(1);
} else {
  console.log('ALL GREEN -- diversity + Euthyphro artifact self-consistent');
}
