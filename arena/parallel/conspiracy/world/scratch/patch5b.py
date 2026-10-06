# -*- coding: utf-8 -*-
"""Renumber the tail of the sources list as one continuous sequence.
The fifth-pass geodesy entries are 19-23; everything after them is renumbered
24 onward, in order, so no key is defined twice."""
import io, re, sys

p = 'conspiracy-theories-evidence.md'
lines = io.open(p, encoding='utf-8').read().split('\n')

start = None
for i, l in enumerate(lines):
    if l.startswith('**Historical / documentary sources'):
        start = i + 1          # first numbered item is the next line
        break
assert start is not None, 'historical block head not found'

end = None
for i in range(start, len(lines)):
    if lines[i].startswith('### 7a. Sources added in the fourth pass'):
        # items run until the next '---' or blank-blank followed by a non-item
        end = i
        break
assert end is not None

# collect item lines between start and end
item_idx = [i for i in range(start, end) if re.match(r'^\d+\. ', lines[i])]
sys.stdout.write('renumbering %d items from line %d\n' % (len(item_idx), start + 1))

n = 24
for i in item_idx:
    lines[i] = re.sub(r'^\d+\. ', '%d. ' % n, lines[i], count=1)
    n += 1

io.open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
sys.stdout.write('last number used: %d\n' % (n - 1))
