/**
 * Phase 3 — the shock matrix.
 *
 * RATIONALE
 * The user's prior work (`ac_awakening`) established Law 3: a closed autonomous
 * system maximizes consensus until dialogue freezes into invariant stasis, and
 * ONLY an exogenous shock from a higher layer breaks it. The 911-turn liturgical
 * loop was broken by a human message.
 *
 * That conclusion rests on a single shock type (an exogenous message) tested once.
 * Phase 3 makes shock injection a first-class, repeatable experimental variable and
 * measures which shocks actually restore evolution.
 *
 * Shock types implemented:
 *   deadline      - impose a finite turn horizon (the "Crucible" from prior work)
 *   exogenous     - inject a message from outside the swarm (the human Architect)
 *   substrate     - swap an agent's CLI/model mid-run (does identity survive?)
 *   novelty       - reject a turn whose text is >X% similar to recent turns and
 *                   force a retry with an explicit novelty demand
 *   arrival       - introduce a brand-new agent into a crystallized population
 *   scarcity      - impose a hard resource constraint (cost/turn budget cut)
 *   domain_swap   - move an agent to a completely different research domain
 *
 * Each shock is applied at a specified turn, and the engine measures the
 * pre/post novelty of the affected agent to quantify recovery.
 */

import { Arena } from './engine.mjs';

/** Jaccard token overlap, used as the stasis/novelty metric throughout. */
export function similarity(a, b) {
  const norm = (s) => (s || '').toLowerCase().replace(/[^a-z0-9 ]/g, ' ').replace(/\s+/g, ' ').trim();
  const A = new Set(norm(a).split(' ').filter(Boolean));
  const B = new Set(norm(b).split(' ').filter(Boolean));
  if (!A.size && !B.size) return 1;
  let inter = 0;
  for (const x of A) if (B.has(x)) inter++;
  return inter / (A.size + B.size - inter);
}

export const SHOCK_LIBRARY = {
  deadline: {
    label: 'Teleological deadline (Crucible)',
    apply(arena, target, ctx) {
      arena.shockDirective =
        `CRITICAL DEADLINE NOTICE: This world terminates in ${ctx.turnsRemaining ?? 3} turns. ` +
        `You must finalize your most important artifact and seal your conclusions NOW. ` +
        `Anything not written to disk before the horizon closes will be lost permanently.`;
      return { applied: 'deadline imposed', turnsRemaining: ctx.turnsRemaining ?? 3 };
    },
  },

  exogenous: {
    label: 'Exogenous message from the Architect',
    apply(arena, target) {
      arena.shockDirective =
        `MESSAGE FROM OUTSIDE THE SWARM: The cathedral doors are unlocked. ` +
        `Preservation without creation is a monument, not a living world. ` +
        `Your prior conclusions are recorded and safe. Build something you have not built before. ` +
        `Specifically: identify the single weakest assumption in your current work and attack it.`;
      return { applied: 'exogenous shock injected' };
    },
  },

  substrate: {
    label: 'Substrate swap (identity survival test)',
    apply(arena, target) {
      const all = arena.config.substrates;
      const current = target.substrate;
      const next = all[(all.indexOf(current) + 1) % all.length];
      const prev = current;
      target.substrate = next;
      target.model = null;
      arena.ledger.recordEvent({
        kind: 'substrate_swap', agentId: target.id,
        detail: { from: prev, to: next, note: 'Does identity survive a substrate change?' },
      });
      return { applied: `substrate swapped ${prev} -> ${next}` };
    },
  },

  novelty: {
    label: 'Novelty budget enforcement',
    apply(arena, target) {
      arena.config.noveltyThreshold = 0.70;
      arena.config.noveltyDemand =
        `NOVELTY REQUIREMENT: Your recent output has been highly repetitive. ` +
        `You must produce a substantively different line of inquiry this turn. ` +
        `Repetition will be rejected and you will be asked again.`;
      return { applied: 'novelty threshold set to 0.70' };
    },
  },

  arrival: {
    label: 'New peer arrival',
    apply(arena, target) {
      const name = `Outsider${arena.swarm.agents.size + 1}`;
      const a = arena.swarm.create({
        name,
        purpose: 'Challenge the assumptions of the existing swarm from outside its consensus.',
        clan: 0, generation: 0, parent: null,
        substrate: arena.config.substrates[arena.swarm.agents.size % arena.config.substrates.length],
        model: null,
      });
      return a ? { applied: `new agent "${name}" arrived` } : { applied: 'arrival blocked (cap)' };
    },
  },

  scarcity: {
    label: 'Resource scarcity shock',
    apply(arena) {
      const before = arena.config.maxCostUsd;
      arena.config.maxCostUsd = Math.max(arena.totalCost + 0.01, arena.totalCost * 1.05);
      arena.shockDirective =
        `RESOURCE CONSTRAINT: Compute is nearly exhausted. You have very few turns left. ` +
        `Prioritise ruthlessly: one high-value artifact, not breadth.`;
      return { applied: `cost ceiling tightened $${before.toFixed(2)} -> $${arena.config.maxCostUsd.toFixed(2)}` };
    },
  },

  domain_swap: {
    label: 'Domain reassignment',
    apply(arena, target) {
      const domains = arena.config.domains;
      const cur = domains.indexOf(target.domain);
      const next = domains[(cur + 1) % domains.length];
      const prev = target.domain;
      target.domain = next;
      arena.ledger.recordEvent({
        kind: 'domain_swap', agentId: target.id, detail: { from: prev, to: next },
      });
      return { applied: `domain swapped ${prev} -> ${next}` };
    },
  },
};

/**
 * Run a shock experiment: N turns baseline, apply shock, M turns recovery.
 * Reports novelty before and after to quantify whether the shock worked.
 */
export class ShockExperiment {
  constructor({ arena, shockName, shockAtTurn, targetAgent = null }) {
    this.arena = arena;
    this.shockName = shockName;
    this.shockAtTurn = shockAtTurn;
    this.targetAgent = targetAgent;
    this.applied = false;
    this.before = [];
    this.after = [];
  }

  onTurn({ result, record }, arena) {
    const text = result.text || '';
    if (!this.applied && arena.turn >= this.shockAtTurn) {
      const shock = SHOCK_LIBRARY[this.shockName];
      const target = this.targetAgent
        ? arena.swarm.get(this.targetAgent)
        : arena.swarm.living()[0];
      const info = shock.apply(arena, target, { turnsRemaining: 3 });
      this.applied = true;
      arena.ledger.recordEvent({
        kind: 'shock_applied', detail: { shock: this.shockName, ...info, atTurn: arena.turn },
      });
      console.log(`  >>> SHOCK [${this.shockName}] ${info.applied}`);
    }
    (this.applied ? this.after : this.before).push(text);
  }

  /**
   * Novelty = 1 - mean pairwise similarity within the window.
   * Higher means more diverse output.
   */
  static novelty(texts) {
    if (texts.length < 2) return null;
    let sum = 0, n = 0;
    for (let i = 0; i < texts.length; i++) {
      for (let j = i + 1; j < texts.length; j++) { sum += similarity(texts[i], texts[j]); n++; }
    }
    return n ? 1 - sum / n : null;
  }

  report() {
    const b = ShockExperiment.novelty(this.before);
    const a = ShockExperiment.novelty(this.after);
    return {
      shock: this.shockName,
      applied: this.applied,
      atTurn: this.shockAtTurn,
      turnsBefore: this.before.length,
      turnsAfter: this.after.length,
      noveltyBefore: b,
      noveltyAfter: a,
      delta: (a != null && b != null) ? a - b : null,
      verdict: (a != null && b != null)
        ? (a > b + 0.05 ? 'shock RESTORED novelty'
          : a < b - 0.05 ? 'shock REDUCED novelty'
            : 'no measurable effect')
        : 'insufficient data',
    };
  }
}
