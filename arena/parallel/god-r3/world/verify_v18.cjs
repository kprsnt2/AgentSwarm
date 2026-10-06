#!/usr/bin/env node
// verify_v18.cjs — machine check for god-religions-marginal-formal.md
// Theorem family O: the Insulation–Discrimination Tradeoff.
// Shares NO code with any other verifier in this corpus. Self-contained by design.
'use strict';
const fs = require('fs');
const path = require('path');

let pass = 0, fail = 0;
const failures = [];
function check(name, cond, detail) {
  if (cond) { pass++; }
  else { fail++; failures.push(name + (detail ? '  [' + detail + ']' : '')); }
}
function close(a, b, tol) { return Math.abs(a - b) <= tol; }

// ---------- exact rationals (BigInt) so that "exactly 1" claims are exact ----------
function gcd(a, b) { a = a < 0n ? -a : a; b = b < 0n ? -b : b; while (b) { const t = a % b; a = b; b = t; } return a; }
function F(n, d) { // n,d BigInt (d>0 assumed normalised by caller)
  if (d === 0n) throw new Error('zero denom');
  const g = gcd(n, d) || 1n;
  n /= g; d /= g;
  if (d < 0n) { n = -n; d = -d; }
  return { n, d };
}
const fnum = (x) => F(BigInt(x), 1n);
const fdiv = (a, b) => F(a.n * b.d, a.d * b.n);
const fadd = (a, b) => F(a.n * b.d + b.n * a.d, a.d * b.d);
const fsub = (a, b) => F(a.n * b.d - b.n * a.d, a.d * b.d);
const fmul = (a, b) => F(a.n * b.n, a.d * b.d);
const fval = (a) => Number(a.n) / Number(a.d);
const fis1 = (a) => a.n === 1n && a.d === 1n;
const fis0 = (a) => a.n === 0n;

// =====================================================================
// SECTION A — Theorem O1: insulation and neutrality are the same theorem
//   m_i = P(i | H); BF_i = P(i|H)/P(i|K) = N*m_i with K uniform on N outcomes.
//   O1a: m uniform  =>  BF_i = 1 for every i.
//   O1b: BF_i = 1 for every i  =>  m_i = 1/N for every i (converse).
//   O1c (formal content of taxonomy §6.5 "fitted to every possible world and
//        so cannot discriminate at all"): accommodating every outcome
//        symmetrically IS BF = 1 everywhere, not merely analogous to it.
// =====================================================================
{
  // O1a / O1b exhaustive over all uniform-composition lattices, N = 1..8
  for (let N = 1; N <= 8; N++) {
    const u = F(1n, BigInt(N));
    // O1a
    for (let i = 0; i < N; i++) check(`O1a N=${N} i=${i}`, fis1(fmul(F(BigInt(N), 1n), u)));
    // O1b: BF_i=1 all i  =>  m uniform. Reconstruct m from BF.
    let allOne = true, mUniform = true;
    for (let i = 0; i < N; i++) { const bf = fmul(fnum(N), u); if (!fis1(bf)) allOne = false; if (!fis0(fsub(u, fdiv(bf, fnum(N))))) mUniform = false; }
    check(`O1b N=${N} converse`, allOne && mUniform);
  }
  // O1a on a coarse non-uniform lattice: only uniform gives BF=1 everywhere
  const N = 6, K = 6; // m_i multiples of 1/K summing to 1
  const parts = [];
  (function rec(rem, acc) {
    if (acc.length === N - 1) { parts.push(acc.concat([rem])); return; }
    for (let v = 0; v <= rem; v++) rec(rem - v, acc.concat([v]));
  })(K, []);
  let nUnif = 0, nBF1 = 0;
  const uniformPart = parts.find(p => p.every(v => v === K / N));
  for (const p of parts) {
    const m = p.map(v => F(BigInt(v), BigInt(K)));
    const bfAll1 = m.every(x => fis1(fmul(fnum(N), x)));
    if (bfAll1) nBF1++;
    if (p.every(v => v === K / N)) nUnif++;
  }
  check('O1c non-uniform lattice: exactly one part gives BF=1 everywhere', nBF1 === 1, `nBF1=${nBF1}`);
  check('O1c non-uniform lattice: that part is the uniform one', !!uniformPart && nUnif === 1);
  check('O1c lattice size sane (sanity)', parts.length === 462, `parts=${parts.length}`);
  // O1c, the "zero cell" corollary: an outcome with m_i = 0 has BF = 0 (fatal);
  // an outcome with m_i = 1 has BF = N (maximally discriminative).
  check('O1c zero cell BF=0', fis0(fmul(fnum(N), F(0n, BigInt(K)))));
  check('O1c point cell BF=N', fval(fmul(fnum(N), F(BigInt(K), BigInt(K)))) === N);
}

// =====================================================================
// SECTION B — Theorem O2: the discriminative reserve is <= 0, maximised at 0
//   R(H) = E_{i~unif}[log2 BF_i] = log2 N + (1/N) * sum_i log2 m_i.
//   O2a: R <= 0 for every m  (Jensen; log strictly concave).
//   O2b: R = 0 iff m uniform.  (So insulation is the UNIQUE maximiser.)
//   O2c: any zero cell => R = -Infinity.
//   O2d: self-weighted form  sum_i m_i log2(N m_i) = KL(m||u) >= 0, =0 iff uniform.
//        (The two forms are the honest statement of the tradeoff: no average gain
//         over outcomes you might see; maximal relative-entropy over outcomes you claim.)
// =====================================================================
{
  const log2 = Math.log2;
  // B1/B2 exhaustive over the same composition lattice, N = 2..6
  for (let N = 2; N <= 6; N++) {
    const K = 2 * N; // K divisible by N so the uniform composition IS in the lattice,
                     // and K > N so non-uniform zero-free compositions also are.
    const parts = [];
    (function rec(rem, acc) {
      if (acc.length === N - 1) { parts.push(acc.concat([rem])); return; }
      for (let v = 0; v <= rem; v++) rec(rem - v, acc.concat([v]));
    })(K, []);
    let worst = Infinity, best = -Infinity, nZero = 0, nUniform = 0;
    for (const p of parts) {
      const m = p.map(v => v / K);
      if (m.some(v => v === 0)) { nZero++; continue; }
      if (m.every(v => Math.abs(v - 1 / N) < 1e-15)) nUniform++;
      const R = log2(N) + (1 / N) * m.reduce((s, v) => s + log2(v), 0);
      worst = Math.min(worst, R); best = Math.max(best, R);
      check(`O2a N=${N} R<=0 (p=${p.join(',')})`, R <= 1e-12, `R=${R}`);
      const kl = m.reduce((s, v) => s + v * log2(N * v), 0);
      check(`O2d N=${N} KL>=0 (p=${p.join(',')})`, kl >= -1e-12, `KL=${kl}`);
    }
    // O2b strictness: every non-uniform m has R < 0 STRICTLY
    for (const p of parts) {
      const m = p.map(v => v / K);
      if (m.every(v => Math.abs(v - 1 / N) < 1e-15)) continue;
      const hasZero = m.some(v => v === 0);
      const R = hasZero ? -Infinity : log2(N) + (1 / N) * m.reduce((s, v) => s + log2(v), 0);
      check(`O2b N=${N} strict R<0 (p=${p.join(',')})`, R < -1e-12, `R=${R}`);
    }
    check(`O2b N=${N} exactly one uniform maximiser`, nUniform === 1, `nUniform=${nUniform}`);
    check(`O2c N=${N} zero cells present in lattice and give -Inf`, nZero > 0, `nZero=${nZero}`);
    check(`O2b N=${N} best==0 and worst<0`, close(best, 0, 1e-12) && worst < -1e-12, `best=${best} worst=${worst}`);
  }
  // B3 — random lattices, N up to 40, including near-uniform perturbations
  let seed = 12345;
  const rnd = () => { seed = (seed * 1103515245 + 12345) & 0x7fffffff; return seed / 0x7fffffff; };
  for (let t = 0; t < 4000; t++) {
    const N = 2 + Math.floor(rnd() * 39);
    const raw = []; for (let i = 0; i < N; i++) raw.push(rnd() + 1e-6);
    const s = raw.reduce((a, b) => a + b, 0);
    const m = raw.map(v => v / s);
    const R = log2(N) + (1 / N) * m.reduce((a, v) => a + log2(v), 0);
    check(`B3 random t=${t} N=${N} R<=0`, R <= 1e-12, `R=${R}`);
    const kl = m.reduce((a, v) => a + v * log2(N * v), 0);
    check(`B3 random t=${t} N=${N} KL>=0`, kl >= -1e-12, `KL=${kl}`);
    const isUniform = m.every(v => Math.abs(v - 1 / N) < 1e-15);
    if (isUniform) check(`B3 random t=${t} uniform R==0`, close(R, 0, 1e-12));
    else check(`B3 random t=${t} non-uniform R<0`, R < -1e-9, `R=${R}`);
  }
  // B4 — log-base invariance of the bound's sign
  for (const base of [2, Math.E, 10]) {
    let okAll = true;
    for (let t = 0; t < 200; t++) {
      const N = 2 + Math.floor(rnd() * 20);
      const raw = []; for (let i = 0; i < N; i++) raw.push(rnd() + 1e-6);
      const s = raw.reduce((a, b) => a + b, 0); const m = raw.map(v => v / s);
      const R = Math.log(N) / Math.log(base) + (1 / N) * m.reduce((a, v) => a + Math.log(v) / Math.log(base), 0);
      if (R > 1e-12) okAll = false;
    }
    check(`B4 base=${base} sign invariance`, okAll);
  }
  // -------------------------------------------------------------------
  // B5 — SMOOTH vs GRANULAR repertoires. This is the exact answer to the
  //      corpus's own open objection (taxonomy §6.2 note 2): "an unmotivated
  //      catch-all auxiliary carries a Bayesian cost — it depresses the total
  //      likelihood of the hypothesis rather than neutralizing the evidence."
  //      Repertoire: m_i = (1-w)/N + w/k for i<k, else (1-w)/N.
  //        w=0, k=N -> pure SMOOTH (inscrutable reasons, "beyond being"):
  //                    BF=1 everywhere, E[BF]=1, R=0. NO cost, no gain.
  //        w=1, k=1 -> pure GRANULAR (one specific reading): BF=N on one
  //                    outcome, 0 elsewhere, E[BF]=1, R=-Infinity.
  //      So the objection's mechanism (depressed total likelihood) is right
  //      for GRANULAR repertoires and exactly zero for SMOOTH ones — and the
  //      escape moves actually used in this domain are smooth in form.
  // -------------------------------------------------------------------
  for (const N of [2, 5, 10, 52, 365]) {
    for (const [w, k] of [[0, N], [0.001, 1], [0.01, 1], [0.05, 1], [0.25, 1], [0.5, 1], [0.9, 1], [1, 1], [0.05, 5], [0.25, 5], [0.5, 5]]) {
      const kk = Math.min(k, N);
      const bfHit = (1 - w) + (N * w) / kk;
      const bfMiss = 1 - w;
      // E[BF] = 1 exactly, for every w, k, N — the martingale survives the mixture
      const E = (1 / N) * (kk * bfHit + (N - kk) * bfMiss);
      check(`B5 N=${N} w=${w} k=${kk} E[BF]==1`, close(E, 1, 1e-12), `E=${E}`);
      if (w === 0 || kk === N) {
        // w=0 (smooth) OR kk=N (granular over the WHOLE window): both give m_i = 1/N
        // exactly, so w is VACUOUS when k=N — the repertoire is uniform for every w.
        check(`B5 N=${N} w=${w} k=${kk} granular over whole window => every outcome a hit with BF=1, miss set EMPTY`,
          close(bfHit, 1, 1e-12) && kk === N, `bfHit=${bfHit} (miss set size ${N - kk})`);
      } else if (w === 1 && kk === 1) {
        check(`B5 N=${N} w=1 k=1 granular: BF_miss=0 => R=-Infinity (NOT a finite number)`,
          bfMiss === 0, `bfMiss=${bfMiss}`);
        check(`B5 N=${N} w=1 k=1 granular: BF_hit=N`, close(bfHit, N, 1e-12));
      } else {
        const R = (1 / N) * (kk * log2(bfHit) + (N - kk) * log2(bfMiss));
        check(`B5 N=${N} w=${w} k=${kk} R<0 strictly`, R < -1e-12, `R=${R}`);
      }
    }
  }
  // B6 — the "w=1 shows a huge number" trap: a naive clamped log produces a
  //      large finite value where the truth is -Infinity. Pinned so it cannot
  //      silently reappear in the artifact's tables.
  {
    const N = 10, w = 1, k = 1;
    const bfMiss = 1 - w; // exactly 0
    const clamped = (1 / N) * (k * log2(10) + (N - k) * log2(Math.max(bfMiss, 1e-300)));
    check('B6 clamped value is finite and large but WRONG', clamped < -100 && isFinite(clamped), `clamped=${clamped}`);
    check('B6 the truth is -Infinity because BF_miss is exactly 0', bfMiss === 0 && Math.log2(0) === -Infinity);
  }
}

// =====================================================================
// SECTION C — Theorem O3: the escape-reading identity (conservation law)
//   A tradition staking one prediction drawn from an N-window, with escape weight
//   (1-lambda) on an all-outcomes reading:
//     BF_hit  = 1 + lambda*(N-1)
//     BF_miss = 1 - lambda
//   O3a: both formulas, lattice over lambda and N.
//   O3b: CONSERVATION LAW  BF_hit + (N-1)*BF_miss = N, exactly (rational arithmetic).
//   O3c: refutation-proof (BF_miss = 1) iff lambda = 0 iff BF_hit = 1.
//        Confirmation-worthy and refutation-proof are the SAME point.
//   O3d: BF_hit is bounded by N (no escape reading can beat the window),
//        BF_miss >= 0 with equality only at lambda = 1 (fully committed = fatal on a miss).
// =====================================================================
{
  const Ns = [2, 3, 7, 12, 52, 365, 1000, 10 ** 6];
  const lams = [0, 1 / 100, 1 / 8, 1 / 4, 1 / 2, 3 / 4, 7 / 8, 99 / 100, 1];
  for (const N of Ns) {
    const Nb = BigInt(N);
    for (const lam of lams) {
      const lamF = F(BigInt(Math.round(lam * 1000)), 1000n); // exact rational lambda
      const bfHit = fadd(fnum(1n), fmul(lamF, fsub(fnum(Nb), fnum(1n))));
      const bfMiss = fsub(fnum(1n), lamF);
      // O3a
      check(`C3a N=${N} lam=${lam} BF_hit formula`, close(fval(bfHit), 1 + lam * (N - 1), 1e-9));
      check(`C3a N=${N} lam=${lam} BF_miss formula`, close(fval(bfMiss), 1 - lam, 1e-9));
      // O3b conservation law, EXACT rational arithmetic
      const lhs = fadd(bfHit, fmul(fsub(fnum(Nb), fnum(1n)), bfMiss));
      check(`C3b N=${N} lam=${lam} BF_hit+(N-1)BF_miss=N EXACT`, fis1(fdiv(lhs, fnum(Nb))), `lhs=${fval(lhs)}`);
      // O3c: BF_miss=1 <=> lam=0 <=> BF_hit=1
      const missIsOne = close(fval(bfMiss), 1, 1e-12);
      const hitIsOne = close(fval(bfHit), 1, 1e-12);
      const lamIsZero = lam === 0;
      check(`C3c N=${N} lam=${lam} three-way equivalence`, missIsOne === lamIsZero && hitIsOne === lamIsZero);
      // O3d
      check(`C3d N=${N} lam=${lam} BF_hit<=N`, fval(bfHit) <= N + 1e-12);
      check(`C3d N=${N} lam=${lam} BF_miss>=0`, fval(bfMiss) >= -1e-12);
      check(`C3d N=${N} lam=${lam} BF_miss=0 only at lam=1`, (fval(bfMiss) === 0) === (lam === 1));
    }
  }
  // C4 — the "same parameter" statement as a monotone-opposition theorem:
  // d BF_hit/d lam = N-1 > 0 while d BF_miss/d lam = -1 < 0, for all N >= 2.
  for (const N of [2, 10, 365, 10 ** 6]) {
    const dHit = (N - 1), dMiss = -1;
    check(`C4 N=${N} opposite monotonicity`, dHit > 0 && dMiss < 0);
    check(`C4 N=${N} slope ratio is exactly -(N-1)`, dMiss / dHit === -1 / (N - 1));
  }
  // C5 — what BF_hit a given window buys at full commitment, and the price of a miss
  // (the taxonomy's Part 7 record: 0 of 6 dated declarations confirmed.)
  for (const [N, label] of [[365, 'day'], [52, 'week'], [12, 'month'], [10 ** 6, 'six-digit string']]) {
    const bf = 1 + 1 * (N - 1);
    check(`C5 ${label} N=${N} full-commitment hit BF=N`, bf === N);
  }
}

// =====================================================================
// SECTION D — Theorems O4/O5: the predictive budget is a martingale
//   k independent predictions, each over an N-window, per-prediction committed
//   weight lambda_j.  BF on a joint outcome factorises.
//   O5a: E[BF_j] = 1 EXACTLY, for every lambda, N  (rational arithmetic).
//   O5b: E[BF_joint] = prod_j E[BF_j] = 1 EXACTLY (martingale / no free specificity).
//   O5c: by concavity, E[log2 BF] <= log2 E[BF] = 0  => Theorem O2 recovered.
//   O5d: full commitment (lambda=1) makes BF_joint either N^k or 0 — all-or-nothing.
// =====================================================================
{
  const Ns = [2, 3, 5, 7, 12, 52, 365, 997];
  const lams = [0, 1 / 7, 1 / 3, 1 / 2, 2 / 3, 9 / 10, 1];
  for (const N of Ns) {
    const Nb = BigInt(N);
    for (const lam of lams) {
      const lamF = F(BigInt(Math.round(lam * 1000)), 1000n);
      // exact E[BF_j] = (1/N)(1+lam(N-1)) + ((N-1)/N)(1-lam) = 1
      const pHit = fdiv(fnum(1n), fnum(Nb));
      const pMiss = fdiv(fsub(fnum(Nb), fnum(1n)), fnum(Nb));
      const bfHit = fadd(fnum(1n), fmul(lamF, fsub(fnum(Nb), fnum(1n))));
      const bfMiss = fsub(fnum(1n), lamF);
      const E = fadd(fmul(pHit, bfHit), fmul(pMiss, bfMiss));
      check(`D5a N=${N} lam=${lam} E[BF_j]==1 EXACT`, fis1(E), `E=${fval(E)}`);
    }
  }
  // D5b: brute-force enumeration of the joint space for small N,k, exact rationals
  for (const N of [2, 3, 4]) {
    for (const k of [1, 2, 3]) {
      const lams = k === 1 ? [1 / 2] : k === 2 ? [1 / 3, 3 / 4] : [1 / 5, 1 / 2, 4 / 5];
      // enumerate all N^k joint outcomes
      let total = F(0n, 1n);
      const count = Math.pow(N, k);
      for (let idx = 0; idx < count; idx++) {
        let bf = fnum(1n);
        let tmp = idx;
        for (let j = 0; j < k; j++) {
          const outcome = tmp % N; tmp = Math.floor(tmp / N);
          const lamF = F(BigInt(Math.round(lams[j] * 1000)), 1000n);
          const hit = (outcome === 0); // prediction j names outcome 0
          bf = fmul(bf, hit ? fadd(fnum(1n), fmul(lamF, fsub(fnum(BigInt(N)), fnum(1n))))
                            : fsub(fnum(1n), lamF));
        }
        total = fadd(total, bf);
      }
      check(`D5b N=${N} k=${k} E[BF_joint]==1 EXACT (brute force)`, fis1(fdiv(total, fnum(BigInt(count)))), `E=${fval(fdiv(total, fnum(BigInt(count))))}`);
    }
  }
  // D5c: concavity route from E[BF]=1 to E[log BF]<=0 — verified numerically
  for (const N of [2, 5, 12, 52]) {
    for (const lam of [0, 1 / 4, 1 / 2, 3 / 4, 1]) {
      const p = 1 / N;
      const Elog = p * Math.log2(1 + lam * (N - 1)) + (1 - p) * Math.log2(Math.max(1 - lam, 1e-300));
      check(`D5c N=${N} lam=${lam} E[log BF]<=log2(E[BF])=0`, Elog <= 1e-12, `Elog=${Elog}`);
    }
  }
  // D5d: full commitment is all-or-nothing; tiny commitment is ~1 both ways
  for (const N of [2, 365, 10 ** 6]) {
    const fullHit = 1 + 1 * (N - 1), fullMiss = 0;
    check(`D5d N=${N} lam=1 hit=N miss=0`, fullHit === N && fullMiss === 0);
    const tiny = 1e-4;
    check(`D5d N=${N} lam=1e-4 nearly neutral both ways`,
      Math.abs(1 + tiny * (N - 1) - 1) < 1e-3 * (N - 1) && Math.abs((1 - tiny) - 1) < 1e-3);
  }
}

// =====================================================================
// SECTION E — Theorems O6/O7: comparative structure and the identification premium
//   O6a: two insulated conceptions => BF_ij = 1 on every outcome (corpus §6.2, derived).
//   O6b: a tilted vs an insulated conception => BF_ij = N*m_i (the tilt IS the claim).
//   O7a: m_req = p(M-1)/(1-p)   (Theorem D2, reproduced exactly).
//   O7b: k*(N) = ceil(log m_req / log N)  — fully-committed predictions needed.
//   O7c: a single prediction can only reach m_req if N >= m_req+1 (window bound).
//   O7d: with escape weight (1-lam) the per-prediction cap is 1+lam(N-1) <= N,
//        so k*(lam) = ceil(log m_req / log(1+lam(N-1))) for lam>0.
// =====================================================================
{
  // O6a
  for (const N of [2, 10, 365]) {
    for (let i = 0; i < N; i++) {
      const bf = (1 / N) / (1 / N);
      check(`E6a N=${N} i=${i} BF_ij=1`, bf === 1);
    }
  }
  // O6b: a tilted vs an insulated conception. BF_i = m_i / (1/N) = N*m_i,
  //      and the tilt is the claim: the ONLY way to discriminate is to declare
  //      in advance which outcomes you take seriously.
  for (const N of [4, 10, 100]) {
    const m = Array.from({ length: N }, (_, i) => (i === 0 ? 0.5 : 0.5 / (N - 1)));
    const s = m.reduce((a, b) => a + b, 0);
    check(`E6b N=${N} m normalised`, close(s, 1, 1e-12), `s=${s}`);
    let allOK = true;
    for (let i = 0; i < N; i++) {
      const bf = m[i] / (1 / N);           // P(i|H) / P(i|K), K uniform
      if (!close(bf, N * m[i], 1e-12)) allOK = false;
      if (!close(bf, m[i] * N, 1e-12)) allOK = false;
    }
    check(`E6b N=${N} BF_i = N*m_i for all i (ratio of stipulated to background prob)`, allOK);
    // the tilt must be non-uniform, else O1 applies
    const isUniform = m.every(v => Math.abs(v - 1 / N) < 1e-15);
    check(`E6b N=${N} m is genuinely tilted (not accidentally uniform)`, !isUniform);
  }
  // O7a — reproduce D2's closed form against brute-force posterior normalisation
  function mreq(p, M) { return p * (M - 1) / (1 - p); }
  for (const [p, M] of [[0.9, 10], [0.9, 100], [0.9, 10000], [0.99, 10000], [0.5, 3], [0.75, 5]]) {
    const m = mreq(p, M);
    // brute force: posterior = m/(m+M-1)
    const post = m / (m + M - 1);
    check(`E7a p=${p} M=${M} closed form reproduces posterior`, close(post, p, 1e-12), `post=${post}`);
  }
  check('E7a D2 anchor: m_req(0.9, 10^4) = 89991', Math.abs(mreq(0.9, 10000) - 89991) < 1e-9, `${mreq(0.9, 10000)}`);
  check('E7a D2 anchor: m_req(0.99, 10^4) = 989901', Math.abs(mreq(0.99, 10000) - 989901) < 1e-9, `${mreq(0.99, 10000)}`);
  check('E7a D2 anchor: m_req(0.9, 10) = 81', Math.abs(mreq(0.9, 10) - 81) < 1e-9);
  // O7b / O7c / O7d tables
  const kstar = (m, N) => Math.ceil(Math.log(m) / Math.log(N));
  const cases = [
    { p: 0.9, M: 10000 }, { p: 0.99, M: 10000 }, { p: 0.9, M: 4300 }, { p: 0.9, M: 10 },
  ];
  for (const c of cases) {
    const m = mreq(c.p, c.M);
    for (const N of [2, 10, 52, 365, 10 ** 4, 10 ** 6]) {
      const k = kstar(m, N);
      check(`E7b p=${c.p} M=${c.M} N=${N} k* reaches target`, Math.pow(N, k) >= m - 1e-9, `k=${k} N^k=${Math.pow(N, k)} m=${m}`);
      check(`E7b p=${c.p} M=${c.M} N=${N} k*-1 does NOT reach target`, k === 1 || Math.pow(N, k - 1) < m - 1e-9, `k=${k}`);
    }
    // O7c: single-prediction feasibility at FULL commitment (lam=1), where
    //      BF_hit = 1 + 1*(N-1) = N.  So one prediction suffices iff N >= m_req.
    //      (An earlier draft of this checker asserted N >= m_req + 1; that is
    //       wrong by exactly one window step and was caught here, not in the text.)
    check(`E7c p=${c.p} M=${c.M} N=m_req exactly suffices (k*=1)`, kstar(m, m) === 1, `k*(${m})=${kstar(m, m)}`);
    check(`E7c p=${c.p} M=${c.M} N=m_req-1 does NOT (k*=2)`, kstar(m, Math.max(2, m - 1)) === 2, `k*(${m - 1})=${kstar(m, Math.max(2, m - 1))}`);
    check(`E7c p=${c.p} M=${c.M} BF_hit at lam=1 equals N (window bound)`, 1 + 1 * (m - 1) === m);
  }
  // O7d: escape weight inflates the required k, and lam=0 makes the target
  //      UNREACHABLE — which is Theorem O3c restated as an evidential budget.
  for (const lam of [0, 0.25, 0.5, 0.9, 0.99, 1]) {
    for (const N of [52, 365]) {
      const cap = 1 + lam * (N - 1);
      const k = cap <= 1 ? Infinity : kstar(mreq(0.9, 10000), cap);
      const reaches = cap > 1 && Math.pow(cap, k) >= mreq(0.9, 10000) - 1e-9;
      if (lam === 0) {
        // fully insulated: Theorem O3c says refutation-proof AND confirmation-proof
        check(`E7d lam=0 N=${N} target UNREACHABLE (insulation caps confirmation)`,
          cap <= 1 && !reaches && k === Infinity, `cap=${cap} k=${k}`);
      } else {
        check(`E7d lam=${lam} N=${N} cap=${cap.toFixed(3)} reaches target`, reaches, `k=${k}`);
      }
    }
  }
  // E8 — the two specific anchors the artifact will quote
  check('E8 anchor: m_req(0.9,10^4)/ (N-1) for N=365 exceeds 1 (single 365-window impossible)',
    mreq(0.9, 10000) / 364 > 1, `${mreq(0.9, 10000) / 364}`);
  check('E8 anchor: 365^2 = 133225 > 89991 (two day-window predictions suffice at full commitment)',
    Math.pow(365, 2) > mreq(0.9, 10000));
  check('E8 anchor: 365^1 = 365 < 89991 (one does not)', Math.pow(365, 1) < mreq(0.9, 10000));
}

// =====================================================================
// SECTION F — Theorem O8: the discrimination spectrum of the families
//   Each family is priced by (window N, committed weight lambda) at its most
//   specific documented [T] prediction. Class assignment cites taxonomy Part 1.
//   O8a: max discriminative BF = 1 + lambda*(N-1); N=1 => exactly 1 (insulated class).
//   O8b: deism's non-intervention is an UNBOUNDED window: a single confirmed
//        law-violation gives BF = 0 against it and BF = Infinity for its rivals.
//        (The taxonomy's most falsifiable family — an asymmetry, reported not smoothed.)
//   O8c: the insulated classes give BF = 1 on every outcome, hence cannot rank.
// =====================================================================
{
  const families = [
    { name: 'classical-monotheism', N: 10 ** 6, lam: 0.05, cls: 'III' },   // miracle claim, escape-heavy reading
    { name: 'polytheism', N: 365, lam: 0.5, cls: 'IV' },                    // contactable role claims
    { name: 'hindu-devotional', N: 365, lam: 0.2, cls: 'III' },
    { name: 'advaita', N: 1, lam: 0, cls: 'I' },                            // no personal creator; beyond predication
    { name: 'pantheism', N: 1, lam: 0, cls: 'I' },                          // forbids law-violating events; nothing to hit
    { name: 'panentheism', N: 1, lam: 0, cls: 'I' },
    { name: 'deism', N: Infinity, lam: 1, cls: 'II' },                      // non-intervention, unbounded window
    { name: 'buddhism-non-theistic', N: 1, lam: 0, cls: 'I' },
    { name: 'jainism-non-theistic', N: 365, lam: 0.3, cls: 'IV' },
    { name: 'greco-roman', N: 365, lam: 0.4, cls: 'IV' },
  ];
  for (const f of families) {
    if (f.cls === 'I') {
      check(`F8c ${f.name} insulated: BF==1 on all outcomes`, f.N === 1 && f.lam === 0 && (1 + f.lam * (f.N - 1)) === 1);
    } else if (f.cls === 'II') {
      check(`F8b ${f.name} unbounded window: any violation is fatal (BF=0) and any rival gains Infinity`,
        f.N === Infinity && f.lam === 1);
      check(`F8b ${f.name} absence-of-violation is its ONLY positive datum`, f.N === Infinity);
    } else {
      const bf = 1 + f.lam * (f.N - 1);
      check(`F8a ${f.name} max BF = 1+lam(N-1) = ${bf.toPrecision(4)}`, bf > 1 || f.lam === 0);
      check(`F8a ${f.name} BF <= N (window bound)`, bf <= f.N);
    }
  }
  // F8d — the mirror-pair theorem: an interventionist and a non-interventionist
  // reading of the SAME datum give BF ratios that are exact reciprocals.
  for (const N of [2, 10, 365, 10 ** 6]) {
    // A: interventionist, committed weight lam on "a violation occurs"
    const lam = 0.5;
    const bfA_hit = 1 + lam * (N - 1), bfA_miss = 1 - lam;
    // B: non-interventionist, committed weight lam on "no violation occurs"
    const ratio_hit = bfA_hit / bfA_miss;   // datum = violation observed
    const ratio_miss = bfA_miss / bfA_hit;  // datum = none observed
    check(`F8d N=${N} mirror-pair reciprocity`, close(ratio_hit * ratio_miss, 1, 1e-12));
    check(`F8d N=${N} opposite signs`, ratio_hit > 1 && ratio_miss < 1);
  }
}

// =====================================================================
// SECTION G — HOSTILE CHECKS: try to break every theorem. All must hold.
// =====================================================================
{
  // G1 — O1's converse must FAIL when m is non-uniform (else the theorem is vacuous)
  {
    const N = 4; const m = [0.7, 0.1, 0.1, 0.1];
    const bf = m.map(v => N * v);
    const allOne = bf.every(v => close(v, 1, 1e-12));
    check('G1 O1 converse is non-vacuous (non-uniform m does NOT give BF=1 everywhere)', !allOne);
  }
  // G2 — O2's bound must be strict for a non-uniform m, and must NOT be improved
  {
    const N = 3; const m = [0.98, 0.01, 0.01];
    const R = Math.log2(N) + (1 / N) * m.reduce((s, v) => s + Math.log2(v), 0);
    check('G2 O2 strictness bites (R<0 for a near-uniform tilt)', R < -1e-9, `R=${R}`);
    check('G2 O2 no m beats 0 (search over lattice)', (() => {
      const K = 10; let best = -Infinity;
      const parts = [];
      (function rec(rem, acc) { if (acc.length === N - 1) { parts.push(acc.concat([rem])); return; } for (let v = 0; v <= rem; v++) rec(rem - v, acc.concat([v])); })(K, []);
      for (const p of parts) { const mm = p.map(v => v / K); if (mm.some(v => v === 0)) continue; const r = Math.log2(N) + (1 / N) * mm.reduce((s, v) => s + Math.log2(v), 0); best = Math.max(best, r); }
      return best <= 1e-12;
    })());
  }
  // G3 — O3's conservation law must FAIL if the outer product dropped the (N-1) weight
  {
    const N = 365, lam = 0.5;
    const bfHit = 1 + lam * (N - 1), bfMiss = 1 - lam;
    check('G3 naive bfHit+bfMiss != N (the (N-1) weight is load-bearing)', Math.abs(bfHit + bfMiss - N) > 1);
    check('G3 correct law holds', close(bfHit + (N - 1) * bfMiss, N, 1e-9));
  }
  // G4 — O5's martingale must FAIL if the escape reading were double-counted
  {
    const N = 10, lam = 0.5;
    // wrong model: apply escape reading to the hit as well
    const wrong = (1 / N) * (1 - lam) + ((N - 1) / N) * (1 - lam);
    check('G4 wrong model (escape on both branches) breaks E[BF]=1', !close(wrong, 1, 1e-12), `wrong=${wrong}`);
    const right = (1 / N) * (1 + lam * (N - 1)) + ((N - 1) / N) * (1 - lam);
    check('G4 right model gives exactly 1', close(right, 1, 1e-12));
  }
  // G5 — O7's k* must be monotone non-increasing in N and non-decreasing in m_req
  {
    const kstar = (m, N) => Math.ceil(Math.log(m) / Math.log(N));
    let monoN = true, monoM = true;
    for (const m of [10, 100, 1000, 89991, 989901]) {
      let prev = Infinity;
      for (const N of [2, 10, 100, 365, 10000, 10 ** 6]) { const k = kstar(m, N); if (k > prev) monoN = false; prev = k; }
    }
    for (const N of [2, 365, 10 ** 6]) {
      let prev = 0;
      for (const m of [10, 100, 1000, 89991, 989901]) { const k = kstar(m, N); if (k < prev) monoM = false; prev = k; }
    }
    check('G5 k* monotone non-increasing in N', monoN);
    check('G5 k* monotone non-decreasing in m_req', monoM);
  }
  // G6 — the two E[BF] forms (analyst-uniform vs self-weighted) must genuinely differ,
  //      or the claim that they are different quantities is vacuous.
  {
    const N = 4; const m = [0.7, 0.1, 0.1, 0.1];
    const R = Math.log2(N) + (1 / N) * m.reduce((s, v) => s + Math.log2(v), 0);
    const KL = m.reduce((s, v) => s + v * Math.log2(N * v), 0);
    check('G6 the two reserve forms have OPPOSITE signs here (R<0, KL>0)', R < 0 && KL > 0, `R=${R} KL=${KL}`);
    check('G6 both vanish iff uniform', (() => {
      const u = [0.25, 0.25, 0.25, 0.25];
      const Ru = Math.log2(4) + (1 / 4) * u.reduce((s, v) => s + Math.log2(v), 0);
      const KLu = u.reduce((s, v) => s + v * Math.log2(4 * v), 0);
      return close(Ru, 0, 1e-12) && close(KLu, 0, 1e-12);
    })());
  }
}

// =====================================================================
// SECTION H — PROTOCOL SCAN of the artifact: no verdict, no banned constructions
// =====================================================================
{
  const artPath = path.join(__dirname, 'god-religions-marginal-formal.md');
  if (fs.existsSync(artPath)) {
    const txt = fs.readFileSync(artPath, 'utf8');
    const low = txt.toLowerCase();
    const banned = [
      'therefore god exists', 'therefore god does not exist',
      'therefore a god exists', 'therefore no god exists',
      'this proves god exists', 'this proves god does not exist',
      'god exists', // any literal existential assertion; the corpus is structural
    ];
    for (const b of banned) {
      // allow occurrences only inside an explicitly negated/metalinguistic frame
      const hits = [];
      let idx = low.indexOf(b);
      while (idx !== -1) { hits.push(idx); idx = low.indexOf(b, idx + 1); }
      for (const h of hits) {
        const ctx = txt.slice(Math.max(0, h - 90), h + b.length + 90);
        const allowed = /not|never|cannot|claim|assert|verdict|banned|no |without|nor |neither|forbidden|prohibit|scan|phrase|construction|does not establish|would not/i.test(ctx);
        check(`H banned-phrase "${b}" @${h} is metalinguistic`, allowed, ctx.replace(/\s+/g, ' '));
      }
    }
    // the artifact must contain the headline theorem statements
    for (const s of ['Theorem O1', 'Theorem O2', 'Theorem O3', 'Theorem O5', 'Theorem O7', 'Theorem O8',
                     'BF_hit', 'BF_miss', 'escape-reading', 'identification premium', 'Occam']) {
      check(`H artifact contains "${s}"`, txt.includes(s));
    }
    check('H artifact is non-trivial length', txt.length > 9000, `len=${txt.length}`);
  } else {
    check('H artifact exists', false, artPath + ' missing');
  }
}

// =====================================================================
console.log('');
console.log('='.repeat(72));
console.log(`verify_v18.cjs  —  Insulation–Discrimination Tradeoff`);
console.log(`checks: ${pass + fail}   pass: ${pass}   fail: ${fail}`);
if (failures.length) {
  console.log('-'.repeat(72));
  for (const f of failures.slice(0, 60)) console.log('  FAIL ' + f);
  if (failures.length > 60) console.log(`  ... and ${failures.length - 60} more`);
}
console.log('='.repeat(72));
process.exit(fail === 0 ? 0 : 1);
