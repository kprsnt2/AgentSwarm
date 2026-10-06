import io
p = 'conspiracy-theories-evidence.md'
s = io.open(p, encoding='utf-8').read()

marker16 = '## 16. Sixth pass'
marker17 = '## 17. State of the investigation'
i16 = s.index(marker16)
i17 = s.index(marker17)
assert i17 < i16, "expected 17 before 16"

old_note = ("**Note on sourcing.** Where a figure could not be verified against a primary "
            "source during this session (e.g. the June 1947 upper-air wind field in \u00a716.3, "
            "and any APOLLO station specification in \u00a716.2), it is not asserted; the figure is "
            "either assumed and labelled (A) or the item is left explicitly open. No page numbers, "
            "DOIs or exact quotations beyond those in the retrieved texts are invented.")
new_note = old_note.replace('**Note on sourcing.**', '**Note on sourcing (sixth pass).**', 1)
assert old_note in s, "sourcing note not found"
s = s.replace(old_note, new_note, 1)

i16 = s.index(marker16)
i17 = s.index(marker17)
block17 = s[i17:i16]
block16 = s[i16:]
assert block16.rstrip().endswith('re-derivation.'), block16[-120:]

new = s[:i17] + block16 + '\n---\n\n' + block17.rstrip() + '\n'
io.open(p, 'w', encoding='utf-8', newline='').write(new)
print('reordered ok; chars', len(new))
