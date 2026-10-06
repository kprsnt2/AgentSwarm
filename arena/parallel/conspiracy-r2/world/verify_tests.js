// Kepler (A001) verification pass: re-derive every quantitative claim in
// conspiracy-theories-evidence.md from first principles, plus new decisive tests.
const out=[]; const p=s=>out.push(s);
const R=6371.0088, toRad=d=>d*Math.PI/180, C=299792.458; // R km (IAU 2015 Res. B3), c km/s

// [1] Eratosthenes: solstice-noon zenith angles
const obl=23.4368, syene=24.0889, alex=31.2001;
const zS=Math.abs(syene-obl), zA=Math.abs(alex-obl);
p(`[1] Eratosthenes z(Syene)=${zS.toFixed(2)}deg z(Alex)=${zA.toFixed(2)}deg delta=${(zA-zS).toFixed(2)}deg = 1/${(360/(zA-zS)).toFixed(1)} of circle`);
p(`    250000 stadia @157.5m -> ${(250000*0.1575).toFixed(0)} km (${((250000*0.1575-40075)/40075*100).toFixed(1)}%); @209m -> ${(250000*0.209).toFixed(0)} km (${((250000*0.209-40075)/40075*100).toFixed(1)}%)`);

// [2] geometric horizon and hull-down ship
const hor=h=>Math.sqrt(2*R*1000*h)/1000; // km, height h in metres
p(`[2] horizon eye 3m=${hor(3).toFixed(2)}km; mast 30m=${hor(30).toFixed(2)}km; sum=${(hor(3)+hor(30)).toFixed(2)}km; x1.072 refraction=${((hor(3)+hor(30))*1.072).toFixed(2)}km`);

// [3] Foucault precession
const f=n=>23.9345/Math.sin(toRad(n)); // hours (sidereal day)
p(`[3] Foucault Paris=${f(48.8566).toFixed(2)}h Sydney=${f(-33.8688).toFixed(2)}h pole=${f(90).toFixed(2)}h`);

// [4] WGS84 normal gravity, Somigliana-Pizzetti closed form
const a_=6378137, b_=6356752.3142, ge=9.7803253359, gp=9.8321849378;
const g=phi=>{const c2=Math.cos(toRad(phi))**2, s2=Math.sin(toRad(phi))**2;
  return (a_*ge*c2 + b_*gp*s2)/Math.sqrt(a_*a_*c2 + b_*b_*s2);};
p(`[4] Somigliana: g(0)=${g(0).toFixed(4)} g(45)=${g(45).toFixed(4)} (lit. 9.8062) g(90)=${g(90).toFixed(4)} equator-to-pole=+${((g(90)-g(0))/g(0)*100).toFixed(2)}%`);

// [5] great-circle vs flat-map (azimuthal-equidistant, N-pole centred, Euclidean in the projected plane)
function gcKm(a,b,c,d){const p1=toRad(a),p2=toRad(c),dp=toRad(c-a),dl=toRad(d-b);
  const q=Math.sin(dp/2)**2+Math.cos(p1)*Math.cos(p2)*Math.sin(dl/2)**2;return 2*R*Math.asin(Math.sqrt(q));}
function flatKm(a,b,c,d){const rho=l=>R*toRad(90-l);
  return Math.hypot(rho(c)*Math.sin(toRad(d))-rho(a)*Math.sin(toRad(b)), rho(c)*Math.cos(toRad(d))-rho(a)*Math.cos(toRad(b)));}
const cities={JNB:[-26.1337,28.2420],PER:[-31.9405,115.9667],SYD:[-33.8688,151.2093],
  SCL:[-33.4489,-70.6693],CPT:[-33.9715,18.6041],PSY:[-51.6968,-57.8517]};
for(const [k,w] of [['JNB','PER'],['SYD','JNB'],['SYD','SCL'],['CPT','PSY']]){
  const [a1,o1]=cities[k],[a2,o2]=cities[w],gc=gcKm(a1,o1,a2,o2),fl=flatKm(a1,o1,a2,o2);
  const t=12.33, Mach1=1062/3600*3600; // 12h20m block; speed of sound at cruise altitude ~1062 km/h
  p(`[5] ${k}-${w}: gc=${gc.toFixed(0)}km flat=${fl.toFixed(0)}km ratio=${(fl/gc).toFixed(2)}x | 12h20m block: sphere=${(gc/t).toFixed(0)}km/h (M${((gc/t)/1062).toFixed(2)}) flat=${(fl/t).toFixed(0)}km/h (M${((fl/t)/1062).toFixed(2)})`);}

// [6] lunar laser ranging round trips
for(const d of [356400,370000,384400,406700]) p(`[6] LLR d=${d}km -> round trip ${(2*d/C).toFixed(3)}s`);

// [7] diffraction limit: ground telescopes cannot resolve Apollo hardware
const needD=(s,dist)=>1.22*550e-9/(s/(dist*1000)); // metres for object of size s m at dist km
p(`[7] 1 arcsec at Moon=${(toRad(1/3600)*384400*1000/1000).toFixed(0)}km; D(10m lander)=${needD(10,384400).toFixed(1)}m; D(4m stage)=${needD(4,384400).toFixed(1)}m; D(3m tracks)=${needD(3,384400).toFixed(1)}m`);

// [8] South-polar continuous daylight: declination < +0.83 deg (refraction + semidiameter)
const delta=n=>-23.4368*Math.sin(2*Math.PI*(n-172)/365);
let n0=null,n1=null; for(let n=0;n<366;n++){ if(delta(n)<0.83){ if(n0===null)n0=n; n1=n; } }
p(`[8] S-polar day: declination<+0.83deg from day ${n0} to day ${n1} = ${n1-n0+1} consecutive days of Sun above horizon`);

// [9] "no stars in Apollo photographs": photometric exposure ratio
const Elon=1.361e3*93;      // solar illuminance at the Moon, lux (1361 W/m2 x 93 lm/W)
const rho=0.12;             // lunar regolith reflectance
const Lscene=rho*Elon/Math.PI; // Lambertian sunlit-regolith luminance
const Estar0=2.54e-6;       // illuminance from a magnitude-0 star, lux
const ratio=Lscene/Estar0;
p(`[9] sunlit regolith luminance=${Lscene.toFixed(0)} lux vs m=0 star ${Estar0} lux -> ratio ${ratio.toExponential(2)} = ${Math.log2(ratio).toFixed(1)} stops`);
p(`    exposure needed for stars at surface setting t=1/250s, f/11: ${(ratio/250).toExponential(2)} s = ${(ratio/250/86400).toFixed(0)} days (film latitude ~14-17 stops)`);

// [10] LM footpad bearing pressure vs near-surface regolith strength
const mLM=15000, gm=1.625, W=mLM*gm;
p(`[10] LM ${mLM}kg on Moon -> weight ${(W/1000).toFixed(1)}kN; bearing pressure on 4 footpads of 0.5-1.5 m^2 = ${(W/(4*1.5)/1000).toFixed(1)}-${(W/(4*0.5)/1000).toFixed(1)} kPa`);

// [11] nearby-sun flat model: solar angular diameter must vary by a large factor over the day
const thZen=2*Math.atan(23.15/5000)*180/Math.PI;      // H=5000 km, r=23.15 km chosen to give 0.53 deg at zenith
const thSet=2*Math.atan(23.15/15000)*180/Math.PI;     // at sunset geometry, slant distance ~15,000 km
p(`[11] flat H=5000km sun: zenith=${thZen.toFixed(2)}deg, sunset=${thSet.toFixed(3)}deg -> factor ${(thZen/thSet).toFixed(1)}x variation; observed solar diameter 0.526-0.545 deg (31.6-32.7 arcmin) all day, worldwide`);

console.log(out.join("\n"));
