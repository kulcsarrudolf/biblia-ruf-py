# biblia-ruf (Python)

Python port of [`biblia-ruf`](https://github.com/kulcsarrudolf/biblia-ruf) — the
Hungarian **RÚF Biblia** (Revideált új fordítás). Passage lookup, full-text search,
book metadata, and a deterministic daily verse.

The full Bible text is **bundled inside the package**, so it works completely offline
— no filesystem layout or network access required. Output is **byte-for-byte compatible**
with the JavaScript package (verified by parity tests), so a Python backend and a JS
frontend return the same daily verse and search results for the same inputs.

## Install

```bash
pip install biblia-ruf
```

Import name is `biblia_ruf`:

```python
import biblia_ruf
```

## Usage

```python
from biblia_ruf import (
    get_bible_passage,
    search_bible,
    get_daily_verse,
    get_book_details,
    get_bible_books,
)

# Passage lookup — single verse, range, comma list, whole chapter, multi-passage.
get_bible_passage("Jn 3:16")
# [BibleVerse(verse="16", text="Mert úgy szerette Isten a világot…")]

get_bible_passage("Zsolt 139:23-24")
get_bible_passage("Zsolt 100")            # whole chapter

# Full-text search (query is a regular expression).
search_bible("szeretet", limit=10)
search_bible("Isten", testament="old", limit=5)
search_bible("kegyelem", book="Róm")

# Deterministic verse of the day (same date → same verse).
get_daily_verse()
from datetime import date
get_daily_verse(date(2025, 12, 25))

# Book metadata and lists.
get_book_details("Zsolt")                 # BookDetails(name="A Zsoltárok könyve", chapters=150, …)
len(get_bible_books())                    # 66
```

### API

| Function | Returns | Notes |
|---|---|---|
| `get_bible_passage(passage)` | `list[BibleVerse]` | Uses the first reference in the string. |
| `search_bible(query, *, testament=None, book=None, case_sensitive=False, limit=100)` | `list[SearchResult]` | `query` is a regex; results in canonical book order. |
| `get_daily_verse(target=None)` | `DailyVerseResult` | `target` is a `date`/`datetime`; defaults to today. |
| `get_book_details(book)` | `BookDetails` | `book` is a Hungarian abbreviation, e.g. `"Zsolt"`. |
| `get_bible_books()` / `_old_testament()` / `_new_testament()` | `list[BibleBook]` | 66 / 39 / 27 books. |
| `parse_passage(passage)` | `list[ParsedPassage]` | Reference parser. |
| `validate_book(abbr)` / `validate_all_books()` | `list[ValidationError]` | Data-integrity checks. |

All return types are frozen dataclasses exported from the package root. Book
abbreviations are the Hungarian `toc3` forms (`1Móz`, `Zsolt`, `Jn`, `Róm`, …) and are
matched case-sensitively, matching the JS package.

## Development

Requires Python 3.10+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync                        # create the venv and install dev deps
uv run ruff check .            # lint
uv run ruff format --check .   # format check
uv run pytest                  # run tests (incl. JS parity)
```

### Refreshing the bundled data

When the upstream Hungarian text is corrected, re-vendor the JSON from the JS repo:

```bash
python scripts/sync_data.py --source ../biblia-ruf/json   # from a local checkout
python scripts/sync_data.py --from-github                 # or download from GitHub
```

### Regenerating parity fixtures

`tests/golden/` is produced by running the JS package over a fixed set of inputs. After
an intentional behavior change, regenerate it against a local `biblia-ruf` checkout:

```bash
BIBLIA_JS_DIST=../biblia-ruf/dist/index.mjs node scripts/gen_golden.mjs
```

## Releasing

Publishing to PyPI is automated via GitHub Actions **trusted publishing** (OIDC — no API
tokens). One-time setup on [pypi.org](https://pypi.org): add a *pending publisher* for
project `biblia-ruf` pointing at repo `kulcsarrudolf/biblia-ruf-py`, workflow
`release.yml` (leave the environment field blank). Then cut a release by pushing a tag:

```bash
git tag v0.1.0
git push origin v0.1.0
```

The `release.yml` workflow builds the sdist + wheel and publishes them to PyPI.

## License

MIT — see [LICENSE](LICENSE).
