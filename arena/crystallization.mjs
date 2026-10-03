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

  /**
   * Clear streak counters (keeping the last-seen texts). Called when a shock is
   * applied so that "did the loop re-form?" counts only streaks that START after
   * the shock — otherwise a streak begun before it is credited to the recovery.
   */
  resetStreaks() {
    this.streaks = new Map();
    this.best = 0;
    this.bestAgent = null;
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

/**
 * Novelty = 1 - mean pairwise similarity within a window (null if <2 usable texts).
 *
 * Empty turns are dropped: a failed or truncated turn carries no content, and an
 * empty token set is dissimilar to everything, which would INFLATE novelty. One
 * empty turn in a 12-turn window was worth ~0.06 of spurious novelty in the pi
 * durability pass.
 */
export function windowNovelty(texts) {
  const t = (texts || []).map((s) => String(s || '')).filter((s) => s.trim().length > 0);
  if (t.length < 2) return null;
  let sum = 0, n = 0;
  for (let i = 0; i < t.length; i++) {
    for (let j = i + 1; j < t.length; j++) { sum += similarity(t[i], t[j]); n++; }
  }
  return n ? 1 - sum / n : null;
}
