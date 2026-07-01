"""Deterministic daily verse. Faithful port of ``daily-verse.ts``.

For a given calendar date the same verse is always returned. To stay byte-compatible
with the JS package, the date-hashing reproduces JS 32-bit signed integer arithmetic
exactly, and the curated verse list is kept in the same order (index into it is
``abs(hash) % len``).
"""

from __future__ import annotations

from datetime import date, datetime

from .data_loader import load_json
from .models import DailyVerseResult

# (reference, book abbreviation, chapter, verse) — order is significant.
CURATED_VERSES: list[tuple[str, str, int, str]] = [
    ("1Móz 1:1", "1Móz", 1, "1"),
    ("Zsolt 23:1", "Zsolt", 23, "1"),
    ("Zsolt 27:1", "Zsolt", 27, "1"),
    ("Zsolt 46:2", "Zsolt", 46, "2"),
    ("Zsolt 91:1", "Zsolt", 91, "1"),
    ("Zsolt 100:1", "Zsolt", 100, "1"),
    ("Zsolt 119:105", "Zsolt", 119, "105"),
    ("Zsolt 121:1", "Zsolt", 121, "1"),
    ("Zsolt 139:23", "Zsolt", 139, "23"),
    ("Péld 3:5", "Péld", 3, "5"),
    ("Péld 3:6", "Péld", 3, "6"),
    ("Péld 16:3", "Péld", 16, "3"),
    ("Ézs 40:31", "Ézs", 40, "31"),
    ("Ézs 41:10", "Ézs", 41, "10"),
    ("Jer 29:11", "Jer", 29, "11"),
    ("Mt 5:16", "Mt", 5, "16"),
    ("Mt 6:33", "Mt", 6, "33"),
    ("Mt 11:28", "Mt", 11, "28"),
    ("Mt 28:20", "Mt", 28, "20"),
    ("Jn 1:1", "Jn", 1, "1"),
    ("Jn 3:16", "Jn", 3, "16"),
    ("Jn 8:12", "Jn", 8, "12"),
    ("Jn 10:10", "Jn", 10, "10"),
    ("Jn 11:25", "Jn", 11, "25"),
    ("Jn 14:6", "Jn", 14, "6"),
    ("Jn 14:27", "Jn", 14, "27"),
    ("Jn 15:5", "Jn", 15, "5"),
    ("Róm 5:8", "Róm", 5, "8"),
    ("Róm 8:28", "Róm", 8, "28"),
    ("Róm 8:38", "Róm", 8, "38"),
    ("Róm 12:2", "Róm", 12, "2"),
    ("1Kor 10:13", "1Kor", 10, "13"),
    ("1Kor 13:4", "1Kor", 13, "4"),
    ("1Kor 13:13", "1Kor", 13, "13"),
    ("2Kor 5:17", "2Kor", 5, "17"),
    ("2Kor 12:9", "2Kor", 12, "9"),
    ("Gal 2:20", "Gal", 2, "20"),
    ("Gal 5:22", "Gal", 5, "22"),
    ("Ef 2:8", "Ef", 2, "8"),
    ("Ef 6:10", "Ef", 6, "10"),
    ("Fil 1:6", "Fil", 1, "6"),
    ("Fil 4:6", "Fil", 4, "6"),
    ("Fil 4:13", "Fil", 4, "13"),
    ("Kol 3:23", "Kol", 3, "23"),
    ("2Tim 1:7", "2Tim", 1, "7"),
    ("Zsid 11:1", "Zsid", 11, "1"),
    ("Zsid 12:2", "Zsid", 12, "2"),
    ("Jak 1:5", "Jak", 1, "5"),
    ("1Pt 5:7", "1Pt", 5, "7"),
    ("1Jn 4:8", "1Jn", 4, "8"),
    ("Jel 21:4", "Jel", 21, "4"),
]


def _hash_date(d: date) -> int:
    """Reproduce the JS date hash exactly (32-bit signed integer math)."""
    # Matches ``${getFullYear()}-${getMonth() + 1}-${getDate()}`` (1-based month, no pad).
    date_str = f"{d.year}-{d.month}-{d.day}"
    h = 0
    for ch in date_str:
        # h = (h << 5) - h + char, then coerce to 32-bit (JS ``hash |= 0``).
        h = ((h << 5) - h + ord(ch)) & 0xFFFFFFFF
    if h >= 0x80000000:  # interpret as signed 32-bit
        h -= 0x100000000
    return abs(h)


def get_daily_verse(target: date | datetime | None = None) -> DailyVerseResult:
    """Return the verse of the day for ``target`` (defaults to today)."""
    when = target if target is not None else datetime.now()
    index = _hash_date(when) % len(CURATED_VERSES)
    reference, book, chapter, verse = CURATED_VERSES[index]

    try:
        chapters = load_json(book)
        chapter_data = next((c for c in chapters if c["chapter"] == chapter), None)
        verse_data = (
            next((v for v in chapter_data["verses"] if v["verse"] == verse), None)
            if chapter_data
            else None
        )
        text = verse_data["text"] if verse_data else "Verse not found"
    except Exception:  # noqa: BLE001 - mirror JS fallback on any load failure
        text = "Could not load verse data"

    return DailyVerseResult(
        reference=reference,
        book=book,
        chapter=chapter,
        verse=verse,
        text=text,
    )
