"""Typed data models for the library. Mirrors the JS ``types.ts`` interfaces.

All models are frozen dataclasses. Note ``BibleVerse.verse`` is a ``str`` (not ``int``),
matching the JS data where verse numbers are strings (e.g. ``"16"``).
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class BibleBook:
    abbreviation: str
    name: str


@dataclass(frozen=True)
class BibleVerse:
    verse: str
    text: str


@dataclass(frozen=True)
class ChapterData:
    chapter: int
    verses: list[BibleVerse]


@dataclass(frozen=True)
class ParsedPassage:
    book: str
    chapter: int
    start_verse: int
    end_verse: int


@dataclass(frozen=True)
class BookDetails:
    name: str
    abbreviation: str
    abbreviation_eng: str
    chapters: int
    verses: dict[int, int] = field(default_factory=dict)


@dataclass(frozen=True)
class SearchResult:
    book: str
    book_name: str
    chapter: int
    verse: str
    text: str
    reference: str


@dataclass(frozen=True)
class DailyVerseResult:
    reference: str
    book: str
    chapter: int
    verse: str
    text: str
