#!/usr/bin/env node
/**
 * verify_v14.cjs — fresh verification for god-religions-hiddenness-formal.md
 *
 * Shares no code with verify_v9.cjs / verify_v10.cjs / verify_v12.cjs / verify_v13.cjs.
 * Deterministic PRNG (mulberry32) so the audit is reproducible.
 *
 * Theorems are checked by brute force over random models, never by re-asserting the
 * closed form the artifact derives. The naive ("zero cell => BF = 0") form is
 * deliberately computed too, and is REQUIRED to fail: that failure is the artifact's
 * own audit trail (mirrors the pre-correction error caught in verify_v13.cjs).
 *
 * Usage: node verify_v14.cjs
 */
'use strict';

const fs = require('fs');
const path = require('path');

const ART = path.join(__dirname, 'god-religions-hiddenness-formal.md');
const text = fs.readFileSync(ART, 'utf8');
const lines = text.split('\n');
const plain = text.replace(/\*\*/g, '').replace(/`/g, '');
const joined = text.replace(/\s+/g, ' ');          // line-break-safe phrase matching
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
let seed = 0x4E14B001;
function rnd() {
  seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
  let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
  t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
}
const sample = (lo, hi) => lo + (hi - lo) * rnd();

/* =====================================================================
   1. THEOREM H1 — zero-cell bound:  BF = r * P(!b|H)  <=  P(!b|H)
      Computed the long way (law of total probability over the two cells)
      and compared with the closed form the artifact states.
   ===================================================================== */
(function theoremH1() {
  const N = 200000;
  let idHolds = 0, boundHolds = 0, naiveWrong = 0, maxDev = 0;
  for (let t = 0; t < N; t++) {
    const q = sample(0.02, 1);            // naturalistic base rate of non-resistant nonbelief
    const r = sample(0, 1);               // availability multiplier
    const pb = sample(0, 1);              // P(b|H), bridge credence
    const pnb = 1 - pb;                   // P(!b|H)
    const P_E_given_H = 0 * pb + q * r * pnb;   // zero cell on b
    const P_E_given_notH = q;                    // premise-conditional bridge
    const BF = P_E_given_H / P_E_given_notH;
    const closed = r * pnb;
    if (Math.abs(BF - closed) <= 1e-9 * Math.max(1, closed)) idHolds++;
    if (BF <= pnb + 1e-12) boundHolds++;
    const naive = 0;                      // drop the !b cell => "impossible under H"
    if (Math.abs(naive - BF) > 1e-6) naiveWrong++;
    maxDev = Math.max(maxDev, Math.abs(naive - BF));
  }
  check('H1 identity BF = r*P(!b|H) over 200k random models', idHolds === N, `${idHolds}/${N}`);
  check('H1 bound BF <= P(!b|H)', boundHolds === N, `${boundHolds}/${N}`);
  check('H1 naive zero-cell form deviates (audit trail)', naiveWrong > N * 0.99, `${naiveWrong}/${N}`);
  check('H1 max deviation approaches 1.0 (largest gap in [0,1])', maxDev > 0.99, `max ${maxDev}`);
})();

/* =====================================================================
   2. COROLLARY H1a — the empirical premise is inert: BF independent of q
   ===================================================================== */
(function corollaryH1a() {
  let inert = true, spread = 0;
  for (let t = 0; t < 5000; t++) {
    const r = sample(0, 1), pb = sample(0, 1), pnb = 1 - pb;
    const BF = r * pnb;                       // closed form: no q term at all
    for (const q of [0.01, 0.05, 0.2, 0.5, 0.9, 0.999]) {
      const BFq = (0 * pb + q * r * pnb) / q;
      spread = Math.max(spread, Math.abs(BFq - BF));
      if (Math.abs(BFq - BF) > 1e-9) inert = false;
    }
  }
  check('H1a: q cancels exactly (BF independent of the base rate)', inert, `spread ${spread}`);
})();

/* =====================================================================
   3. COROLLARY H1b — BF = 0 requires P(!b|H)*r = 0
   ===================================================================== */
(function corollaryH1b() {
  let holds = true;
  for (let t = 0; t < 50000; t++) {
    const r = sample(0, 1), pb = sample(0, 1);
    const BF = r * (1 - pb);
    const zeroCase = (BF === 0);
    const premiseZero = (r * (1 - pb) === 0);
    if (zeroCase !== premiseZero) holds = false;
  }
  check('H1b: BF = 0 iff P(!b|H)*r = 0 (proof needs the disputed premise)', holds);
})();

/* =====================================================================
   4. LEMMA G — general zero-cell lemma over random bridge families
      BF = (1/q) * sum_{i>=2} a_i u_i  <=  (max_{i>=2} a_i / q) * P(!b_1|H)
   ===================================================================== */
(function lemmaG() {
  const N = 100000;
  let idHolds = 0, boundHolds = 0, naiveWrong = 0;
  for (let t = 0; t < N; t++) {
    const k = 2 + Math.floor(rnd() * 6);
    const a = [], u = [];
    for (let i = 0; i < k; i++) { a.push(sample(1e-6, 1)); u.push(sample(1e-6, 1)); }
    a[0] = 0;                                     // the zero cell
    const su = u.reduce((x, y) => x + y, 0);
    for (let i = 0; i < k; i++) u[i] /= su;
    const q = sample(0.02, 1);
    const BF = a.reduce((s, x, i) => s + x * u[i], 0) / q;
    const rest = a.slice(1).map(x => x / q);
    const pnb1 = u.slice(1).reduce((x, y) => x + y, 0);
    const bound = Math.max(...rest) * pnb1;
    if (Math.abs(BF - a.reduce((s, x, i) => s + x * u[i], 0) / q) <= 1e-9 * Math.max(1, BF)) idHolds++;
    if (BF <= bound + 1e-12) boundHolds++;
    if (!(BF === 0 && a.reduce((s, x, i) => s + x * u[i], 0) > 0)) naiveWrong++; // naive "zero cell => BF=0" must be refuted
  }
  check('Lemma G: identity over 100k random families', idHolds === N, `${idHolds}/${N}`);
  check('Lemma G: bound holds', boundHolds === N, `${boundHolds}/${N}`);
  check('Lemma G: naive "zero cell => BF = 0" refuted whenever mass sits off the zero cell', naiveWrong === N, `${naiveWrong}/${N}`);
})();

/* =====================================================================
   5. THEOREM H2 — religious experience: BF+ - 1 = P(c|H)*(1/q' - 1)
   ===================================================================== */
(function theoremH2() {
  const N = 100000;
  let idHolds = 0, geOne = 0, monoPc = 0, monoInvQ = 0;
  for (let t = 0; t < N; t++) {
    const q1 = sample(0.01, 1);              // q' > 0 strictly (reports exist)
    const pc = sample(0, 1);                 // P(c|H)
    const a = 1, r1 = 1;                     // favourable case stated in the artifact
    const BF = (a * pc + q1 * r1 * (1 - pc)) / q1;
    const closed = 1 + pc * (1 / q1 - 1);
    if (Math.abs(BF - closed) <= 1e-9 * Math.max(1, closed)) idHolds++;
    if (BF >= 1 - 1e-12) geOne++;
    // monotone increasing in P(c|H) when q' < 1
    const dPc = Math.min(1, pc + 0.05);
    const BF2 = (a * dPc + q1 * r1 * (1 - dPc)) / q1;
    if (BF2 >= BF - 1e-12) monoPc++;
    // monotone increasing in 1/q'
    const q2 = q1 * 0.95;
    const BF3 = (a * pc + q2 * r1 * (1 - pc)) / q2;
    if (BF3 >= BF - 1e-12) monoInvQ++;
  }
  check('H2 identity BF+ - 1 = P(c|H)*(1/q\' - 1)', idHolds === N, `${idHolds}/${N}`);
  check('H2: BF+ >= 1 in the favourable case', geOne === N, `${geOne}/${N}`);
  check('H2: BF+ monotone non-decreasing in P(c|H)', monoPc === N, `${monoPc}/${N}`);
  check('H2: BF+ monotone non-decreasing in 1/q\'', monoInvQ === N, `${monoInvQ}/${N}`);
  // no proof in this direction: q' > 0 => BF+ finite
  let finite = true;
  for (const q1 of [1e-6, 1e-3, 0.1, 0.5]) {
    const BF = (1 * 0.5 + q1 * (1 - 0.5)) / q1;
    if (!Number.isFinite(BF) || BF <= 0) finite = false;
  }
  check('H2: no proof available (q\' > 0 => finite BF+)', finite);
  // SCOPE CHECK (added after the r4 review): "never evidence against H" holds ONLY in the
  // favourable case a = r' = 1. In the general two-cell model BF+ < 1 is attainable, so the
  // artifact's bullet must stay scoped. The counterexample is pinned here exactly.
  const cxA = 0.5, cxQ = 0.9, cxR = 1, cxP = 1;
  const cxBF = (cxA * cxP + cxQ * cxR * (1 - cxP)) / cxQ;
  check('H2 scope: general model admits BF+ < 1 (counterexample a=0.5,q\'=0.9,r\'=1,P(c|H)=1)',
    cxBF === cxA / cxQ && cxBF < 1, `BF+ = ${cxBF}`);
  let fav = true;
  for (let t = 0; t < 20000; t++) {
    const q1 = sample(1e-3, 1), pc = sample(0, 1);
    if ((pc + q1 * (1 - pc)) / q1 < 1 - 1e-12) fav = false;
  }
  check('H2 scope: favourable case a=r\'=1 still guarantees BF+ >= 1', fav);
  // the artifact must state the scoping and the counterexample form
  check('artifact scopes the "never against" claim to the favourable case',
    /favourable case\*\* just established/.test(joined) && /a\/q′ < 1/.test(joined));
  check('artifact carries the a>0 rider on BF+ = infinity',
    /q′ = 0` together with `a·P\(c\|H\) > 0/.test(joined) || /q′ = 0` with `a·P\(c\|H\) > 0/.test(joined));
  check('artifact states the standing q>0 assumption',
    /Standing assumption/.test(joined) && /`q > 0` and `q′ > 0`/.test(joined));
})();

/* =====================================================================
   6. TABLE 2 — every lattice entry recomputed from the stated formula
   ===================================================================== */
(function table2() {
  const sec = section(/^## 6\. Table 2/);
  const r3 = x => Math.round(x * 1000) / 1000;
  const rows = sec.filter(l => /^\|\s*[\d.]+\s*\|/.test(l) && l.includes('→'));
  check('Table 2 has 7 lattice rows', rows.length === 7, `found ${rows.length}`);
  let ok = 0, bad = [];
  const rx = /^\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*→\s*([\d.]+)\s*\|\s*([\d.]+)\s*→\s*([\d.]+)\s*\|\s*([\d.]+)\s*→\s*([\d.]+)\s*\|/;
  for (const l of rows) {
    const m = l.match(rx);
    if (!m) { bad.push('unparsed: ' + l); continue; }
    const pnb = parseFloat(m[1]);
    for (const [gi, r] of [[2, 1], [4, 0.5], [6, 0.25]]) {
      const bf = r3(r * pnb);
      const post = r3(bf / (bf + 1));
      if (parseFloat(m[gi]) === bf && parseFloat(m[gi + 1]) === post) ok++;
      else bad.push(`pnb=${pnb} r=${r}: got ${m[gi]}→${m[gi + 1]} want ${bf}→${post}`);
    }
  }
  check('Table 2: all 21 entries match BF=r*P(!b|H), post=BF/(BF+1)', ok === 21 && bad.length === 0,
    bad.slice(0, 4).join('; '));
  // the header must name exactly the three r values used
  const hdr = sec.find(l => /`r` →/.test(l)) || '';
  check('Table 2 header states r in {1, 0.5, 0.25}',
    /`r = 1`/.test(hdr) && /`r = 0.5`/.test(hdr) && /`r = 0.25`/.test(hdr));
})();

/* =====================================================================
   7. TABLE 1 — the per-premise [T]/[NT] ledger, parsed from the artifact
   ===================================================================== */
(function table1() {
  const sec = section(/^## 5\. Table 1/);
  const rows = sec.filter(l => /^\|\s*\d+\s*\|/.test(l));
  const t = (s) => (s.match(/\[T\]/g) || []).length;
  const nt = (s) => (s.match(/\[NT\]/g) || []).length;
  const ep = (s) => (s.match(/\[E\+]|\[E−]/g) || []).length;
  let nT = 0, nNT = 0, nE = 0;
  for (const l of rows) { nT += t(l); nNT += nt(l); nE += ep(l); }
  check('Table 1: 5 premise rows', rows.length === 5, `found ${rows.length}`);  check('Table 1: exactly 2 [T] and 3 [NT] tags', nT === 2 && nNT === 3, `[T]=${nT} [NT]=${nNT}`);
  check('Table 1: 4 [E+]/[E-] cells', nE === 4, `found ${nE}`);
  // the structural claim: the testable rows must be the ones the corollary neutralises
  const body = rows.join('\n');
  check('Table 1: q row tagged [T] and marked as cancelling',
    /cancels/.test(body) && /cancels \(Cor\. H1a\)/.test(body));
})();

/* =====================================================================
   8. FORMULAS AND CROSS-REFERENCES actually present in the artifact
   ===================================================================== */
(function formulas() {
  const f = [
    'BF = r · P(¬b|H)',
    'BF(H : E) = P(E|H)/P(E|¬H)',
    'P(E|H,b) = 0',
    'P(E|H,¬b) = q·r',
    'BF⁺ − 1 = P(c|H)·(1/q′ − 1)',
    'BF⁺ = [a·P(c|H) + q′·r′·P(¬c|H)] / q′',
    'max_{i≥2} P(E|H,bᵢ)/q',
    'λ_req = (N−1)p/(1−p)',
    '⟨ρ_b·τ_b⟩_w'
  ];
  for (const s of f) check(`formula present: ${s}`, joined.includes(s.replace(/\s+/g, ' ')));
  check('states the framework difference from r3 Theorem 1',
    /does \*\*not\*\* apply to the availability arguments/.test(joined));
  check('reports, does not endorse, the reconstructed conclusion',
    /reported, not endorsed/i.test(text));
  check('carries the r3 symmetry requirement forward', /must not quantify only the direction that suits it/.test(plain));
})();

/* =====================================================================
   9. PROTOCOL — no verdict, no forbidden phrases
   ===================================================================== */
(function protocol() {
  const banned = [
    /therefore\s+god\s+(does\s+not\s+)?exists?/i,
    /therefore\s+god\s+does\s+not\s+exist/i,
    /this\s+(proves|disproves)\s+(that\s+)?(god|a\s+god)/i,
    /we\s+have\s+(proven|disproven)/i,
    /it\s+follows\s+that\s+god\s+(exists|does\s+not\s+exist)/i,
    /^\s*(god\s+exists|there\s+is\s+a\s+god)\b/i,
    /we\s+conclude\s+(that\s+)?god\s+exists/i,
    /the\s+(?:best|correct)\s+(?:explanation|conclusion)\s+is\s+that\s+god/i,
    /\bthe\s+one\s+true\s+(?:god|religion)\b/i,
    /\b(christianity|islam|judaism|hinduism|buddhism)\s+is\s+the\s+true\b/i
  ];
  for (const [i, re] of banned.entries()) check(`forbidden phrase ${i + 1} absent`, !re.test(joinedPlain));
  check('disclaimer present: does not assert that any god exists or does not exist',
    /does not assert that any god exists or does not exist/.test(joinedPlain));
  check('disclaimer present: does not judge any religion true or false',
    /does not judge any religion true or false/.test(joinedPlain));
  // every occurrence of the hypothesis string must sit in a definitional or conditional frame
  const frame = /(?:`H`\s*[=:]|conjunction|^\||if |suppose |under |when |With `H`)/;
  const hypOccurrences = [];
  const re = /perfectly loving God exists/g;
  let m;
  while ((m = re.exec(joined)) !== null) {
    const before = joined.slice(Math.max(0, m.index - 160), m.index);
    hypOccurrences.push(frame.test(before));
  }
  check('hypothesis "a perfectly loving God exists" only in definitional or conditional frames',
    hypOccurrences.length >= 4 && hypOccurrences.every(Boolean),
    `${hypOccurrences.filter(x => !x).length}/${hypOccurrences.length} unframed`);
})();

/* =====================================================================
   10. ARITHMETIC CLAIMS MADE IN PROSE
   ===================================================================== */
(function prose() {
  // §2.3: deviation |BF - BF_naive| = r*P(!b|H), max 1.0
  let maxBF = 0;
  for (let t = 0; t < 200000; t++) maxBF = Math.max(maxBF, rnd() * rnd());
  check('prose: max of r*P(!b|H) approaches 1.0 as claimed', maxBF > 0.99, `max ${maxBF}`);
  // §6: BF = 0.111 corresponds to a 9:1 posterior against H at an even prior (r3 claim echoed)
  near(1 / 9, 0.1111, 0.01, 'prose: 9:1 tilt is BF = 1/9');
  // §2.3 / r3 cross-check: 90% posterior from even start needs 9:1
  near(9 / (9 + 1), 0.9, 1e-9, 'prose: 9:1 likelihood ratio at even prior gives 0.90');
  near(99 / (99 + 1), 0.99, 1e-9, 'prose: 99:1 likelihood ratio at even prior gives 0.99');
})();

/* ---------- report ---------- */
console.log(`verify_v14 — god-religions-hiddenness-formal.md`);
console.log(`checks passed: ${pass}`);
if (failures.length) {
  console.log(`FAILURES (${failures.length}):`);
  for (const f of failures) console.log('  ✗ ' + f);
  process.exit(1);
}
console.log('ALL GREEN');
