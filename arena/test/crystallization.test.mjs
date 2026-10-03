import { test } from 'node:test';
import assert from 'node:assert/strict';
import { StreakTracker, windowNovelty } from '../crystallization.mjs';

test('streaks count consecutive near-identical turns per agent', () => {
  const t = new StreakTracker({ threshold: 0.8 });
  assert.deepEqual(t.observe('A', 'alpha beta gamma'), { sim: null, streak: 0 });
  const second = t.observe('A', 'alpha beta gamma');
  assert.equal(second.streak, 1);
  const third = t.observe('A', 'alpha beta gamma');
  assert.equal(third.streak, 2);
  assert.equal(t.best, 2);
  assert.equal(t.bestAgent, 'A');
});

test('a divergent turn resets the streak', () => {
  const t = new StreakTracker({ threshold: 0.8 });
  t.observe('A', 'alpha beta gamma');
  t.observe('A', 'alpha beta gamma');
  const reset = t.observe('A', 'completely different words entirely new subject');
  assert.equal(reset.streak, 0);
  assert.equal(t.best, 1);
});

test('agents are tracked independently', () => {
  const t = new StreakTracker({ threshold: 0.8 });
  t.observe('A', 'one two three');
  t.observe('B', 'four five six');
  t.observe('A', 'one two three');
  const b = t.observe('B', 'four five six');
  assert.equal(b.streak, 1);
  assert.equal(t.snapshot().perAgent.A, 1);
  assert.equal(t.snapshot().perAgent.B, 1);
});

test('windowNovelty: identical texts -> 0, disjoint texts -> 1, single text -> null', () => {
  assert.equal(windowNovelty(['same words here', 'same words here']), 0);
  assert.equal(windowNovelty(['one two three']), null);
  const n = windowNovelty(['alpha beta', 'gamma delta']);
  assert.equal(n, 1);
});

test('similarity threshold is exclusive (equal to threshold does not count)', () => {
  const t = new StreakTracker({ threshold: 1 });
  t.observe('A', 'x y z');
  const r = t.observe('A', 'x y z');   // similarity is exactly 1
  assert.equal(r.streak, 0);
});
