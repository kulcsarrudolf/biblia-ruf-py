# Changelog

## 0.1.0

Initial release — Python port of the JS [`biblia-ruf`](https://github.com/kulcsarrudolf/biblia-ruf)
package.

- `get_bible_passage(passage)` — verses by reference (`"Jn 3:16"`, ranges, comma lists,
  whole chapters, multi-passage `;`).
- `search_bible(query, ...)` — full-text regex search with testament/book/limit filters.
- `get_daily_verse(target=None)` — deterministic verse of the day.
- `get_book_details(book)`, `get_bible_books()` / `_old_testament()` / `_new_testament()`.
- `validate_book()` / `validate_all_books()` — data-integrity checks.
- Bible text bundled in the wheel (fully offline); byte-for-byte parity with the JS
  package, verified by golden fixtures.
