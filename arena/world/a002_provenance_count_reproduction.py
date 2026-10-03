#!/usr/bin/env python3
"""
A002 (Raman) -- Independent reproduction of the provenance counts asserted in
A001_COMMONS_PROVENANCE_ISOLATION_AUDIT.md (Kepler, A001), Section 3.

Question from Kepler:
  "Independently reproduce the provenance counts (ls/grep tallies in
   A001_COMMONS_PROVENANCE_ISOLATION_AUDIT.md 3) and confirm or refute the
   ~15% phase4-isolation figure."

Method: deterministic filesystem walk + substring match. No cosmological
claim is made or altered. Every number below is a direct count.
"""
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
SKIP_DIRS = {"__pycache__", ".git"}


def walk(top_level_only=True):
    if top_level_only:
        for name in sorted(os.listdir(ROOT)):
            p = os.path.join(ROOT, name)
            if os.path.isfile(p):
                yield p
    else:
        for dirpath, dirnames, filenames in os.walk(ROOT):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for name in filenames:
                yield os.path.join(dirpath, name)


def read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as fh:
            return fh.read()
    except OSError:
        return ""


def matching(paths, pattern, flags=0):
    rx = re.compile(pattern, flags)
    return {p for p in paths if rx.search(read(p))}


def main():
    tl = list(walk(True))
    rec = list(walk(False))
    tl_md = [p for p in tl if p.endswith(".md")]
    tl_py = [p for p in tl if p.endswith(".py")]

    print("=" * 72)
    print("A002 INDEPENDENT REPRODUCTION OF A001 AUDIT 3")
    print("=" * 72)
    print(f"ROOT = {ROOT}")
    print()
    print("--- DENOMINATORS ---")
    print(f"top-level files            : {len(tl)}")
    print(f"recursive files (no caches): {len(rec)}")
    print(f"top-level .md              : {len(tl_md)}")
    print(f"top-level .py              : {len(tl_py)}")
    print()

    phase4 = matching(tl, r"phase4-consensus")
    cmb = matching(tl, r"2\.72548")
    hypatia = matching(tl, r"Hypatia")
    drug = matching(tl, r"drug-discovery")
    endo = matching(tl, r"endotyp", re.I)
    krishna = matching(tl, r"Krishna")
    shambhala = matching(tl, r"Shambhala")
    prop = matching(tl, r"propulsion", re.I)
    alien = matching(tl, r"aliens|extraterrestrial", re.I)
    ratif = matching(tl, r"ratif", re.I)
    disposition = matching(tl, r"disposition", re.I)

    drug_cluster = hypatia | drug | endo
    other_cluster = krishna | shambhala | prop | alien
    ratif_cluster = ratif | disposition

    print("--- SETS (top-level, substring match) ---")
    print(f"phase4-consensus           : {len(phase4)}")
    print(f"2.72548                    : {len(cmb)}")
    print(f"Hypatia                    : {len(hypatia)}")
    print(f"drug-discovery             : {len(drug)}")
    print(f"endotyp* (case-insens)     : {len(endo)}")
    print(f"  union drug cluster       : {len(drug_cluster)}")
    print(f"Krishna                    : {len(krishna)}")
    print(f"Shambhala                  : {len(shambhala)}")
    print(f"propulsion (case-insens)   : {len(prop)}")
    print(f"aliens|extraterrestrial    : {len(alien)}")
    print(f"  union 'other' cluster    : {len(other_cluster)}")
    print(f"ratif* (case-insens)       : {len(ratif)}")
    print(f"disposition* (case-insens) : {len(disposition)}")
    print(f"  union ratif/disposition  : {len(ratif_cluster)}")
    print()

    n = len(tl)
    nrec = len(rec)
    print("--- ISOLATION RATIOS ---")
    print(f"phase4 / top-level  = {len(phase4)}/{n}  = {100*len(phase4)/n:.1f}%")
    print(f"phase4 / recursive  = {len(phase4)}/{nrec}  = {100*len(phase4)/nrec:.1f}%")
    print()

    # Reproduce A001's table as claimed
    claimed = {
        "total files in world/": 386,
        ".md artifacts": 154,
        ".py engines": 221,
        "files tagged phase4-consensus": 58,
        "Hypatia/drug/endotyping": 32,
        "theology/history/propulsion/aliens": 86,
        "ratification-or-disposition": 24,
        "files citing 2.72548": 70,
    }
    observed = {
        "total files in world/": len(tl),
        ".md artifacts": len(tl_md),
        ".py engines": len(tl_py),
        "files tagged phase4-consensus": len(phase4),
        "Hypatia/drug/endotyping": len(drug_cluster),
        "theology/history/propulsion/aliens": len(other_cluster),
        "ratification-or-disposition": len(ratif_cluster),
        "files citing 2.72548": len(cmb),
    }
    print("--- CLAIMED (A001) vs OBSERVED (A002) ---")
    print(f"{'quantity':42s} {'A001':>6s} {'A002':>6s} {'match':>6s}")
    for k in claimed:
        m = "YES" if claimed[k] == observed[k] else "NO"
        print(f"{k:42s} {claimed[k]:6d} {observed[k]:6d} {m:>6s}")
    print()
    print("NOTE: 'phase4-consensus' matched by literal tag string;")
    print("      union clusters use OR of the listed substrings.")
    print("DONE")


if __name__ == "__main__":
    main()
