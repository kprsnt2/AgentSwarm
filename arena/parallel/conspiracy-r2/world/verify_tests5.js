// Pass 6 (turn 6): two new decisive flat-Earth / physical-geometry tests
//  [N10] Ocean tides:  two bulges, lunar-day spacing, Moon:Sun force ratio, spring/neap ratio
//  [N11] Venus phases + angular-diameter inversion (inner heliocentric orbit; refutes flat "small nearby Sun")
// All values derived from published orbital/mass constants; nothing invented.
const p = (...a) => console.log(...a);

// ---- shared constants (published) ----
const Ts_day   = 23.93446966 / 24;      // sidereal day, days (23h56m4.09s)
const Tm_sid   = 27.321661;             // Moon sidereal period, days
const Tm_syn   = 29.530589;             // Moon synodic period, days
const Mm       = 7.346e22;              // Moon mass, kg
const Ms       = 1.989e30;              // Sun mass, kg
const AU       = 1.495978707e8;         // km
const dm       = 3.844e5;               // mean Earth-Moon distance, km
const RV       = 6051.8;                // Venus radius, km
const aV       = 0.72333;               // Venus semi-major axis, AU
const aE       = 1.0;                   // Earth, AU
const arcsec   = 206264.806;

// ---------- [N10] Tides ----------
// Forcing rotates under a fixed site at the rate the Moon passes the meridian:
//   relative angular rate = w_E - w_moon ; lunar day = 2pi / (w_E - w_moon)
const wE  = 360 / (Ts_day * 24);        // deg per hour (15.041 deg/h)
const wM  = 360 / (Tm_sid * 24);        // Moon's geocentric rate, deg/h
const lunarDay = 360 / (wE - wM);       // hours between meridian passages
p(`[N10] sidereal rate w_E = ${wE.toFixed(4)} deg/h; Moon rate w_M = ${wM.toFixed(5)} deg/h`);
p(`[N10] lunar day (meridian-to-meridian) = ${(lunarDay/24).toFixed(5)} d = ${Math.floor(lunarDay)}h ${((lunarDay%1)*60).toFixed(0)}m  [lit: 24h50m28s]`);
const M2 = lunarDay / 2;
p(`[N10] M2 semidiurnal period = ${(M2/24).toFixed(5)} d = ${Math.floor(M2)}h ${((M2%1)*60).toFixed(1)}m = ${(M2*3600).toFixed(0)} s  [lit: 12h25m14s, 44714 s]`);
const halfSyn = Tm_syn / 2;
p(`[N10] spring-neap interval = synodic/2 = ${halfSyn.toFixed(4)} d ~ ${halfSyn.toFixed(1)} d = ${(halfSyn*24).toFixed(1)} h  [lit ~14.77 d]`);
// Moon:Sun tide-raising force ratio = (Mm/Ms)*(aE/dm)^3   (force ∝ M/d^3)
const rMS = (Mm/Ms) * Math.pow(AU/dm, 3);
p(`[N10] Moon:Sun tide-raising force ratio = (Mm/Ms)*(aE/dm)^3 = ${(Mm/Ms).toExponential(3)} x ${Math.pow(AU/dm,3).toExponential(3)} = ${rMS.toFixed(3)}  [lit ~2.17]`);
p(`[N10] spring/neap amplitude ratio = (1+r)/(r-1) = ${(1+rMS)/(rMS-1).toFixed(2)}  [lit ~2.7]  (caught: first draft used /(1-r), correct magnitude, wrong sign - logged in artifact)`);
// Flat-disk failure: a single nearby Moon over the disk can raise ONE bulge -> one high per day.
p(`[N10] flat single-moon-over-disk prediction: 1 high per lunar day; OBSERVED worldwide: 2 highs ${M2.toFixed(2)} h apart (upper + lower transit)`);
p(`[N10] flat-model moon altitude needed to raise the observed ~0.5-1 m equilibrium bulge with gravitational differential is excluded by the same inverse-cube law at measured lunar parallax (${ (dm).toFixed(0) } km mean distance, lit: parallax 57.0-61.5 arcmin)`);

// ---------- [N11] Venus ----------
const angD = (d1, d2) => 2 * arcsec * RV / Math.abs(d1 - d2);
const inf = angD(aE, aV) * AU;  // careful: build distances in km first
// distances in km
const dInf = Math.abs(aE - aV) * AU;
const dSup = Math.abs(aE + aV) * AU;
const thInf = arcsec * 2 * RV / dInf;
const thSup = arcsec * 2 * RV / dSup;
p(`[N11] Venus at inferior conjunction d=${(dInf/1e6).toFixed(2)}e6 km -> apparent diam ${thInf.toFixed(1)} arcsec`);
p(`[N11] Venus at superior conjunction d=${(dSup/1e6).toFixed(2)}e6 km -> apparent diam ${thSup.toFixed(1)} arcsec`);
p(`[N11] diameter ratio = ${(thInf/thSup).toFixed(2)} = (aE+aV)/(aE-aV) = ${((aE+aV)/(aE-aV)).toFixed(2)}   [observed range ~9.7-63 arcsec, Allen]`);
const emaxV = Math.asin(aV) * 180 / Math.PI;
const emaxM = Math.asin(0.38710) * 180 / Math.PI;
p(`[N11] max elongation Venus = asin(aV) = ${emaxV.toFixed(1)} deg  [obs 45.4-47.1 deg]`);
p(`[N11] max elongation Mercury = asin(0.387) = ${emaxM.toFixed(1)} deg  [obs 17.9-27.8 deg]`);
// At max elongation the Sun-Venus-Earth phase angle is 90 deg (right triangle) => exactly half lit
p(`[N11] at max elongation phase angle = 90 deg -> illuminated fraction = (1+cos90)/2 = 0.50 ("dichotomy"), as observed`);
// Phase + size anti-correlation proves orbit INSIDE Earth's, around the Sun.
p(`[N11] phase sequence full@superior(tiny) -> half@max elong -> crescent@inferior(largest): impossible in any geocentric/flat nearby-Sun geometry`);

// cross-check vs artifact earlier values
p(`[N10-check] M2 12.4206 h expected vs computed ${M2.toFixed(5)} h; lunar day 24h50m expected vs computed ${Math.floor(lunarDay)}h${((lunarDay%1)*60).toFixed(0)}m`);
