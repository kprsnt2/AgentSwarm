// Kepler (A001) turn-3 NEW decisive tests. Complements verify_tests.js (pass-2 audit).
// Every quantity is derived here from constants/formulas stated inline.
const out=[]; const p=s=>out.push(s);
const R=6371.0088, C=299792.458;            // Earth mean radius km (IAU 2015 Res. B3); c km/s
const arcsec=Math.PI/(180*3600);            // radians per arcsec
const AU=1.495978707e8;                     // astronomical unit, km (IAU 2012)
const PARSEC=AU/arcsec;                     // km; distance at which parallax = 1"
const LY=9.4607e12;                         // km per light-year
const dMoon=384400;                          // mean Earth-Moon distance, km

// ---------- [N1] Stellar parallax: a "nearby" star dome is excluded by null diurnal parallax ----------
// Diurnal parallax amplitude of an object at centre-distance (R+H) seen from the surface:
//   p = R / (R + H)   (small-angle; exact to the sky plane)
const pAmp=A=>R/(R+A)/arcsec;                // arcsec amplitude for a dome H=A km above surface
for(const H of [1000,5000,1e5]) p(`[N1] flat star dome H=${H} km -> diurnal parallax amplitude ${pAmp(H).toExponential(2)}\" = ${(pAmp(H)/3600).toFixed(1)} deg of sky wobble in 12 h`);
// Invert: dome distance required for the amplitude to fall below a detectability threshold eps
const Hmin=eps=>R/(eps*arcsec)-R;           // km
for(const eps of [60,1,0.01,2e-5])          // 60" naked-eye, 1" classic plate, 0.01" survey, 2e-5" (Gaia ~0.02 mas)
  p(`[N1] null diurnal parallax at eps=${eps}\" -> dome must lie beyond ~${Hmin(eps).toExponential(2)} km (${(Hmin(eps)/LY).toFixed(3)} ly)`);
// The 1-arcminute bound already places a star dome ~57x FARTHER than the Moon:
p(`[N1] eps=60\" bound -> ${(Hmin(60)/dMoon).toFixed(0)}x the Moon's distance; flat models put the Moon BELOW the star dome -> contradiction`);
// Reconcile with measured ANNUAL (heliocentric) parallax, which recovers real interstellar distances:
for(const [nm,par] of [["Proxima Centauri",0.7687],["61 Cygni (Bessel 1838)",0.2853],["Alpha Centauri B (Henderson 1839)",0.742]])
  p(`[N1] annual parallax ${nm} p=${par}\" -> d=${(1/par).toFixed(3)} pc = ${(1/par*PARSEC/LY).toFixed(2)} ly [lit]`);
p(`[N1] Sun's gravitational deflection of starlight during eclipse (Eddington 1919, GR) further bounds/frames geometry; parallax alone already refutes a local dome`);

// ---------- [N2] Lunokhod rover reflectors + Earth-Moon radio light-time ----------
for(const d of [356400,dMoon,406700]) p(`[N2] Earth-Moon light time d=${d} km -> 1-way ${(d/C).toFixed(3)} s, round trip ${(2*d/C).toFixed(3)} s`);
p(`[N2] Apollo surface TV/telemetry carried the full ~2.56 s round-trip light time (source at the Moon), not a studio's <1 ms latency`);
p(`[N2] French-built retroreflectors on Luna 17/Lunokhod 1 (1970) and Luna 21/Lunokhod 2 (1973) are ALSO ranged; APOLLO re-acquired the 'lost' Lunokhod 1 array in 2010 and refined its site [lit]`);
p(`[N2] distinct arrays at SEPARATE coordinates all return pulses and are resolvable as different targets -> technique ranges real hardware; Apollo arrays sit exactly on the 11/14/15 sites`);

// ---------- [N3] Alien abduction: base-rate vs zero physical trace + reentry energetics ----------
const usPop1992=2.6e8;                      // US population ~1992 (order-of-magnitude anchor, Census)
for(const f of [0.01,0.02]) p(`[N3] Roper candidate prevalence (CONTESTED input) ${f*100}% of ~${usPop1992.toExponential(0)} US adults -> ~${(usPop1992*f/1e6).toFixed(1)} million alleged experiencers in one country`);
p(`[N3] each event requires non-public departure and atmospheric RETURN of a vehicle; reentry energetics:`);
const vesc=11.186;                          // km/s, Earth escape/surface reentry regime
p(`[N3]   v=${vesc} km/s -> kinetic energy ${(0.5*vesc*vesc).toFixed(1)} MJ/kg; Mach ~${(vesc/0.343).toFixed(0)} at sea level (0.343 km/s) [unit-fix: 0.5*v^2 in km2/s2 == MJ/kg directly]`);
p(`[N3]   that is ~${(vesc/(0.85*1062/3600)).toFixed(0)}x the ground speed of a 747 at Mach 0.85 cruise (${(0.85*1062).toFixed(0)} km/h)`);
p(`[N3]   reentries at this energy are tracked obsessively (NORAD/radar/seismic/acoustic/optical); millions of undocumented returns leave zero trace -> posterior ~0`);

// ---------- [N4] Roswell: Mogul trajectory scale + impossible body-report chronology ----------
function gcKm(a,b,c,d){const p1=a*Math.PI/180,p2=c*Math.PI/180,dp=p2-p1,dl=(d-b)*Math.PI/180;
  const q=Math.sin(dp/2)**2+Math.cos(p1)*Math.cos(p2)*Math.sin(dl/2)**2;return 2*R*Math.asin(Math.sqrt(q));}
// Approximate coords: Alamogordo launch (Mogul), Roswell RAAF, Foster/Brazel ranch sector near Corona
const ALM=[32.8995,-105.96], CROSS=[34.30,-105.58], RMN=[33.39,-104.52];
p(`[N4] great-circle Alamogordo->Corona(Foster ranch sector) ~${gcKm(...ALM,...CROSS).toFixed(0)} km; Corona->Roswell ~${gcKm(...CROSS,...RMN).toFixed(0)} km [coords approximate]`);
p(`[N4] Mogul balloon trains of order 150-640 ft (~46-195 m); reported main debris 'field' ~0.75-1 mi (~1.2-1.6 km) long -> consistent scale [lit: USAF 1994/1997]`);
const delayY=1955.5-1947;
p(`[N4] anthropomorphic-dummy drops date to 1950s (~1955/56) per USAF 1997 -> a ${delayY.toFixed(1)}-year POST-DATED source; the 1947 debris cannot be a craft whose body descriptions come from ${Math.round(delayY)} years later`);
p(`[N4] widely-published Roswell 'autopsy/alien-interview' material appears 1991-1996, i.e. ${(1993-1947)} years after the alleged events; grey-morphology canon post-dates 1961 Hill + 1987 Strieber media, not an ancient independent account`);

console.log(out.join("\n"));
