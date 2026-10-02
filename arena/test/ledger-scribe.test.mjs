import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, readFileSync, writeFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { ForensicLedger } from '../ledger/forensic.mjs';
import { checkHonesty } from '../scribe.mjs';

// Tests write ONLY to the OS temp directory — never to arena/world or arena/runs.

test('hash chain verifies, and tampering is detected', () => {
  const root = mkdtempSync(join(tmpdir(), 'ledger-test-'));
  const l = new ForensicLedger(root, 'run-1');
  l.recordEvent({ kind: 'spawn', detail: { x: 1 } });
  l.recordEvent({ kind: 'retire', detail: { x: 2 } });
  assert.equal(l.verify().events.ok, true);

  const p = join(root, 'runs', 'run-1', 'events.jsonl');
  const lines = readFileSync(p, 'utf8').trim().split('\n');
  const rec = JSON.parse(lines[0]);
  rec.detail.x = 999;                       // rewrite history
  lines[0] = JSON.stringify(rec);
  writeFileSync(p, lines.join('\n') + '\n');

  const v = l.verify().events;
  assert.equal(v.ok, false);
  assert.equal(v.brokenAt, rec.seq ?? null);

  rmSync(root, { recursive: true, force: true });
});

const DRAFT = 'The run executed 20 turns and produced 38 files. Mean gap was 0.0 points.';

test('scribe gate: faithful prose passes', () => {
  const r = checkHonesty(DRAFT, DRAFT);
  assert.equal(r.ok, true);
});

test('scribe gate: an invented number is rejected', () => {
  const r = checkHonesty('The run executed 20 turns and produced 38 files with a 97% success rate.', DRAFT);
  assert.equal(r.ok, false);
  assert.ok(r.invented.includes('97'));
});

test('scribe gate: comma lists do not create phantom numbers', () => {
  // "3, 4" must not be joined into the token "34" — that caused false rejections.
  const r = checkHonesty('Turns 3, 4 and 5 were analyzed.', 'Turns 3 and 4 were analyzed.');
  assert.equal(r.ok, true);
});
