# Contributing

The most useful contribution is an **erratum**: a wrong German form, an unnatural translation,
a wrong answer in the key, or a Swiss fact that has changed. Use the
[erratum template](.github/ISSUE_TEMPLATE/erratum.yml). Native speakers are especially welcome:
no native speaker has reviewed this book yet.

## Working on the book

```bash
python3 tools/gen.py            # regenerate vocabulary tables, Anki files, plan, counters
python3 tools/check_book.py     # source gates (no TeX needed)
latexmk -pdf main.tex           # build
scripts/install-hooks.sh        # pre-commit: secret scan + gates
```

Run the **source gates before the build**. They read `.tex` and `data/` and cost seconds; a
build costs minutes.

## House rules

* **One source of truth.** Unit order and titles: `data/units.tsv`. Vocabulary: `data/vocab/uNN.tsv`
  (`pos<TAB>de<TAB>pl<TAB>note`; every noun carries its article and plural). Never edit `generated/`
  or `anki/` by hand; edit the data and re-run `tools/gen.py`.
* **Numbers are computed.** Counts in prose come from `\val{key}`. A typed count decays silently.
* **Every exercise has an answer**, written at the point of use with `\exitem{question}{answer}`.
* **Facts about Switzerland that need a primary source** are wrapped in `\verify{...}`.
  They are counted in Appendix F; clearing one means you checked a primary source.
* **German is checked, not felt.** Read each example aloud and check the case and gender
  against the word list before committing.
* **Voice.** Idiomatic Polish, second person. No marketing register.

## Pull requests

CI runs the source gates, then the PDF build. Do not push a PR with red gates.
