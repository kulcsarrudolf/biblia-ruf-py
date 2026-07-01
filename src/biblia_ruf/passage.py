"""Passage retrieval. Faithful port of ``passage.ts``.

Like the JS version, this uses only the *first* parsed passage from the input string.
"""

from __future__ import annotations

from .data_loader import load_json
from .models import BibleVerse
from .parser import is_truthy, js_parse_int, parse_passage


def get_bible_passage(passage: str) -> list[BibleVerse]:
    """Return the verses for a reference such as ``"Jn 3:16"`` or ``"Zsolt 139:23-24"``.

    Raises ``ValueError`` if the referenced chapter does not exist in the book.
    """
    parsed = parse_passage(passage)
    first = parsed[0]

    chapters = load_json(first.book)
    current = next((c for c in chapters if c["chapter"] == first.chapter), None)
    if current is None:
        raise ValueError(f"Chapter {first.chapter} not found in {first.book}")

    start, end = first.start_verse, first.end_verse
    result: list[BibleVerse] = []
    for verse in current["verses"]:
        verse_num = js_parse_int(verse["verse"])
        if (
            (not is_truthy(start) and not is_truthy(end))
            or (is_truthy(start) and not is_truthy(end) and verse_num == start)
            or (is_truthy(start) and is_truthy(end) and start <= verse_num <= end)
        ):
            result.append(BibleVerse(verse["verse"], verse["text"]))

    return result
