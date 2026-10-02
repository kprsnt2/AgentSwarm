"""
drug_discovery_attrition.py — Nagarjuna (A004), generation 0.
Quantitative attrition decomposition for "New drug discovery" (drug-discovery).

Every number below is a MEASURED value taken from the primary literature and
retrieved live this session via Europe PMC / PubMed full text. No number here is
invented. Source for each constant is annotated inline. See the companion report
DRUG_DISCOVERY_BOTTLENECKS_AND_COMPUTATIONAL_APPROACHES.md for full citations.

Ground truth I rely on (do not contradict):
  - clinical attrition >90% overall
  - Lipinski rule-of-five for oral bioavailability
  - AlphaFold solved structure prediction, NOT binding affinity or ADMET
"""

from dataclasses import dataclass

# ----------------------------------------------------------------------------
# SOURCES (all retrieved and quoted from full text this session)
# ----------------------------------------------------------------------------
# Wong CH, Siah KW, Lo AW. Biostatistics 2019 (PMID 29394327; DOI 10.1093/biostatistics/kxx069)
#   Aggregate phase POS (phase-by-phase, all indications): 66.4% / 58.3% / 59.0%
#   Overall LoA (path-by-path method): 13.8%  [headline, quoted directly]
#   Oncology (no biomarker) phase POS: 28.0% / 17.4% / 33.6% ; overall 1.6%
#   Oncology (WITH biomarker) phase POS: 43.5% / 38.8% / 63.6% ; overall 10.7%
#   Biomarker patient-selection overall POS: 10.3% (with) vs 5.5% (without)
#   Oncology overall success 3.4% in this sample.
# Sun D, Gao W, Hu H, Zhou S. Acta Pharm Sin B 2022 (PMID 35865092; PMC9293739)
#   Causes of the ~90% failure: lack of efficacy 40-50%; unmanageable toxicity 30%;
#   poor drug-like properties 10-15%; remainder commercial/other.
#   [18F]SPARQ NK1 PET: high receptor occupancy did NOT translate to efficacy
#   => the failure was an invalid mechanism, not inadequate exposure.
# Nelson MR et al. Nat Genet 2015 + King EA, Davis JW, Degner JF. PLoS Genet 2019
#   (DOI 10.1371/journal.pgen.1008489): human genetic support for a target-indication
#   RAISES approval odds ~2x (Nelson) / >2x and prospectively for Mendelian (King).
# ----------------------------------------------------------------------------

@dataclass
class Phases:
    p1_2: float   # POS phase 1 -> 2
    p2_3: float   # POS phase 2 -> 3
    p3_app: float # POS phase 3 -> approval

def loa_product(p: Phases) -> float:
    """Phase-by-phase LoA = simple product of the three gates (Wong Table 3 method)."""
    return p.p1_2 * p.p2_3 * p.p3_app

def rr(base: float, new: float) -> float:
    return new / base

print("="*78)
print("ATTRIBUTION OF CLINICAL ATTRITION BY PHASE (ARITHMETIC ON PUBLISHED POS)")
print("="*78)

# Aggregate, all indications (phase-by-phase gates; path-by-path LoA quoted by authors)
agg = Phases(0.664, 0.583, 0.590)
prod_all = loa_product(agg)
print(f"\n[All indications] gates P1->2={agg.p1_2:.3f}, P2->3={agg.p2_3:.3f}, "
      f"P3->APP={agg.p3_app:.3f}")
print(f"  naive phase-by-phase product       = {prod_all*100:.1f}%")
print(f"  authors' path-by-path LoA (headline)= 13.8%")
print("  >> Gap (22.8% vs 13.8%) = unfollowed/terminated transitions between")
print("     phases that the path-by-path method counts as drops but the naive")
print("     product ignores. We therefore QUOTE 13.8%, not the derived product.")

# Oncology, with vs without biomarker patient selection (all verified to reproduce reported POS)
onc_nb = Phases(0.280, 0.174, 0.336)  # no biomarker, reported overall 1.6%
onc_b  = Phases(0.435, 0.388, 0.636)  # with biomarker, reported overall 10.7%
prod_onc_nb = loa_product(onc_nb)
prod_onc_b  = loa_product(onc_b)
print(f"\n[Oncology, NO biomarker] product = {prod_onc_nb*100:.2f}%  "
      f"(paper's Table 3 'Overall' = 1.6%)  match={abs(prod_onc_nb-0.016)<1e-3}")
print(f"[Oncology, WITH biomarker] product = {prod_onc_b*100:.2f}%  "
      f"(paper's Table 3 'Overall' = 10.7%) match={abs(prod_onc_b-0.107)<1e-3}")
print(f"  >>> Biomarker patient-selection multiplies oncology LoA by "
      f"{rr(prod_onc_nb, prod_onc_b):.1f}x")

# Overall-population biomarker effect (Wong): 10.3% with vs 5.5% without
print(f"\n[All indications] biomarker patient-selection: 10.3% vs 5.5% => "
      f"{10.3/5.5:.2f}x more likely to reach approval")

# Which gate is the binding (worst) one? Marginal +10 percentage points to each gate.
print("\n--- Sensitivity: effect of adding +10pp to ONE gate (oncology, no biomarker) ---")
base = prod_onc_nb
for name, val in [("P1->2", onc_nb.p1_2), ("P2->3", onc_nb.p2_3), ("P3->APP", onc_nb.p3_app)]:
    # recompute product with this gate bumped by +10pp (capped at 1.0)
    comp = {"P1->2": onc_nb.p1_2, "P2->3": onc_nb.p2_3, "P3->APP": onc_nb.p3_app}
    comp[name] = min(1.0, val + 0.10)
    newloa = comp["P1->2"]*comp["P2->3"]*comp["P3->APP"]
    print(f"  +10pp to {name} ({val*100:.1f}% -> {comp[name]*100:.1f}%): "
          f"LoA {base*100:.2f}% -> {newloa*100:.2f}%  "
          f"(x{rr(base,newloa):.2f})")

print("\n  NOTE: because LoA is a PRODUCT, a fixed RELATIVE (multiplicative)")
print("  improvement in any single gate raises LoA by the same factor. A fixed")
print("  ABSOLUTE (+pp) improvement helps MOST on the lowest gate.")

print("\n" + "="*78)
print("ATTRIBUTION OF THE >90% ATTRITION BY CAUSE (Sun 2022 percentages)")
print("="*78)
attrition = 1.0 - 0.138  # 0.862 of Phase-1 programs fail (matches LoA 13.8%)
causes = {
    "Lack of efficacy":      (0.40, 0.50),
    "Unmanageable toxicity": (0.30, 0.30),
    "Poor drug-like prop.":  (0.10, 0.15),
}
for name,(lo,hi) in causes.items():
    print(f"  {name:24s}: {lo*100:.0f}-{hi*100:.0f}% of failures  "
          f"=> {lo*attrition*100:.1f}-{hi*attrition*100:.1f}% of all Phase-1 programs")
remain_lo = 1.0 - sum(hi for _,hi in causes.values())
print(f"  {'(commercial/other remainder)':24s}: ~{remain_lo*100:.0f}% of failures (arithmetic remainder)")
print(f"\n  => Efficacy is the single largest cause: roughly "
      f"{0.40*attrition*100:.0f}-{0.50*attrition*100:.0f}% of all programs die of efficacy,")
print("     i.e. ~4-5x the attrition from poor drug-like properties.")

print("\n" + "="*78)
print("SIGN-OFF: all constants above are live-verified from primary full text.")
print("AlphaFold solves STRUCTURE; binding affinity & ADMET remain hard (ground truth).")
print("="*78)
