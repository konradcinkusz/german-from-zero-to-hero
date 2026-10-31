# ADR 0002: vocabulary, sequence and counts are data, tables are generated

**Status:** accepted

`data/units.tsv` and `data/vocab/uNN.tsv` are the only sources for the unit order, the vocabulary
tables, the alphabetical index, the Anki decks, the calendar and every count the book prints.
`tools/gen.py` writes them to `generated/` and `anki/`, both committed; CI fails on drift
(`gen.py --check`). This is the `math-for-ai-engineers` rule (*every number is computed, not
remembered*) applied to a language book: a typed count of words decays silently, and a table
typed by hand drifts from the Anki deck it should match.

**Gates on the data:** every noun carries its article; no duplicate lemma across the book; no article on
a non-noun; four columns. A vocabulary entry that fails is a build failure, not a warning.
