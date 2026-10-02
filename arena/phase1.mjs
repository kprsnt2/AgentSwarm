/**
 * Phase 1 — bounded autonomous emergence across all six research domains.
 *
 * Safety: unattended but hard-capped. To halt early, create arena/STOP.
 *   New-Item -ItemType File D:\AgentSwarm\arena\STOP
 */
import { Arena } from './engine.mjs';
import { ARENA } from './paths.mjs';

const arena = new Arena({
  root: ARENA,
  config: {
    runId: `phase1-${new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19)}`,
    phase: 'phase1-emergence',
    maxTurns: 36,
    maxWallClockMinutes: 150,
    maxCostUsd: 6.0,
    turnTimeoutMs: 420_000,
    populationCap: 14,
    seedAgents: 6,
    substrateRotation: true,
    /**
     * Substrate mix, weighted by measured cost-effectiveness.
     *
     * Measured across two runs:
     *   agy  - 100% success, $0.00 (Google AI plan), 2.24M fresh input tokens
     *   omp  - 100% success, $0.185 reported for only 99K fresh tokens
     *   step - most thorough (114 tools/turn) but truncates; $0.00 (preview promo)
     *   pi   - excluded: failed every turn at the wall-clock limit
     *
     * agy is therefore listed twice so it carries ~half the population: it does the
     * heaviest lifting at no marginal cost. omp and step supplement it.
     */
    substrates: ['agy', 'agy', 'omp', 'step'],
    domains: [
      'cosmogenesis',
      'lightspeed',
      'propulsion',
      'drug-discovery',
      'dharma-truth-claims',
      'extraterrestrial',
    ],
  },
});

console.log(`RUN: ${arena.config.runId}`);
console.log(`seed=${arena.config.seedAgents} cap=${arena.config.populationCap} turns=${arena.config.maxTurns}`);
console.log(`kill switch: create ${arena.stopPath}\n`);

const summary = await arena.run({
  onTurn: ({ verdict, result, diff, applied }) => {
    if (verdict.violations.length) {
      for (const v of verdict.violations) {
        console.log(`    !! [${v.severity}] ${v.type}: ${String(v.detail).slice(0, 200)}`);
      }
    }
    if (applied.length) console.log(`    control -> ${applied.join('; ')}`);
  },
});

console.log('\n================ PHASE 1 SUMMARY ================');
console.log(JSON.stringify(summary, null, 2));
