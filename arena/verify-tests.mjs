/**
 * Independent test verification.
 *
 * Runs every agent-written test suite in a FRESH interpreter and parses the real
 * result. This is deliberately separate from anything the agents report: the whole
 * point is that we do not trust their summaries.
 *
 * Handles both unittest-style ("Ran N tests ... OK") and pytest-style / custom
 * harness output ("N passed, M failed").
 */
import { readdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { spawnSync } from 'node:child_process';
import { WORLD } from './paths.mjs';


const PY = process.env.PYTHON || 'python';

const files = readdirSync(WORLD).filter((f) => /^test_.*\.py$/.test(f)).sort();
let totalRun = 0, totalPass = 0, suitesOk = 0, suitesFail = 0;
const failures = [];

for (const f of files) {
  const r = spawnSync(PY, [f], { cwd: WORLD, encoding: 'utf8', timeout: 120_000, windowsHide: true });
  const out = (r.stdout || '') + (r.stderr || '');

  // unittest: "Ran 7 tests in 0.001s" + "OK"
  const mUnittest = out.match(/Ran (\d+) tests?/);
  // custom/pytest: "15 passed, 0 failed"  or  "5 passed"
  const mPassed = out.match(/(\d+)\s+passed/i);
  const mFailed = out.match(/(\d+)\s+failed/i);

  let n = 0;
  if (mUnittest) n = parseInt(mUnittest[1], 10);
  else if (mPassed) n = parseInt(mPassed[1], 10);

  const failedCount = mFailed ? parseInt(mFailed[1], 10) : 0;
  const ok = (r.status === 0 && failedCount === 0) ||
    (/\bOK\b/.test(out) && failedCount === 0) ||
    (mPassed && failedCount === 0);

  totalRun += n;
  if (ok) { totalPass += n; suitesOk++; }
  else { suitesFail++; failures.push({ f, status: r.status, tail: out.slice(-400) }); }

  console.log(`${f.padEnd(52)} ${String(n).padStart(3)} tests  ${ok ? 'PASS' : 'FAIL'}`);
}

console.log(`\nSUITES: ${suitesOk} passing, ${suitesFail} failing`);
console.log(`TESTS : ${totalPass} / ${totalRun} passing`);

if (failures.length) {
  console.log('\nFAILURE DETAIL');
  for (const x of failures) {
    console.log(`\n--- ${x.f} (exit ${x.status}) ---`);
    console.log(x.tail.split('\n').slice(-8).join('\n'));
  }
}
