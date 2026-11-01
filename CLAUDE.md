# CLAUDE.md — working on this book

Context for continuing *Deutsch von Null bis B2*. Read this before touching a unit.
Conventions are inherited from `math-for-ai-engineers` and `maf-book`, and from the
`architecture-standards` marketplace (research-documentation, repo-baseline, readme-badges,
open-source-release, self-hosted-runners).

## Status

Read the numbers from the generated ledgers, never from this file:

```bash
python3 tools/debt.py     # units written, vocabulary, exercises, [?] flags
```

**Review status: native-speaker review NOT ESTABLISHED.** Reported on every build; this ledger
must not quietly go away. German examples were written carefully and checked against the word
lists, but a native speaker has not read them.

## Non-negotiable conventions

1. **One source of truth, generated tables.** `data/units.tsv` is the sequence; `data/vocab/uNN.tsv`
   is the vocabulary. `generated/` and `anki/` are written by `tools/gen.py`, committed, and gated on
   drift. Never hand-edit them.
2. **Every number is computed.** A count in prose is `\val{key}` (keys in `generated/values.tex`).
   The gate `check_book.py` fails on a `\val{}` with no definition. Do not type "about 1500 words".
3. **Every noun has its article and plural**, in the data and on the page. A noun without an article
   fails `gen.py`.
4. **Every exercise has its answer**, written at the point of use: `\exitem{question}{answer}`. Answers
   are collected into Appendix A. Minimum 8 per unit (gate).
5. **A fact about Switzerland that depends on law, a regulator or a date is wrapped in
   `\verify{...}`** unless you opened the primary source in this session. The count is printed.
   Clearing one means a source was checked, not that it felt right.
6. **Hours are not promised.** The orientation table is "approximate, from a planning conversation".
   One hour a day is B1, not B2; do not edit that claim to be kinder.
7. **No placeholder text ships** (gate: TODO/FIXME/XXX/TBD).
8. **Run the source gates before the build**: `python3 tools/gen.py --check && python3 tools/check_book.py`.
   They read source and take seconds.

## Flashcards and drills

* `data/cards/grammar.tsv` (hand-written, `level, category, difficulty, question, answer`) and `data/vocab/`
  generate `flashcards/areas/*.tex`; `flashcards/dfcards.cls` is a light sibling of `csharp-flashcards`'
  `mybeamer.cls` (same card mechanic: question slide, answer frame, badge, 1-3 difficulty; no minted,
  no fontawesome, plain pdflatex). Never hand-edit `flashcards/areas/`.
* Every unit ends its exercises with `\drill{NN}`: a vocabulary drill generated from that unit's own word
  list (seeded by the unit number, so regenerating changes nothing). It tests vocabulary memory, not grammar.
* Not done: an ab-ovo bundle (`compile-bundle.py` in csharp-flashcards). Add it if the platform should read this deck.

## Unit anatomy (gate-enforced)

`\unitopen{NN}`, a `candos` block, `\vocabtable{NN}`, a `dialog`, a `falle` (trap for Polish speakers)
box, a `cwiczenia` block, and a `\weekend{...}` production task. Optional: `szwajcaria`, `praca`,
`zasada`, `uwaga` boxes.

## Build traps (inherited, cost time elsewhere)

* An exit-0 background build proves nothing; read `tools/check_log.py` output.
* `\vocabtable` (command) and `vocabtab` (environment) are different names on purpose: `\newenvironment`
  defines a command of the environment's name.
* `longtable` cannot sit in `multicols`: the index is paragraphs, not a table.
* An unchanged page count after an edit is a build that did not run.
* Authoring aid: `tools/gen.py --partial` and `check_book.py --partial` skip unwritten units. CI never
  passes `--partial`; a missing unit is a failure there.

## Where CI runs

GitHub-hosted runners, deliberately (public repository): `docs/RUNNER.md`.
