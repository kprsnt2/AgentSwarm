/**
 * Post — generate the conclusion post for a run.
 *
 * Two uses:
 *
 *   1. BACKFILL. Every run writes its post automatically, but runs that finished
 *      before the scribe existed have none. This regenerates them from the ledger:
 *
 *        node post.mjs                 # every run that lacks a post
 *        node post.mjs --all           # every run, overwriting existing posts
 *        node post.mjs <runId>         # one run
 *
 *   2. RE-ROLL. If a polish step failed (substrate down, honesty gate rejected the
 *      output), re-run it:
 *
 *        node post.mjs <runId> --force
 *
 * FLAGS
 *   --all              process every run, not just the missing ones
 *   --force            overwrite an existing post for the same run
 *   --no-llm           deterministic ledger draft only (free, no model call)
 *   --substrate <name> substrate for the polish step (default: agy)
 *   --list             show which runs have posts and which do not
 *
 * WHY THIS IS SAFE TO RE-RUN: the deterministic draft is rebuilt from the ledger
 * every time, so regenerating a post can never lose the underlying facts. Only the
 * prose changes.
 */

import { existsSync, readdirSync } from 'node:fs';
import { join } from 'node:path';

import { writePost, readPosts, POSTS_DIR } from './scribe.mjs';

const ARENA = 'D:\\AgentSwarm\\arena';

const argv = process.argv.slice(2);

// Single-pass parse. A value-taking flag consumes the next token, so a runId can
// never be confused with a flag's value (the earlier filter-based version would
// treat `omp` in `--substrate omp` as a runId if the flags were reordered).
const VALUE_FLAGS = new Set(['--substrate']);
const flags = { all: false, force: false, noLlm: false, list: false, substrate: 'agy' };
const positional = [];

for (let i = 0; i < argv.length; i++) {
  const a = argv[i];
  if (a === '--all') flags.all = true;
  else if (a === '--force') flags.force = true;
  else if (a === '--no-llm') flags.noLlm = true;
  else if (a === '--list') flags.list = true;
  else if (VALUE_FLAGS.has(a)) {
    const v = argv[++i];
    if (v === undefined) { console.error(`${a} needs a value`); process.exit(1); }
    if (a === '--substrate') flags.substrate = v;
  } else if (a.startsWith('-')) {
    console.error(`unknown flag: ${a}`);
    console.error('valid: --all --force --no-llm --list --substrate <name>');
    process.exit(1);
  } else positional.push(a);
}

if (positional.length > 1) {
  console.error(`expected at most one runId, got ${positional.length}: ${positional.join(', ')}`);
  process.exit(1);
}
const onlyRun = positional[0] || null;

// ---------------------------------------------------------------- discover runs

const runsDir = join(ARENA, 'runs');
if (!existsSync(runsDir)) {
  console.error(`no runs directory: ${runsDir}`);
  process.exit(1);
}

const allRuns = readdirSync(runsDir, { withFileTypes: true })
  .filter((d) => d.isDirectory())
  .map((d) => d.name)
  .filter((n) => existsSync(join(runsDir, n, 'turns.jsonl')))
  .sort();

if (!allRuns.length) {
  console.error('no runs with turns.jsonl found');
  process.exit(1);
}

const existing = new Set(readPosts(ARENA).map((p) => p.runId));

// ---------------------------------------------------------------- --list

if (flags.list) {
  console.log(`${allRuns.length} runs with ledgers, ${existing.size} with posts\n`);
  for (const id of allRuns) {
    console.log(`  ${existing.has(id) ? '[post]' : '[    ]'}  ${id}`);
  }
  console.log(`\nposts live in ${join(ARENA, POSTS_DIR)}`);
  process.exit(0);
}

// ---------------------------------------------------------------- pick the work

let targets;
if (onlyRun) {
  if (!allRuns.includes(onlyRun)) {
    console.error(`unknown run: ${onlyRun}\n`);
    console.error('available runs:');
    for (const id of allRuns) console.error(`  ${id}`);
    process.exit(1);
  }
  targets = [onlyRun];
} else if (flags.all) {
  targets = allRuns;
} else {
  // Default: the runs that need one. `--force` implies "do them again anyway".
  targets = flags.force ? allRuns : allRuns.filter((id) => !existing.has(id));
}

if (!targets.length) {
  console.log('every run already has a post.');
  console.log('Use --all to regenerate them, or --list to see the mapping.');
  process.exit(0);
}

// ---------------------------------------------------------------- generate

console.log('='.repeat(70));
console.log(`SCRIBE — writing ${targets.length} post(s)`);
console.log('='.repeat(70));
console.log(`mode      : ${flags.noLlm ? 'deterministic draft only (no model)' : `deterministic draft + ${flags.substrate} polish`}`);
console.log(`overwrite : ${flags.force || flags.all ? 'yes' : 'no (missing only)'}`);
console.log('');

let ok = 0;
let failed = 0;
let polished = 0;

for (const runId of targets) {
  console.log(`--- ${runId}`);
  try {
    const post = await writePost({
      root: ARENA,
      runId,
      substrate: flags.substrate,
      useLLM: !flags.noLlm,
      onLog: (m) => console.log(`    ${m}`),
    });
    ok += 1;
    if (post.polished) polished += 1;
    console.log(`    → ${post.file}  ${post.polished ? '(polished)' : '(deterministic draft)'}`);
  } catch (err) {
    failed += 1;
    console.error(`    FAILED: ${err}`);
  }
}

console.log('\n' + '='.repeat(70));
console.log(`${ok} post(s) written (${polished} polished, ${ok - polished} deterministic), ${failed} failed`);
console.log(`output: ${join(ARENA, POSTS_DIR)}`);
console.log(`\nTo publish them on the site:`);
console.log(`  node export-site.mjs && cd ..\\site && node build.mjs`);
