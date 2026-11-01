#!/usr/bin/env python3
"""Source gates for the book. Reads the .tex sources; needs no PDF.

  1. units.tsv and units/ agree, and each unit opens with its own number.
  2. every unit carries the required teaching elements.
  3. every exercise item has a non-empty answer.
  4. every \\val{key} resolves in generated/values.tex.
  5. environments and braces balance in every source file.
  6. no TODO / FIXME / placeholder text ships.

Run before building: these gates read the source and cost seconds, where a
build costs minutes.  Stdlib only.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errs = []


def err(msg):
    errs.append(msg)


def strip_comments(s):
    return re.sub(r"(?<!\\)%.*", "", s)


def balanced_args(s, start):
    """Return (text, end) of the {...} group starting at s[start]=='{'."""
    depth, i = 0, start
    while i < len(s):
        c = s[i]
        if c == "\\":
            i += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return s[start + 1:i], i + 1
        i += 1
    return None, len(s)


rows = [ln.split("\t") for ln in (ROOT / "data/units.tsv").read_text(encoding="utf-8").splitlines()[1:] if ln.strip()]
expected = {f"u{int(r[0]):02d}-{r[2]}.tex": int(r[0]) for r in rows}
present = {p.name for p in (ROOT / "units").glob("u*.tex")}
PARTIAL = "--partial" in sys.argv  # authoring aid only: CI never passes it
for name in sorted(expected.keys() - present):
    if PARTIAL:
        continue
    err(f"units/{name} is listed in data/units.tsv but does not exist")
for name in sorted(present - expected.keys()):
    err(f"units/{name} exists but is not listed in data/units.tsv")

REQUIRED = [
    (r"\\begin\{candos\}", "a \\begin{candos} block (can-do goals)"),
    (r"\\vocabtable\{\d\d\}", "\\vocabtable{NN}"),
    (r"\\begin\{dialog\}", "at least one dialog"),
    (r"\\begin\{cwiczenia\}", "an exercise block"),
    (r"\\drill\{\d\d\}", "\\drill{NN} (generated vocabulary drill)"),
    (r"\\weekend\{", "a \\weekend{...} production task"),
    (r"\\begin\{falle\}", "a trap box for Polish speakers (falle)"),
]

values = (ROOT / "generated/values.tex").read_text(encoding="utf-8") if (ROOT / "generated/values.tex").exists() else ""
keys = set(re.findall(r"gval@([A-Za-z0-9.]+)\}", values))

sources = sorted(ROOT.glob("units/*.tex")) + sorted(ROOT.glob("frontmatter/*.tex")) + \
    sorted(ROOT.glob("appendices/*.tex")) + [ROOT / "main.tex", ROOT / "preamble.tex"]

for p in sources:
    if not p.exists():
        err(f"{p.relative_to(ROOT)} missing")
        continue
    rel = p.relative_to(ROOT)
    s = strip_comments(p.read_text(encoding="utf-8"))

    # 5. balance
    begins = re.findall(r"\\begin\{([A-Za-z*]+)\}", s)
    ends = re.findall(r"\\end\{([A-Za-z*]+)\}", s)
    for env in set(begins) | set(ends):
        if begins.count(env) != ends.count(env):
            err(f"{rel}: \\begin{{{env}}} x{begins.count(env)} vs \\end x{ends.count(env)}")
    depth = 0
    i = 0
    while i < len(s):
        c = s[i]
        if c == "\\":
            i += 2
            continue
        depth += (c == "{") - (c == "}")
        if depth < 0:
            err(f"{rel}: unmatched closing brace")
            break
        i += 1
    if depth > 0:
        err(f"{rel}: {depth} unclosed brace(s)")

    # 6. placeholders
    for m in re.finditer(r"\b(TODO|FIXME|XXX|TBD|lorem ipsum)\b", p.read_text(encoding="utf-8"), re.I):
        err(f"{rel}: placeholder text {m.group(0)!r}")

    # 4. values
    for k in re.findall(r"\\val\{([^}]+)\}", s):
        if k not in keys:
            err(f"{rel}: \\val{{{k}}} has no definition in generated/values.tex")

    if p.parent.name == "units" and p.name in expected:
        nn = f"{expected[p.name]:02d}"
        opens = re.findall(r"\\unitopen\{(\d\d)\}", s)
        if opens != [nn]:
            err(f"{rel}: must contain exactly one \\unitopen{{{nn}}}, found {opens}")
        dr = re.findall(r"\\drill\{(\d\d)\}", s)
        if dr != [nn]:
            err(f"{rel}: \\drill must name this unit ({nn}), found {dr}")
        vt = re.findall(r"\\vocabtable\{(\d\d)\}", s)
        if vt != [nn]:
            err(f"{rel}: \\vocabtable must name this unit ({nn}), found {vt}")
        for pat, what in REQUIRED:
            if not re.search(pat, s):
                err(f"{rel}: missing {what}")
        n_ex = 0
        for m in re.finditer(r"\\exitem\{", s):
            q, end = balanced_args(s, m.end() - 1)
            if q is None or not q.strip():
                err(f"{rel}: \\exitem with an empty or unbalanced question")
                continue
            if end >= len(s) or s[end] != "{":
                err(f"{rel}: \\exitem lacks an answer argument near {q[:40]!r}")
                continue
            a, _ = balanced_args(s, end)
            if a is None or not a.strip():
                err(f"{rel}: \\exitem with an empty answer near {q[:40]!r}")
            n_ex += 1
        if n_ex < 8:
            err(f"{rel}: only {n_ex} exercise items (minimum 8)")
        cando = "".join(re.findall(r"\\begin\{candos\}.*?\\end\{candos\}", s, re.S))
        if len(re.findall(r"\\item", cando)) < 3:
            err(f"{rel}: fewer than 3 can-do goals")

# README and the landing page state the plan's size in prose; they must match the data
vals = dict(re.findall(r"gval@([A-Za-z0-9.]+)\}\{(\d+)\}", values))
for doc in ("README.md", "docs/index.html"):
    t = (ROOT / doc).read_text(encoding="utf-8")
    for n in re.findall(r"(\d+) jednostek", t):
        if n != vals.get("units.total"):
            err(f"{doc}: says {n} jednostek, data/units.tsv has {vals.get('units.total')}")
    for n in re.findall(r"\+ (\d+) tygodni[ea]? buforow", t):
        if int(n) != int(vals.get("weeks.total", 0)) - int(vals.get("units.total", 0)):
            err(f"{doc}: says {n} buffer weeks, the plan has {int(vals.get('weeks.total',0)) - int(vals.get('units.total',0))}")

if errs:
    print("\n".join("FAIL " + e for e in errs))
    print(f"\n{len(errs)} problem(s)")
    sys.exit(1)
print(f"check_book: {len(rows)} units, {len(sources)} sources, all gates green")
