"""Per-book metadata. Ported from ``book-details.ts``."""

from __future__ import annotations

from .data_loader import load_json
from .models import BookDetails


def get_book_details(book: str) -> BookDetails:
    """Return metadata for a book identified by its Hungarian abbreviation (``toc3``).

    Raises ``ValueError`` if the abbreviation is unknown (JS throws an ``Error``).
    """
    metadata = load_json("biblia")
    book_content = load_json(book)

    verses: dict[int, int] = {ch["chapter"]: len(ch["verses"]) for ch in book_content}

    entry = next((b for b in metadata if b["toc3"] == book), None)
    if entry is None:
        raise ValueError(f"Book not found: {book}")

    return BookDetails(
        name=entry["title"],
        abbreviation=entry["toc3"],
        abbreviation_eng=entry["slug"],
        chapters=len(entry["chapter"]),
        verses=verses,
    )
