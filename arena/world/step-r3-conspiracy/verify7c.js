// ===== turn 7: great-circle routes, implied ground speeds, flat-map contrast =====
const D2R = Math.PI / 180;
const a = 6378.137, b = 6356.7523, R = (2 * a + b) / 3;
const gc = (p, q) => {
  const [f1, l1] = p.map(v => v * D2R), [f2, l2] = q.map(v => v * D2R);
  const h = Math.sin((f2 - f1) / 2) ** 2 + Math.cos(f1) * Math.cos(f2) * Math.sin((l2 - l1) / 2) ** 2;
  return 2 * R * Math.asin(Math.sqrt(h));
};
const AZ = (f, l) => { // azimuthal-equidistant (flat-Earth "AE") centred on the N pole, km
  const r = (90 - f) * D2R * R, t = l * D2R;
  return [r * Math.cos(t), r * Math.sin(t)];
};
const eu = (u, v) => Math.hypot(u[0] - v[0], u[1] - v[1]);

const SYD = [-33.9467, 151.1819], SCL = [-33.3926, -70.7858];
const PER = [-31.9403, 115.9667], LHR = [51.4706, -0.4543];
const AKL = [-37.0081, 174.7850], DOH = [25.2732, 51.6089];
const SYD2 = [-33.8688, 151.2093], LHR2 = [51.5074, -0.1278];
const SIN = [1.3644, 103.9915], LAX = [33.9416, -118.4085], DFW = [32.8998, -97.0403], GRU = [-23.4356, -46.4731];

console.log('route            GC(km)     flown(t)   implied speed (km/h)');
const legs = [
  ['SYD-SCL', SYD, SCL, gc(SYD, SCL), [12.8, 14.0]],
  ['PER-LHR', PER, LHR, gc(PER, LHR), [17.5, 17.8]],
  ['AKL-DOH', AKL, DOH, gc(AKL, DOH), [17.0, 17.0]],
  ['LHR-SYD', LHR2, SYD2, gc(LHR2, SYD2), [22.8, 22.8]],
];
for (const [n, p, q, d, t] of legs)
  console.log(`  ${n.padEnd(12)} ${d.toFixed(0).padStart(8)}   ${t.join('-').padStart(7)} h   ${(d / t[1]).toFixed(0)}-${(d / t[0]).toFixed(0)}`);

console.log('\nSYD-SCL via a northern hub (the only route family available on a north-centred AE map):');
for (const [n, hub] of [['SIN', SIN], ['LAX', LAX], ['DFW', DFW], ['GRU', GRU]]) {
  const d1 = gc(SYD, hub), d2 = gc(hub, SCL);
  console.log(`  via ${n}: ${d1.toFixed(0)} + ${d2.toFixed(0)} = ${(d1 + d2).toFixed(0)} km  (AE-map chords: ${eu(AZ(...SYD), AZ(...hub)).toFixed(0)} + ${eu(AZ(...hub), AZ(...SCL)).toFixed(0)} = ${(eu(AZ(...SYD), AZ(...hub)) + eu(AZ(...hub), AZ(...SCL))).toFixed(0)} km)`);
}
const d2s = eu(AZ(...SYD), AZ(...SCL));
console.log(`  direct SYD-SCL: GC ${gc(SYD, SCL).toFixed(0)} km, AE-map chord ${d2s.toFixed(0)} km`);
console.log(`  => the cheapest northern-hub GC detour (via SIN, ${(gc(SYD, SIN) + gc(SIN, SCL)).toFixed(0)} km) is ${(1 + (gc(SYD, SIN) + gc(SIN, SCL)) / gc(SYD, SCL)).toFixed(2)}x the observed non-stop distance.`);
console.log(`  => observed non-stop SYD-SCL time 12.8-14.0 h; a SIN-hub detour would need ${((gc(SYD, SIN) + gc(SIN, SCL)) / 846).toFixed(1)} h at the same 846 km/h.`);
