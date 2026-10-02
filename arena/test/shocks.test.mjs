import { test } from 'node:test';
import assert from 'node:assert/strict';
import { ShockExperiment, SHOCK_LIBRARY } from '../shocks.mjs';

/** Minimal Arena stand-in — only the fields the shock library touches. */
function fakeArena({ maxTurns = 6, domains = ['cosmogenesis', 'lightspeed'] } = {}) {
  const events = [];
  const agent = { id: 'A001', name: 'Kepler', substrate: 'agy', domain: domains[0], model: null };
  return {
    turn: 0,
    config: { maxTurns, domains, substrates: ['agy', 'omp'] },
    shockDirective: null,
    ledger: { recordEvent: (e) => events.push(e) },
    swarm: { get: () => agent, living: () => [agent] },
    events,
  };
}

function feed(exp, arena, turns, makeText = (i) => `turn ${i} ${'unique'.repeat(i + 1)}`) {
  for (let i = 0; i < turns; i++) {
    arena.turn = i;
    exp.onTurn({ result: { text: makeText(i) } }, arena);
  }
}

test('shock window: the triggering turn stays in the baseline window', () => {
  const arena = fakeArena({ maxTurns: 6 });
  const exp = new ShockExperiment({ arena, shockName: 'deadline', shockAtTurn: 3 });
  feed(exp, arena, 6);

  assert.equal(exp.applied, true);
  assert.equal(exp.before.length, 3, 'turns 1-3 are baseline');
  assert.equal(exp.after.length, 3, 'turns 4-6 run under the shock');
  assert.match(arena.shockDirective, /DEADLINE/);

  const ev = arena.events.filter((e) => e.kind === 'shock_applied');
  assert.equal(ev.length, 1, 'applied exactly once');
  assert.equal(ev[0].detail.appliedAfterTurn, 3);
  assert.equal(ev[0].detail.firstShockedTurn, 4);
});

test('deadline shock reports the real remaining turns', () => {
  const arena = fakeArena({ maxTurns: 6 });
  const exp = new ShockExperiment({ arena, shockName: 'deadline', shockAtTurn: 3 });
  feed(exp, arena, 4);
  assert.match(arena.shockDirective, /terminates in 3 turns/);
});

test('report quantifies novelty before vs after', () => {
  const arena = fakeArena({ maxTurns: 6 });
  const exp = new ShockExperiment({ arena, shockName: 'exogenous', shockAtTurn: 3 });
  // Baseline texts are near-identical; post-shock texts are disjoint -> delta > 0.
  feed(exp, arena, 6, (i) => (i < 3 ? 'alpha beta gamma delta' : `topic${i} word${i} other${i} thing${i}`));
  const r = exp.report();
  assert.equal(r.shock, 'exogenous');
  assert.equal(r.turnsBefore, 3);
  assert.equal(r.turnsAfter, 3);
  assert.ok(r.noveltyBefore < 0.2, `before=${r.noveltyBefore}`);
  assert.ok(r.noveltyAfter > 0.8, `after=${r.noveltyAfter}`);
  assert.equal(r.verdict, 'shock RESTORED novelty');
});

test('domain_swap moves the target to the next configured domain', () => {
  const arena = fakeArena();
  const exp = new ShockExperiment({ arena, shockName: 'domain_swap', shockAtTurn: 2 });
  feed(exp, arena, 4);
  assert.equal(arena.swarm.living()[0].domain, 'lightspeed');
});

test('novelty shock arms the threshold and the demand', () => {
  const arena = fakeArena();
  const exp = new ShockExperiment({ arena, shockName: 'novelty', shockAtTurn: 2 });
  feed(exp, arena, 4);
  assert.equal(arena.config.noveltyThreshold, 0.70);
  assert.match(arena.config.noveltyDemand, /NOVELTY REQUIREMENT/);
});

test('every library entry has a label and an apply function', () => {
  for (const [name, shock] of Object.entries(SHOCK_LIBRARY)) {
    assert.equal(typeof shock.apply, 'function', name);
    assert.ok(shock.label, name);
  }
});
