/**
 * Repo-relative paths, derived from this file's location.
 *
 * The arena scripts previously hardcoded `D:\AgentSwarm\...`, which made the
 * repository non-reproducible on any other machine or checkout path. Everything
 * now resolves from `import.meta.url`.
 */

import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

/** This file lives in arena/. */
export const ARENA = dirname(fileURLToPath(import.meta.url));
/** Repository root (the parent of arena/). */
export const REPO = join(ARENA, '..');
/** The static site source directory. */
export const SITE = join(REPO, 'site');
/** The agents' writable research directory (never written by tooling). */
export const WORLD = join(ARENA, 'world');
/** Per-run forensic ledgers. */
export const RUNS = join(ARENA, 'runs');
/** Scribe conclusion posts. */
export const POSTS = join(ARENA, 'posts');
/** Shared memory commons. */
export const MEMORY = join(ARENA, 'memory');
