#!/usr/bin/env python3
"""Show an excerpt of an existing run log; this does not repeat its commands."""
import math
import re
import shutil
import sys
import unicodedata
from pathlib import Path

source = Path(sys.argv[1])
raw = source.read_text(errors='replace')
text = re.sub(r'\x1b\[[0-9;]*[A-Za-z]', '', raw)
lines = [line for line in text.splitlines()
         if not re.match(r'^\S+:\S+ \$\s*$', line)]
while lines and not lines[-1].strip():
    lines.pop()
columns = shutil.get_terminal_size((120, 33)).columns
selected = []
rows = 0
for line in reversed(lines):
    width = sum(0 if unicodedata.combining(c) else
                2 if unicodedata.east_asian_width(c) in 'WF' else 1
                for c in line)
    needed = max(1, math.ceil(width / columns))
    if selected and rows + needed > 22:
        break
    selected.append(line)
    rows += needed
print('\n'.join(reversed(selected)))
when = re.search(r'(?:UTC|Captured):\s*(\d{4}-\d\d-\d\d[^\n]*)', text)
print('\nRecorded log view: ' + source.name)
print('Original UTC: ' + when.group(1) if when else 'Original transcript retained; commands are not re-run by this viewer.')
