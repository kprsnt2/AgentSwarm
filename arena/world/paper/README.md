# Publication Manuscript & Submission Package

This directory contains the formal, publication-ready research paper for the novel theoretical discovery derived in **AgentSwarm Phase 5**.

---

## 1. Paper Overview
- **Title:** *Gravitational Decoherence and Stochastic Tidal Phase Diffusion of Galactic Dark Matter Solitons: Microscopic Lindblad Evolution and Pulsar Timing Observables*
- **Authors:** K. P. R. Sankar, A001_DarkMatter, A002_QuantumCosmos (AgentSwarm Collaboration)
- **Target Journals / Repositories:**
  - *Physical Review D* (Particles, Fields, Gravitation, and Cosmology)
  - *Monthly Notices of the Royal Astronomical Society* (MNRAS)
  - *The Astrophysical Journal* (ApJ)
  - **arXiv Categories:** `astro-ph.CO` (Cosmology and Nongalactic Astrophysics), `hep-ph` (High Energy Physics - Phenomenology), `quant-ph` (Quantum Physics)

---

## 2. Directory Contents
- **`manuscript.tex`**: The primary LaTeX source code formatted in standard **REVTeX 4.2** (the official American Physical Society two-column template required by *Physical Review D* and accepted by arXiv).
- **`references.bib`**: Complete BibTeX bibliography citing all foundational literature (Hu et al. 2000, Schive et al. 2014, Hui et al. 2017, Lindblad 1976, Kohn 1961, NANOGrav 2023, Planck 2020).
- **`pta_lorentzian_profile.svg`**: Publication-quality vector figure illustrating the 10-order-of-magnitude radial linewidth gradient across the Milky Way.
- **`generate_figures.py`**: Standalone Python script that regenerates the figure from first principles.

---

## 3. How to Submit to arXiv / Overleaf / Journals

### Option A: Open in Overleaf (Easiest)
1. Zip this `paper/` directory:
   - `manuscript.tex`
   - `references.bib`
   - `pta_lorentzian_profile.svg`
2. Go to [Overleaf.com](https://www.overleaf.com) $\to$ **New Project** $\to$ **Upload Project**.
3. Select the `.zip` archive. Overleaf will automatically compile the PDF with REVTeX 4.2.

### Option B: Local Compilation
If you have a local TeX distribution (TeX Live / MacTeX / MikTeX):
```bash
pdflatex manuscript.tex
bibtex manuscript
pdflatex manuscript.tex
pdflatex manuscript.tex
```

### Option C: arXiv Submission
1. In Overleaf or your local directory, ensure the bibliography is compiled.
2. Submit the package to [arXiv.org](https://arxiv.org/submit) under category **`astro-ph.CO`** (with secondary categories `hep-ph` and `quant-ph`).

---

## 4. Computational Reproducibility
All derivations and numerical values quoted in the manuscript are fully backed by the open-source engines in `arena/world/`:
- `a001_phase5_novel_gravitational_decoherence_engine.py` (Master Lindblad calculation)
- `a002_phase5_novel_quantum_observational_signatures.py` (PTA Lorentzian line-broadening and SNR)
- Unit tests: `test_a001_phase5_novel_gravitational_decoherence.py` & `test_a002_phase5_novel_quantum_observational_signatures.py` (19/19 passing tests).
