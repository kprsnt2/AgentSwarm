// god-religions-truth_evil_evidential_reach_calc.cjs
// Purpose: compute the maximum evidential reach, in Bayes-factor units, of the
// evidential problem of evil, as a function of the one parameter the data cannot bound.
//
// MODEL
//   P  = "intense suffering exists with its observed distribution" (scale, cruelty,
//        apparent absence of merit-tracking, pre-human animal suffering)
//   H_n = naturalism / most rivals: P(P|H_n) ~= 1  (biology entails suffering; it is observed)
//   H_t = classical theism:         P(P|H_t) = x  (stipulated via auxiliaries)
//
// x is the entire battleground. "Gratuitous" suffering is defined by the absence of a
// hidden justifying good, and its absence is unobservable by construction — Wykstra's
// CORNEA noseeum inference (IJPR 1984) is exactly the argument that we have no handle
// on the conditions under which a transcendent God would produce visible justifications.
// So x is a stipulated parameter, not a measurement: the argument's strength is the x a
// defender is willing to grant, and that is a prior, not a datum.
//
// AUXILIARY TAX (prayer-audit §7 / B14-rule §6): m auxiliaries at 100:1 apiece
// consume m*2 orders of |log10 BF|.
//
// REFERENCES (from the artifact family):
//   decisive-datum standard: 3 day-exact predictions -> BF ~ 10^7.7   (taxonomy ledger; prayer audit P2)
//   best prayer literature:  log10(BF01) ~ 0.15                     (prayer audit §3)
//   testimony ceiling:        BF = 10^6 vs prior 10^-12 -> ~10^-6   (proof-bounds §4 / R3)

const Pn = 1.0;
const grid = [1, 0.99, 0.9, 0.5, 0.25, 0.1, 0.05, 0.01];

console.log("Evidential reach of the evidential problem of evil");
console.log("P(pattern | naturalism) = " + Pn + "   (stipulated: biology entails the observed suffering)");
console.log("P(pattern | classical theism) = x  (the only movable parameter; no observable handle)");
console.log("");

let maxAbsLog = 0;
for (const x of grid) {
  const BF = x / Pn;
  const log10 = Math.log10(BF);
  maxAbsLog = Math.max(maxAbsLog, Math.abs(log10));
  const m = Math.ceil(Math.abs(log10) / 2);
  console.log(
    "x=" + String(x).padEnd(5) +
    "  BF=" + BF.toFixed(4).padEnd(7) +
    "  log10(BF)=" + log10.toFixed(4).padStart(8) +
    "  auxiliaries@100:1 to neutralize = " + m
  );
}

console.log("");
console.log("GAP TO DECISIVE STANDARD: max |log10 BF| over the whole stipulation grid = " + maxAbsLog.toFixed(4));
console.log("  vs decisive-datum standard 10^7.7 -> shortfall = " + (7.7 - maxAbsLog).toFixed(2) + " orders of magnitude");
console.log("  vs best prayer-literature value 0.15 -> the argument only MATCHES a null's");
console.log("  achieved weight if the defender grants x >= " + Math.pow(10, -0.15).toFixed(3) +
  "; only the hostile cells x <= 0.1 clear that band, and each is erased by one auxiliary");
console.log("");
console.log("SYMMETRY: the same tax applies to any rival's stipulation, in either direction;");
console.log("  the naturalist who declines a hidden-goods story pays the same kappa (B14 rule §6).");
console.log("REACH: even total evidential success bears on the attribute conjunction");
console.log("  (omnipotence ^ benevolence), not on existence, number, unity, or identity of the divine.");