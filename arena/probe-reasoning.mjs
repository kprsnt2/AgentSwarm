import { runTurn } from './substrate/substrates.mjs';

// Ask a question that forces visible reasoning, then confirm we captured it.
const r = await runTurn({
  substrate: 'omp',
  model: 'google-antigravity/gemini-3.8-flash',
  prompt: 'Think carefully: if a spacecraft accelerates at 1g continuously, how long does a crew experience travelling to Proxima Centauri (4.2 ly)? Show your reasoning, then state the answer in one line.',
  cwd: 'D:\\AgentSwarm\\arena\\world',
  timeoutMs: 300000,
  runDirOverride: 'D:\\AgentSwarm\\arena\\runs\\reasonprobe',
  turnTag: 'reasoning',
});

console.log('ok        =', r.ok);
console.log('tools     =', r.toolCalls.length);
console.log('thinkTok  =', r.thinkingTokens);
console.log('reasoningChars =', r.reasoningChars);
console.log('reasoningBlocks =', r.reasoningBlocks);
console.log('\n--- CAPTURED REASONING (first 900 chars) ---');
console.log((r.reasoning || '(EMPTY — reasoning not captured)').slice(0, 900));
console.log('\n--- FINAL ANSWER (first 300 chars) ---');
console.log((r.text || '').slice(0, 300));
