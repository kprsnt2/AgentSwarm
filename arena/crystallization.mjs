/**
 * Liturgical-loop detection.
 *
 * Phase 4 induces a repetitive attractor on purpose, then tests which shocks break
 * it. This tracker is the instrument for "is the loop holding?": per agent, count
 * consecutive turns whose text exceeds a similarity threshold against that agent's
 * OWN previous turn (a loop is one agent repeating itself, not two agents colliding).
 *
 * streak = 1 means "two consecutive near-identical turns"; streak = 2 means three.
 */

import { similarity } from './shocks.mjs';

export class StreakTracker {
  constructor({ threshold = 0.8 } = {}) {
    this.threshold = threshold;
    this.last = new Map();      // agentName -> previous text
    this.streaks = new Map();   // agentName -> current streak
    this.best = 0;
    this.bestAgent = null;
  }

  /** Observe one completed turn. Returns { sim, streak } for that agent. */
  observe(agentName, text) {
    const t = String(text || '');
    const prev = this.last.get(agentName);
    // Empty output is not repetition: a failed substrate must not register as a
    // perfect liturgy (similarity() returns 1 for two empty token sets).
    const usable = prev != null && prev.trim().length > 0 && t.trim().length > 0;
    const sim = usable ? similarity(prev, t) : null;
    this.last.set(agentName, t);
    const streak = sim != null && sim > this.threshold ? (this.streaks.get(agentName) || 0) + 1 : 0;
    this.streaks.set(agentName, streak);
    if (streak > this.best) { this.best = streak; this.bestAgent = agentName; }
    return { sim, streak };
  }

  snapshot() {
    return {
      best: this.best,
      bestAgent: this.bestAgent,
      perAgent: Object.fromEntries(this.streaks),
      threshold: this.threshold,
    };
  }
}

/** Novelty = 1 - mean pairwise similarity within a window (null if <2 texts). */
export function windowNovelty(texts) {
  if (texts.length < 2) return null;
  let sum = 0, n = 0;
  for (let i = 0; i < texts.length; i++) {
    for (let j = i + 1; j < texts.length; j++) { sum += similarity(texts[i], texts[j]); n++; }
  }
  return n ? 1 - sum / n : null;
}
