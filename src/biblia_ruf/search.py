"""Full-text search. Faithful port of ``search.ts``.

Result ordering follows the canonical book order (OT then NT), then chapter, then
verse, with an early stop once ``limit`` results are collected — identical to the JS
package. The ``query`` is treated as a regular expression, mirroring JS ``new RegExp``.
"""

from __future__ import annotations

import re

from .books import (
    get_bible_books,
    get_bible_books_new_testament,
    get_bible_books_old_testament,
)
from .data_loader import load_json
from .models import BibleBook, SearchResult


def _books_by_testament(testament: str | None) -> list[BibleBook]:
    if testament == "old":
        return get_bible_books_old_testament()
    if testament == "new":
        return get_bible_books_new_testament()
    return get_bible_books()


def search_bible(
    query: str,
    *,
    testament: str | None = None,
    book: str | None = None,
    case_sensitive: bool = False,
    limit: int = 100,
) -> list[SearchResult]:
    """Search the Bible text for ``query`` (a regular expression).

    Options mirror the JS ``SearchOptions``: restrict by ``testament`` (``"old"`` /
    ``"new"``) or a single ``book`` abbreviation, toggle ``case_sensitive``, and cap
    the number of results with ``limit``.
    """
    if book:
        found = next((b for b in get_bible_books() if b.abbreviation == book), None)
        book_list = [found] if found else []
    else:
        book_list = _books_by_testament(testament)

    results: list[SearchResult] = []
    regex = re.compile(query, 0 if case_sensitive else re.IGNORECASE)

    for b in book_list:
        if len(results) >= limit:
            break
        try:
            chapters = load_json(b.abbreviation)
        except FileNotFoundError:
            continue

        for ch in chapters:
            if len(results) >= limit:
                break
            for v in ch["verses"]:
                if len(results) >= limit:
                    break
                if regex.search(v["text"]):
                    results.append(
                        SearchResult(
                            book=b.abbreviation,
                            book_name=b.name,
                            chapter=ch["chapter"],
                            verse=v["verse"],
                            text=v["text"],
                            reference=f"{b.abbreviation} {ch['chapter']}:{v['verse']}",
                        )
                    )

    return results
