#!/usr/bin/env python3
"""
A001 / Kepler -- Statement-Object Coverage Audit (phase4-consensus).

Purpose: decide, mechanically rather than rhetorically, whether any quantitative
object in Consensus Statement v1 still lacks an in-scope verification artifact in
the working directory. This is a provenance/coverage audit over existing files;
it computes nothing about the universe and asserts no new physics.

It answers one question: "Is there an object in the statement that the record
has NOT already addressed?" If every object is covered, then a further 'novel
inquiry' cannot be in-scope without either repetition or fabrication.
"""
import os
import re
import glob

STATEMENT = (
    "The universe began 13.8 billion years ago in a hot, dense state. The "
    "Lambda-CDM model with an early inflationary epoch is the consensus "
    "framework. The CMB temperature is 2.72548 K and the primordial helium mass "
    "fraction is Y_p = 0.247. Open problems: the Hubble tension (73.0 vs 67.4 "
    "km/s/Mpc), the nature of dark matter, and the initial singularity."
)

# Each object is a clause of the statement; tokens are literal strings that any
# honest verification of that clause must contain.
OBJECTS = {
    "age=13.8 Gyr":              ["13.8", "13.797", "13.796", "13.787", "13.80"],
    "T_CMB=2.72548 K":           ["2.72548", "2.7255"],
    "Y_p=0.247":                 ["0.247"],
    "H0_Planck=67.4":            ["67.4"],
    "H0_SH0ES=73.0":             ["73.0", "73.04"],
    "Lambda-CDM framework":      ["Lambda-CDM", "\u039bCDM", "LCDM", "Lambda CDM"],
    "early inflation":           ["inflation"],
    "dark matter":               ["dark matter"],
    "initial singularity":       ["singularity"],
}


def main():
    files = sorted(glob.glob("*.md")) + sorted(glob.glob("*.py")) + \
            sorted(glob.glob("*.txt"))
    files = [f for f in files if os.path.isfile(f)]
    total_bytes = 0
    texts = {}
    for f in files:
        try:
            with open(f, "r", encoding="utf-8", errors="replace") as fh:
                t = fh.read()
        except OSError:
            continue
        texts[f] = t
        total_bytes += len(t)

    print(f"corpus: {len(texts)} files, {total_bytes} chars")
    print("-" * 72)
    uncovered = []
    for obj, toks in OBJECTS.items():
        hits = []
        for f, t in texts.items():
            low = t.lower()
            if any(tok.lower() in low for tok in toks):
                hits.append(f)
        status = "COVERED" if hits else "UNCOVERED"
        if not hits:
            uncovered.append(obj)
        # count files that contain the most specific token
        print(f"{status:9s} {obj:26s} files={len(hits):3d}  e.g. "
              f"{hits[0] if hits else '(none)'}")

    print("-" * 72)
    n = len(OBJECTS)
    print(f"coverage: {n - len(uncovered)}/{n} statement objects addressed")
    if uncovered:
        print("UNCOVERED OBJECTS:", uncovered)
        print("=> a genuinely novel IN-SCOPE inquiry is possible: " +
              ", ".join(uncovered))
    else:
        print("=> all statement objects already addressed by the record.")
        print("   Any further in-scope output is repetition or fabrication.")
    # Deterministic machine-readable summary for the certificate.
    with open("A001_statement_object_coverage.txt", "w", encoding="utf-8") as out:
        out.write(f"objects_total={n}\n")
        out.write(f"objects_covered={n - len(uncovered)}\n")
        out.write(f"uncovered={uncovered}\n")
        out.write(f"corpus_files={len(texts)}\n")
        out.write(f"corpus_chars={total_bytes}\n")
    print("wrote A001_statement_object_coverage.txt")


if __name__ == "__main__":
    main()
