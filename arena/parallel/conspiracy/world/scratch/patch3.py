import io
p = 'derivation3.py'
s = io.open(p, encoding='utf-8').read()

NL = chr(92) + 'n'          # the two-character sequence \n as it appears in source

OLD2 = 'print("' + NL + '  HONEST READING OF THIS TABLE -- the argument is not uniformly strong:")'
assert OLD2 in s, "anchor 2 not found"
NEW2 = ('print("' + NL + '  HONEST READING -- the concession is CONDITIONAL ON p, not categorical.")\n'
        'print("  (An earlier draft said the argument \'carries only via the survey")\n'
        'print("   figures\'; the n=1,700 row of this very table refutes that.)")')
s = s.replace(OLD2, NEW2, 1)

OLD3 = ('print("   * For n = 1,700 documented claimants and p = 1e-3, P(no record) = 18%.")\n'
        'print("     The silence is NOT surprising for the documented claimant count.")\n'
        'print("     This is the weakest form of the argument and must be conceded.")\n'
        'print("   * For n = 1,700 and p = 1e-2, P(no record) = 4e-8.")\n'
        'print("   * For any survey-implied n (>= ~1e7) and any p >= 1e-4, P < 1e-400.")\n'
        'print("  So the strength of the silence argument is entirely a function of which")\n'
        'print("  n is accepted.  The documented n does not carry it; the survey n does.")\n'
        'print("  The surveys are described by the source itself as \'contested\', so this")\n'
        'print("  step is reported as an assumption, not a result.")')
assert OLD3 in s, "anchor 3 not found"
NEW3 = ('print("   * n = 1,700 documented claimants, p = 1e-3: P(no record) = 18% -- the")\n'
        'print("     silence is NOT surprising.  That is the weak case and it is conceded.")\n'
        'print("   * n = 1,700, p = 1e-2: P(no record) = 4e-8 -- the silence IS surprising")\n'
        'print("     on the documented count ALONE.")\n'
        'print("   * Any survey-implied n (>= ~3e6) at any tabulated p >= 1e-6: P < 1e-7.")\n'
        'print("  So the argument needs only the premise that a physical abduction has at")\n'
        'print("  least a ~1-in-100 chance of leaving a verifiable record.  The contested")\n'
        'print("  5-6% surveys strengthen it; they are not load-bearing for it.  The")\n'
        'print("  genuinely uncertain quantity is p itself -- a judgement about how")\n'
        'print("  recordable a physical event is, not a measurement.")')
s = s.replace(OLD3, NEW3, 1)

OLD4 = 'print(f"' + NL + '  TIMING.  Precision requires a sharp return.  For the measured")'
assert OLD4 in s, "anchor 4 not found"
NEW4 = ('print(f"' + NL + '  TIMING.  CAVEAT: a pulse width does not by itself bound timing")\n'
        'print(f"  precision -- a clean symmetric pulse can be centroided well below its")\n'
        'print(f"  own width given enough photons -- so the WIDTH below is a SUPPORTING")\n'
        'print(f"  argument.  What makes the exclusion HARD is the photon deficit above.")')
s = s.replace(OLD4, NEW4, 1)

OLD5_UNUSED = 'print("  least 304x too broad to yield the")'
pass

pass

io.open(p, 'w', encoding='utf-8').write(s)
print("all patches applied")
