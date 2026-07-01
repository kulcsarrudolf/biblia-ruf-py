"""Passage-reference parser. Faithful port of ``passage-parser.ts``.

This deliberately mirrors the JS behavior — including its quirks — so output matches
the JS package for the same input. In particular:

* Book abbreviations are matched case-sensitively (no normalization).
* Numbers are parsed with JS ``parseInt`` semantics (leading digits, ``NaN`` on
  failure) rather than Python's stricter ``int()``. Unparseable verse numbers yield
  ``nan`` and are handled downstream exactly as the JS truthiness checks handle them.

Hardening (validation, friendly errors) is intentionally deferred to a later change.
"""

from __future__ import annotations

import math
import re

from .book_details import get_book_details
from .models import ParsedPassage

_LEADING_INT = re.compile(r"^\s*([+-]?\d+)")


def js_parse_int(token: str) -> float:
    """Mimic JavaScript ``parseInt(token, 10)``: read a leading integer, else ``NaN``."""
    match = _LEADING_INT.match(token)
    if match is None:
        return math.nan
    return int(match.group(1))


def is_truthy(value: float) -> bool:
    """JS truthiness for numbers: ``0`` and ``NaN`` are falsy, everything else truthy."""
    if value is None:
        return False
    if isinstance(value, float) and math.isnan(value):
        return False
    return bool(value)


def _get_book(passage: str) -> str:
    return passage.split(" ")[0]


def _get_chapter(passage: str) -> float:
    return js_parse_int(passage.split(" ")[1].split(":")[0])


def _get_verse_ranges(passage: str) -> list[tuple[float, float]]:
    ref = passage.split(" ")[1].split(":")
    verse_spec = ref[1] if len(ref) > 1 else ""

    if verse_spec:
        ranges: list[tuple[float, float]] = []
        for chunk in verse_spec.split(","):
            bounds = chunk.split("-")
            start = js_parse_int(bounds[0])
            end = js_parse_int(bounds[1]) if len(bounds) > 1 else math.nan
            ranges.append((start, end if is_truthy(end) else start))
        return ranges

    # No verse specified → whole chapter, using the book's verse count for this chapter.
    book = _get_book(passage)
    chapter = _get_chapter(passage)
    details = get_book_details(book)
    count = details.verses.get(chapter, 0) if isinstance(chapter, int) else 0
    return [(1, count)]


def parse_passage(input_passage: str) -> list[ParsedPassage]:
    """Parse a reference string into one or more :class:`ParsedPassage` entries.

    Supports single verses (``"Jn 3:16"``), ranges (``"Zsolt 139:23-24"``), comma lists
    (``"Zsolt 139:3,23-24"``), whole chapters (``"Zsolt 100"``), and multiple passages
    separated by ``;`` (``"Zsolt 1;Péld 10"``).
    """
    passages = input_passage.replace("; ", ";").split(";")

    result: list[ParsedPassage] = []
    for passage in passages:
        book = _get_book(passage)
        chapter = _get_chapter(passage)
        for start, end in _get_verse_ranges(passage):
            result.append(ParsedPassage(book, chapter, start, end))
    return result
