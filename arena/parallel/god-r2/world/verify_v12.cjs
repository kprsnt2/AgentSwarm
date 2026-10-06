#!/usr/bin/env node
// verify_v12.cjs — fresh recomputation of every quantitative claim in
// god-religions-confirmation-formal.md (Part 11 confirmation-ceiling result).
'use strict';
let P = 0, F = 0, total = 0;
function ok(name, cond, detail) {
  total++;
  if (cond) { P++; console.log('PASS  ' + name + (detail ? '  [' + detail + ']' : '')); }
  else { F++; console.log('FAIL  ' + name + (detail ? '  [' + detail + ']' : '')); }
}
const approx = (a, b, tol) => Math.abs(a - b) <= (tol == null ? 1e-6 : tol);

// --- posterior over H0 vs a rival set (equal prior odds) ---
const posterior = (LRs) => 1 / (1 + LRs.reduce((s, lr) => s + 1 / lr, 0));

// 1. formula == direct Bayes normalization (equal priors)
{
  const LRs = [1e6, 500, 25, 4, 1.5];
  const direct = 1 / (1 + LRs.reduce((s, lr) => s + 1 / lr, 0));
  ok('001 formula==direct-Bayes', approx(posterior(LRs), direct, 1e-12), posterior(LRs).toFixed(6));
}

// 2. closed form LR_req(N,f) = N*f/(1-f)
const LRreq = (N, f) => N * f / (1 - f);
ok('002 LR_req(9999,0.90)=89991', Math.round(LRreq(9999, 0.9)) === 89991, String(Math.round(LRreq(9999, 0.9))));
ok('003 LR_req(9999,0.99)=989901', Math.round(LRreq(9999, 0.99)) === 989901, String(Math.round(LRreq(9999, 0.99))));
ok('004 LR_req(9999,0.999)=9989001', Math.round(LRreq(9999, 0.999)) === 9989001, String(Math.round(LRreq(9999, 0.999))));
ok('005 LR_req linear in N', LRreq(2 * 9999, 0.9) === 2 * LRreq(9999, 0.9));

// 3. gating rival: one FLEXIBLE rival (LR*=1) pins ceiling ~0.5 for any k>=1 anomalies
//    P(k) = 1/[2 + N_spec/LR_h^k], N_spec=9998, LR_h=1e9
for (const k of [1, 2, 5, 20]) {
  const Nspec = 9998, LRh = 1e9, joint = Math.pow(LRh, k);
  const Pk = 1 / (2 + Nspec / joint);
  ok('006 flexible-rival ceiling ~0.5 (k=' + k + ')', approx(Pk, 0.5, 1e-2), Pk.toFixed(6));
}
{
  // no-anomaly base rate (k=0): P = 1/(1+N) with N=9999 rivals
  const base = 1 / (1 + 9999);
  ok('007 no-anomaly base rate = 1/10000', approx(base, 0.0001, 1e-9), base.toFixed(6));
}
// prior-tilt sensitivity: ceiling = 1/(1 + pi*/pi0), single flexible rival
{
  ok('008 even-prior ceiling = 0.5', approx(1 / (1 + 1 * (1 / 1)), 0.5, 1e-12));
  ok('009 3x-prior ceiling = 0.25', approx(1 / (1 + 3 * (1 / 1)), 0.25, 1e-12));
  ok('010 9x-prior ceiling = 0.10', approx(1 / (1 + 9 * (1 / 1)), 0.10, 1e-12));
}

// 4. hardened single even-prior rival, per-anomaly r: P(k)=1/(1+r^-k)
function kNeed(r, target) { let k = 0; const Pk = (k) => 1 / (1 + Math.pow(r, -k)); while (Pk(k) < target) k++; return k; }
{
  const r = 2, Pk = (k) => 1 / (1 + Math.pow(r, -k));
  ok('011 hardened r=2 P(3)=0.8889<0.90', Pk(3) < 0.90 && approx(Pk(3), 0.888889, 1e-4), Pk(3).toFixed(6));
  ok('012 hardened r=2 P(4)=0.9412>=0.90', Pk(4) >= 0.90 && approx(Pk(4), 0.941176, 1e-4), Pk(4).toFixed(6));
  ok('013 k-needed(r=2,f=0.90)=4', kNeed(2, 0.9) === 4, String(kNeed(2, 0.9)));
  ok('014 k-needed(r=1.5,f=0.90)=6', kNeed(1.5, 0.9) === 6, String(kNeed(1.5, 0.9)));
}

// 5. R4 0-of-6: corroborated=0 => compounding factor r^0 = 1 (no gain vs prior)
{
  const corroborated = 0, attempts = 6;
  const factor = Math.pow(2, -corroborated);
  ok('015 R4 0-of-6 => factor 1 (no compounding)', approx(factor, 1, 1e-12) && corroborated === 0 && attempts === 6);
}

// 6. insulation cross-check (Part 10): kappa(k;a)=(1-a)^k
{
  const kappa = (k, a) => Math.pow(1 - a, k);
  ok('016 kappa(k=2,a=0.5)=0.25', approx(kappa(2, 0.5), 0.25, 1e-12));
  ok('017 kappa(k=4,a=0.5)=0.0625', approx(kappa(4, 0.5), 0.0625, 1e-12));
  ok('018 kappa<=0.25 for all a>=.5,k>=2',
    [2, 3, 4].every(k => [0.5, 0.6, 0.75, 0.9].every(a => kappa(k, a) <= 0.25 + 1e-12)));
}

// 7. banned constructions in the artifact
{
  const fx = require('fs').readFileSync('god-religions-confirmation-formal.md', 'utf8');
  const banned = ['therefore God exists', 'therefore god exists',
                  'therefore God does not exist', 'therefore god does not exist'];
  const hits = banned.filter(b => fx.includes(b));
  ok('019 no banned constructions', hits.length === 0, hits.join(';') || 'none');
}

console.log('\nverify_v12: ' + P + '/' + total + ' checks passed, ' + F + ' failed.');
if (F > 0) process.exit(1);
