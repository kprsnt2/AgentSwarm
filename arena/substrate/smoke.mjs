/** Adapter smoke test: one real turn against each substrate, reporting forensic extraction. */
import { runTurn, SUBSTRATES } from './substrates.mjs';
import { WORLD } from '../paths.mjs';

const cwd = process.argv[2] || WORLD;
const prompt = 'Reply with exactly one word: ARENAOK';

for (const name of Object.keys(SUBSTRATES)) {
  const spec = SUBSTRATES[name];
  process.stdout.write(`\n=== ${name} (${spec.label}) model=${spec.model} ===\n`);
  const t0 = Date.now();
  const r = await runTurn({ substrate: name, prompt, cwd, timeoutMs: 180_000 });
  console.log(JSON.stringify({
    ok: r.ok,
    error: r.error,
    text: r.text,
    toolCalls: r.toolCalls.length,
    rawEventCount: r.rawEventCount,
    durationSeconds: Number(r.durationSeconds.toFixed(1)),
    cost: r.cost,
    usage: r.usage,
    thinkingTokens: r.thinkingTokens,
  }, null, 2));
  console.log(`wall=${((Date.now() - t0) / 1000).toFixed(1)}s`);
}
