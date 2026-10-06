# -*- coding: utf-8 -*-
import io, sys
p = 'conspiracy-theories-evidence.md'
s = io.open(p, encoding='utf-8').read()

subs = [
 ("(9) **Annual stellar parallax and stellar aberration (\u00a714):** on a stationary plane with the stars on a dome at 1,000\u201310,000 mi, *every* star must show an annual parallax of 1.9 \u00d7 10\u2079\u20131.9 \u00d7 10\u00b9\u2070 arcsec and zero aberration; measured, the nearest star shows 0.77\u2033 and stars show ~20\u2033 of annual aberration from Earth's 29.78 km/s orbital motion. The exclusion is 8\u201310 orders of magnitude and is independent of every flat-model parameter.",
  "(9) **Annual stellar parallax and stellar aberration (\u00a714):** on a stationary plane with the stars on a dome at 1,000\u201310,000 mi, *every* star must show an annual parallax of 1.9 \u00d7 10\u2079\u20131.9 \u00d7 10\u00b9\u2070 arcsec and zero aberration; measured, the nearest star shows 0.768\u2033 (Gaia DR3) and stars show ~20\u2033 of annual aberration from Earth's 29.78 km/s orbital motion. The exclusion is ~9\u201310.4 orders of magnitude and is independent of every flat-model parameter."),
 ("a setting Sun 4\u00d7 too small, an annual stellar parallax of ~10\u2079\u201310\u00b9\u2070 arcsec against the measured 0.77\u2033",
  "a setting Sun 4.26\u00d7 too small, an annual stellar parallax of ~10\u2079\u201310\u00b9\u2070 arcsec against the measured 0.768\u2033"),
 ("(annual parallax 0.77\u2033; annual aberration ~20\u2033)", "(annual parallax 0.768\u2033; annual aberration ~20\u2033)"),
 ("both excluding the stationary-plane and nearby-dome claims by 8\u201310 orders of magnitude",
  "both excluding the stationary-plane and nearby-dome claims by ~9\u201310.4 orders of magnitude"),
 ("so loose regolith is about 300\u00d7 less conductive than solid rock, which is what a granular powder with point contacts should be.",
  "so loose regolith is two to three orders of magnitude less conductive than solid rock (the precise ratio, now verified in \u00a714.5, is 140\u00d7\u2013460\u00d7 \u2014 an earlier draft said \"about 300\u00d7\", which is fair for granite alone but not across the measured igneous range), which is what a granular powder with point contacts should be."),
 ("a global lunar heat output of **6.4 \u00d7 10\u00b9\u00b9 W (645 GW)**", "a global lunar heat output of **6.4 \u00d7 10\u00b9\u00b9 W (640 GW)**"),
 ("global lunar heat output 645 GW", "global lunar heat output 640 GW"),
 ("(\u00a710.0 item 1, \u00a713.2a); see source 36.", "(\u00a710.0 item 1, \u00a713.2(a))."),
 ("Cost: a few hundred dollars, or an astronomy textbook.",
  "Cost: the textbook is free and the measurement is a two-century-old published result; a *new* sub-arcsecond astrometric confirmation would need an observatory, but none is needed to check the published value."),
]

for a, b in subs:
    n = s.count(a)
    sys.stdout.write("%2d x  %s\n" % (n, a[:76].replace('\n', ' ')))
    s = s.replace(a, b)

io.open(p, 'w', encoding='utf-8', newline='').write(s)
sys.stdout.write("written\n")
