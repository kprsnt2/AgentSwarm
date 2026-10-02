# Agent Swarm — Findings Site

A static site presenting the forensic study of an autonomous multi-agent research swarm.

## Two builds — pick one

| Build | Path | Use when |
|---|---|---|
| **Self-contained** | `dist/index.html` | **Recommended.** One file, works by double-clicking. No server. |
| Source | `index.html` + `data/findings.json` | Editing the site; needs an HTTP server. |

### The `file://` problem (important)

`index.html` loads its data with `fetch('data/findings.json')`. Browsers **block
`fetch` on the `file://` protocol** for security, so opening `index.html` directly
shows:

> Could not load `data/findings.json`. Run `node export-site.mjs` …

The data is fine — the browser is refusing to read it. Two fixes:

1. **Use the self-contained build** (`dist/index.html`). `build.mjs` inlines the JSON
   into the page, so there is nothing to fetch. Double-click and it works.
2. **Serve over HTTP** if you're editing the source version:
   ```powershell
   cd D:\AgentSwarm\site
   python -m http.server 8899 --bind 127.0.0.1
   # open http://127.0.0.1:8899/
   ```

## Rebuilding after a swarm run

```powershell
cd D:\AgentSwarm\arena
node export-site.mjs      # 1. refresh data/findings.json from the ledgers
cd D:\AgentSwarm\site
node build.mjs            # 2. produce the self-contained dist/index.html
```

Always rebuild after a run — `dist/` embeds a snapshot of the data at build time.

### Runs that were silently missing

`export-site.mjs` originally selected run directories with `/^phase\d/`, which meant
every **`direct-*`** run (the ad-hoc `node new-run.mjs -q "..."` runs) was dropped —
their turns, costs, findings and artifacts never reached the site at all, with no
warning. The filter now takes any run directory containing a `turns.jsonl` ledger.

If the site's totals look lower than the work you know was done, check for this class
of bug first: the exporter is a *snapshot*, and a filter that silently excludes input
produces a page that looks fine but is wrong.

## Files

```
site/
├── index.html          source page (fetches data/findings.json)
├── build.mjs           inlines the data → dist/index.html
├── data/
│   └── findings.json   generated from the arena's forensic ledgers
├── dist/
│   ├── index.html      self-contained build (160 KB) ← ship this
│   └── preview.png     rendered screenshot
└── README.md
```

## Deploying

`dist/index.html` is a single self-contained file — drop it anywhere:

- **GitHub Pages**: copy `dist/index.html` into the repo as `index.html`
- **Vercel / Netlify**: deploy the `dist/` directory, no build command
- **Alongside kprsnt.in**: copy into the static directory under a subpath (e.g. `/swarm/`)
- **Email / share**: it's one file with no dependencies

No server, no framework, no runtime dependencies.

## Structure of the page

| Section | Content |
|---|---|
| Headline | Aggregate metrics from the ledger |
| Method | Four design commitments + epistemic classification table |
| Substrate benchmark | Per-harness success rate, cost/turn, tool calls/turn |
| Honesty oracle | Three violation classes + scorer calibration |
| Phase 2 | Adversarial goal, claimed-vs-verified table, result |
| Stasis | The 911-turn failure mode and its measurement |
| **Conclusion posts** | **One post per run, written by the Scribe agent** |
| Research output | Physics spot-check, numerical audit, artifacts |
| Engineering findings | Eight silent-failure bugs and their fixes |
| Limits | What the study does *not* establish |
| Next | Phase 3 and open work |

### Conclusion posts

The `#posts` section renders the posts written by the arena's conclusion agent (see
`arena/scribe.mjs`). Each post is a collapsible card showing the run, its key totals,
and whether the prose was model-polished or shipped as the deterministic ledger draft.

Post bodies arrive as Markdown in `findings.json` and are rendered by a small renderer
in `index.html` (`md()`). It escapes HTML **before** applying any Markdown rules, so
agent-authored prose can never inject markup into the page.

If the section shows "No conclusion posts yet", the arena has not produced any — run
`node post.mjs` from `arena/` to backfill them for existing runs.

## Editing

All styling is inline in `index.html` under a single `<style>` block using CSS custom
properties. The palette matches the `kprsnt.in` dark theme:

```css
--bg:#0a0c10   --fg:#e6e9ef   --acc:#5eead4   --acc2:#38bdf8
```

To change a colour, edit the `:root` block. To add a section, add the markup plus a
matching `getElementById` block inside the `Promise.resolve(...).then(D => {...})`
callback near the bottom.

## Note on the JavaScript

All dynamic rendering happens inside **one** `.then()` callback. A `.catch()` at the
end reports load failures. Because every section is populated from the same callback,
**an exception in one section silently prevents later sections from rendering** — the
catch swallows it.

If a section appears empty, check the browser console. This bit me during development:
a test harness containing only one section threw on a missing `headline-stats` element
and everything after it stayed blank, which looked like a data bug but was a DOM bug.

A quick way to verify a build:

```powershell
# renders the page and greps for known content
& "C:\Program Files\Google\Chrome\Application\chrome.exe" `
  --headless=new --disable-gpu --virtual-time-budget=12000 --dump-dom `
  "file:///D:/AgentSwarm/site/dist/index.html" | Select-String "gemini-3.8-flash-high"
```
