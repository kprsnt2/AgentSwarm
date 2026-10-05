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
 * Output: dist/ (self-contained HTML files) and docs/ (for GitHub Pages)
 */

import { readFileSync, writeFileSync, mkdirSync, existsSync, copyFileSync, cpSync, rmSync, readdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

// Resolved from this file's location so a clone works anywhere.
const SITE = dirname(fileURLToPath(import.meta.url));
const REPO = join(SITE, '..');
const docsDir = join(REPO, 'docs');

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

function transformPage(content, fileName, isIndex = false) {
  let out = content;

  // 1. Inject the inline data right before the main script.
  if (out.includes('<script>\nconst fmt')) {
    out = out.replace('<script>\nconst fmt', inlineLoader + '\n<script>\nconst fmt');
  } else if (out.includes('<script>\nconst esc')) {
    out = out.replace('<script>\nconst esc', inlineLoader + '\n<script>\nconst esc');
  } else {
    out = out.replace('<script>', inlineLoader + '\n<script>');
  }

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

  // 4. Add a build stamp to footer if index
  if (isIndex) {
    out = out.replace(
      "data as of ${new Date(D.generatedAt).toLocaleString()}",
      "data as of ${new Date(D.generatedAt).toLocaleString()} · self-contained build"
    );
  }

  // ---------------------------------------------------------------------------
  // VERIFY THE REWRITES ACTUALLY HAPPENED.
  // ---------------------------------------------------------------------------
  const failures = [];
  if (!out.includes('id="findings-data"')) failures.push('inline data block was not injected');
  if (out.includes("fetch('data/findings.json')")) failures.push("fetch('data/findings.json') still present — loader was not replaced");
  if (!out.includes('Promise.resolve(window.__FINDINGS__)')) failures.push('inline-data loader was not wired up');

  if (failures.length) {
    console.error(`BUILD FAILED on ${fileName}:`);
    for (const f of failures) console.error(`  - ${f}`);
    process.exit(1);
  }
  return out;
}

const PAGES = [
  { file: 'index.html', isIndex: true },
  { file: 'dashboard.html', isIndex: false },
  { file: 'findings.html', isIndex: false },
  { file: 'questions.html', isIndex: false },
  { file: 'posts.html', isIndex: false },
  { file: 'benchmark.html', isIndex: false },
  { file: 'audit.html', isIndex: false },
];

mkdirSync(join(SITE, 'dist'), { recursive: true });
mkdirSync(docsDir, { recursive: true });

for (const p of PAGES) {
  const srcPath = join(SITE, p.file);
  if (!existsSync(srcPath)) continue;
  const rawHtml = readFileSync(srcPath, 'utf8');
  const builtHtml = transformPage(rawHtml, p.file, p.isIndex);
  
  writeFileSync(join(SITE, 'dist', p.file), builtHtml, 'utf8');
  writeFileSync(join(docsDir, p.file), builtHtml, 'utf8');
  
  const kbSize = (builtHtml.length / 1024).toFixed(0);
  console.log(`wrote dist/${p.file} and docs/${p.file} (${kbSize} KB)`);
}

// Write .nojekyll for GitHub Pages
writeFileSync(join(docsDir, '.nojekyll'), '', 'utf8');

for (const asset of ['preview.png']) {
  const src = join(SITE, 'dist', asset);
  if (existsSync(src)) {
    copyFileSync(src, join(docsDir, asset));
  }
}

// Copy corpus pages
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

console.log(`\nAll standalone pages built into dist/ and docs/ for GitHub Pages.`);
console.log(`Commit and push to publish:`);
console.log(`  git add -A && git commit -m "Rebuild site" && git push`);
