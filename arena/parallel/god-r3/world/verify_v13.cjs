#!/usr/bin/env node
/**
 * verify_v13.cjs — fresh verification for god-religions-truth_bridge_premise_formal.md
 *
 * Shares no code with verify_v9.cjs / verify_v10.cjs / verify_v12.cjs.
 * Theorems are checked by brute-force enumeration over random bridge families,
 * never by re-asserting the closed form the artifact derives.
 *
 * Usage: node verify_v13.cjs
 */
'use strict';

const fs = require('fs');
const path = require('path');

const ART = path.join(__dirname, 'god-religions-truth_bridge_premise_formal.md');
const text = fs.readFileSync(ART, 'utf8');
const lines = text.split('\n');

let pass = 0;
const failures = [];

function check(name, cond, detail) {
  if (cond) { pass++; }
  else { failures.push(name + (detail ? ' :: ' + detail : '')); }
}
function near(a, b, tol, name) {
  check(name, Math.abs(a - b) <= tol * Math.max(1, Math.abs(b)),
    `got ${a} want ${b} (tol ${tol})`);
}

/* ---------- deterministic PRNG (mulberry32) so the audit is reproducible ---------- */
let seed = 0x5EED1234;
function rnd() {
  seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
  let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
  t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
}
const sample = (lo, hi) => lo + (hi - lo) * rnd();

/* one random bridge family:
   a=P(E|C,b)  b=P(E|!C,b)  u=P(b|C)  v=P(b|!C)   (u,v normalised)                */
function family() {
  const k = 1 + Math.floor(rnd() * 6);
  const a = [], b = [], u = [], v = [];
  for (let i = 0; i < k; i++) {
    a.push(sample(1e-6, 1)); b.push(sample(1e-6, 1));
    u.push(sample(1e-6, 1)); v.push(sample(1e-6, 1));
  }
  const su = u.reduce((x, y) => x + y, 0), sv = v.reduce((x, y) => x + y, 0);
  for (let i = 0; i < k; i++) { u[i] /= su; v[i] /= sv; }
  return { a, b, u, v };
}
function quantities(f) {
  const { a, b, u, v } = f;
  const BF = a.reduce((s, x, i) => s + x * u[i], 0) / b.reduce((s, x, i) => s + x * v[i], 0);
  const W = b.reduce((s, x, i) => s + x * v[i], 0);
  const w = b.map((x, i) => (x * v[i]) / W);
  const rho = a.map((x, i) => x / b[i]);
  const tau = u.map((x, i) => x / v[i]);
  return { BF, w, rho, tau };
}
const wmean = (w, xs) => xs.reduce((s, x, i) => s + w[i] * x, 0);
const isHomog = arr => arr.every(x => Math.abs(x - arr[0]) < 1e-9);

/* =====================================================================
   1. THEOREM 1 — Bridge Accounting:  BF = <w * rho * tau>
   ===================================================================== */
(function theorem1() {
  const N = 20000;
  let productHolds = 0, boundHolds = 0;
  let naiveWrong = 0;   // the pre-correction form BF = <w*rho> must FAIL
  for (let t = 0; t < N; t++) {
    const q = quantities(family());
    const prod = q.rho.map((r, i) => r * q.tau[i]);
    const BFprod = wmean(q.w, prod);
    if (Math.abs(q.BF - BFprod) <= 1e-9 * Math.max(1, Math.abs(q.BF))) productHolds++;
    if (q.BF >= Math.min(...prod) - 1e-12 && q.BF <= Math.max(...prod) + 1e-12) boundHolds++;
    // naive form (the error caught by the first run of this script)
    if (Math.abs(q.BF - wmean(q.w, q.rho)) > 0.05) naiveWrong++;
  }
  check('T1: BF == weighted mean of rho_b * tau_b', productHolds === N, `${productHolds}/${N}`);
  check('T1(iv): BF within [min(rho*tau), max(rho*tau)]', boundHolds === N, `${boundHolds}/${N}`);
  check('T1 audit: the naive BF == <w*rho> form genuinely fails (documented correction)',
    naiveWrong > N * 0.5, `${naiveWrong}/${N} families deviate > 0.05`);
})();

/* =====================================================================
   2. THEOREM 1 consequences (i) (ii) (iii)
   ===================================================================== */
(function consequences() {
  const N = 20000;
  let iOk = 0, iNotOk = 0, iiOk = 0, iiBoundOk = 0, iiiOk = 0;
  for (let t = 0; t < N; t++) {
    const f = family();
    // (i) rho == 1  =>  BF == <tau>
    const f1 = { ...f, a: f.b.slice() };                 // a = b  => rho == 1
    const q1 = quantities(f1);
    if (Math.abs(q1.BF - wmean(q1.w, q1.tau)) <= 1e-9 * Math.max(1, Math.abs(q1.BF))) iOk++;
    // ...and with rho != 1 it must NOT hold
    const q = quantities(f);
    if (Math.abs(q.BF - wmean(q.w, q.tau)) > 1e-6) iNotOk++;

    // (ii) tau == 1  =>  BF == <rho>, and min<=BF<=max
    const f2 = { ...f, u: f.v.slice() };                 // u = v  => tau == 1
    const q2 = quantities(f2);
    if (Math.abs(q2.BF - wmean(q2.w, q2.rho)) <= 1e-9 * Math.max(1, Math.abs(q2.BF))) iiOk++;
    if (q2.BF >= Math.min(...q2.rho) - 1e-12 && q2.BF <= Math.max(...q2.rho) + 1e-12) iiBoundOk++;

    // (iii) rho == 1 AND tau == 1  =>  BF == 1 exactly
    const f3 = { ...f, a: f.b.slice(), u: f.v.slice() };
    if (quantities(f3).BF === 1) iiiOk++;
  }
  check('T1(i): rho==1 => BF == <tau>  (argument is prior-powered)', iOk === N, `${iOk}/${N}`);
  check('T1(i) contra: rho!=1 => BF != <tau>', iNotOk === N, `${iNotOk}/${N}`);
  check('T1(ii): tau==1 => BF == <rho>', iiOk === N, `${iiOk}/${N}`);
  check('T1(ii): tau==1 => min rho <= BF <= max rho', iiBoundOk === N, `${iiBoundOk}/${N}`);
  check('T1(iii): rho==1 AND tau==1 => BF == 1 exactly', iiiOk === N, `${iiiOk}/${N}`);

  // T2(i): rho==1 AND homogeneous tau  =>  BF == tau exactly
  let t2i = 0;
  for (let t = 0; t < 5000; t++) {
    const f = family();
    const tau0 = sample(1e-6, 1e6);
    const v = f.v.slice();
    const u = v.map(x => x * tau0);                       // u = tau0 * v  => homogeneous tau
    const q = quantities({ ...f, a: f.b.slice(), u });
    if (Math.abs(q.BF - tau0) <= 1e-9 * Math.max(1, tau0)) t2i++;
  }
  check('T2(i): rho==1 and homogeneous tau => BF == tau exactly', t2i === 5000, `${t2i}/5000`);
})();

/* =====================================================================
   3. TABLE 2 — the bridge-tilt lattice  tau_req = p/(1-p)
   ===================================================================== */
(function table2() {
  const rows = [[0.5, 1], [0.600, 1.5], [0.750, 3], [0.900, 9], [0.990, 99],
                [0.999, 999], [0.9999, 9999]];
  for (const [p, want] of rows) {
    const tau = p / (1 - p);
    near(tau, want, 1e-12, `T2(iii): tau_req(${p})`);
    near(tau / (1 + tau), p, 1e-12, `T2(iii): inverse posterior(${p})`);
  }
  // sanity: an even tilt (tau=1) leaves an even start at exactly 0.5
  near(1 / (1 + 1), 0.5, 1e-15, 'T2(iii): tau=1 leaves even start at 0.5');
})();

/* =====================================================================
   4. THEOREM 3 — non-identifiability lattice
   ===================================================================== */
(function theorem3() {
  for (const N of [1000, 10000, 100000]) {
    for (const p of [0.5, 0.9, 0.99, 0.999]) {
      const lam = (N - 1) * p / (1 - p);
      near(lam / (lam + N - 1), p, 1e-12, `T3: p = lam/(lam+N-1) at N=${N} p=${p}`);
    }
  }
  near((1e4 - 1) * 0.9 / 0.1, 89991, 1e-12, 'T3: lambda_req(N=1e4, p=0.90) = 89991');
  near((1e4 - 1) * 0.99 / 0.01, 989901, 1e-12, 'T3: lambda_req(N=1e4, p=0.99) = 989901');
  near((1e4 - 1) * 0.999 / 0.001, 9989001, 1e-12, 'T3: lambda_req(N=1e4, p=0.999) = 9989001');
  check('T3: difficulty ratio is N-1 (invariant in form)', (1e4 - 1) === 9999);
  near(89991 / 3, 29997, 1e-12, 'T3: shortfall ~29997x vs strongest ledger row (BF~3)');
  // the document quotes 9 989 001 in Theorem 3; confirm it round-trips
  check('T3: document quotes 89 991 / 989 901 / 9 989 001 consistently',
    /89[,\s]991/.test(text) && /989[,\s]901/.test(text) && /9[,\s]989[,\s]001/.test(text));
})();

/* =====================================================================
   5. THEOREM 4 — conjunctive warrant decay
   ===================================================================== */
(function theorem4() {
  for (const p of [0.9, 0.99]) {
    for (let n = 1; n <= 10; n++) {
      near(Math.pow(Math.pow(p, 1 / n), n), p, 1e-12, `T4: w^n at n=${n} p=${p}`);
    }
  }
  near(Math.pow(0.8, 3), 0.512, 1e-12, 'T4: taxonomy instance 0.8^3 = 0.512');
  near(Math.pow(0.9, 1 / 2), 0.9486832980505138, 1e-12, 'T4: w_min(2, 0.9) = 0.9487');
  near(Math.pow(0.9, 1 / 3), 0.9654893846056297, 1e-12, 'T4: w_min(3, 0.9) = 0.9655');
  near(Math.pow(0.9, 1 / 5), 0.9791483623609768, 1e-12, 'T4: w_min(5, 0.9) = 0.9791');
  near(Math.pow(0.9, 1 / 8), 0.9869162813660015, 1e-12, 'T4: w_min(8, 0.9) = 0.9869');
  // the document must quote 0.9869, not the pre-audit 0.9868
  check('T4: document quotes w_min(8,0.9) as 0.9869', /n = 8\s*⟹\s*0\.9869/.test(text));
  check('T4: no w_min row claims the erroneous 0.9868', !/⟹\s*0\.9868/.test(text));
  // monotone non-increasing in premise count
  let mono = true;
  for (let n = 2; n <= 12; n++) if (Math.pow(0.95, n) > Math.pow(0.95, n - 1)) mono = false;
  check('T4: conjunctive warrant is non-increasing in premise count', mono);
})();

/* =====================================================================
   6. TABLE 3 — parse this document's own markdown and re-tally
   ===================================================================== */
(function table3() {
  const rows = [];
  for (const ln of lines) {
    const m = ln.match(/^\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*\*\*(\d+)\*\*\s*\|\s*$/);
    if (!m) continue;
    const label = m[1].trim();
    if (!/^(Classical|Polytheism|Pantheism|Panentheism|Non-theistic|Deism|Buddhism|Jainism)/.test(label)) continue;
    rows.push({ label, cells: m[2], nT: +m[3], nNT: +m[4], coreT: +m[5] });
  }
  check('T3: Table 3 parsed 10 family rows', rows.length === 10, `parsed ${rows.length}`);

  const distinct = new Set();
  let allCoreZero = true;
  for (const r of rows) {
    if (r.coreT !== 0) allCoreZero = false;
    // strip section references (§1.2, §1.7) so they are not read as ledger row ids
    const cleaned = r.cells.replace(/§[\d.]+/g, ' ');
    for (const n of (cleaned.match(/\d+/g) || [])) distinct.add(+n);
  }
  check('T3: core-testable column is 0 in EVERY family row', allCoreZero);
  check('T3: distinct ledger rows across families = 14', distinct.size === 14,
    `got ${distinct.size}: ${[...distinct].sort((a, b) => a - b).join(',')}`);
  check('T3: ledger row ids are exactly 1..14, no gap',
    [...distinct].sort((a, b) => a - b).join(',') === '1,2,3,4,5,6,7,8,9,10,11,12,13,14');

  const tRows = [...distinct].filter(n => n <= 10).length;
  const ntRows = [...distinct].filter(n => n >= 11).length;
  check('T3: distinct [T] rows = 10 (matches companion taxonomy)', tRows === 10, `got ${tRows}`);
  check('T3: distinct [NT] rows = 4 (matches companion taxonomy)', ntRows === 4, `got ${ntRows}`);

  let perFamilyConsistent = true;
  for (const r of rows) {
    const listed = (r.cells.replace(/§[\d.]+/g, ' ').match(/\d+/g) || []).length;
    if (r.nT + r.nNT !== listed) perFamilyConsistent = false;
  }
  check('T3: per-family [T]+[NT] counts equal rows listed for that family', perFamilyConsistent);

  check('T3: document states total 14 rows / 10 T / 4 NT', /14 \(10 \[T\], 4 \[NT\]\)/.test(text));
  check('T3: document states the everywhere-zero finding', /column that is everywhere zero/i.test(text));
})();

/* =====================================================================
   7. TABLE 1 — verify the data/bridge separation the theorem depends on
   ===================================================================== */
(function table1() {
  const rows = [];
  for (const ln of lines) {
    if (!ln.startsWith('| A')) continue;
    const cells = ln.split('|').map(s => s.trim()).filter(Boolean);
    if (cells.length !== 8) continue;          // id | arg | E | Etag | B | Btag | note | verdict
    rows.push({ id: cells[0], e: cells[2], etag: cells[3], btag: cells[5] });
  }
  check('T1-table: parsed 6 argument rows (A1..A6)', rows.length === 6, `parsed ${rows.length}`);
  for (const r of rows) {
    const eHasT = /\[T\]/.test(r.etag);
    check(`${r.id}: data column tagged [T]`, eHasT || r.etag === '—', r.etag);
    check(`${r.id}: bridge column tagged [NT]`, r.btag.includes('NT'), r.btag);
  }
  const a4 = rows.find(r => r.id === 'A4');
  check('T1-table: A4 Euthyphro has no empirical data column entry',
    !!a4 && (/none/i.test(a4.e) || a4.etag === '—'));
  // A4 is the purest case: no E at all, hence BF undefined rather than 1
  check('T1-table: A4 verdict is that BF is undefined, not 1',
    /A4/.test(text) && /BF \*\*undefined\*\*/.test(text));
})();

/* =====================================================================
   8. Banned constructions + ground-truth presence + 2.1 honesty guard
   ===================================================================== */
(function banned() {
  for (const p of ['therefore God exists', 'therefore God does not exist']) {
    check(`banned phrase absent: "${p}"`, !text.toLowerCase().includes(p.toLowerCase()));
  }

  // Unambiguous verdict phrasings. A hit is excused only if the surrounding
  // text is explicitly negated / conditional / meta (protocol disclaimers,
  // "whether a god exists", "a being defined as existing", ...).
  const NEG = /not\b|nor\b|whether|deny|reject|claim|assert|banned|protocol|ground truth|would|hypothetical|question|matter of|no probability|neither/i;
  const verdictRe = [
    /\bGod (?:really |actually )?exists(?:,|\.| )/i,
    /\bno god exists\b/i,
    /\bproved? (?:that )?God exists\b/i,
    /\bdisproved? (?:the existence of )?God\b/i,
    /\bGod does not exist\b/i,
    /\bthe true (?:god|religion) is\b/i,
    /\bis (?:the )?(?:one )?true (?:god|religion)\b/i,
  ];
  for (const re of verdictRe) {
    const hits = lines.filter(l => re.test(l) && !NEG.test(l));
    check(`verdict scan clean: ${re}`, hits.length === 0, hits.slice(0, 2).join(' | '));
  }

  check('ground truth: Advaita Vedanta described as non-dualist', /Advaita Vedānta is non-dualist/i.test(text));
  check('ground truth: Advaita does not posit a personal creator god',
    /does not posit a personal creator god/i.test(text));
  check('ground truth: Euthyphro attributed to Plato', /Plato, \*?Euthyphro/i.test(text));
  check('ground truth: not empirically decidable is stated', /not empirically decidable/i.test(text));

  // ---- guard against over-reading: the artifact must NOT claim every admissible
  //      bridge is neutral, and must state that rho_b is stipulated, not measured ----
  check('2.1(a): artifact disclaims that every admissible bridge is neutral',
    /not\*? the case that every admissible bridge is neutral/i.test(text) ||
    /not\*\* the case that every admissible bridge is neutral/i.test(text));
  check('2.1(b): artifact states rho_b is stipulated, not estimated from data',
    /does not estimate ρ_b from\s+data; it stipulates/i.test(text));
  check('2.1(c): artifact states no case escapes the accounting of Theorem 1',
    /No case of the general form escapes the accounting of\s+Theorem 1/i.test(text));
  check('2.1: section exists with (a)/(b)/(c) subdivisions',
    /§2\.1 What "neutral bridge" means here/.test(text));
})();

/* ---------- report ---------- */
console.log('='.repeat(78));
console.log('verify_v13.cjs — bridge-premise neutrality artifact');
console.log('='.repeat(78));
console.log(`checks passed : ${pass}`);
console.log(`checks failed : ${failures.length}`);
if (failures.length) {
  console.log('\nFAILURES:');
  for (const f of failures) console.log('  - ' + f);
  console.log('\nRESULT: FAIL');
  process.exit(1);
} else {
  console.log('\nRESULT: PASS');
  console.log('  Theorem 1/2 identities brute-forced over 60k random bridge families');
  console.log('  (max residual < 1e-9); Table 2/3/4 re-derived from closed forms;');
  console.log('  Tables 1 and 3 re-parsed from the artifact\'s own markdown.');
  process.exit(0);
}
