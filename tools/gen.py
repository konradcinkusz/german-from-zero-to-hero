#!/usr/bin/env python3
"""Generate everything the book computes from data/.

Single sources of truth:
  data/units.tsv        the unit sequence (titles, levels, grammar focus)
  data/vocab/uNN.tsv    the vocabulary of unit NN

Written to generated/ and anki/ (both COMMITTED, so a changed number shows up
in review and CI can fail on drift):
  generated/structure.tex     \\part / \\input sequence for main.tex
  generated/meta.tex          unit titles, levels, weeks as \\csdef macros
  generated/vocab-uNN.tex     one vocabulary table per unit
  generated/vocab-index.tex   alphabetical German-Polish index (Appendix C)
  generated/plan-table.tex    the 52-week calendar (front matter)
  generated/values.tex        every count the book prints, as \\gval keys
  anki/german-<level>.tsv     Anki import files, one per level

Usage:  python3 tools/gen.py          write
        python3 tools/gen.py --check  fail if anything on disk is stale
Stdlib only.
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

PARTIAL = "--partial" in sys.argv  # authoring aid only: CI never passes it
ROOT = Path(__file__).resolve().parent.parent
LEVELS = ["A1", "A2", "B1", "B2"]
LEVEL_TITLE = {
    "A1": "A1 — Fundamenty",
    "A2": "A2 — Codzienność i praca",
    "B1": "B1 — Samodzielność",
    "B2": "B2 — Język zawodowy",
}
POS = {"n", "v", "adj", "adv", "prep", "ph", "conj", "num", "pron", "other"}
NOUN = re.compile(r"^(der|die|das) [^,]+(, .+)?$")
SPECIAL = {"&": r"\&", "%": r"\%", "#": r"\#", "_": r"\_", "$": r"\$"}


def tex(s: str) -> str:
    out = "".join(SPECIAL.get(c, c) for c in s)
    return out.replace("~", r"\textasciitilde{}")


def lemma(de: str) -> str:
    s = de.split(",")[0].strip()
    s = re.sub(r"^(der|die|das|sich) ", "", s)
    return s.lower()


def colour_article(de: str) -> str:
    m = re.match(r"^(der|die|das) (.*)$", de)
    if not m:
        return tex(de)
    art, rest = m.groups()
    mac = {"der": r"\artm", "die": r"\artf", "das": r"\artn"}[art]
    return f"{mac}{{{art}}} {tex(rest)}"


def read_units():
    rows = []
    lines = (ROOT / "data/units.tsv").read_text(encoding="utf-8").splitlines()
    for ln in lines[1:]:
        if not ln.strip():
            continue
        n, level, slug, de, pl, grammar = ln.split("\t")
        rows.append(dict(n=int(n), level=level, slug=slug, de=de, pl=pl, grammar=grammar))
    errs = []
    for i, u in enumerate(rows, 1):
        if u["n"] != i and not PARTIAL:
            errs.append(f"units.tsv: row {i} has n={u['n']}")
        if u["level"] not in LEVELS:
            errs.append(f"units.tsv: unit {u['n']} has level {u['level']}")
        if not re.fullmatch(r"[a-z0-9-]+", u["slug"]):
            errs.append(f"units.tsv: bad slug {u['slug']}")
    order = [LEVELS.index(u["level"]) for u in rows]
    if order != sorted(order):
        errs.append("units.tsv: levels are not contiguous and ascending")
    return rows, errs


def calendar_week(u):
    # one buffer week after every level: A1 12 units + 1, A2 12 + 1, ...
    return u["n"] + LEVELS.index(u["level"])


def read_vocab(units):
    vocab, errs, seen = {}, [], {}
    for u in units:
        nn = f"{u['n']:02d}"
        p = ROOT / f"data/vocab/u{nn}.tsv"
        if not p.exists():
            errs.append(f"missing {p.relative_to(ROOT)}")
            vocab[u["n"]] = []
            continue
        rows = []
        lines = p.read_text(encoding="utf-8").splitlines()
        if not lines or lines[0] != "pos\tde\tpl\tnote":
            errs.append(f"{p.name}: first line must be the header pos<TAB>de<TAB>pl<TAB>note")
            lines = lines[1:]
        else:
            lines = lines[1:]
        for k, ln in enumerate(lines, 2):
            if not ln.strip():
                continue
            cols = ln.split("\t")
            if len(cols) != 4:
                errs.append(f"{p.name}:{k}: expected 4 tab-separated columns, got {len(cols)}")
                continue
            pos, de, pl, note = [c.strip() for c in cols]
            if pos not in POS:
                errs.append(f"{p.name}:{k}: unknown pos {pos!r}")
            if not de or not pl:
                errs.append(f"{p.name}:{k}: empty German or Polish")
            if pos == "n" and not NOUN.match(de):
                errs.append(f"{p.name}:{k}: noun without article: {de!r}")
            if pos != "n" and re.match(r"^(der|die|das) ", de) and pos != "ph":
                errs.append(f"{p.name}:{k}: article on a non-noun: {de!r}")
            key = (lemma(de), pos)
            if key in seen:
                errs.append(f"{p.name}:{k}: duplicate of {seen[key]}: {de!r}")
            seen[key] = f"u{nn}"
            rows.append(dict(pos=pos, de=de, pl=pl, note=note, unit=u["n"], level=u["level"]))
        vocab[u["n"]] = rows
    return vocab, errs


def count_in_units(units):
    """Counts read from the unit sources, so Appendix F never types them."""
    tot = defaultdict(int)
    per_level = defaultdict(lambda: defaultdict(int))
    for u in units:
        p = ROOT / f"units/u{u['n']:02d}-{u['slug']}.tex"
        if not p.exists():
            continue
        s = p.read_text(encoding="utf-8")
        s = re.sub(r"(?<!\\)%.*", "", s)
        c = dict(
            written=1,
            exercises=len(re.findall(r"\\exitem\{", s)),
            dialogs=len(re.findall(r"\\begin\{dialog\}", s)),
            candos=len(re.findall(r"\\item", "".join(re.findall(r"\\begin\{candos\}.*?\\end\{candos\}", s, re.S)))),
            traps=len(re.findall(r"\\begin\{falle\}", s)),
            swiss=len(re.findall(r"\\begin\{szwajcaria\}", s)),
            work=len(re.findall(r"\\begin\{praca\}", s)),
            verify=len(re.findall(r"\\verify\{", s)),
        )
        for k, v in c.items():
            tot[k] += v
            per_level[u["level"]][k] += v
    return tot, per_level


def build():
    units, errs = read_units()
    if PARTIAL:
        # keep units whose source exists, so a half-written book still builds
        units = [u for u in units if (ROOT / f"units/u{u['n']:02d}-{u['slug']}.tex").exists()]
    vocab, verrs = read_vocab(units)
    errs += verrs
    out = {}

    # structure.tex
    s = ["% GENERATED by tools/gen.py from data/units.tsv -- do not edit.\n"]
    cur = None
    for u in units:
        if u["level"] != cur:
            cur = u["level"]
            s.append(f"\\part{{{LEVEL_TITLE[cur]}}}\n")
        s.append(f"\\input{{units/u{u['n']:02d}-{u['slug']}}}\n")
    out["generated/structure.tex"] = "".join(s)

    # meta.tex
    m = ["% GENERATED by tools/gen.py -- do not edit.\n"]
    for u in units:
        nn = f"{u['n']:02d}"
        m.append(f"\\csdef{{unittitle@{nn}}}{{{tex(u['pl'])}}}\n")
        m.append(f"\\csdef{{unittitlede@{nn}}}{{{tex(u['de'])}}}\n")
        m.append(f"\\csdef{{unitlevel@{nn}}}{{{u['level']}}}\n")
        m.append(f"\\csdef{{unitweek@{nn}}}{{{calendar_week(u)}}}\n")
        m.append(f"\\csdef{{unitgrammar@{nn}}}{{{tex(u['grammar'])}}}\n")
        m.append(f"\\csdef{{unitwords@{nn}}}{{{len(vocab[u['n']])}}}\n")
    out["generated/meta.tex"] = "".join(m)

    # vocab tables
    for u in units:
        nn = f"{u['n']:02d}"
        t = [f"% GENERATED by tools/gen.py from data/vocab/u{nn}.tsv -- do not edit.\n",
             "\\begin{vocabtab}\n"]
        for r in vocab[u["n"]]:
            t.append(f"\\vrow{{{colour_article(r['de'])}}}{{{tex(r['pl'])}}}{{{tex(r['note'])}}}\n")
        t.append("\\end{vocabtab}\n")
        out[f"generated/vocab-u{nn}.tex"] = "".join(t)

    # alphabetical index
    allrows = [r for u in units for r in vocab[u["n"]]]
    allrows.sort(key=lambda r: (lemma(r["de"]).translate(str.maketrans("äöüß", "aous")), r["de"]))
    t = ["% GENERATED by tools/gen.py -- do not edit.\n", "\\begin{indextable}\n"]
    for r in allrows:
        t.append(f"\\irow{{{colour_article(r['de'])}}}{{{tex(r['pl'])}}}{{{r['unit']}}}\n")
    t.append("\\end{indextable}\n")
    out["generated/vocab-index.tex"] = "".join(t)

    # plan table
    t = ["% GENERATED by tools/gen.py -- do not edit.\n", "\\begin{plantable}\n"]
    last_level, buf = None, 0
    for i, u in enumerate(units):
        t.append(f"{calendar_week(u)} & {u['level']} & {u['n']} & {tex(u['pl'])} & {tex(u['grammar'])}\\\\\n")
        nxt = units[i + 1]["level"] if i + 1 < len(units) else None
        if nxt != u["level"]:
            w = calendar_week(u) + 1
            t.append(f"\\rowcolor{{lightgray}}{w} & {u['level']} & --- & \\textit{{Tydzień buforowy i test poziomu {u['level']}}} & powtórka, \\textit{{Anki}}, mock-test\\\\\n")
    t.append("\\end{plantable}\n")
    out["generated/plan-table.tex"] = "".join(t)

    # values
    cnt, per = count_in_units(units)
    v = {}
    v["units.total"] = len(units)
    v["weeks.total"] = calendar_week(units[-1]) + 1
    v["vocab.total"] = len(allrows)
    for L in LEVELS:
        v[f"units.{L}"] = sum(1 for u in units if u["level"] == L)
        v[f"vocab.{L}"] = sum(1 for r in allrows if r["level"] == L)
        for k in ("exercises", "dialogs", "traps", "swiss", "work", "verify", "written", "candos"):
            v[f"{k}.{L}"] = per[L][k]
    for k in ("exercises", "dialogs", "traps", "swiss", "work", "verify", "written", "candos"):
        v[f"{k}.total"] = cnt[k]
    v["nouns.der"] = sum(1 for r in allrows if r["pos"] == "n" and r["de"].startswith("der "))
    v["nouns.die"] = sum(1 for r in allrows if r["pos"] == "n" and r["de"].startswith("die "))
    v["nouns.das"] = sum(1 for r in allrows if r["pos"] == "n" and r["de"].startswith("das "))
    v["vocab.verbs"] = sum(1 for r in allrows if r["pos"] == "v")
    t = ["% GENERATED by tools/gen.py -- do not edit.\n"]
    for k in sorted(v):
        t.append(f"\\csdef{{gval@{k}}}{{{v[k]}}}\n")
    out["generated/values.tex"] = "".join(t)

    # anki
    for L in LEVELS:
        t = ["#separator:tab\n", "#html:false\n", "#notetype:Basic (and reversed card)\n",
             f"#deck:Deutsch::{L}\n", "#tags column:4\n"]
        for r in allrows:
            if r["level"] != L:
                continue
            back = r["pl"] + (f" ({r['note']})" if r["note"] else "")
            t.append(f"{r['de']}\t{back}\t\t{L} u{r['unit']:02d} {r['pos']}\n")
        out[f"anki/german-{L.lower()}.tsv"] = "".join(t)
    return out, errs


def main():
    check = "--check" in sys.argv
    out, errs = build()
    if errs:
        print("\n".join("ERROR " + e for e in errs))
        return 1
    stale = []
    for rel, content in out.items():
        p = ROOT / rel
        if check:
            if not p.exists() or p.read_text(encoding="utf-8") != content:
                stale.append(rel)
        else:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding="utf-8")
    if check:
        if stale:
            print("STALE (run python3 tools/gen.py and commit):")
            print("\n".join("  " + s for s in stale))
            return 1
        print(f"gen --check: {len(out)} generated files current")
        return 0
    print(f"gen: wrote {len(out)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
