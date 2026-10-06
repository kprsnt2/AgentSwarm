// turn 9 — verify every NEW [CALC] figure from the 1994/1997 USAF primary reports
const Y = 0.9144, LB = 0.45359237, FT = 0.3048, IN = 0.0254, MI = 1609.344;
let n = 0, bad = 0;
function chk(name, got, want, tol) {
  n++;
  const ok = Math.abs(got - want) <= (tol || 1e-9) * Math.max(1, Math.abs(want));
  if (!ok) { bad++; console.log("FAIL " + name + " got=" + got + " want=" + want); }
  else console.log("ok   " + name + " = " + got);
}

// --- 1994 USAF report: Brazel's contemporaneous debris inventory (Roswell Daily Record, 9 Jul 1947) ---
chk("200 yd field diameter -> m", 200 * Y, 182.88, 1e-4);
chk("600 ft train -> m", 600 * FT, 182.88, 1e-4);
chk("coincidence check: 200 yd == 600 ft in metres", (200 * Y) - (600 * FT), 0, 1e-9);
chk("~5 lb total debris -> kg", 5 * LB, 2.26796185, 1e-6);
chk("main bundle 3 ft -> m (used FT not Y)", 3 * FT, 0.9144, 1e-9);
chk("main bundle 7 in -> m", 7 * IN, 0.1778, 1e-6);
chk("main bundle 8 in -> m", 8 * IN, 0.2032, 1e-6);
chk("rubber bundle 18 in -> m", 18 * IN, 0.4572, 1e-6);
chk("rubber bundle 20 in -> m", 20 * IN, 0.508, 1e-6);
chk("Brazel 12 ft balloon estimate -> m", 12 * FT, 3.6576, 1e-9);
chk("target leg 48 in -> m", 48 * IN, 1.2192, 1e-9);
chk("stick 1/4 in square -> mm", 0.25 * IN * 1000, 6.35, 1e-4);
chk("stick 1/2 in square -> mm", 0.5 * IN * 1000, 12.7, 1e-4);
chk("1994: balloon max sea-level diameter 25 ft -> m", 25 * FT, 7.62, 1e-9);
chk("FBI telegram 20 ft balloon -> m", 20 * FT, 6.096, 1e-9);

// timing
chk("4 Jun 1947 -> 14 Jun 1947 = 10 d",
  (Date.UTC(1947, 5, 14) - Date.UTC(1947, 5, 4)) / 86400000, 10, 1e-9);
chk("Alamogordo I field trip 28 May-7 Jun 1947 -> days",
  (Date.UTC(1947, 5, 7) - Date.UTC(1947, 4, 28)) / 86400000 + 1, 11, 1e-9);
chk("GAO: 24 Jun-28 Jul 1947 window -> days",
  (Date.UTC(1947, 6, 28) - Date.UTC(1947, 5, 24)) / 86400000 + 1, 35, 1e-9);

// Mogul train statistics
chk("mean balloon spacing on 183 m train, 30 balloons -> m", 182.88 / 30, 6.096, 1e-9);
chk("mean balloon spacing on 183 m train, 31 balloons -> m", 182.88 / 31, 5.8993548387, 1e-9);

// 1997 USAF report: dummy-drop programme
chk("67 dummies / 43 flights -> per flight", 67 / 43, 1.5581395349, 1e-6);
chk("98,000 ft -> km", 98000 * FT / 1000, 29.8704, 1e-6);
chk("Jun 1954 - Feb 1959 inclusive -> months",
  (1959 - 1954) * 12 + (2 - 6) + 1, 57, 1e-9);
chk("1953-1959 span (1959-1953) -> years = report's 'six-year period'", 1959 - 1953, 6, 1e-9);
chk("1953-1959 inclusive calendar years", 1959 - 1953 + 1, 7, 1e-9);
chk("window Jun 1954-Feb 1959 -> years", 57 / 12, 4.75, 1e-9);
chk("KC-97 26 Jun 1956 lag after 8 Jul 1947 release -> days",
  (Date.UTC(1956, 5, 26) - Date.UTC(1947, 6, 8)) / 86400000, 3276, 1e-6);
chk("KC-97 26 Jun 1956 lag after 8 Jul 1947 release -> years",
  3276 / 365.25, 8.9684, 1e-3);
chk("bodies-hospital claims lag: 1959 balloon mishap minus Jul 1947 -> years",
  (Date.UTC(1959, 0, 1) - Date.UTC(1947, 6, 1)) / (365.25 * 86400000), 11.4944, 1e-3);

// Helgoland charge (Flight 2 purpose)
chk("5,000 short tons TNT -> TJ", 5000 * 4.184 / 1000, 20.92, 1e-6);
chk("5,000 short tons TNT -> kg (TNT 4.184e6 J/kg)", 5000 * 907.18474, 4535923.7, 1e-6);

chk("8.8 statute miles south of Walker AFB -> km", 8.8 * MI / 1000, 14.1622, 1e-3);
chk("KC-97 prop failure 4.5 min after takeoff -> s", 4.5 * 60, 270, 1e-9);

// density cross-check on Brazel's 2.27 kg over a 183 m field
chk("areal density of 2.268 kg over 182.88 m dia disc -> g/m^2",
  2267.96185 / (Math.PI * (182.88 / 2) ** 2), 0.08634, 2e-3);
chk("disk area (182.88 m dia) -> m^2", Math.PI * (182.88 / 2) ** 2, 26267.7157, 1e-6);

console.log("\n" + n + " checks, " + bad + " failures");
process.exit(bad ? 1 : 0);
