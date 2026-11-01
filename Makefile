.PHONY: all gen check verify clean debt flashcards
# Everything under generated/ and anki/ is computed from data/ and COMMITTED,
# so a changed number shows up in review and CI can fail on drift.

all: gen check
	latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex
	python3 tools/check_log.py main.log

gen:
	python3 tools/gen.py

# Source gates: read .tex and data/, need no PDF. Run these BEFORE a build.
check:
	python3 tools/gen.py --check
	python3 tools/check_book.py

verify: check

# Beamer flashcard decks (pdflatex, no shell-escape): grammar cards and the vocabulary deck
flashcards: gen
	cd flashcards && latexmk -pdf -interaction=nonstopmode -halt-on-error grammar.tex
	cd flashcards && latexmk -pdf -interaction=nonstopmode -halt-on-error vocab.tex

debt:
	@python3 tools/debt.py

clean:
	latexmk -C
	rm -f *.ilg *.ind *.idx
