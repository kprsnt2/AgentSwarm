/**
 * Build a self-contained site.
 *
 * PROBLEM THIS SOLVES: the site fetches data/findings.json, which browsers block on
 * the file:// protocol (CORS). Opening index.html by double-clicking therefore shows
 * "Could not load data/findings.json".
 *
 * FIX: inline the JSON into the page as a <script type="application/json"> block.
 * The built file then works from file://, from a local server, and from any static
 * host — with zero configuration.
 *
 * Usage: node build.mjs
 * Output: dist/index.html  (single self-contained file)
 */

import { readFileSync, writeFileSync, mkdirSync, existsSync, copyFileSync, cpSync, rmSync, readdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

// Resolved from this file's location so a clone works anywhere.
const SITE = dirname(fileURLToPath(import.meta.url));
const html = readFileSync(join(SITE, 'index.html'), 'utf8');

// Guard the data read: a missing findings.json previously threw an uncaught ENOENT,
// which reads like a broken build script rather than "run the exporter first".
const dataPath = join(SITE, 'data', 'findings.json');
if (!existsSync(dataPath)) {
  console.error(`missing ${dataPath}`);
  console.error('Run the exporter first:  cd ..\\arena && node export-site.mjs');
  process.exit(1);
}
const data = readFileSync(dataPath, 'utf8');

// Validate the JSON before embedding so we never ship a broken page.
let parsed;
try { parsed = JSON.parse(data); }
catch (e) { console.error('findings.json is not valid JSON:', e.message); process.exit(1); }
console.log(`embedding ${(data.length / 1024).toFixed(0)} KB of data ` +
  `(${parsed.runs.length} runs, ${parsed.substrates.length} substrates, ` +
  `${parsed.artifacts.length} artifacts, ${(parsed.posts || []).length} posts)`);

// Older findings.json files predate the Scribe, so `posts` may be absent. The page
// reads D.posts directly; default it here rather than making every call site guard.
if (!Array.isArray(parsed.posts)) parsed.posts = [];
const normalized = JSON.stringify(parsed);

// Replace the fetch-based loader with an inline-data loader.
// The page's render logic stays identical; only the data source changes.
const inlineLoader = `<script id="findings-data" type="application/json">${normalized.replace(/<\//g, '<\\/')}</script>
<script>
/* Inlined at build time by build.mjs so the page works from file:// too. */
(function () {
  var el = document.getElementById('findings-data');
  var D = JSON.parse(el.textContent);
  window.__FINDINGS__ = D;
})();
</script>`;

let out = html;

// 1. Inject the inline data right before the main script.
out = out.replace('<script>\nconst fmt', inlineLoader + '\n<script>\nconst fmt');

// 2. Replace the fetch chain with a direct use of the inlined data.
out = out.replace(
  "fetch('data/findings.json').then(r => r.json()).then(D => {",
  "Promise.resolve(window.__FINDINGS__).then(D => {"
);

// 3. Make the failure message accurate for the self-contained build.
out = out.replace(
  "`<div class=\"note bad\">Could not load <code>data/findings.json</code>. Run <code>node export-site.mjs</code> from the arena directory, and serve this site over HTTP (not file://).</div>`",
  "`<div class=\"note bad\">No findings data embedded. Rebuild with <code>node build.mjs</code>.</div>`"
);

// 4. Add a build stamp to the footer metadata.
out = out.replace(
  "data as of ${new Date(D.generatedAt).toLocaleString()}",
  "data as of ${new Date(D.generatedAt).toLocaleString()} · self-contained build"
);

// ---------------------------------------------------------------------------
// VERIFY THE REWRITES ACTUALLY HAPPENED.
//
// String.replace() returns the input unchanged when the pattern is not found — it
// does not throw. So if index.html is edited in a way that moves one of the anchors
// above, this build silently emits a page that still calls fetch() and therefore
// shows "Could not load data/findings.json" when opened from file:// or GitHub Pages.
// That failure looks like a data problem and is miserable to debug. Fail loudly here
// instead, at build time, where the cause is obvious.
// ---------------------------------------------------------------------------
const failures = [];
if (!out.includes('id="findings-data"')) failures.push('inline data block was not injected');
if (out.includes("fetch('data/findings.json')")) failures.push("fetch('data/findings.json') still present — loader was not replaced");
if (!out.includes('Promise.resolve(window.__FINDINGS__)')) failures.push('inline-data loader was not wired up');
if (failures.length) {
  console.error('BUILD FAILED — index.html changed in a way build.mjs did not expect:');
  for (const f of failures) console.error(`  - ${f}`);
  console.error('\nThe rewrite anchors in build.mjs no longer match site/index.html.');
  console.error('Fix the anchors (or index.html) so the self-contained build is correct.');
  process.exit(1);
}

mkdirSync(join(SITE, 'dist'), { recursive: true });
writeFileSync(join(SITE, 'dist', 'index.html'), out, 'utf8');

const size = (out.length / 1024).toFixed(0);
console.log(`wrote dist/index.html (${size} KB, self-contained)`);

// ---------------------------------------------------------------------------
// PUBLISH TO docs/ FOR GITHUB PAGES.
//
// GitHub Pages can only serve from the repository root or /docs — not from an
// arbitrary subdirectory. The site source lives in site/, so it must be copied to
// docs/ at the repo root to be reachable.
//
// This is done HERE, in the same step as the build, on purpose: a separate manual
// copy step is one people forget, and a stale docs/ means Pages keeps serving an old
// page while the source looks correct. (That is exactly how the previous dist/ went
// stale.) One command now produces both the artifact and the deployable copy.
// ---------------------------------------------------------------------------
const REPO = join(SITE, '..');
const docsDir = join(REPO, 'docs');
try {
  mkdirSync(docsDir, { recursive: true });
  writeFileSync(join(docsDir, 'index.html'), out, 'utf8');
  // .nojekyll tells GitHub to serve these files verbatim instead of running them
  // through Jekyll, which would otherwise try to process the HTML.
  writeFileSync(join(docsDir, '.nojekyll'), '', 'utf8');
  for (const asset of ['preview.png']) {
    const src = join(SITE, 'dist', asset);
    if (existsSync(src)) {
      copyFileSync(src, join(docsDir, asset));
    }
  }

  // Corpus pages (generated by arena/export-corpus.mjs) travel with the site, so a
  // report link works from file:// and from Pages without a server.
  const corpusSrc = join(SITE, 'corpus');
  if (existsSync(corpusSrc)) {
    const count = readdirSync(corpusSrc).length;
    for (const target of [join(SITE, 'dist', 'corpus'), join(docsDir, 'corpus')]) {
      rmSync(target, { recursive: true, force: true });
      cpSync(corpusSrc, target, { recursive: true });
    }
    console.log(`copied corpus/ (${count} pages) to dist/ and docs/`);
  } else {
    console.warn('site/corpus/ not found — run  node arena/export-corpus.mjs  to generate report pages');
  }

  console.log(`wrote docs/index.html (GitHub Pages, /docs)`);
} catch (e) {
  console.error(`could not write docs/ (Pages copy skipped): ${e.message}`);
}

console.log(`\nThis single file works from file://, a local server, or any static host.`);
console.log(`Commit and push to publish:`);
console.log(`  git add -A && git commit -m "Rebuild site" && git push`);
