# biblia-ruf (Python)

Python port of [`biblia-ruf`](https://github.com/kulcsarrudolf/biblia-ruf) — the
Hungarian **RÚF Biblia** (Revideált új fordítás). Passage lookup, full-text search,
book metadata, and a deterministic daily verse. The Bible text is bundled inside the
package, so it works fully offline with no network access.

> Status: early development. The public API is being ported PR by PR.

## Install

```bash
pip install biblia-ruf
```

## Usage

```python
from biblia_ruf import get_bible_passage, get_daily_verse, search_bible, get_bible_books

get_bible_passage("Jn 3:16")
get_bible_passage("Zsolt 139:23-24")
get_bible_books()          # 66 books
get_daily_verse()          # deterministic verse of the day
search_bible("szeretet", limit=10)
```

## Development

```bash
uv sync
uv run ruff check .
uv run ruff format --check .
uv run pytest
```

## License

MIT — see [LICENSE](LICENSE).
