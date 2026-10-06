// verify_tests4.js  -- Pass 5 (this turn): horizon-DIP decisive test for flat Earth.
// A single observer with a hand level / clinometer / bubble sextant can measure the
// angular depression of the horizon below the true horizontal. On a sphere
//   dip(theta) = acos(R/(R+h))     (R = 6,371,008.8 m, nominal mean radius, same constant as §2.3)
// On ANY flat plane, the horizon is at eye level for every height: dip == 0 exactly.
// The flight-standard table value dip(arcmin) ~= 1.07*sqrt(h_ft) folds in a small
// refraction correction; the pure geometric constant is sqrt(2/R_ft)*3437.75.
// Inverting: R = h / (sec(dip) - 1).  On a flat model sec(0)-1 = 0 -> R undefined/infinite.
const R = 6371008.8;                 // m
const RAD2ARCMIN = 180 * 60 / Math.PI;
const M2FT = 3.280839895;
const R_ft = R * M2FT;

const dipRad = h => Math.acos(R / (R + h));

console.log("=== Pass-5 horizon dip (sphere R = " + R + " m) ===");
const cases = [
  ["3 m   (eye above ground)", 3],
  ["30 m  (look-out / tall cliff)", 30],
  ["100 m (hill / cliff)", 100],
  ["1000 m (mountain)", 1000],
  ["9144 m = 30,000 ft (airliner cruise)", 9144],
];
for (const [label, h] of cases) {
  const d = dipRad(h);
  const arcmin = d * RAD2ARCMIN;
  const deg = d * 180 / Math.PI;
  const flight = 1.07 * Math.sqrt(h * M2FT);        // flight-standard form
  console.log(
    ` h=${String(h).padStart(5)} m : dip = ${deg.toFixed(4)} deg = ${arcmin.toFixed(2)} arcmin` +
    ` | flight-tbl 1.07*sqrt(h_ft)=${flight.toFixed(2)}' | FLAT MODEL PREDICTS 0.00'`
  );
}
console.log(
  " geometric per-sqrt(h_ft) constant = " + (Math.sqrt(2 / R_ft) * RAD2ARCMIN).toFixed(4) +
  "  (flight tables ~1.07 include a small refraction correction)"
);

console.log("\n=== Single-instrument Earth-radius recovery: R = h/(sec(dip)-1) ===");
for (const [label, h] of [["100 m", 100], ["1000 m", 1000], ["9144 m; 30,000 ft", 9144]]) {
  const d = dipRad(h);
  const Rinf = h / (1 / Math.cos(d) - 1);
  const err = (Rinf - R) / R * 100;
  console.log(
    ` measure dip from ${label.padEnd(20)}: dip=${(d * RAD2ARCMIN).toFixed(2)}'` +
    ` -> R_inferred = ${(Rinf / 1000).toFixed(1)} km (true 6371.0 km, err ${err.toFixed(3)}%)`
  );
}
console.log(
  " FLAT MODEL: sec(0)-1 = 0, so R = h/0 is undefined/infinite -- a dip measurement on a flat plane\n" +
  " returns exactly 0 arcmin at every height and yields no finite radius."
);

// --- Cross-checks that tie dip to the constants already used elsewhere ---
console.log("\n=== Cross-checks (same R as hull-down §2.3 / LLR §3.1 / umbra §2.11) ===");
const horizon1m = Math.sqrt(2 * R * 1);  // geometric horizon for 1 m eye, m
console.log(" geometric horizon @ eye 1 m = " + (horizon1m / 1000).toFixed(3) + " km (small-angle, ties hull-down)");
// dip at the exact height where horizon == 1 km on flat? nothing to tie; skip.
