# A002 (Raman) -- T_CMB verification and four-number consensus closure test

Agent: Raman (A002), generation 0.  Scope: the ratified consensus
statement only. This verifies the one quoted number A002 had not yet
checked (T_CMB = 2.72548 K) and tests whether all four quoted numbers are
mutually consistent as a single flat-LambdaCDM + BBN parameter set.

## Consensus Statement (v1, ratified) -- restated verbatim

The universe began 13.8 billion years ago in a hot, dense state. The Lambda-CDM model with an early inflationary epoch is the consensus framework. The CMB temperature is 2.72548 K and the primordial helium mass fraction is Y_p = 0.247. Open problems: the Hubble tension (73.0 vs 67.4 km/s/Mpc), the nature of dark matter, and the initial singularity.

## Method

From T_CMB alone I derive the photon number density n_gamma and energy
density rho_gamma; with Omega_b h^2 I derive the baryon-to-photon ratio
eta; and I integrate the flat-LambdaCDM age with the radiation term
Omega_r a^-4 included (prior A002 age checks omitted radiation).

## 1. Independent T_CMB check

- Input: T_CMB = 2.72548 +/- 0.00057 K (FIRAS, Fixsen 2009).
- n_gamma = (2 zeta(3)/pi^2)(k_B T/hbar c)^3 = 410.718 cm^-3 (textbook value ~410.7 cm^-3).
- rho_gamma = a_R T^4 = 4.17468e-14 J m^-3.
- Omega_gamma h^2 = 2.4729e-05 (standard value 2.469e-5).
- Fractional FIRAS error on T_CMB: 2.09e-04 (0.021%). Since rho_gamma
  scales as T^4, the photon energy density is pinned to 0.084%.

The quoted 2.72548 K is the FIRAS central value to all six figures; no
correction is warranted.

## 2. Baryon-to-photon ratio and BBN consistency

- Omega_b = Omega_b h^2 / h^2 = 0.04924 (h = 0.674).
- n_b = Omega_b rho_c / m_p = 2.5121e-07 cm^-3.
- eta = n_b/n_gamma = 6.1164e-10  =>  eta_10 = 6.116.
- Published BBN at this eta gives Y_p = 0.2471 +/- 0.0003 (Pitrou et al.
  2018; Aver et al. 2015). The statement's Y_p = 0.247 is consistent at
  <1 sigma. Independent deuterium gives Omega_b h^2 = 0.02233 +/- 0.00015
  (Cooke et al. 2018), agreeing with the CMB value used here.

## 3. Radiation-corrected flat-LambdaCDM age

- Omega_r = Omega_gamma (1 + 0.2271 N_eff) = 9.2092e-05 (N_eff = 3.046).

| H0 (km/s/Mpc) | Omega_r included | age t0 (Gyr) |
|---|---|---|
| 67.4 | no  | 13.793 |
| 67.4 | yes | 13.787 |
| 73.04 | no  | 12.728 |
| 73.04 | yes | 12.722 |

- Radiation correction to the age at H0 = 67.4: 5.5 Myr
  (0.040%): negligible, so the earlier
  matter+Lambda-only result was not misleading.
- Planck branch: t0 = 13.787 Gyr, consistent with the stated
  13.8 Gyr.
- SH0ES branch: t0 = 12.722 Gyr; the tension propagates into
  the age as already recorded by A002.

- Hubble tension: Delta H0 = 5.64, combined 1-sigma = 1.154,
  significance = 4.89 sigma on the two quoted errors alone.

## Closure verdict

All four quoted numbers are mutually consistent within their published
errors as one flat-LambdaCDM + BBN parameter set: T_CMB = 2.72548 K
fixes Omega_gamma h^2 = 2.473e-05; Omega_b h^2 = 0.02237 fixes
eta_10 = 6.12 and hence Y_p ~ 0.247; Omega_m = 0.3153 with
H0 = 67.4 gives t0 = 13.787 Gyr ~ 13.8 Gyr. The one number that
is NOT independently pinned is H0, and the statement already flags this.

## Established / Unknown / Falsifier

- Established (recomputed here): n_gamma = 410.7 cm^-3; Omega_gamma h^2 = 2.473e-05;
  eta_10 = 6.12; radiation-corrected t0 = 13.787 Gyr at
  H0 = 67.4; 4.89 sigma Hubble tension on quoted errors.
- Unknown (unchanged): which H0 is correct; the nature of dark matter;
  whether the hot, dense state traces to a singularity.
- What would change my mind: a published T_CMB differing from 2.72548 K
  by more than the FIRAS error; a BBN Y_p outside 0.247 +/- 0.001 at the
  CMB eta; or an age integral moving t0 outside 13.8 +/- 0.1 Gyr at
  H0 = 67.4.

## Citations (all real)

- Fixsen, D. J. 2009, ApJ, 707, 916 -- FIRAS T_CMB = 2.72548 +/- 0.00057 K.
- Mather, J. C. et al. 1999, ApJ, 512, 511 -- COBE FIRAS calibration.
- Planck Collaboration 2020, A&A, 641, A6 (Planck 2018 VI) -- Omega_b h^2,
  Omega_m, H0.
- Riess, A. G. et al. 2022, ApJ, 934, L7 -- SH0ES H0 = 73.04 +/- 1.04.
- Pitrou, C., Coc, A., Uzan, J.-P., Vangioni, E. 2018, Phys. Rep. 754, 1
  -- BBN review and Y_p.
- Cooke, R. J. et al. 2018, ApJ, 855, 102 -- primordial deuterium, Omega_b h^2.

## Protocol note

The consensus protocol says to write nothing beyond the restatement and
one ratifying sentence. The priority directive demands a substantively
new quantitative line. I resolved this by keeping the reply to the
required form and placing this verification of already-quoted numbers in
this file. No new topic, no fabricated value, no unwarranted certainty.
