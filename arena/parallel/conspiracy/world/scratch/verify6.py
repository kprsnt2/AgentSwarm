import io, re
md = io.open('conspiracy-theories-evidence.md', encoding='utf-8').read()
out = io.open('scratch/derivation6.out', encoding='utf-8').read()

checks = [
    ('207.39 ns computed Sagnac', '207.39 ns' in out),
    ('62.17 m light travel', '62.17 m' in out),
    ('0.19% agreement vs 207 ns', 'relative agreement 0.19%' in out),
    ('145.6... 45deg 146.6 ns', '146.6 ns' in out),
    ('Michelson 0.9705', '0.9705' in out),
    ('1.40 sigma', '1.40 sigma' in out),
    ('46 standard deviations', '46 standard deviations' in out),
    ('GPS max 274.6 ns', '274.6 ns' in out),
    ('82.3 m light travel', '82.3 m' in out),
    ('ground moves 41.2 m', '41.2 m' in out),
    ('1.333 arcsec', '1.333 arcsec' in out),
    ('Alamogordo->Corona 158.7 km', '158.7 km' in out),
    ('bearing 12.6 deg', '12.6 deg' in out),
    ('drift 44.1 m/s at 1h', '44.1 m/s' in out),
    ('drift 7.3 m/s at 6h', '7.3 m/s' in out),
    ('drift 1.8 m/s at 24h', '1.8 m/s' in out),
    ('acres 12141 m2', '12141 m^2' in out),
    ('acres 142 m side', '142 m' in out),
    ('balloon volume 118.8', '118.8 m^3' in out),
    ('lift 47.8 kg at 9km', '47.8 kg' in out),
    ('lift 31.8 kg at 12km', '31.8 kg' in out),
    ('lift 19.8 kg at 15km', '19.8 kg' in out),
    ('net 40.1 kg', '40.1 kg' in out),
    ('blue book 5.56%', '5.56%' in out),
    ('beam divergence 3.48 arcsec', '3.48 arcsec' in out),
    ('diffraction 172 m', '172 m' in out),
    ('38x wider', '38x WIDER' in out),
    ('1421x', '1421x' in out),
    ('66.7 ps', '66.7 ps' in out),
    ('20.3 ns spread', '20.3 ns' in out),
    ('304x broad', '304x' in out),
    ('no leftover % placeholders', ('%' not in out.replace('%%','')) or ('%.1f' not in out)),
]
bad = [n for n, ok in checks if not ok]

# markdown-side checks
mdchecks = [
    ('md has 207.4 ns', '207.4 ns' in md),
    ('md has 274.6 ns', '274.6 ns' in md),
    ('md has 46 standard deviations', '46 standard deviations' in md),
    ('md has 158.7 km', '158.7 km' in md),
    ('md has 12,618', '12,618' in md),
    ('md has 701', '701' in md),
    ('md has 5.56%', '5.56%' in md),
    ('md has 13 classes', 'thirteen' in md),
    ('md has M114185541RC', 'M114185541RC' in md),
    ('md has 23 defects', '23 defects' in md),
    ('md has 38x wider', '38× wider' in md),
    ('md has 12.6 deg E of N', '12.6° E of N' in md),
    ('md no stale twelve classes in 2.5', 'twelve independent classes' not in md),
    ('md no stale 159 km typo', '159 km from the SW-SSW' not in md),
]
mdbad = [n for n, ok in mdchecks if not ok]

print('derivation6.out checks : %d/%d ok' % (len(checks)-len(bad), len(checks)))
for n in bad: print('   FAIL:', n)
print('markdown checks        : %d/%d ok' % (len(mdchecks)-len(mdbad), len(mdchecks)))
for n in mdbad: print('   FAIL:', n)

# structural
rows = [l for l in md.split('\n') if l.startswith('| **(')]
print('deliverable table rows : %d (expect 5)' % len(rows))
print('section order          :', [int(m) for m in re.findall(r'^## (\d+)\.', md, re.M)])
print('no orphan placeholders :', '%.1f' not in md and '%%' not in md)
print('file size              : %d chars, %d lines' % (len(md), md.count('\n')+1))
