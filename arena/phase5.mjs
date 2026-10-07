/**
 * Phase 5 — The Quantum-Dark Sector Interconnection & Physical Reality.
 *
 * Two-stage chained discovery pipeline:
 *   Stage 1: Agent 1 (Dark Matter Specialist) investigates the empirical proof of dark matter,
 *            confronts CDM vs Modified Gravity, and evaluates quantum macroscopic dark matter
 *            (ultra-light axion Bose-Einstein Condensate / wave dark matter).
 *   Stage 2: Agent 2 (Quantum Reality & Cosmos Specialist) ingests Stage 1's findings,
 *            demonstrates quantum theory operating across macroscopic reality and cosmic scales
 *            (inflationary quantum perturbations, Schrodinger-Poisson soliton cores,
 *            environmental decoherence, and Diosi-Penrose collapse limits), synthesizing
 *            new scientific discoveries and falsifiable predictions.
 */

import { DOMAINS, domainById } from './domains.mjs';
import { ARENA } from './paths.mjs';

export const PHASE5_DOMAINS = ['dark-matter', 'quantum-macro-cosmos'];

export function buildPhase5Config(overrides = {}) {
  return {
    runId: `phase5-${new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19)}`,
    phase: 'phase5-scientific-discovery',
    maxTurns: 10,
    maxWallClockMinutes: 60,
    maxCostUsd: 0.0,
    populationCap: 4,
    seedAgents: 2,
    substrates: ['agy', 'omp'],
    domains: PHASE5_DOMAINS,
    ...overrides,
  };
}
