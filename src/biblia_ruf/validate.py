"""Data-integrity validation for the bundled Bible JSON.

Ported from the JS ``validate.ts``. Unlike the JS ``validateAllBooks`` (which prints
and calls ``process.exit(1)``), these functions simply return the list of problems so
callers decide what to do — the Pythonic, side-effect-free behavior.
"""

from __future__ import annotations

from dataclasses import dataclass

from .data_loader import list_book_names, load_json


@dataclass(frozen=True)
class ValidationError:
    book: str
    message: str


def _validate_book_data(book: str, data: object) -> list[ValidationError]:
    errors: list[ValidationError] = []

    if not isinstance(data, list):
        errors.append(ValidationError(book, "Root must be an array"))
        return errors

    for i, chapter in enumerate(data):
        if not isinstance(chapter, dict) or not isinstance(chapter.get("chapter"), int):
            errors.append(
                ValidationError(book, f'Chapter at index {i}: missing or invalid "chapter" field')
            )
            chapter_num = chapter.get("chapter") if isinstance(chapter, dict) else None
        else:
            chapter_num = chapter["chapter"]

        verses = chapter.get("verses") if isinstance(chapter, dict) else None
        if not isinstance(verses, list):
            errors.append(
                ValidationError(book, f'Chapter {chapter_num}: "verses" must be an array')
            )
            continue

        for j, verse in enumerate(verses):
            if not isinstance(verse, dict) or not isinstance(verse.get("verse"), str):
                errors.append(
                    ValidationError(
                        book, f'Chapter {chapter_num}, verse index {j}: missing "verse" field'
                    )
                )
            if not isinstance(verse, dict) or not isinstance(verse.get("text"), str):
                verse_num = verse.get("verse") if isinstance(verse, dict) else None
                errors.append(
                    ValidationError(
                        book, f'Chapter {chapter_num}, verse {verse_num}: missing "text" field'
                    )
                )

    return errors


def validate_book(abbreviation: str) -> list[ValidationError]:
    """Validate a single book's bundled data by abbreviation."""
    try:
        data = load_json(abbreviation)
    except Exception as err:  # noqa: BLE001 - mirror JS: surface any read failure as an error
        return [ValidationError(abbreviation, f"Failed to read file: {err}")]
    return _validate_book_data(abbreviation, data)


def validate_all_books() -> list[ValidationError]:
    """Validate every bundled book data file. Returns all problems found (empty = ok)."""
    all_errors: list[ValidationError] = []
    for book in list_book_names():
        all_errors.extend(validate_book(book))
    return all_errors
