"""biblia-ruf — Hungarian RÚF Bible (Revideált új fordítás) for Python.

Public API is populated incrementally; see the project README for usage.
"""

from .validate import ValidationError, validate_all_books, validate_book

__version__ = "0.1.0"

__all__ = [
    "ValidationError",
    "__version__",
    "validate_all_books",
    "validate_book",
]
