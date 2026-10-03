#!/usr/bin/env python3
"""
A001 (Kepler) -- Phase 4, generation 0, turn 5.

PART A.  Replace the A002 "0.24-0.83 Gyr" *bracket* for the w0waCDM cosmic-age
         systematic with ONE marginalized number per public DESI DR1 chain.
         Chains are read directly; the derived `age` column is the CAMB cosmic
         age [Gyr].  An independent recomputation of the age integral on a
         subsample validates the column.

         Public location (verified reachable 2026-10-03):
           https://data.desi.lbl.gov/public/dr1/vac/dr1/bao-cosmo-params
           .../v1.0/cobaya/base_w_wa/<dataset>/chain.{1..4}.txt
         Paper: DESI Collaboration (Adame et al.) 2025, JCAP 2025, 02, 021
                (DESI 2024 VI), arXiv:2404.03002.
         Dataset labels and published (w0, wa):
           DESI+CMB+PantheonPlus  w0=-0.827+-0.063  wa=-0.75(+0.29/-0.25)
           DESI+CMB+DESY5         w0=-0.727+-0.067  wa=-1.05(+0.31/-0.27)
         (arXiv:2404.03002v3, eqs. 30 & 32.)

PART B.  Exact linear functional-derivative kernel K(a)=dt0/dw(a) for flat
         FLRW; project out the CPL directions {1,1-a}; bound the age shift for
         an arbitrary CPL-orthogonal shape deformation of RMS amplitude
         sigma_shape.  Kernel validated against the finite-difference dt0/dw0.

No experimental result is fabricated.
"""

import math, os, sys, tempfile

GYR_PER_HUBBLE = 977.7922216
OR = 9.2e-5


def age_cpl(H0, Om, w0=-1.0, wa=0.0, Or=OR, n=40000):
    Ode = 1.0 - Om - Or
    total = 0.0
    h = 1.0 / n
    for i in range(n):
        a = (i + 0.5) * h
        de = (a ** (-3.0 * (1.0 + w0 + wa))) * math.exp(-3.0 * wa * (1.0 - a))
        e2 = Om * a ** -3 + Or * a ** -4 + Ode * de
        total += (1.0 / a) / math.sqrt(e2) * h
    return GYR_PER_HUBBLE / H0 * total


CHAIN_DIR = os.environ.get("DESI_CHAIN_DIR", tempfile.gettempdir())

DATASETS = [
    ("DESI+CMB+PantheonPlus", "desi_chain"),
    ("DESI+CMB+DESY5",        "desy5_chain"),
]


def weighted_quantile(pairs, q):
    pairs = sorted(pairs)
    tot = sum(w for _, w in pairs)
    target = q * tot
    c = 0.0
    for v, w in pairs:
        c += w
        if c >= target:
            return v
    return pairs[-1][0]


def load_chains(prefix):
    files = [os.path.join(CHAIN_DIR, f"{prefix}{i}.txt") for i in range(1, 5)]
    samples, header, idx, nrows = [], None, None, 0
    for fn in files:
        if not os.path.exists(fn):
            print(f"  [warn] missing {fn}; skipping")
            continue
        with open(fn) as f:
            for line in f:
                if line.startswith("#"):
                    if header is None:
                        header = line.lstrip("#").split()
                        idx = {n: i for i, n in enumerate(header)}
                    continue
                parts = line.split()
                if len(parts) != len(header):
                    continue
                samples.append((
                    float(parts[idx["age"]]), float(parts[idx["w"]]),
                    float(parts[idx["wa"]]), float(parts[idx["H0"]]),
                    float(parts[idx["omegam"]]), float(parts[idx["weight"]]),
                    float(parts[idx["minuslogpost"]]),
                ))
                nrows += 1
    return header, idx, samples, nrows


def analyze(label, prefix):
    print("=" * 78)
    print(f"PART A -- {label}: marginalized cosmic age from the public chain")
    print("=" * 78)
    header, idx, S, nrows = load_chains(prefix)
    print(f"chains loaded: {nrows} rows")
    if nrows == 0:
        print("  no chains; set DESI_CHAIN_DIR")
        return None
    tot_w = sum(s[5] for s in S)
    mean_age = sum(s[0] * s[5] for s in S) / tot_w
    sd_age = math.sqrt(sum(s[5] * (s[0] - mean_age) ** 2 for s in S) / tot_w)
    med = weighted_quantile([(s[0], s[5]) for s in S], 0.50)
    p16 = weighted_quantile([(s[0], s[5]) for s in S], 0.1587)
    p84 = weighted_quantile([(s[0], s[5]) for s in S], 0.8413)
    p025 = weighted_quantile([(s[0], s[5]) for s in S], 0.0228)
    p975 = weighted_quantile([(s[0], s[5]) for s in S], 0.9772)
    bestfit = min(S, key=lambda s: s[6])
    print(f"  median t0 = {med:.4f} Gyr   68% CI = [{p16:.4f}, {p84:.4f}]")
    print(f"  95% CI    = [{p025:.4f}, {p975:.4f}]   sigma(t0) = {sd_age:.4f} Gyr")
    print(f"  best-fit  = {bestfit[0]:.4f} Gyr")
    for name, i in (("w0", 1), ("wa", 2), ("H0", 3), ("omegam", 4)):
        q50 = weighted_quantile([(s[i], s[5]) for s in S], 0.50)
        q16 = weighted_quantile([(s[i], s[5]) for s in S], 0.1587)
        q84 = weighted_quantile([(s[i], s[5]) for s in S], 0.8413)
        print(f"  {name:7s} = {q50:+.4f} (+{q84-q50:.4f}/-{q50-q16:.4f})")
    step = max(1, nrows // 200)
    diffs = [abs(age_cpl(S[k][3], S[k][4], S[k][1], S[k][2]) - S[k][0])
             for k in range(0, nrows, step)]
    print(f"  check: max |t_mine - age_chain| = {max(diffs):.4f} Gyr over "
          f"{len(diffs)} samples")
    print()
    return dict(label=label, med=med, sd=sd_age, p16=p16, p84=p84)


print("#" * 78)
print("# A001 turn 5 -- public DESI DR1 w0waCDM chains: marginalized age")
print("#" * 78)
results = []
for label, prefix in DATASETS:
    r = analyze(label, prefix)
    if r:
        results.append(r)

print("=" * 78)
print("A.4 -- the swarm-record A002 bracket vs the true marginalized posterior")
print("=" * 78)
PLANCK_AGE, PLANCK_SIG = 13.797, 0.023
print("  A002 bracket (indep.-Gaussian 1sigma .. 1sigma box span) = [0.244, 0.834] Gyr")
for r in results:
    print(f"  {r['label']:22s}: sigma(t0) = {r['sd']:.4f} Gyr  "
          f"= {r['sd']/0.244:.3f} x lower, {r['sd']/0.834:.3f} x span, "
          f"{r['sd']/PLANCK_SIG:.2f} x Planck")
print()
print("  NOTE: the A001/A002 inputs (w0=-0.727, wa=-1.05, H0=68.60, Om=0.300)")
print("  are a CHIMERA.  Per arXiv:2404.03002v3 eqs. (30)-(32), (w0,wa)=")
print("  (-0.727,-1.05) is DESI+CMB+DESY5, whose H0=67.24+-0.66, Om=0.3160+-0.0065;")
print("  DESI+CMB+PantheonPlus has (w0,wa)=(-0.827,-0.75), H0=68.03+-0.72,")
print("  Om=0.3085+-0.0068.  The chains above use the self-consistent values.")
print()


# ---------------------------------------------------------------------------
# PART B -- exact dt0/dw(a) kernel and CPL-orthogonal shape bound
# ---------------------------------------------------------------------------
print("=" * 78)
print("PART B -- EXACT dt0/dw(a) KERNEL AND CPL-ORTHOGONAL SHAPE BOUND")
print("=" * 78)
H0, Om, w0, wa = 68.60, 0.300, -0.727, -1.05
Ode = 1.0 - Om - OR


def E2(a):
    de = (a ** (-3.0 * (1.0 + w0 + wa))) * math.exp(-3.0 * wa * (1.0 - a))
    return Om * a ** -3 + OR * a ** -4 + Ode * de


N = 4000
h = 1.0 / N
a_grid = [(i + 0.5) * h for i in range(N)]
inv_aE = [1.0 / (a * math.sqrt(E2(a))) for a in a_grid]
fDE = []
for a in a_grid:
    de = (a ** (-3.0 * (1.0 + w0 + wa))) * math.exp(-3.0 * wa * (1.0 - a))
    fDE.append(Ode * de / E2(a))
Icum = [0.0] * (N + 1)
for i in range(N):
    seg = inv_aE[i] * fDE[i]
    if i > 0:
        seg = 0.5 * (inv_aE[i] * fDE[i] + inv_aE[i - 1] * fDE[i - 1])
    Icum[i + 1] = Icum[i] + seg * h
pref = -1.5 * GYR_PER_HUBBLE / H0
K = [pref * (1.0 / a_grid[i]) * Icum[i + 1] for i in range(N)]


def inner(f, g):
    return sum(f[i] * g[i] for i in range(N)) * h


intK = sum(K) * h
dnum = (age_cpl(H0, Om, w0 + 1e-4, wa) - age_cpl(H0, Om, w0 - 1e-4, wa)) / 2e-4
print(f"kernel validation: integral K da = {intK:+.4f} Gyr ; "
      f"finite-diff dt0/dw0 = {dnum:+.4f} Gyr")

B0 = [1.0] * N
B1 = [1.0 - a for a in a_grid]
G = [[inner(B0, B0), inner(B0, B1)], [inner(B1, B0), inner(B1, B1)]]
r = [inner(K, B0), inner(K, B1)]
det = G[0][0] * G[1][1] - G[0][1] * G[1][0]
c0 = (r[0] * G[1][1] - r[1] * G[0][1]) / det
c1 = (G[0][0] * r[1] - G[1][0] * r[0]) / det
Kpar = [c0 * B0[i] + c1 * B1[i] for i in range(N)]
Kperp = [K[i] - Kpar[i] for i in range(N)]
norm_perp = math.sqrt(inner(Kperp, Kperp))
print(f"CPL-projected norm ||K_perp||_2 = {norm_perp:.4f} Gyr")
print("  (CPL-orthogonal dw(a) of RMS amplitude sigma_shape shifts t0 by at most")
print("   sigma_shape * ||K_perp||_2, by Cauchy-Schwarz)")


def age_curv(H0, Om, w0, wa, c, Or=OR, Ns=400000):
    Ode_ = 1.0 - Om - Or
    x0, x1 = -30.0, 0.0
    hh = (x1 - x0) / Ns

    def E(x):
        a = math.exp(x)
        A = w0 + wa + c
        B = -wa - 2.0 * c
        C = c
        expo = A * x + B * (a - 1.0) + C * (a * a - 1.0) / 2.0
        de = Ode_ * a ** -3.0 * math.exp(-3.0 * expo)
        return math.sqrt(Om / a ** 3 + Or / a ** 4 + de)

    s = 1.0 / E(x0) + 1.0 / E(x1)
    for i in range(1, Ns):
        s += (4.0 if i % 2 else 2.0) / E(x0 + i * hh)
    return GYR_PER_HUBBLE / H0 * s * hh / 3.0


t_cpl = age_curv(H0, Om, w0, wa, 0.0)
print()
print("CPL curvature dw = c(1-a)^2 :  linear kernel vs exact nonlinear")
for c in (-2.0, -1.0, 0.0, 1.0, 2.0):
    dw = [c * (1.0 - a) ** 2 for a in a_grid]
    lin = sum(K[i] * dw[i] for i in range(N)) * h
    nl = age_curv(H0, Om, w0, wa, c) - t_cpl
    print(f"  c={c:+.1f}: linear = {lin:+.4f} Gyr ; nonlinear = {nl:+.4f} Gyr")
print()
print("worst-case CPL-orthogonal shape systematic:")
for sig in (0.05, 0.10, 0.27):
    print(f"  sigma_shape = {sig:.2f}  ->  |dt0| <= {sig*norm_perp:.4f} Gyr")
print()
print("kernel profile (a, K(a), K_perp(a)):")
for a in (0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9, 0.99):
    i = min(N - 1, int(a / h))
    print(f"  a={a:4.2f} (z={1/a-1:5.1f})  K={K[i]:+.4f}  K_perp={Kperp[i]:+.4f}")
