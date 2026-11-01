<!-- badges: house header row (readme-badges standard). Only badges for things this repo has. -->
[![Ask me anything](https://flat.badgen.net/static/Ask%20me/anything?icon=github&color=black&scale=1.01)](https://github.com/konradcinkusz "Ask me anything")
[![Content licence](https://flat.badgen.net/static/content/CC%20BY-NC-SA%204.0?icon=github&color=black&scale=1.01)](https://github.com/konradcinkusz/german-from-zero-to-hero/blob/main/LICENSE-CONTENT "Content licence")
[![Code licence](https://flat.badgen.net/github/license/konradcinkusz/german-from-zero-to-hero?icon=github&color=black&scale=1.01)](https://github.com/konradcinkusz/german-from-zero-to-hero/blob/main/LICENSE "Code licence")
[![Maintained](https://flat.badgen.net/static/Maintained/yes?icon=github&color=black&scale=1.01)](https://github.com/konradcinkusz/german-from-zero-to-hero/commits/main "Commit history")
[![Issues](https://flat.badgen.net/github/issues/konradcinkusz/german-from-zero-to-hero?icon=github&color=black&scale=1.01)](https://github.com/konradcinkusz/german-from-zero-to-hero/issues "Issues")
[![Build](https://github.com/konradcinkusz/german-from-zero-to-hero/actions/workflows/build.yml/badge.svg)](https://github.com/konradcinkusz/german-from-zero-to-hero/actions/workflows/build.yml "Build")

# Deutsch von Null bis B2

## Pobierz

| Plik | Co to jest | Release (najnowszy) | Strona |
|---|---|---|---|
| **Książka (PDF)** | kurs A1 → B2, 48 jednostek + dodatki | [Deutsch-von-Null-bis-B2.pdf](https://github.com/konradcinkusz/german-from-zero-to-hero/releases/latest/download/Deutsch-von-Null-bis-B2.pdf) | [PDF](https://konradcinkusz.github.io/german-from-zero-to-hero/Deutsch-von-Null-bis-B2.pdf) |
| **Fiszki gramatyczne (PDF)** | pytanie → odpowiedź, A1–B2 | [Fiszki-gramatyka.pdf](https://github.com/konradcinkusz/german-from-zero-to-hero/releases/latest/download/Fiszki-gramatyka.pdf) | [PDF](https://konradcinkusz.github.io/german-from-zero-to-hero/Fiszki-gramatyka.pdf) |
| **Fiszki słownictwa (PDF)** | niemiecki → polski, całe słownictwo | [Fiszki-slownictwo.pdf](https://github.com/konradcinkusz/german-from-zero-to-hero/releases/latest/download/Fiszki-slownictwo.pdf) | [PDF](https://konradcinkusz.github.io/german-from-zero-to-hero/Fiszki-slownictwo.pdf) |
| **Anki (A1–B2)** | cztery pliki TSV, karta w obie strony | [anki-decks.zip](https://github.com/konradcinkusz/german-from-zero-to-hero/releases/latest/download/anki-decks.zip) | [A1](https://konradcinkusz.github.io/german-from-zero-to-hero/anki/german-a1.tsv) · [A2](https://konradcinkusz.github.io/german-from-zero-to-hero/anki/german-a2.tsv) · [B1](https://konradcinkusz.github.io/german-from-zero-to-hero/anki/german-b1.tsv) · [B2](https://konradcinkusz.github.io/german-from-zero-to-hero/anki/german-b2.tsv) |

Linki działają po pierwszym wydaniu (tag `v*`) i po włączeniu GitHub Pages. Do tego czasu pobierz PDF-y z artefaktów
[ostatniego builda](https://github.com/konradcinkusz/german-from-zero-to-hero/actions/workflows/build.yml)
(`book-pdf`, `flashcards-pdf`; wygasają po 14 dniach).

**Niemiecki od zera do B2 w 52 tygodnie** — kurs dla inżyniera oprogramowania, który chce
pracować w Szwajcarii (Zurych). Po polsku, z niemieckimi przykładami, dialogami, ćwiczeniami
z kluczem, fiszkami Anki i dodatkiem o szwajcarskim kontekście zawodowym.

* Plan: 4 poziomy (A1 → A2 → B1 → B2), 48 jednostek tygodniowych + 4 tygodnie buforowe.
* Struktura jednostki: cele *can-do*, słownictwo, gramatyka, dialogi, ćwiczenia, zadanie weekendowe.
* Wszystkie liczby (słowa, ćwiczenia, tygodnie) są **liczone z danych**, nie wpisywane — patrz Dodatek F.

## Uczciwie o czasie

Godzina dziennie to ok. 365 godzin w roku: to solidne B1, nie B2. Dojście do B2 w 12 miesięcy
wymaga ok. 600 godzin (ok. 100 min dziennie + 3 h w weekend). Książka opisuje oba tryby
(*tryb 100* i *tryb 60*); szczegóły we Wstępie.

## Status

**Wersja robocza.** Treść nie została sprawdzona przez native speakera. Fakty wymagające źródła
pierwotnego (prawo, urzędy w Szwajcarii) są oznaczone `[?]` i policzone w Dodatku F.
Zgłoś błąd przez [erratum](.github/ISSUE_TEMPLATE/erratum.yml).

## Co dostajesz

| | |
|---|---|
| Anki | `anki/german-a1.tsv` … `german-b2.tsv` — import jest już opisany nagłówkami (talia `Deutsch::A1`, karta w obie strony) |
| Dane | `data/units.tsv` (kolejność), `data/vocab/uNN.tsv` (słownictwo jednostki NN) |

## Budowanie

```bash
python3 tools/gen.py        # generuje tabele słownictwa, Anki, plan, liczniki (stdlib, bez zależności)
make check                  # bramki źródłowe: nie wymagają TeX-a, trwają sekundy
make                        # gen + check + latexmk + kontrola logu
```

Wymaga `latexmk` i pakietów `babel` (polski + niemiecki), `tcolorbox`, `longtable`.
Instalacja hooka (skan sekretów + bramki): `scripts/install-hooks.sh`.

## Zasady repozytorium

Książka stosuje te same konwencje co [`math-for-ai-engineers`](https://github.com/konradcinkusz/math-for-ai-engineers)
i [`maf-book`](https://github.com/konradcinkusz/maf-book) oraz standardy z
[`architecture-standards`](https://github.com/konradcinkusz/architecture-standards): jedno źródło
prawdy dla sekwencji i słownictwa, wygenerowane pliki commitowane i sprawdzane na dryf,
bramki przed buildem, pierwotne źródła dla twierdzeń o świecie. Opis: [`CLAUDE.md`](CLAUDE.md).
Runnery CI: GitHub-hosted (repozytorium publiczne) — [`docs/RUNNER.md`](docs/RUNNER.md).

## Licencje

Treść: [CC BY-NC-SA 4.0](LICENSE-CONTENT). Kod, makra, workflow: [MIT](LICENSE).

---

Konrad Cinkusz · [GitHub](https://github.com/konradcinkusz)
