import { test } from 'node:test';
import assert from 'node:assert/strict';
import { inferClass } from '../classify.mjs';

test('deity truth claims infer metaphysical, not exploratory', () => {
  const questions = [
    'what about Lord Krishna and he is real, Mahabharata happened?',
    'Is Shiva real?',
    'Are the Hindu gods true?',
    'does the soul survive death?',
  ];
  for (const q of questions) {
    const r = inferClass(q);
    assert.equal(r.cls, 'metaphysical', q);
    assert.equal(r.confidence, 'high', q);
  }
});

test('questions about what a text says stay historical', () => {
  assert.equal(inferClass('what do Hindu texts say about multiple universes').cls, 'historical');
  assert.equal(inferClass('what does the Rigveda say about creation').cls, 'historical');
});

test('aliens stay exploratory', () => {
  assert.equal(inferClass('are aliens real?').cls, 'exploratory');
  assert.equal(inferClass('is there extraterrestrial life').cls, 'exploratory');
});

test('engineering and empirical rules still fire', () => {
  assert.equal(inferClass('can we build a fusion reactor by 2040?').cls, 'engineering');
  assert.equal(inferClass('what is the measured density of the intergalactic medium?').cls, 'empirical');
});

test('stem forms match (achievable, historical, measurable)', () => {
  assert.equal(inferClass('Is commercial fusion power achievable by 2040?').cls, 'engineering');
  assert.equal(inferClass('archaeological evidence for the Mahabharata war').cls, 'historical');
  assert.equal(inferClass('how measurable is the Hubble tension?').cls, 'empirical');
});

test('low confidence is reported, never silently guessed', () => {
  const r = inferClass('is P=NP provable?');
  assert.equal(r.confidence, 'low');
  assert.match(r.why, /refusing to guess/);
});
