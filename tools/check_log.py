#!/usr/bin/env python3
"""Fail on what `grep '^!'` cannot see: -file-line-error errors, unresolved
references, and overfull boxes over the budget. Stdlib only."""
import re
import sys

BUDGET_PT = 15.0
s = open(sys.argv[1], encoding="utf-8", errors="replace").read()
bad = []
for m in re.finditer(r"^(?:\./)?[^\s:]+\.tex:\d+: (.*)$|^! (.*)$", s, re.M):
    bad.append(("error", m.group(0)))
for m in re.finditer(r"(Reference|Citation) `[^']+' on page \d+ undefined", s):
    bad.append(("unresolved", m.group(0)))
if re.search(r"Label\(s\) may have changed|Rerun to get", s.split("Output written")[-1] if "Output written" in s else s):
    bad.append(("rerun", "labels still changing after the last pass"))
over_h = [float(x) for x in re.findall(r"Overfull \\hbox \(([\d.]+)pt too wide", s)]
over_v = re.findall(r"Overfull \\vbox \(([\d.]+)pt too high", s)
for x in over_h:
    if x > BUDGET_PT:
        bad.append(("overfull-hbox", f"{x}pt > {BUDGET_PT}pt budget"))
for x in over_v:
    bad.append(("overfull-vbox", f"{x}pt (a table or box that cannot break grew past a page)"))
pages = re.search(r"Output written on .*? \((\d+) pages", s)
print(f"pages={pages.group(1) if pages else '?'} overfull_hbox={len(over_h)} (worst {max(over_h, default=0)}pt) overfull_vbox={len(over_v)}")
if bad:
    for k, m in bad[:12]:
        print(f"FAIL {k}: {m}")
    if len(bad) > 12:
        print(f"... and {len(bad) - 12} more (read the first one: the rest cascade)")
    sys.exit(1)
