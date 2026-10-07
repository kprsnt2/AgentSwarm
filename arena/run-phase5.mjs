/**
 * Phase 5 runner — Sequential Two-Agent Discovery Pipeline:
 *   Domain 1: dark-matter (Proof, evidence, and nature of dark matter)
 *   Domain 2: quantum-macro-cosmos (Quantum mechanics in macroscopic reality & cosmos)
 *
 * Sequence:
 *   Agent 1 investigates Dark Matter, outputs empirical proof, simulation, and handover params.
 *   Agent 2 receives Agent 1's findings, investigates Quantum Cosmos & Macro Reality,
 *   and synthesizes new scientific discoveries.
 */

import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { execSync } from 'node:child_process';
import { ARENA } from './paths.mjs';
import { buildPhase5Config } from './phase5.mjs';

function parseArgs() {
  const args = process.argv.slice(2);
  return {
    dry: args.includes('--dry'),
    runId: args.find(a => a.startsWith('--runId='))?.split('=')[1],
  };
}

const { dry, runId } = parseArgs();
const config = buildPhase5Config(runId ? { runId } : {});

console.log('='.repeat(70));
console.log('PHASE 5: QUANTUM-DARK SECTOR INTERCONNECTION & SCIENTIFIC DISCOVERY');
console.log(`Run ID: ${config.runId}`);
console.log(`Domains: ${config.domains.join(' -> ')}`);
console.log('='.repeat(70));

if (dry) {
  console.log('Dry run requested. Configuration validated.');
  process.exit(0);
}

console.log('\n[Stage 1] Verifying Agent 1 (Dark Matter) research engine...');
const a1Script = join(ARENA, 'world', 'a001_phase5_dark_matter_empirical_proof.py');
if (existsSync(a1Script)) {
  try {
    const out = execSync(`python "${a1Script}"`, { encoding: 'utf8' });
    console.log('Agent 1 engine verified successfully:\n' + out.trim());
  } catch (err) {
    console.error('Agent 1 engine execution failed:', err.message);
  }
} else {
  console.log(`Note: Run agent or execute script when generated: ${a1Script}`);
}

console.log('\n[Stage 2] Verifying Agent 2 (Quantum Cosmos) research engine...');
const a2Script = join(ARENA, 'world', 'a002_phase5_quantum_cosmos_macro_reality.py');
if (existsSync(a2Script)) {
  try {
    const out = execSync(`python "${a2Script}"`, { encoding: 'utf8' });
    console.log('Agent 2 engine verified successfully:\n' + out.trim());
  } catch (err) {
    console.error('Agent 2 engine execution failed:', err.message);
  }
} else {
  console.log(`Note: Run agent or execute script when generated: ${a2Script}`);
}
