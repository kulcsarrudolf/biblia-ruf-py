"""biblia-ruf — Hungarian RÚF Bible (Revideált új fordítás) for Python.

Public API is populated incrementally; see the project README for usage.
"""

from .book_details import get_book_details
from .books import (
    get_bible_books,
    get_bible_books_new_testament,
    get_bible_books_old_testament,
)
from .models import (
    BibleBook,
    BibleVerse,
    BookDetails,
    ChapterData,
    DailyVerseResult,
    ParsedPassage,
    SearchResult,
)
from .validate import ValidationError, validate_all_books, validate_book

__version__ = "0.1.0"

__all__ = [
    "BibleBook",
    "BibleVerse",
    "BookDetails",
    "ChapterData",
    "DailyVerseResult",
    "ParsedPassage",
    "SearchResult",
    "ValidationError",
    "__version__",
    "get_bible_books",
    "get_bible_books_new_testament",
    "get_bible_books_old_testament",
    "get_book_details",
    "validate_all_books",
    "validate_book",
]
