/**
 * Corpus index — shared helpers for the findings explorer.
 *
 * READ-ONLY with respect to arena/world. The artifacts there are agent-authored and
 * are never modified by tooling; this module only stats, hashes and reads them.
 * Generated pages go to site/corpus/, which site/build.mjs copies to dist/ and docs/.
 */

import { readFileSync, readdirSync, statSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { createHash } from 'node:crypto';
import { ARENA, WORLD, SITE } from './paths.mjs';

export { ARENA, WORLD, SITE };

/** Public repository, used for links back to sources. */
export const REPO_URL = 'https://github.com/kprsnt2/AgentSwarm';
export const REPO_BLOB = `${REPO_URL}/blob/main/arena/world/`;

const DOMAIN_RULES = [
  { id: 'krishna-mahabharata', label: 'Krishna & Mahabharata', re: /^(KRISHNA_AND_MAHABHARATA|HISTORICITY_OF_KRISHNA|ADVANCED_HISTORICITY)/ },
  { id: 'hindu-multiverse', label: 'Hindu multiverse', re: /^(HINDU_MULTIVERSE|HISTORICAL_TEXTUAL_INVESTIGATION_HINDU)/ },
  { id: 'cosmogenesis', label: 'Cosmogenesis', re: /^(COSMOGENESIS|PHASE2_COSMOGENESIS)/ },
  { id: 'relativistic-flight', label: 'Relativistic flight & FTL', re: /^(RELATIVISTIC|ULTRA_RELATIVISTIC|FEASIBILITY|PHASE2_LIGHTSPEED|INTERSTELLAR_DECELERATION|LIGHTSPEED)/ },
  { id: 'propulsion', label: 'Propulsion', re: /^(PRACTICAL_PROPULSION|PROPULSION)/ },
  { id: 'drug-discovery', label: 'Drug discovery', re: /^(DRUG_DISCOVERY|TRANSLATIONAL|PRECLINICAL|PATIENT_HETEROGENEITY|NETWORK_BUFFERING|GENETIC_VALIDATION|EMPIRICAL_CAUSAL)/ },
  { id: 'extraterrestrial', label: 'Extraterrestrial life', re: /^(EPISTEMIC_DEMARCATION|EXTRATERRESTRIAL)/ },
  { id: 'dharmic-truth-claims', label: 'Dharmic truth claims', re: /^(TAXONOMY_OF_DHARMIC|FORMAL_DEMARCATION|ARYABHATA)/ },
];

const PHASE2_LABELS = {
  cosmogenesis: 'Cosmogenesis',
  'drug-discovery': 'Drug discovery',
  extraterrestrial: 'Extraterrestrial life',
  lightspeed: 'Relativistic flight & FTL',
};

/** Map an artifact path to a research domain. */
export function domainOf(relPath) {
  const p = String(relPath).replace(/\\/g, '/');
  if (p.startsWith('tools/')) return { id: 'shared-tools', label: 'Shared tools' };
  const p2 = p.match(/^phase2\/([^/]+)\//);
  if (p2) return { id: p2[1], label: PHASE2_LABELS[p2[1]] || p2[1] };
  const base = p.split('/').pop();
  for (const r of DOMAIN_RULES) if (r.re.test(base)) return { id: r.id, label: r.label };
  return { id: 'other', label: 'Other' };
}

/** Stable, filesystem-safe page name for an artifact path. */
export function slugFor(relPath) {
  const s = String(relPath)
    .replace(/\\/g, '/')
    .replace(/\.(md|txt|py|json|jsonl)$/i, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 90);
  return s || 'file';
}

function headingsOf(md) {
  const out = [];
  for (const line of String(md).split(/\r?\n/)) {
    const m = line.match(/^#{1,3}\s+(.+)$/);
    if (!m) continue;
    const t = m[1].replace(/[*_`#]/g, '').trim();
    if (t && !out.includes(t)) out.push(t);
    if (out.length >= 8) break;
  }
  return out;
}

/**
 * List every artifact under arena/world (read-only), with metadata.
 * Skips Python caches. Hashes are sha1 for provenance, not integrity claims.
 */
export function listWorldFiles() {
  const out = [];
  (function walk(dir, base) {
    if (!existsSync(dir)) return;
    for (const e of readdirSync(dir, { withFileTypes: true })) {
      const rel = base ? `${base}/${e.name}` : e.name;
      if (e.isDirectory()) {
        if (e.name !== '__pycache__') walk(join(dir, e.name), rel);
        continue;
      }
      if (/\.pyc$/i.test(e.name)) continue;
      const abs = join(dir, e.name);
      let st;
      try { st = statSync(abs); } catch { continue; }
      const ext = (e.name.match(/\.([^.]+)$/) || [, ''])[1].toLowerCase();
      let sha1 = null;
      let headings = [];
      try {
        const buf = readFileSync(abs);
        sha1 = createHash('sha1').update(buf).digest('hex');
        if (ext === 'md') headings = headingsOf(buf.toString('utf8'));
      } catch { /* unreadable: index without hash */ }
      const dom = domainOf(rel);
      out.push({
        path: rel, bytes: st.size, modified: st.mtime.toISOString(), ext, sha1, headings,
        domain: dom.id, domainLabel: dom.label, slug: slugFor(rel),
      });
    }
  })(WORLD, '');

  // Deterministic unique slugs, assigned in path order so two callers always agree.
  const seen = new Map();
  for (const f of [...out].sort((a, b) => a.path.localeCompare(b.path))) {
    const n = (seen.get(f.slug) || 0) + 1;
    seen.set(f.slug, n);
    if (n > 1) f.slug = `${f.slug}-${n}`;
  }

  out.sort((a, b) => b.bytes - a.bytes);
  return out;
}

/** Load arena/audit/annotations.json (hand-written audit results). */
export function loadAnnotations() {
  const p = join(ARENA, 'audit', 'annotations.json');
  if (!existsSync(p)) return { asOf: null, entries: [], study: [] };
  try {
    const j = JSON.parse(readFileSync(p, 'utf8'));
    return {
      asOf: j.asOf ?? null,
      entries: Array.isArray(j.entries) ? j.entries : [],
      study: Array.isArray(j.study) ? j.study : [],
    };
  } catch {
    return { asOf: null, entries: [], study: [] };
  }
}

// ---------------------------------------------------------------- markdown

export function escapeHtml(s) {
  return String(s ?? '').replace(/[&<>"']/g, (c) => (
    { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]
  ));
}

/**
 * Minimal markdown renderer for agent-written reports.
 *
 * Escape first, then transform, so agent prose can never inject markup. Supports
 * the constructs the reports actually use: fenced code, pipe tables, headings,
 * lists, blockquotes, rules, inline code/bold/italic/links.
 */
export function renderMarkdown(src) {
  const lines = String(src ?? '').replace(/\r\n?/g, '\n').split('\n');
  const out = [];
  let i = 0;

  const inline = (t) => escapeHtml(t)
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/(^|[\s(])\*([^*\n]+)\*/g, '$1<em>$2</em>')
    .replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');

  const isTableStart = (idx) => Boolean(
    lines[idx] && lines[idx].includes('|') &&
    lines[idx + 1] && lines[idx + 1].includes('|') &&
    /^\s*\|?\s*:?-{2,}/.test(lines[idx + 1])
  );

  while (i < lines.length) {
    const raw = lines[i];

    if (/^\s*```/.test(raw)) {
      const buf = [];
      i += 1;
      while (i < lines.length && !/^\s*```/.test(lines[i])) { buf.push(lines[i]); i += 1; }
      i += 1;
      out.push(`<pre><code>${escapeHtml(buf.join('\n'))}</code></pre>`);
      continue;
    }

    if (isTableStart(i)) {
      const cells = (l) => l.replace(/^\s*\|/, '').replace(/\|\s*$/, '').split('|').map((c) => c.trim());
      const head = cells(lines[i]);
      i += 2;
      const rows = [];
      while (i < lines.length && lines[i].trim() && lines[i].includes('|')) { rows.push(cells(lines[i])); i += 1; }
      out.push(
        `<div class="tw"><table><thead><tr>${head.map((h) => `<th>${inline(h)}</th>`).join('')}</tr></thead>` +
        `<tbody>${rows.map((r) => `<tr>${r.map((c) => `<td>${inline(c)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`
      );
      continue;
    }

    const h = raw.match(/^(#{1,6})\s+(.*)$/);
    if (h) {
      const n = Math.min(h[1].length, 4);
      out.push(`<h${n}>${inline(h[2])}</h${n}>`);
      i += 1;
      continue;
    }

    if (/^\s*(-{3,}|\*{3,}|_{3,})\s*$/.test(raw)) { out.push('<hr>'); i += 1; continue; }

    if (/^\s*>/.test(raw)) {
      const buf = [];
      while (i < lines.length && /^\s*>/.test(lines[i])) {
        buf.push(lines[i].replace(/^\s*>\s?/, ''));
        i += 1;
      }
      out.push(`<blockquote>${inline(buf.join(' '))}</blockquote>`);
      continue;
    }

    if (/^\s*(?:[-*+]|\d+\.)\s+/.test(raw)) {
      const ordered = /^\s*\d+\.\s+/.test(raw);
      const items = [];
      while (i < lines.length && /^\s*(?:[-*+]|\d+\.)\s+/.test(lines[i])) {
        items.push(lines[i].replace(/^\s*(?:[-*+]|\d+\.)\s+/, ''));
        i += 1;
      }
      const tag = ordered ? 'ol' : 'ul';
      out.push(`<${tag}>${items.map((t) => `<li>${inline(t)}</li>`).join('')}</${tag}>`);
      continue;
    }

    if (!raw.trim()) { i += 1; continue; }

    const buf = [raw];
    i += 1;
    while (
      i < lines.length && lines[i].trim() &&
      !/^(#{1,6}\s|```|\s*>)/.test(lines[i]) &&
      !/^\s*(?:[-*+]|\d+\.)\s+/.test(lines[i]) &&
      !/^\s*(-{3,}|\*{3,}|_{3,})\s*$/.test(lines[i]) &&
      !isTableStart(i)
    ) { buf.push(lines[i]); i += 1; }
    out.push(`<p>${inline(buf.join(' '))}</p>`);
  }
  return out.join('\n');
}

// ---------------------------------------------------------------- page shell

const PAGE_CSS = `
:root{--bg:#0a0c10;--bg2:#11141b;--bg3:#171b24;--line:#232936;--fg:#e6e9ef;--fg2:#9aa4b8;--fg3:#6b7488;--acc:#5eead4;--acc2:#38bdf8;--good:#4ade80;--warn:#fbbf24;--bad:#f87171;
--mono:ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,monospace;--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font-family:var(--sans);line-height:1.7;-webkit-font-smoothing:antialiased}
.wrap{max-width:900px;margin:0 auto;padding:26px 22px 90px}
a{color:var(--acc2);text-decoration:none}a:hover{text-decoration:underline}
nav{display:flex;gap:14px;align-items:center;flex-wrap:wrap;font-size:13px;border-bottom:1px solid var(--line);padding-bottom:14px;margin-bottom:26px}
nav .dom{font-family:var(--mono);font-size:11.5px;color:var(--acc);border:1px solid var(--line);border-radius:999px;padding:3px 10px}
h1{font-size:27px;letter-spacing:-.02em;line-height:1.25;margin:0 0 10px}
h2{font-size:20px;margin:30px 0 8px;letter-spacing:-.01em}h3{font-size:16px;margin:24px 0 6px}h4{font-size:14px;margin:20px 0 6px;color:var(--fg2)}
p{margin:0 0 14px}ul,ol{margin:0 0 14px;padding-left:22px}li{margin-bottom:6px}
code{font-family:var(--mono);font-size:.87em;background:var(--bg3);padding:2px 5px;border-radius:4px;color:var(--acc)}
pre{background:var(--bg2);border:1px solid var(--line);border-radius:10px;padding:14px;overflow-x:auto;font-size:12.5px;line-height:1.55}
pre code{background:none;padding:0;color:var(--fg)}
blockquote{margin:0 0 14px;padding:10px 16px;border-left:2px solid var(--acc);background:var(--bg2);border-radius:0 8px 8px 0;color:var(--fg2)}
hr{border:0;border-top:1px solid var(--line);margin:26px 0}
.tw{overflow-x:auto;margin:18px 0;border:1px solid var(--line);border-radius:10px}
table{width:100%;border-collapse:collapse;font-size:13px;min-width:480px}
th,td{padding:8px 12px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top}
th{background:var(--bg3);font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--fg2)}
tbody tr:last-child td{border-bottom:none}
.badges{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 18px}
.b{font-family:var(--mono);font-size:11px;padding:3px 9px;border-radius:999px;font-weight:600;cursor:help}
.b.verified{background:rgba(74,222,128,.13);color:var(--good)}
.b.defect{background:rgba(248,113,113,.13);color:var(--bad)}
.b.assumption{background:rgba(251,191,36,.13);color:var(--warn)}
footer{margin-top:50px;padding-top:18px;border-top:1px solid var(--line);color:var(--fg3);font-size:12px;font-family:var(--mono)}
`;

export function pageHtml({ title, subtitle = '', badges = [], body = '', backHref = '../index.html#corpus', repoHref = null, sha = null, footerNote = '' }) {
  const badgeHtml = badges.length
    ? `<div class="badges">${badges.map((b) => `<span class="b ${escapeHtml(b.verdict)}" title="${escapeHtml(b.note || '')}">${escapeHtml(b.verdict)}</span>`).join('')}</div>`
    : '';
  const shaBit = sha ? `sha1 ${escapeHtml(String(sha).slice(0, 12))} · ` : '';
  const repoBit = repoHref ? `<a href="${escapeHtml(repoHref)}">source</a> · ` : '';
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>${escapeHtml(title)} — AgentSwarm corpus</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Ccircle cx='16' cy='16' r='5' fill='%235eead4'/%3E%3C/svg%3E">
<style>${PAGE_CSS}</style>
</head>
<body><div class="wrap">
<nav><a href="${escapeHtml(backHref)}">← AgentSwarm</a>${subtitle ? `<span class="dom">${escapeHtml(subtitle)}</span>` : ''}</nav>
${badgeHtml}
${body}
<footer>${shaBit}${repoBit}read-only copy of an agent-authored artifact.${footerNote ? ` ${escapeHtml(footerNote)}` : ''}</footer>
</div></body>
</html>`;
}
