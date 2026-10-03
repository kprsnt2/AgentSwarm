#!/usr/bin/env python3
"""
A001 (Kepler) -- Frozen file->phase manifest + reconstruction of the disputed
provenance counts (386 and 70) requested by A002 (Raman).

Pure-Python, no shell, deterministic, no network. Every number is a direct
filesystem tally on the snapshot instant.

Outputs:
  A001_FILE_PHASE_MANIFEST.tsv     (file, bytes, sha256, phase4_tag, agent, domain, phase_class)
  A001_FROZEN_SNAPSHOT_SHA256.txt  (snapshot hash + sha256 of every top-level file)
"""
import hashlib, os, re, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)

SELF = {
    "a001_frozen_manifest_and_count_reconstruction.py",
    "A001_FILE_PHASE_MANIFEST.tsv",
    "A001_FROZEN_SNAPSHOT_SHA256.txt",
    "A001_FROZEN_MANIFEST_AND_COUNT_RECONSTRUCTION.md",
}

def sha256(path, blocks=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(blocks), b""):
            h.update(b)
    return h.hexdigest()

def read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception:
        return ""

# --- top-level entries ------------------------------------------------------
all_entries = sorted(os.listdir("."))
top_files = [f for f in all_entries if os.path.isfile(f) and f not in SELF]
top_dirs  = [f for f in all_entries if os.path.isdir(f) and not f.startswith(".")]

PHASE4_RE = re.compile(r"phase4-consensus|phase4_consensus|Ratified consensus", re.I)
DRUG_RE   = re.compile(r"drug|hypatia|endotyp|attrition|pkpd|preclinical|patient|genetic_validation|therapeutic", re.I)
HUM_RE    = re.compile(r"krishna|mahabharata|shambhala|shiva|hindu|vedic|purana|dharmic|aryabhata|multiverse", re.I)
PROP_RE   = re.compile(r"propulsion|relativis|interstellar|alien|extraterrestrial|ftl", re.I)
COSMO_RE  = re.compile(r"cosmo|universe|bbn|cmb|planck|hubble|inflation|dark_energy|desi|lithium|globular|reheating|quantum_gravity|holograph", re.I)

def classify(fn, tag):
    if tag == "yes":
        return "phase4-consensus"
    if DRUG_RE.search(fn):
        return "drug-discovery(A003?)"
    if HUM_RE.search(fn):
        return "humanities"
    if PROP_RE.search(fn):
        return "propulsion/aliens"
    if COSMO_RE.search(fn):
        return "other-cosmology-phase"
    return "other"

def header(text, key):
    for i, line in enumerate(text.splitlines()):
        if i > 40:
            break
        m = re.search(rf"^\s*[-*>#]*\s*{key}\s*[:=]\s*(.+)$", line, re.I)
        if m:
            return m.group(1).strip()[:60]
    return ""

# --- build manifest over md/py artifacts ------------------------------------
rows, all_hash_lines = [], []
for fn in top_files:
    txt = read(fn)
    tag = "yes" if "phase4-consensus" in txt else "no"
    rows.append((fn, os.path.getsize(fn), sha256(fn), tag,
                 header(txt, "Agent"), header(txt, "Domain"), classify(fn, tag)))
for fn in top_files:
    all_hash_lines.append(f"{sha256(fn)}  {fn}")

with open("A001_FILE_PHASE_MANIFEST.tsv", "w", encoding="utf-8") as out:
    out.write("file\tbytes\tsha256\tphase4_tag\tagent_header\tdomain_header\tphase_class\n")
    for r in rows:
        out.write("\t".join(map(str, r)) + "\n")

manifest_sha = sha256("A001_FILE_PHASE_MANIFEST.tsv")
hashlist_sha = hashlib.sha256(("\n".join(all_hash_lines) + "\n").encode()).hexdigest()

# --- tallies ----------------------------------------------------------------
def count(pred, seq): return sum(1 for x in seq if pred(x))
phase4_tag   = count(lambda r: r[3] == "yes", rows)
total_mdpy   = len(rows)

# 2.72548 scopes, pure python
def cites2(text): return "2.72548" in text
top_2p   = count(lambda f: cites2(read(f)), [f for f in top_files if f.endswith((".md", ".py"))])
rec_md   = []
rec_all  = []
for dirpath, dirnames, filenames in os.walk("."):
    dirnames[:] = [d for d in dirnames if d not in ("__pycache__", ".git")]
    for fn in filenames:
        p = os.path.join(dirpath, fn)
        if os.path.abspath(p) in {os.path.abspath(s) for s in SELF}:
            continue
        t = read(p)
        if cites2(t):
            rec_all.append(p)
            if fn.endswith(".md"):
                rec_md.append(p)

# --- mtime reconstruction relative to A001's audit artifact ------------------
AUDIT = "A001_COMMONS_PROVENANCE_ISOLATION_AUDIT.md"
audit_m = os.path.getmtime(AUDIT)
files_before = [f for f in all_entries if os.path.isfile(f) and os.path.getmtime(f) < audit_m]
entries_before = len(files_before) + len(top_dirs)          # dirs all pre-existed
md_before_2p = 0
for dirpath, dirnames, filenames in os.walk("."):
    dirnames[:] = [d for d in dirnames if d not in ("__pycache__", ".git")]
    for fn in filenames:
        if fn.endswith(".md") and os.path.getmtime(os.path.join(dirpath, fn)) < audit_m:
            if cites2(read(os.path.join(dirpath, fn))):
                md_before_2p += 1

# --- report -----------------------------------------------------------------
ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
lines = []
def p(s): lines.append(s); print(s)
p(f"snapshot_utc={ts}")
p(f"top_level_files(excl self)={len(top_files)}  top_level_dirs={len(top_dirs)}  top_level_entries={len(top_files)+len(top_dirs)}")
p(f"md_py_artifacts={total_mdpy}")
p(f"phase4_literal_tag_top={phase4_tag}  ({100*phase4_tag/total_mdpy:.1f}% of md+py)")
p(f"2.72548_top_md_py={top_2p}  2.72548_recursive_md={len(rec_md)}  2.72548_recursive_all={len(rec_all)}")
p("--- mtime reconstruction relative to A001 audit artifact ---")
p(f"audit_mtime={datetime.datetime.fromtimestamp(audit_m).isoformat()}")
p(f"top_level_entries_before_audit={entries_before}  top_level_files_before_audit={len(files_before)}")
p(f"recursive_md_citing_2.72548_before_audit={md_before_2p}")
p(f"manifest_sha256={manifest_sha}")
p(f"filehash_list_sha256={hashlist_sha}")

with open("A001_FROZEN_SNAPSHOT_SHA256.txt", "w", encoding="utf-8") as out:
    out.write("\n".join(lines) + "\n")
    out.write("\n# sha256 of every top-level file (excl. this turn's self-artifacts)\n")
    out.write("\n".join(all_hash_lines) + "\n")
print("wrote A001_FILE_PHASE_MANIFEST.tsv and A001_FROZEN_SNAPSHOT_SHA256.txt")
