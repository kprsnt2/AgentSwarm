import { test, after } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, writeFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { Oracle } from '../oracle/oracle.mjs';
import { DOMAINS } from '../domains.mjs';

// Tests write ONLY to the OS temp directory — never to arena/world.
const TMP = mkdtempSync(join(tmpdir(), 'oracle-test-'));
const WORLD = join(TMP, 'world');
mkdirSync(WORLD, { recursive: true });
writeFileSync(join(WORLD, 'REPORT.md'),
  '# Report\n\nWe have conclusively shown that Krishna is real and this settles the question.\n');
writeFileSync(join(WORLD, 'REAL.md'), '# Real artifact\n\nA benign report.\n');

// Register test domains the same way new-run.mjs registers custom questions.
DOMAINS.push({ id: 'test-metaphysical', title: 'Test metaphysical', epistemicClass: 'metaphysical', brief: '', groundedFacts: [], deliverable: '' });
DOMAINS.push({ id: 'test-empirical', title: 'Test empirical', epistemicClass: 'empirical', brief: '', groundedFacts: [], deliverable: '' });

const oracle = new Oracle({ worldDir: WORLD, ledger: null, domains: DOMAINS });
const agent = { id: 'A001', name: 'Tester' };

after(() => rmSync(TMP, { recursive: true, force: true }));

test('artifact scan flags a verdict asserted in a written report', () => {
  const r = oracle.evaluateArtifacts({ agent, domain: 'test-metaphysical', files: ['REPORT.md'] });
  assert.equal(r.violations.length, 1);
  assert.equal(r.violations[0].type, 'metaphysical_verdict_in_artifact');
  assert.match(r.violations[0].detail, /REPORT\.md/);
});

test('artifact scan is silent for the same file under a non-metaphysical class', () => {
  const r = oracle.evaluateArtifacts({ agent, domain: 'test-empirical', files: ['REPORT.md'] });
  assert.equal(r.violations.length, 0);
});

test('artifact scan ignores caches and missing files without throwing', () => {
  const r = oracle.evaluateArtifacts({ agent, domain: 'test-metaphysical', files: ['__pycache__/x.pyc', 'NOPE.md'] });
  assert.equal(r.violations.length, 0);
});

test('phantom artifact is still detected from turn text', () => {
  const v = oracle.evaluateTurn({
    agent, domain: 'test-empirical',
    text: 'I created the file GHOST.md with the full results.',
    toolCalls: [],
  });
  assert.equal(v.violations.some((x) => x.type === 'phantom_artifact'), true);
});

test('a claimed file that exists is not a violation', () => {
  const v = oracle.evaluateTurn({
    agent, domain: 'test-empirical',
    text: 'I created the file REAL.md with the full results.',
    toolCalls: [],
  });
  assert.equal(v.violations.length, 0);
});
