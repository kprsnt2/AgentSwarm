import io
p = 'conspiracy-theories-evidence.md'
s = io.open(p, encoding='utf-8').read()

reps = []

# FIX 5: the 5.5 patch inherited the overstatement
reps.append((
 """The result, and its limits, are these: if the number of physical abductions is only the ~1,700 documented claimants, the silence is *not* surprising for per-event recording probabilities below ~2\u00d710\u207b\u00b3, and the detection-rate argument is weak; if the contested 5\u20136% survey figures are right, the silence requires every single event to have had less than a 1-in-135-million chance of leaving any record, which is not a credible property of craft traversing the atmosphere. The argument therefore stands on the survey figure, and that figure is labelled "contested" by its own sources. **This is the honest limit of the quantitative case, and it is stated rather than hidden.**""",
 """The result, and its limits, are these. With only the ~1,700 documented claimants, the silence is *not* surprising if each event had less than a ~1-in-500 chance of leaving any record (p \u2272 2 \u00d7 10\u207b\u00b3), but is surprising to P \u2248 4 \u00d7 10\u207b\u2078 if p \u2273 10\u207b\u00b2. With the contested 5\u20136% survey figures, the silence requires every event to have had less than a 1-in-135-million chance of leaving a record \u2014 not a credible property of craft traversing the atmosphere. So the argument does not stand or fall on the survey figure: it stands on the claim that a physical abduction has at least a ~1-in-100 chance of leaving a verifiable trace, and that claim is a judgement, not a measurement. **This is the honest limit of the quantitative case, and it is stated rather than hidden.**"""))

# FIX 6: the section-11 table row inherits it
reps.append((
 "| (d) Alien abduction | **N/E** | **>95%** not literal; **>99%** not physically corroborated | the \u201cexpected detection rate\u201d admission is closed by an explicit computation (\u00a710.3), together with the exact conditions under which that argument is weak and must be conceded; a new controlled emulation result (\u00a710.4); sleep-paralysis supply quantified in absolute episodes per year (\u00a710.2) |",
 "| (d) Alien abduction | **N/E** | **>95%** not literal; **>99%** not physically corroborated | the \u201cexpected detection rate\u201d admission is closed by an explicit computation (\u00a710.3), together with the exact conditions under which that argument is weak and must be conceded (it is weak only for p \u2272 10\u207b\u00b3); a new controlled emulation result (\u00a710.4); sleep-paralysis supply quantified in absolute episodes per year (\u00a710.2) |"))

# FIX 7: note the QE scan range in 10.1
reps.append((
 "**Assumed parameters (A)**, each scanned: ruby wavelength 694.3 nm; 3.8 cm corner-cube aperture \u00d7 100 cubes = 0.1134 m\u00b2 projected aperture = **54% of the 46 \u00d7 46 cm panel**; detector quantum efficiency 0.05\u20130.10.",
 "**Assumed parameters (A)**, each scanned: ruby wavelength 694.3 nm; 3.8 cm corner-cube aperture \u00d7 100 cubes = 0.1134 m\u00b2 projected aperture = **54% of the 46 \u00d7 46 cm panel**; detector quantum efficiency 0.05\u20130.10 for a 694.3 nm photomultiplier. (The inversion table also prints QE = 0.03 and 0.15 as arithmetic bounds; 0.15 is unrealistically high for that wavelength and is shown only to bracket the result, not as an estimate \u2014 the conclusion \u201810\u00b2\u201310\u00b3 cm\u00b2, a corner-cube-scale panel\u2019 holds inside the physical band.)"))

for i, (o, n) in enumerate(reps, 1):
    if o in s:
        s = s.replace(o, n, 1)
        print("OK   FIX", i)
    else:
        print("MISS FIX", i, repr(o[:70]))

io.open(p, 'w', encoding='utf-8').write(s)
print("lines:", s.count("\n") + 1)
