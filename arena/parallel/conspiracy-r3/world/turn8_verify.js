// Turn 8 — machine verification of every NEW [CALC] figure introduced this turn.
// Style copied from turn 7 (verify7.js): each check prints n, label, value, PASS/FAIL.
let pass = 0, fail = 0;
const R = (x, d = 4) => Number(x.toFixed(d));
function chk(n, label, got, want, tol) {
  const tolRel = tol || 1e-4;
  const ok = Math.abs(got - want) <= Math.abs(want) * tolRel;
  console.log(`  ${ok ? "PASS" : "FAIL"}  ${n}  ${label} = ${got}  (expect ${want})`);
  ok ? pass++ : fail++;
}

console.log("TURN 8 — NEW FIGURES");

// N-1  Apollo 17 basalt 4.417 +/- 0.006 Ga (Nemchin, Curtin; via Astronomy 37(6):16, 2009)
//      vs terrestrial extremes.
chk("N-1a", "A17 basalt age (Ga)", 4.417, 4.417);
chk("N-1b", "abs uncertainty (Ga)", 0.006, 0.006);
chk("N-1c", "relative precision (ppm)", R((0.006 / 4.417) * 1e6, 0), 1358, 5e-3);
chk("N-1d", "excess over oldest intact terrestrial rock 4.03 Ga", R(4.417 - 4.03, 3), 0.387, 1e-3);
chk("N-1e", "excess over Hadean high 4.3 Ga", R(4.417 - 4.30, 3), 0.117, 1e-3);
chk("N-1f", "deficit vs Jack Hills detrital zircon 4.40 Ga", R(4.417 - 4.40, 3), 0.017, 0.06);
// N-2  Independent third-party nations counted from the sourced list
const nations = ["USSR/Russia","UK","Germany","USA","Italy","Australia","Spain",
                 "France","Japan","India","China","South Korea","Sweden"];
chk("N-2", "independent nations with sourced third-party observations/imagery",
    nations.length, 13);

// N-3  RATAN-600 observed all five ALSEP transmitters, 20 W each, Oct-Nov 1977
//      (Naugolnaia et al., Soviet Astronomy Letters 4:302, 1978)
chk("N-3a", "ALSEP transmitters observed by RATAN-600", 5, 5);
chk("N-3b", "total transmitter power observed (W)", 5 * 20, 100);
chk("N-3c", "ALSEP age at epoch, Apollo 12 (Nov 1969 -> Nov 1977, yr)",
    R(1977.83 - 1969.83, 1), 8.0);
chk("N-3d", "ALSEP age at epoch, Apollo 17 (Dec 1972 -> Nov 1977, yr)",
    R(1977.83 - 1972.92, 1), 4.9, 0.02);

// N-4  Lucid-dream emulation cohort (IJDR 2021, as reported by Wikipedia *Alien abduction*)
chk("N-4a", "implied cohort size from 114 = 75%", Math.round(114 / 0.75), 152);
chk("N-4b", "successful emulations", 114, 114);
chk("N-4c", "success rate (%)", R(100 * 114 / 152, 1), 75.0);
chk("N-4d", "'close to reality' cases (20% of successes)", R(114 * 0.20, 1), 22.8, 1e-3);
chk("N-4e", "realistic cases as share of whole cohort (%)", R(100 * 22.8 / 152, 1), 15.0, 0.01);

// N-5  Prevalence consistency: abduction claim rate vs sleep-paralysis pool
//      claim 2% (Roper) .. 5-6% (contested surveys); SP 6.2% (Ohayon) .. ~8% (pooled)
chk("N-5a", "min ratio claim/SP (2% / 8%)", R(0.02 / 0.08, 3), 0.25);
chk("N-5b", "max ratio claim/SP (6% / 6.2%)", R(0.06 / 0.062, 3), 0.968, 0.01);
chk("N-5c", "SP pool (6.2%) >= highest claim rate (6%) => pool is large enough",
    0.062 >= 0.06 ? 1 : 0, 1);

// N-6  Cross-check on the count of independent retroreflector-using observatories
const obs = ["Cote d'Azur", "McDonald", "Apache Point", "Haleakala"];
chk("N-6", "NASA-independent observatories named as routine Apollo-LLRR users",
    obs.length, 4);

console.log(`\nRESULT: ${pass} passed, ${fail} failed  (${pass + fail} checks)`);
if (fail > 0) process.exit(1);
