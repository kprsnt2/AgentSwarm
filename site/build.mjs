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

import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const SITE = 'D:\\AgentSwarm\\site';
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
  "data generated ${new Date(D.generatedAt).toLocaleString()}",
  "data generated ${new Date(D.generatedAt).toLocaleString()} · self-contained build"
);

mkdirSync(join(SITE, 'dist'), { recursive: true });
writeFileSync(join(SITE, 'dist', 'index.html'), out, 'utf8');

const size = (out.length / 1024).toFixed(0);
console.log(`wrote dist/index.html (${size} KB, self-contained)`);
console.log(`\nThis single file works from file://, a local server, or any static host.`);
