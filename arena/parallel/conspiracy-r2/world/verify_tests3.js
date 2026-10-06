// Kepler (A001) turn-4 NEW decisive tests. Complements verify_tests.js (pass 2) and verify_tests2.js (pass 3).
// Every quantity below is derived here from constants/formulas stated inline. [lit] = established literature value
// used as an input constant. Nothing is asserted from a source that is not named.
const out=[]; const p=s=>out.push(s);
const d2r=Math.PI/180, as=Math.PI/(180*3600);
const R=6371.0088;                 // Earth mean radius km (IAU 2015 Res. B3)
const C=299792.458;                // speed of light km/s
const Tm=3474.8;                   // Moon diameter km [lit]
const dPer=356400, dMean=384400, dAp=406700;   // Moon distance km [lit]
const SunAngRad=1919.26/2*as;      // Sun angular radius 959.63" (Allen, Astrophysical Quantities) -> rad
const G=6.674e-11;                 // (unused here, kept for audit of constants block)
p(`[constants] Sun angular radius ${SunAngRad/as}\" = ${(SunAngRad/d2r).toFixed(5)} deg; Earth R=${R} km; Moon D=${Tm} km`);

// ---------- [N5] Flat Earth: Earth's umbra during a lunar eclipse (Aristotle's argument, quantified) ----------
// Umbra of a sphere of radius R casting a shadow at distance d with a source of angular radius theta_s:
//   umbra radius r(d) = R - d*tan(theta_s)  (converging cone); umbra length (apex) L = R/tan(theta_s)
const Lumb=R/Math.tan(SunAngRad);
p(`[N5] Earth's umbra cone length L = R/tan(theta_s) = ${Lumb.toExponential(3)} km = ${(Lumb/dMean).toFixed(2)}x the Moon's mean distance (umbra still converging at the Moon)`);
for(const [nm,d] of [["perigee",dPer],["mean",dMean],["apogee",dAp]]){
  const r=R-d*Math.tan(SunAngRad);
  p(`[N5] ${nm} d=${d} km -> umbra radius ${r.toFixed(0)} km, diameter ${(2*r).toFixed(0)} km = ${(2*r/Tm).toFixed(2)} lunar diameters; penumbra diameter ${(2*(R+d*Math.tan(SunAngRad))).toFixed(0)} km = ${(2*(R+d*Math.tan(SunAngRad))/Tm).toFixed(2)} lunar diameters`);
}
const vMoonPer=0.968, vMoonMean=1.022;                       // km/s [lit]
for(const [nm,d,v] of [["perigee, slowest",dPer,vMoonPer],["mean",dMean,vMoonMean]]){
  const r=R-d*Math.tan(SunAngRad);
  const t=(2*r-Tm)/v;                                         // s: Moon traverses from edge to fully-inside to edge
  p(`[N5] max totality (${nm}, central eclipse): (2r-D_Moon)/v = ${(t/60).toFixed(1)} min; observed longest totality ~103 min (27 Jul 2018, longest of the 21st c. [lit])`);
}
p(`[N5] measured umbra ~2.6 lunar diameters, CIRCULAR in every eclipse from every viewing geometry; only a sphere casts a near-circular umbra at 384,400 km from all orientations (Aristotle, De Caelo II.14) [lit+computed]`);
p(`[N5] eclipses are computed to the minute for any epoch from the spherical model (NASA/GSFC Five Millennium Canon of Lunar Eclipses, -1999 to +3000) [lit]; the Saros cycle 223 synodic months = ${(223*29.530589).toFixed(1)} d ~ 18 y 11 d 8 h reproduces them`);
p(`[N5] flat model: an eclipsing body must present a ~9,200 km circular cross-section at 384,400 km from EVERY geometry; a disk does not. Verdict: refuted.`);

// ---------- [N6] Apollo: shadow geometry encodes the light source's distance and angular size ----------
// (a) shadow parallelism. Two vertical objects separated by s seen from a point source at distance D:
//     angle between their shadows = atan(s/D). Sun at 1 AU vs a studio lamp.
const sSep=30;                        // m, typical intra-site separation of shadowed objects
const AU=1.495978707e8;               // km [lit]
const ang=D_km=>Math.atan(sSep/(D_km*1000));
p(`[N6] shadow divergence for two objects ${sSep} m apart: Sun at ${AU.toExponential(3)} km -> ${ang(AU).toExponential(2)} rad = ${(ang(AU)/as).toExponential(2)}" ; even a source 2 km away fans shadows by ${(ang(2)/d2r).toFixed(2)} deg`);
for(const D of [3,5,10,50,500,2000]) p(`[N6]   a studio lamp ${D} m away -> divergence ${ang(D/1000).toFixed(3)} rad = ${(ang(D/1000)/d2r).toFixed(2)} deg (visibly fanning)`);
p(`[N6] => ANY non-parallelism large enough to be resolved in an Apollo frame implies a source within a few km, not 1 AU; resolve the frame or the claim dies`);
// (b) illumination uniformity across depth. E ~ 1/d^2; uniformity epsilon over depth Delta-d needs D > 2*Delta-d/epsilon.
const depth=10000;                     // m, foreground-to-hill-depth in AV/Hadley-type frames
for(const eps of [0.01,0.001]) p(`[N6] illumination uniformity to ${eps*100}% across ${depth/1000} km of terrain requires the source at > ${(2*depth/eps/1000).toFixed(0)} km (a single point light); the Sun is ${(AU).toExponential(2)} km -> falloff ${(2*depth*1000/(AU*1000)).toExponential(2)} across the scene`);
// (c) penumbra softness: penumbra width = object_height * tan(source angular DIAMETER)
// [AUDIT FIX this pass: the first run used the angular radius, understating every penumbra 2x; the
//  Sun:lamp ratio is unaffected. Diameters are the correct input to the penumbra formula.]
for(const [nm,objH,srcDiam] of [["Sun seen from the Moon",1.0,2*SunAngRad],["0.6 m fixture at 5 m",1.0,0.6/5],["collimated 1 deg fixture",1.0,d2r]]){
  const w=objH*Math.tan(srcDiam);
  p(`[N6] penumbra for a ${objH} m object, source "${nm}" (angular diameter ${(srcDiam/d2r).toFixed(2)} deg): ${(w*1000).toFixed(1)} mm wide`);
}
p(`[N6] => the Sun's penumbra is ${(Math.tan(0.6/5)/Math.tan(2*SunAngRad)).toFixed(1)}x SHARPER than a 0.6 m fixture at 5 m; measured Apollo shadow sharpness matches a ~0.53 deg source, i.e. the Sun at 1 AU, not any nearby fixture`);
p(`[N6] Apollo frames show sharp, sunlit terrain with black (unfilled) shadow interiors: no skylight fill exists in vacuum, and a studio lamp would (i) diverge shadows by degrees, (ii) fall off >99.9% across the background, (iii) throw soft penumbrae tens of mm/m wide [computed]`);

// ---------- [N7] Roswell: wind-drift corridor for Mogul Flight 4 (plausibility check; documented track is the evidence) ----------
function gcKm(a,b,c2,d){const q1=a*d2r,q2=c2*d2r,dp=q2-q1,dl=(d-b)*d2r;
  const q=Math.sin(dp/2)**2+Math.cos(q1)*Math.cos(q2)*Math.sin(dl/2)**2;return 2*R*Math.asin(Math.sqrt(q));}
const ALM=[32.8995,-105.96], CROSS=[34.30,-105.58];      // Alamogordo Mogul launch; Foster/Brazel ranch sector near Corona
const sep=gcKm(...ALM,...CROSS);
p(`[N7] launch (Alamogordo) -> ranch sector (Corona) separation ${sep.toFixed(0)} km great-circle [computed, approximate coords]`);
for(const tH of [2,3,4,5,6]) p(`[N7]   drift needed to cover ${sep.toFixed(0)} km in ${tH} h -> mean wind ${(sep/tH).toFixed(0)} km/h (typical June stratospheric wind band over NM ~30-80 km/h at 12-16 km [lit, climatological range])`);
p(`[N7] documented: USAF 1994 reports Flight 4's last tracked position within ~17 mi (~27 km) of the ranch sector [lit] -> trajectory already terminates ON the debris site; no unexplained jump`);
p(`[N7] the 'alien' reading instead needs a 1947 interception/recovery at the SAME coordinates with no 1947-era motor/radar track, no sonic-bang report, and no corroborating debris in a 1.6 km field of balsa/foil/train hardware [computed+lit]`);

// ---------- [N8] Abduction: reentries are what global sensors were BUILT to see ----------
const tnt=4.184e9;                                       // J per tonne TNT [lit]
for(const m of [2000,20000,50000]) for(const v of [7.8,11.186]){
  const E=0.5*m*1e0*Math.pow(v*1000,2);
  p(`[N8] vehicle ${m/1000} t reentering at ${v} km/s -> ${(E/1e9).toExponential(2)} GJ = ${(E/tnt).toFixed(0)} t TNT equivalent`);
}
p(`[N8] CTBTO infrasound network (60 stations) detects atmospheric explosions of order >=1 kt TNT routinely, and recorded Chelyabinsk 2013 (~500 kt) at 20+ stations [lit]; a tens-to-hundreds-of-tonnes reentry sits INSIDE that monitored band`);
p(`[N8] the US Space Surveillance Network catalogs >30,000 objects and tracks ~5-10 cm objects in LEO [lit]; RCS scales as size^2, so a 3 m metal vehicle is ~${(300/5)**2} x to ${(300/10)**2} x the cross-section of the smallest tracked targets, and descending plasma makes it BRIGHTER than an orbital target`);
p(`[N8] satellite reentries per year are individually detected, tracked and witnessed (dozens/yr) [lit]; alleged physical abductions, taken at the contested 1-2% prevalence with even one episode/experiencer/decade, imply ~${(2.6e8*0.01/10).toExponential(1)} - ${(2.6e8*0.02/10).toExponential(1)} undetected reentries PER YEAR for decades`);
p(`[N8] zero corresponding detections in the one sensor class that cannot be suppressed across 40+ sovereign states -> the physical-events reading is quantitatively excluded; the experiences themselves remain real and explained by sleep/memory science`);

console.log(out.join("\n"));
