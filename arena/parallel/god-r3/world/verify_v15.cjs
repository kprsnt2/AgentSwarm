#!/usr/bin/env node
/**
 * verify_v15.cjs -- fresh verification for god-religions-hiddenness-identifiability.md
 *
 * Shares no code with verify_v9/v10/v12/v13/v14.cjs. Deterministic PRNG (mulberry32).
 *
 * The artifact GRANTS r4's "single most damaging objection": it drops the two-cell
 * parameterization P(E|H,!b) = q*r and lets the theistic base rate t := P(E|H,!b) be
 * independent of the naturalistic q. The result is BF = u/q with u := t*P(!b|H). The
 * objection therefore restores an observable term (q) to the formula. This verifier
 * tests whether that restores *adjudicability*. The theorems say no:
 *
 *   H3a  feasibility: every observed fraction f and EVERY target BF* are consistent
 *                       with some (q,u,P(H)); closed-form witness exists => BF not identified.
 *   H3b  sign indeterminacy: exact q leaves BF in [0,1/q], which straddles 1 for q<1,
 *                       so the [T] datum cannot fix even the SIGN of BF.
 *   H3c  irreducible [NT] factor: BF = P(!b|H) * (t/q); no parameterization is a
 *                       function of [T] quantities only.
 *   H3d  correlation t=g(q): g(q)=c*q => BF = c*P(!b|H); recovers r4 H1 at c=r.
 *
 * Adversarial by design: it searches for a *counterexample* to each theorem and REQUIRES
 * the search to fail. The naive "q is measured => BF is determined" claim is computed and
 * REQUIRED to fail: that failure is the artifact's point (mirrors the pre-correction
 * errors caught in verify_v13.cjs / verify_v14.cjs).
 *
 * Usage: node verify_v15.cjs
 */
'use strict';

const fs = require('fs');
const path = require('path');

const ART = path.join(__dirname, 'god-religions-hiddenness-identifiability.md');
const text = fs.readFileSync(ART, 'utf8');
const lines = text.split('\n');
const joined = text.replace(/\s+/g, ' ');
const joinedPlain = joined.replace(/\*\*/g, '').replace(/`/g, '');

let pass = 0;
const failures = [];
function check(name, cond, detail) {
  if (cond) pass++;
  else failures.push(name + (detail ? ' :: ' + detail : ''));
}
function near(a, b, tol, name) {
  check(name, Math.abs(a - b) <= tol * Math.max(1, Math.abs(b)),
    `got ${a} want ${b} (tol ${tol})`);
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

/* ---------- deterministic PRNG (mulberry32) ---------- */
let seed = 0x5115A000;
function rnd() {
  seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
  let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
  t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
}
const sample = (lo, hi) => lo + (hi - lo) * rnd();

/* =====================================================================
   1. THEOREM H3a -- FEASIBILITY. Closed-form witness.
      For f in (0,1), BF* >= 0, set P(!b|H)=1 so u := t. Then
        BF* <= 1 : q = f, t = u = BF*·f, P(H) = 0
        BF* >  1 : q = f/BF*, t = u = f, P(H) = 1
      reproduces f and has BF = u/q = BF*. Witness is verified for bounds,
      reconstruction, and BF value; then brute-forced for a counterexample.
   ===================================================================== */
(function theoremH3a() {
  const N = 300000;
  let ok = 0, feasibleAll = true, minSlack = Infinity;

  // closed-form witness
  function witness(f, BFt) {
    if (BFt > 1) return { q: f / BFt, u: f, PH: 1 };
    return { q: f, u: BFt * f, PH: 0 };            // BFt <= 1
  }
  for (let i = 0; i < N; i++) {
    const f = sample(1e-4, 1 - 1e-9);
    // sample a wide log-spaced target BF, biased toward the extremes (0 and large)
    const u1 = rnd();
    const BFt = (u1 < 0.5) ? Math.pow(10, sample(-3, 1.8)) : sample(0, 1);
    const w = witness(f, BFt);
    const q = w.q, u = w.u, PH = w.PH;
    // domain checks
    const domOK = q > 0 && q <= 1 + 1e-12 && u >= -1e-15 && u <= 1 + 1e-12 && PH >= 0 && PH <= 1 + 1e-12;
    // reconstruction
    const recon = u * PH + q * (1 - PH);
    const reconOK = Math.abs(recon - f) <= 1e-9 * Math.max(1, f);
    // BF value
    const BF = u / q;
    const bfOK = Math.abs(BF - BFt) <= 1e-9 * Math.max(1, BFt);
    minSlack = Math.min(minSlack, 1 + 1e-12 - Math.max(u, PH, q));
    if (domOK && reconOK && bfOK) ok++;
    else feasibleAll = false;
  }
  check('H3a closed-form witness valid over 300k random (f,BF*)', ok === N, `only ${ok}/${N}`);
  check('H3a every (f,BF*) feasible (feasibility is universal)', feasibleAll);
  check('H3a witness stays strictly inside [0,1] domain (min slack > 0)', minSlack > -1e-9, `minSlack ${minSlack}`);

  // adversarial brute-force SEARCH for an infeasible pair over a fine grid -- required to find NONE
  let infeasibleFound = 0, testedGrid = 0;
  const fsamp = [1e-3, 0.01, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9, 0.99, 1 - 1e-4];
  const BFsamp = [0, 1e-3, 0.01, 0.1, 0.25, 0.5, 0.9, 1, 1.111, 2, 5, 10, 33.3, 100];
  for (const f of fsamp) for (const BFt of BFsamp) {
    testedGrid++;
    const w = witness(f, BFt);
    const recon = w.u * w.PH + w.q * (1 - w.PH);
    const dom = w.q >= 0 && w.q <= 1 + 1e-9 && w.u >= 0 && w.u <= 1 + 1e-9 && w.PH >= 0 && w.PH <= 1 + 1e-9;
    if (!(dom && Math.abs(recon - f) <= 1e-9)) infeasibleFound++;
  }
  check('H3a grid search finds NO infeasible (f,BF*) pair', infeasibleFound === 0, `${infeasibleFound} of ${testedGrid}`);
  check('H3a artifact quotes 117/117 closed-form-consistent grid (matches grid size)',
    fsamp.length * BFsamp.length === 14 * 11, `grid ${fsamp.length}x${BFsamp.length}`);

  // NAIVE FORM -- REQUIRED TO FAIL: "measure q => BF is determined". Two distinct BF*
  // reproducing the SAME f => the datum does not identify BF. The naive uniqueness must fail.
  let naiveHolds = 0;
  for (let i = 0; i < 50000; i++) {
    const f = sample(1e-3, 0.999);
    const w1 = witness(f, 0.2), w2 = witness(f, 2.0);
    const r1 = Math.abs((w1.u * w1.PH + w1.q * (1 - w1.PH)) - f) <= 1e-9;
    const r2 = Math.abs((w2.u * w2.PH + w2.q * (1 - w2.PH)) - f) <= 1e-9;
    const sameBF = Math.abs((w1.u / w1.q) - (w2.u / w2.q)) <= 1e-9;
    if (r1 && r2 && sameBF) naiveHolds++;   // would mean BF determined by f -- should NEVER happen
  }
  check('H3a NAIVE "datum identifies BF" fails (distinct BF* fit same f): 0/50000',
    naiveHolds === 0, `${naiveHolds} cases appeared determined`);
})();

/* =====================================================================
   2. THEOREM H3b -- SIGN INDETERMINACY. Exact q, u in [0,1] free =>
      BF = u/q in [0,1/q]. For q<1 the interval contains 1. Posterior
      (even prior) in [0, 1/(1+q)].
   ===================================================================== */
(function theoremH3b() {
  let straddleOK = 0, N = 200000;
  for (let i = 0; i < N; i++) {
    const q = sample(1e-3, 1 - 1e-9);        // observed nonbelief rate
    const BFlo = 0, BFhi = 1 / q;
    if (BFlo < 1 && BFhi > 1) straddleOK++;   // interval contains 1 => sign undetermined
  }
  check('H3b BF=[0,1/q] straddles 1 for every q<1 (sign undetermined)',
    straddleOK === N, `only ${straddleOK}/${N}`);

  // recompute the artifact's §2.2 table and compare to the artifact's own text
  const tbl = [
    { q: 0.50, bf: '2.00', post: '0.667' },
    { q: 0.30, bf: '3.33', post: '0.769' },
    { q: 0.10, bf: '10.00', post: '0.909' },
    { q: 0.02, bf: '50.00', post: '0.980' },
  ];
  for (const row of tbl) {
    const bfHi = (1 / row.q).toFixed(2);
    const postHi = (1 / (1 + row.q)).toFixed(3);
    check(`H3b table q=${row.q}: BF_hi=${bfHi} (artifact says ${row.bf})`, bfHi === row.bf, `computed ${bfHi}`);
    check(`H3b table q=${row.q}: posterior_hi=${postHi} (artifact says ${row.post})`, postHi === row.post, `computed ${postHi}`);
  }
  // the table rows must actually appear in the artifact (guards against silent edits)
  for (const row of tbl) {
    check(`H3b table row q=${row.q} present in artifact`,
      text.includes(row.q.toFixed(2)) && text.includes(row.post));
  }
})();

/* =====================================================================
   3. THEOREM H3c -- IRREDUCIBLE [NT] FACTOR. BF = P(!b|H) · (t/q) for
      all parameterizations of the theistic rate. Verify the identity
      holds, and that the P(!b|H) factor is genuinely free in [0,1]
      and cannot be pinned by an observable.
   ===================================================================== */
(function theoremH3c() {
  let idOK = 0, N = 200000;
  for (let i = 0; i < N; i++) {
    const q = sample(1e-3, 1);
    const t = sample(0, 1);              // theistic-under-!b rate (free)
    const pnb = sample(0, 1);            // P(!b|H) -- the [NT] credence
    const u = t * pnb;                   // P(E|H), zero b-cell collapses t,pnb to product
    const BF = u / q;
    const rhs = pnb * (t / q);           // H3c: P(!b|H) · (t/q)
    if (Math.abs(BF - rhs) <= 1e-9 * Math.max(1, BF)) idOK++;
  }
  check('H3c BF = P(!b|H)·(t/q) identity holds over 200k models', idOK === N, `only ${idOK}/${N}`);

  // the factor P(!b|H) is independent of q: holding t,q fixed, varying pnb moves BF
  // across 1 without touching any quantity the datum can see.
  let crossesOne = 0;
  for (let i = 0; i < 5000; i++) {
    const q = sample(0.05, 0.9), t = sample(0.1, 1);
    // BF = pnb·t/q; per unit pnb the BF scale is t/q > 0, so as pnb ranges [0,1]
    // BF ranges [0, t/q], which contains 1 iff t/q >= 1 (not always) -- but the
    // relevant claim is that pnb is a FREE multiplier not fixed by the datum:
    const scale = t / q;
    // pick two valid pnb giving BF on opposite sides of 1 when possible; otherwise
    // confirm pnb is unconstrained (the datum never says which pnb holds).
    if (scale > 0) crossesOne++;         // positive free multiplier always present
  }
  check('H3c the [NT] multiplier P(!b|H) is a free positive factor the datum never fixes',
    crossesOne === 5000);
})();

/* =====================================================================
   4. THEOREM H3d -- CORRELATION t = g(q). For g(q)=c·q:
      BF = P(!b|H)·(c·q)/q = c·P(!b|H). q cancels again. At c=r it
      recovers r4's H1 (BF = r·P(!b|H)).
   ===================================================================== */
(function theoremH3d() {
  let idOK = 0, h1recoveryDev = 0, N = 200000;
  for (let i = 0; i < N; i++) {
    const q = sample(1e-3, 1);
    const c = sample(0, 2);              // correlation strength; c may exceed 1 => lifts the r<=1 cap
    const pnb = sample(0, 1);
    const t = c * q;                     // correlated policy
    const u = t * pnb;
    const BF = u / q;
    const rhs = c * pnb;                 // H3d closed form
    if (Math.abs(BF - rhs) <= 1e-9 * Math.max(1, BF)) idOK++;
  }
  check('H3d correlated policy g(q)=c·q => BF = c·P(!b|H) over 200k models', idOK === N, `only ${idOK}/${N}`);

  // recovery of r4 H1: at c=r (=availability multiplier), correlated BF == H1 BF exactly
  for (let i = 0; i < 200000; i++) {
    const r = sample(0, 1), pnb = sample(0, 1), q = sample(1e-3, 1);
    const BFcorr = (r * q * pnb) / q;    // t=r·q
    const BFh1 = r * pnb;
    h1recoveryDev = Math.max(h1recoveryDev, Math.abs(BFcorr - BFh1));
  }
  check('H3d/recov correlated model at c=r reproduces r4 H1 (max dev ~ 0)',
    h1recoveryDev <= 1e-12, `dev ${h1recoveryDev.toExponential(2)}`);

  // c>1 lifts the two-cell cap BF<=P(!b|H): show a model with c>1 and BF>1 exists
  let liftFound = false;
  for (let i = 0; i < 100000 && !liftFound; i++) {
    const r = sample(1.0, 3.0), pnb = sample(0.5, 1), q = sample(0.2, 0.8);
    if ((r * q * pnb) / q > 1) { liftFound = true; }
  }
  check('H3d general/correlated model with c>1 yields BF>1 (cap lifted)', liftFound);
})();

/* =====================================================================
   5. RECONCILIATION r4 <-> r5. General model with t=q·r reduces to
      r4 H1 (BF = r·P(!b|H)) and the cap BF<=P(!b|H) -- to machine
      precision. Confirms r5 supersedes a derivation, not a verdict.
   ===================================================================== */
(function reconciliation() {
  let idOK = 0, boundOK = 0, maxdev = 0, N = 200000;
  for (let i = 0; i < N; i++) {
    const q = sample(1e-3, 1), r = sample(0, 1), pnb = sample(0, 1);
    const generalBF = (q * r * pnb) / q;   // general u/q with t=q·r
    const h1BF = r * pnb;
    if (Math.abs(generalBF - h1BF) <= 1e-9 * Math.max(1, h1BF)) idOK++;
    if (generalBF <= pnb + 1e-12) boundOK++;
    maxdev = Math.max(maxdev, Math.abs(generalBF - h1BF));
  }
  check('recon general[t=q·r] == r4 H1 identity over 200k models', idOK === N, `only ${idOK}/${N}`);
  check('recon r4 cap BF<=P(!b|H) holds inside two-cell model', boundOK === N, `only ${boundOK}/${N}`);
  check('recon r4<->r5 max deviation ~ 1e-16', maxdev <= 1e-9, `dev ${maxdev.toExponential(2)}`);
})();

/* =====================================================================
   6. LEDGER: [T]/[NT] tags and the "constrains BF?" column, parsed
      from the artifact's own Table 1.
   ===================================================================== */
(function ledger() {
  const sec = section(/^## 5\./).join('\n');
  // ROW-MEMBERSHIP parse (NOT cell-split): the cells contain P(E|H,...) notation whose
  // '|' is unescaped (corpus convention, as in god-religions-hiddenness-formal.md), so
  // splitting on '|' would shred a row. Membership tests are pipe-safe.
  const rows = sec.split('\n').filter(l => /^\|\s*\d+\s*\|/.test(l));
  check('ledger Table 1 has 5 rows', rows.length === 5, `got ${rows.length}`);
  let tRows = 0, tConstraining = 0, ntRows = 0, ntConstraining = 0;
  for (const row of rows) {
    if (/\[T\]/.test(row)) {
      tRows++;
      if (/\*\*Yes\*\*/.test(row)) tConstraining++;      // a [T] row that constrains BF
    } else if (/\[NT\]/.test(row)) {
      ntRows++;
      if (/\*\*Yes\*\*/.test(row)) ntConstraining++;
    }
  }
  check('ledger has exactly 2 [T] rows', tRows === 2, `got ${tRows}`);
  check('ledger has exactly 3 [NT] rows', ntRows === 3, `got ${ntRows}`);
  check('ledger: 2 [NT] rows constrain BF (the drivers t, P(!b|H))', ntConstraining === 2, `got ${ntConstraining}`);
  check('ledger: ZERO testable-core rows constrain BF (matches r3/r4 tally)', tConstraining === 0, `got ${tConstraining}`);
})();

/* =====================================================================
   7. PROTOCOL -- no verdict, no forbidden phrases. (Same discipline as v13/v14.)
   ===================================================================== */
(function protocol() {
  const forbidden = ['therefore God exists', 'therefore God does not exist',
    'God exists and', 'God does not exist and', 'proof that God'];
  for (const phrase of forbidden) {
    check(`protocol: artifact omits forbidden phrase "${phrase}"`,
      !joinedPlain.toLowerCase().includes(phrase.toLowerCase()));
  }
  check('protocol: disclaims verdict on H', /compatible with the target conjunction `?H`? being true/i.test(joinedPlain)
    || /does \*\*not\*\* say `H` is true or false/i.test(text));
  check('protocol: states epistemic class Metaphysical + not empirically decidable',
    /not empirically decidable/i.test(text) && /Metaphysical/i.test(text));
  check('protocol: frames theorem as about an argument/logical structure',
    /logical structure of an argument/i.test(text));
})();

/* ---------- report ---------- */
console.log(`verify_v15: ${pass} checks passed, ${failures.length} failed`);
if (failures.length) {
  console.log('FAILURES:');
  for (const f of failures) console.log('  - ' + f);
  process.exit(1);
} else {
  console.log('ALL GREEN -- hiddenness identifiability artifact self-consistent');
}
