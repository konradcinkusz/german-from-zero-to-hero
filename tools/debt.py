#!/usr/bin/env python3
"""Print the outstanding-work ledgers from generated/values.tex. Never fatal:
these are reported, not gated, and must not quietly go away."""
import re
from pathlib import Path

v = dict(re.findall(r"gval@([A-Za-z0-9.]+)\}\{(\d+)\}", (Path(__file__).resolve().parent.parent / "generated/values.tex").read_text()))
g = lambda k: int(v.get(k, 0))
print(f"units written: {g('written.total')} of {g('units.total')}")
print(f"vocabulary: {g('vocab.total')} entries  (A1 {g('vocab.A1')} / A2 {g('vocab.A2')} / B1 {g('vocab.B1')} / B2 {g('vocab.B2')})")
print(f"exercise items: {g('exercises.total')}  dialogs: {g('dialogs.total')}  can-do goals: {g('candos.total')}")
print(f"facts flagged \\verify{{}} (need a primary source or a native speaker): {g('verify.total')}")
print("native-speaker review: NOT ESTABLISHED  (reported on every build; see CLAUDE.md)")
