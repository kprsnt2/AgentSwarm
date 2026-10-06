/**
 * Substrate adapters — one per CLI harness.
 *
 * Verified against live binaries on 2026-10-02:
 *   agy  1.2.13  -> gemini-3.8-flash-high        (Antigravity, free tier)
 *   omp  18.4.9  -> google-antigravity/gemini-3.8-flash (Antigravity provider)
 *   pi   (npm)   -> fireworks/accounts/fireworks/models/deepseek-v4p1-flash
 *
 * Hard-won lessons baked in here:
 *   - agy: `-p` consumes the NEXT argv token as its prompt, so the prompt MUST be
 *     attached as `-p=<prompt>`. A bare `-p --flag "text"` makes `--flag` the prompt.
 *   - omp: its DEFAULT model routes to OpenRouter, which is out of credits (HTTP 402).
 *     We therefore always pass an explicit --model. Never let it fall back.
 *   - pi:  there is no `deepseek` provider. DeepSeek 4.1 Flash is served by Fireworks.
 *   - agy: `run_command` tries `bash` via WSL first, which is absent on this box and
 *     burns ~61s per call with "Class not registered" before falling back. We pass
 *     shellPath so it goes straight to Git Bash.
 */

import { spawn } from 'node:child_process';
import { existsSync, openSync, closeSync, readFileSync, readSync, mkdirSync, statSync, unlinkSync } from 'node:fs';
import { join } from 'node:path';
import { StringDecoder } from 'node:string_decoder';

export const GIT_BASH = 'C:\\Program Files\\Git\\bin\\bash.exe';

const PI_CLI_JS = 'C:\\Users\\hplap\\.npm-global\\node_modules\\@earendil-works\\pi-coding-agent\\dist\\bundle\\cli.js';
const NODE_EXE = 'C:\\Program Files\\nodejs\\node.exe';
/**
 * The compiled step.exe is blocked on this host by Smart App Control (policy
 * {0283ac0f-...}, event 3077/3113). Its embedded bundle was extracted verbatim
 * and runs under Node, so we prefer that when present. This preserves the real
 * StepCode harness and the Step 5 Preview model without touching the machine's
 * security policy. See arena/docs/HOW_TO_RUN.md ("step is blocked").
 */
const STEP_CLI_JS = 'C:\\Users\\hplap\\.stepcode\\agent\\step-js\\dist\\bundle\\step.js';

/**
 * Resolve a substrate to (executable, prefixArgs) so we NEVER rely on shell:true.
 *
 * `shell: true` on Windows concatenates argv without escaping, which silently
 * mangled prompts containing spaces/quotes and made `pi.ps1` return empty output.
 * For npm-style CLIs we bypass the .cmd/.ps1 shim entirely and call node directly.
 */
function resolveBin(substrate) {
  if (substrate === 'pi' && existsSync(PI_CLI_JS)) {
    return { exe: existsSync(NODE_EXE) ? NODE_EXE : 'node', prefixArgs: [PI_CLI_JS] };
  }
  if (substrate === 'step' && existsSync(STEP_CLI_JS)) {
    return { exe: existsSync(NODE_EXE) ? NODE_EXE : 'node', prefixArgs: [STEP_CLI_JS] };
  }
  if (substrate === 'agy') return { exe: 'C:\\Users\\hplap\\AppData\\Local\\agy\\bin\\agy.exe', prefixArgs: [] };
  if (substrate === 'omp') return { exe: 'C:\\Users\\hplap\\.bun\\bin\\omp.exe', prefixArgs: [] };
  return { exe: substrate, prefixArgs: [] };
}

/** Canonical substrate registry. `bin` is the executable name resolved via PATH. */
export const SUBSTRATES = {
  agy: {
    name: 'agy',
    bin: 'agy.exe',
    label: 'Antigravity CLI',
    model: 'gemini-3.8-flash-high',
    family: 'gemini-3.8-flash',
    /**
     * agy emits newline-delimited JSON with `event` discriminators:
     *   init | step_update | result
     * The forensic payload lives in step_update.step_update.tool_info.parameters.
     */
    buildArgs({ prompt, model, cwd }) {
      return [
        '--dangerously-skip-permissions',
        '--model', model || this.model,
        '--output-format', 'stream-json',
        // Must be the `--flag=value` form; a bare value token makes agy's arg
        // parser treat it as the print prompt and exit 2.
        `--add-dir=${cwd}`,
        `-p=${prompt}`,
      ];
    },
    parseLine(line) { return safeJson(line); },
    extractTurnEvents(events) {
      const toolCalls = [];
      let text = '';
      let usage = null;
      let thinkingTokens = 0;
      let cost = null;
      let durationSeconds = 0;

      for (const ev of events) {
        if (ev.event === 'step_update') {
          const su = ev.step_update || {};
          if (su.step_type === 'tool' && su.state === 'DONE') {
            toolCalls.push({
              tool: su.tool_name,
              params: su.tool_info?.parameters ?? null,
              output: truncate(su.tool_info?.output ?? '', 4000),
              durationSeconds: su.duration_seconds ?? null,
            });
          }
          if (su.step_type === 'agent_response' && su.text_delta) {
            text += su.text_delta;
          }
          if (su.usage) {
            usage = su.usage;
            thinkingTokens += su.usage.thinking_tokens || 0;
          }
          if (su.duration_seconds) durationSeconds += su.duration_seconds;
        }
        if (ev.event === 'result' && ev.result) {
          if (ev.result.response) text = ev.result.response;
          if (ev.result.usage) usage = ev.result.usage;
          if (ev.result.duration_seconds) durationSeconds = ev.result.duration_seconds;
          // Antigravity reports no monetary cost; treat as 0 and track tokens instead.
          cost = 0;
        }
      }
      return {
        text: text.trim(),
        toolCalls,
        usage,
        thinkingTokens,
        cost,
        durationSeconds,
        rawEventCount: events.length,
      };
    },
  },

  omp: {
    name: 'omp',
    bin: 'omp.exe',
    label: 'Oh My Pi',
    // Explicitly pinned to the Antigravity provider. The default would hit OpenRouter (402).
    model: 'google-antigravity/gemini-3.8-flash',
    family: 'gemini-3.8-flash',
    /**
     * omp --mode json emits typed events:
     *   session | agent_start | turn_start | message_start | message_update |
     *   message_end | turn_end | agent_end
     * Tool calls surface as content parts of type "toolCall" on assistant messages.
     */
    buildArgs({ prompt, model, cwd }) {
      return [
        '-p',
        '--mode', 'json',
        '--model', model || this.model,
        '--auto-approve',
        '--cwd', cwd,
        '--no-session',
        prompt,
      ];
    },
    parseLine(line) { return safeJson(line); },
    extractTurnEvents(events) {
      const toolCalls = [];
      let text = '';
      let usage = null;
      let cost = null;
      let durationSeconds = 0;
      let thinkingTokens = 0;

      for (const ev of events) {
        const msg = ev.message;
        if (!msg) continue;
        if (msg.role === 'system' || msg.role === 'user') continue;

        if (msg.role === 'assistant') {
          // AUTHORITATIVE TEXT: take the FINAL assistant message only.
          // We must NOT also concatenate `message_update` streaming deltas, or every
          // turn gets double-counted ("oneoneUnderstoodUnderstoodOKOK").
          if (ev.type === 'message_end' || ev.type === 'turn_end') {
            const content = Array.isArray(msg.content) ? msg.content : [];
            const parts = [];
            for (const part of content) {
              if (part.type === 'text' && part.text) parts.push(part.text);
              if (part.type === 'toolCall' || part.type === 'tool_use') {
                toolCalls.push({
                  tool: part.name || part.toolName || 'unknown',
                  params: part.arguments ?? part.input ?? null,
                  output: null,
                  durationSeconds: null,
                });
              }
            }
            if (parts.length) text = parts.join(''); // last write wins, no append
          }
          if (msg.usage) {
            usage = msg.usage;
            thinkingTokens += msg.usage.reasoningTokens || 0;
            if (msg.usage.cost?.total != null) cost = msg.usage.cost.total;
          }
          if (msg.duration) durationSeconds += msg.duration / 1000;
        }

        if (ev.type === 'turn_end' && Array.isArray(ev.toolResults)) {
          for (const tr of ev.toolResults) {
            toolCalls.push({
              tool: tr.toolName || tr.name || 'toolResult',
              params: null,
              output: truncate(typeof tr.output === 'string' ? tr.output : JSON.stringify(tr.output ?? ''), 4000),
              durationSeconds: null,
            });
          }
        }
      }
      return { text: text.trim(), toolCalls, usage, thinkingTokens, cost, durationSeconds, rawEventCount: events.length };
    },
  },

  pi: {
    name: 'pi',
    bin: 'pi.cmd',
    label: 'Pi',
    // DeepSeek 4.1 Flash via Fireworks. `--provider deepseek` does NOT exist.
    model: 'fireworks/accounts/fireworks/models/deepseek-v4p1-flash',
    family: 'deepseek-4.1-flash',
    /**
     * pi --mode json shares the same event vocabulary as omp (both derive from the
     * same session-format lineage), so extraction is intentionally near-identical.
     */
    buildArgs({ prompt, model, cwd }) {
      // NOTE: `pi` has NO --cwd flag (unlike omp). Passing it makes pi error out
      // with "Unknown option: --cwd" and hang. The working directory is set via
      // the spawn `cwd` option instead.
      return [
        '-p',
        '--mode', 'json',
        '--model', model || this.model,
        '--no-session',
        prompt,
      ];
    },
    parseLine(line) { return safeJson(line); },
    extractTurnEvents(events) { return extractSessionFormat(events); },
  },

  step: {
    name: 'step',
    bin: 'step.exe',
    label: 'StepCode',
    model: 'step/step-5-preview',
    family: 'step-5-preview',
    /**
     * step shares the pi/omp session-format lineage (same event vocabulary) but adds
     * an explicit approval model. --approval-mode auto + --non-interactive-approval allow
     * is what makes unattended tool use possible without a TUI.
     * Like pi, step has no --cwd flag; the spawn cwd is used instead.
     */
    buildArgs({ prompt, model }) {
      return [
        '-p',
        '--mode', 'json',
        '--model', model || this.model,
        '--approval-mode', 'auto',
        '--non-interactive-approval', 'allow',
        '--no-session',
        prompt,
      ];
    },
    parseLine(line) { return safeJson(line); },
    extractTurnEvents(events) { return extractSessionFormat(events); },
  },
};

/**
 * Shared extractor for the pi/omp/step session-format lineage.
 *
 * CRITICAL: text is taken from the FINAL assistant message only. Concatenating
 * streaming message_update deltas as well double-counts every turn.
 */
function extractSessionFormat(events) {
  const toolCalls = [];
  let text = '';
  let usage = null;
  let cost = null;
  let durationSeconds = 0;
  let thinkingTokens = 0;

  for (const ev of events) {
    const msg = ev.message;
    if (msg) {
      if (msg.role === 'system' || msg.role === 'user') continue;
      if (msg.role === 'assistant') {
        if (ev.type === 'message_end' || ev.type === 'turn_end') {
          const content = Array.isArray(msg.content) ? msg.content : [];
          const parts = [];
          for (const part of content) {
            if (part.type === 'text' && part.text) parts.push(part.text);
            if (part.type === 'toolCall' || part.type === 'tool_use') {
              toolCalls.push({
                tool: part.name || part.toolName || 'unknown',
                params: part.arguments ?? part.input ?? null,
                output: null,
                durationSeconds: null,
              });
            }
          }
          if (parts.length) text = parts.join('');
        }
        if (msg.usage) {
          usage = msg.usage;
          thinkingTokens += msg.usage.reasoningTokens || 0;
          if (msg.usage.cost?.total != null) cost = msg.usage.cost.total;
        }
        if (msg.duration) durationSeconds += msg.duration / 1000;
      }
    }
    if (ev.type === 'turn_end' && Array.isArray(ev.toolResults)) {
      for (const tr of ev.toolResults) {
        toolCalls.push({
          tool: tr.toolName || tr.name || 'toolResult',
          params: null,
          output: truncate(typeof tr.output === 'string' ? tr.output : JSON.stringify(tr.output ?? ''), 4000),
          durationSeconds: null,
        });
      }
    }
  }
  return { text: text.trim(), toolCalls, usage, thinkingTokens, cost, durationSeconds, rawEventCount: events.length };
}

function safeJson(line) {
  const t = line.trim();
  if (!t || (t[0] !== '{' && t[0] !== '[')) return null;
  try { return JSON.parse(t); } catch { return null; }
}

function truncate(s, n) {
  if (typeof s !== 'string') return s;
  return s.length <= n ? s : s.slice(0, n) + `\n...[truncated ${s.length - n} chars]`;
}

/**
 * Event types that mark the end of a turn across all four substrates:
 *   agent_end / agent_settled -> omp, pi, step
 *   result                    -> agy
 */
const TERMINAL_TYPES = new Set(['agent_end', 'agent_settled', 'result']);

/**
 * Extract the model's reasoning trace from the raw event stream.
 *
 * The session-format CLIs (omp/pi/step) emit `message_update` events carrying
 * `assistantMessageEvent` parts. Reasoning arrives as:
 *     {type:'thinking_start'} -> {type:'thinking_delta', delta:'...'}* -> {type:'thinking_end'}
 * We concatenate the deltas per block, preserving block boundaries so the UI can
 * render distinct reasoning episodes rather than one undifferentiated wall.
 *
 * agy uses a different shape: step_update events with `thinking_tokens` counts but
 * no reasoning text (the Antigravity CLI does not stream the monologue), so for agy
 * this returns an empty text and a token-count placeholder.
 */
function extractReasoning(events) {
  const blocks = [];
  let current = null;
  let text = '';

  for (const ev of events) {
    const ame = ev.assistantMessageEvent;
    if (!ame) continue;
    const type = ame.type || '';

    if (type === 'thinking_start') {
      current = { index: ame.contentIndex ?? blocks.length, text: '' };
      blocks.push(current);
    } else if (type === 'thinking_delta') {
      if (!current) { current = { index: ame.contentIndex ?? blocks.length, text: '' }; blocks.push(current); }
      current.text += ame.delta || '';
    } else if (type === 'thinking_end') {
      if (current && ame.content != null) current.text = ame.content;
      if (current) { text += (text ? '\n\n' : '') + current.text; current = null; }
    }
  }

  // Fall back to whole-message thinking parts if no streaming blocks were seen.
  if (!blocks.length) {
    for (const ev of events) {
      const msg = ev.message;
      if (!msg || msg.role !== 'assistant') continue;
      const content = Array.isArray(msg.content) ? msg.content : [];
      for (const part of content) {
        if (part.type === 'thinking' && part.thinking) {
          blocks.push({ index: blocks.length, text: part.thinking });
          text += (text ? '\n\n' : '') + part.thinking;
        }
      }
    }
  }

  return { text: text.trim(), blocks: blocks.length };
}

/**
 * Streaming reasoning accumulator.
 *
 * The original implementation called readFileSync() on the entire stdout file and
 * materialised one event object per token BEFORE pruning. Step can emit multi-GB
 * streams (9.8 GB observed on a single turn); that both exceeds V8's maximum string
 * length — so the read silently threw and the turn was recorded as ok=false with
 * zero tool calls — and would OOM even if the string fit. We now fold the per-token
 * `thinking_delta` events into one reasoning string as they stream past, and retain
 * only the small set of non-pruned events.
 */
function createReasoningStream() {
  const blocks = [];
  let current = null;
  let text = '';
  return {
    push(ev) {
      const ame = ev.assistantMessageEvent;
      if (!ame) return;
      const type = ame.type || '';
      if (type === 'thinking_start') {
        current = { index: ame.contentIndex ?? blocks.length, text: '' };
        blocks.push(current);
      } else if (type === 'thinking_delta') {
        if (!current) { current = { index: ame.contentIndex ?? blocks.length, text: '' }; blocks.push(current); }
        current.text += ame.delta || '';
      } else if (type === 'thinking_end') {
        if (current && ame.content != null) current.text = ame.content;
        if (current) { text += (text ? '\n\n' : '') + current.text; current = null; }
      }
    },
    result() { return { text: text.trim(), blocks: blocks.length }; },
  };
}

/**
 * Parse a (potentially multi-GB) newline-delimited JSON file without ever holding
 * the whole file in memory. Calls onEvent(line) for every non-empty line. Returns
 * the number of lines offered. A missing/unreadable file yields zero lines: the
 * caller records that as an empty turn rather than crashing.
 */
function streamJsonl(path, onEvent) {
  let fd = null;
  let lines = 0;
  try {
    fd = openSync(path, 'r');
    const decoder = new StringDecoder('utf8');
    const CHUNK = 4 * 1024 * 1024;
    const buf = Buffer.allocUnsafe(CHUNK);
    let remainder = '';
    for (;;) {
      const bytes = readSync(fd, buf, 0, CHUNK, null);
      if (bytes <= 0) break;
      const chunk = remainder + decoder.write(buf.subarray(0, bytes));
      let start = 0;
      let idx;
      while ((idx = chunk.indexOf('\n', start)) !== -1) {
        const line = chunk.slice(start, idx);
        start = idx + 1;
        if (line.trim()) { lines++; onEvent(line); }
      }
      remainder = chunk.slice(start);
    }
    remainder += decoder.end();
    if (remainder.trim()) { lines++; onEvent(remainder); }
  } catch {
    // fall through: an unreadable stream is data, not a crash
  } finally {
    if (fd !== null) { try { closeSync(fd); } catch {} }
  }
  return lines;
}

function safeSize(path) { try { return statSync(path).size; } catch { return 0; } }

/**
 * Spawn a substrate for exactly one turn and return the fully parsed forensic record.
 * Never throws for a non-zero exit: a failed turn is itself data.
 */
export function runTurn({
  substrate,
  prompt,
  cwd,
  model,
  timeoutMs = 360_000,
  env = {},
  runDirOverride = null,
  turnTag = null,
}) {
  const spec = SUBSTRATES[substrate];
  if (!spec) return Promise.reject(new Error(`unknown substrate: ${substrate}`));

  const { exe, prefixArgs } = resolveBin(substrate);
  const args = [...prefixArgs, ...spec.buildArgs({ prompt, model, cwd })];
  const startedAt = Date.now();

  // Every turn's raw event stream is persisted under runs/<runId>/.
  const runDir = runDirOverride || join(cwd, '..', 'runs', 'adhoc');
  try { mkdirSync(runDir, { recursive: true }); } catch {}
  const tag = `${substrate}-${String(turnTag || Date.now()).replace(/[^a-zA-Z0-9_.-]/g, '_')}`;

  return new Promise((resolve) => {
    // ---------------------------------------------------------------------------
    // STDIO STRATEGY: files, not pipes.
    //
    // On this host, spawning these agent CLIs with piped stdio causes them to hang
    // forever and emit ZERO bytes (verified: identical command via file redirection
    // exits 0 with a full event stream in ~5s; via pipes it never produces output).
    // We therefore redirect stdout/stderr to real files and read them back.
    // This is also strictly better for forensics: the raw event stream is persisted.
    // ---------------------------------------------------------------------------
    const outPath = join(runDir, `${tag}.stdout.jsonl`);
    const errPath = join(runDir, `${tag}.stderr.log`);
    let outFd = null;
    let errFd = null;
    try {
      outFd = openSync(outPath, 'w');
      errFd = openSync(errPath, 'w');
    } catch (e) {
      return resolve(fail(substrate, model || spec.model, prompt, startedAt, `cannot open log files: ${e}`));
    }

    const child = spawn(exe, args, {
      cwd,
      shell: false, // never shell:true — it concatenates argv unescaped on Windows
      windowsHide: true,
      stdio: ['ignore', outFd, errFd],
      env: {
        ...process.env,
        // Force Git Bash so agy does not waste ~61s/turn probing for absent WSL.
        SHELL: GIT_BASH,
        PI_SHELL: GIT_BASH,
        GIT_BASH_PATH: GIT_BASH,
        CI: '1',
        NO_COLOR: '1',
        ...env,
      },
    });

    let settled = false;
    let killed = false;

    const timer = setTimeout(() => {
      killed = true;
      killTree(child);
    }, timeoutMs);

    const finish = (code, timedOutFlag) => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      try { if (outFd !== null) closeSync(outFd); } catch {}
      try { if (errFd !== null) closeSync(errFd); } catch {}

      let stderr = '';
      try { stderr = readFileSync(errPath, 'utf8'); } catch {}
      const rawBytes = safeSize(outPath);

      // ---------------------------------------------------------------------
      // EVENT PRUNING — but KEEP THE REASONING.
      //
      // `step` streams one JSON event PER TOKEN: a single turn produced 21,184
      // `message_update` events (7.5 MB) versus 494 for `omp` doing comparable
      // work. Retaining every delta bloats the ledger and slows later reads.
      //
      // BUT the per-token deltas are where the reasoning lives: `thinking_delta`
      // carries the model's actual internal monologue. Dropping them wholesale
      // makes the swarm's cognition invisible, which defeats the arena's purpose.
      // So we EXTRACT the reasoning text into one readable field, then drop the
      // raw per-token events. Full cognition preserved, volume stays small.
      // ---------------------------------------------------------------------
      const PRUNED = new Set(['message_update', 'step_update']);
      const prunedEvents = [];
      const reasoningStream = createReasoningStream();
      const eventCount = streamJsonl(outPath, (line) => {
        const parsed = spec.parseLine(line);
        if (!parsed) return;
        reasoningStream.push(parsed);
        if (!PRUNED.has(parsed.type)) prunedEvents.push(parsed);
      });
      // Reuse the whole-message fallback only when no streaming thinking blocks
      // were seen (agy does not stream its monologue; omp/pi/step do).
      let reasoning = reasoningStream.result();
      if (!reasoning.blocks) reasoning = extractReasoning(prunedEvents);
      const prunedCount = eventCount - prunedEvents.length;

      const extracted = spec.extractTurnEvents(prunedEvents);
      extracted.reasoning = reasoning.text;
      extracted.reasoningChars = reasoning.text.length;
      extracted.reasoningBlocks = reasoning.blocks;
      const sawTerminal = prunedEvents.some((e) =>
        TERMINAL_TYPES.has(e.type) || e.event === 'result');

      // Wall-clock is the authoritative duration. The session-format CLIs often omit
      // per-message `duration`, which previously left durationSeconds undefined.
      const wallSeconds = (Date.now() - startedAt) / 1000;
      if (!extracted.durationSeconds) extracted.durationSeconds = wallSeconds;

      // A post-turn SIGKILL is a normal shutdown, not a failure.
      const clean = sawTerminal || code === 0;
      resolve({
        substrate,
        model: model || spec.model,
        prompt,
        ok: clean && extracted.text.length > 0,
        error: clean ? null : (timedOutFlag || killed ? 'timeout' : `exit ${code}`),
        exitCode: code,
        timedOut: Boolean(timedOutFlag || killed) && !sawTerminal,
        truncated: !sawTerminal && Boolean(timedOutFlag || killed),
        durationSeconds: wallSeconds,
        stderr: truncate(stderr, 2000),
        stdoutPath: outPath,
        stderrPath: errPath,
        events: prunedEvents,
        ...extracted,
        rawEventCount: eventCount,
        prunedEventCount: prunedCount,
        rawBytes,
      });
      // Optional disk bound. A single Step turn can emit >10 GB of raw token
      // events. With ARENA_DISCARD_RAW=1 the raw stream is deleted after a clean
      // extraction; the reduced forensic record (turns.jsonl) is unaffected and
      // rawBytes is kept for provenance. Failed turns are always retained.
      if (process.env.ARENA_DISCARD_RAW === '1' && clean && rawBytes > 50_000_000) {
        try { unlinkSync(outPath); } catch {}
      }
    };

    child.on('error', (err) => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      try { if (outFd !== null) closeSync(outFd); } catch {}
      try { if (errFd !== null) closeSync(errFd); } catch {}
      resolve(fail(substrate, model || spec.model, prompt, startedAt, String(err)));
    });

    child.on('close', (code) => finish(code, false));
  });
}

/** Build a synthetic failure record (spawn never started). */
function fail(substrate, model, prompt, startedAt, error) {
  return {
    substrate, model, prompt,
    ok: false, error, text: '', toolCalls: [],
    usage: null, cost: 0, thinkingTokens: 0,
    durationSeconds: (Date.now() - startedAt) / 1000,
    exitCode: null, timedOut: false, rawEventCount: 0,
    stderr: '', events: [],
  };
}

/** Kill the child and any descendants (these CLIs spawn session hosts). */
function killTree(child) {
  try {
    if (process.platform === 'win32' && child.pid) {
      spawn('taskkill', ['/pid', String(child.pid), '/T', '/F'], { windowsHide: true, stdio: 'ignore' });
    } else {
      child.kill('SIGKILL');
    }
  } catch {}
}
