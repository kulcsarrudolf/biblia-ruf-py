from biblia_ruf import (
    get_bible_books,
    get_bible_books_new_testament,
    get_bible_books_old_testament,
    get_book_details,
)
from biblia_ruf.data_loader import list_book_names


def test_book_counts():
    assert len(get_bible_books_old_testament()) == 39
    assert len(get_bible_books_new_testament()) == 27
    assert len(get_bible_books()) == 66


def test_book_order_is_old_then_new():
    books = get_bible_books()
    assert books[0].abbreviation == "1Móz"
    assert books[38].abbreviation == "Mal"  # last OT book
    assert books[39].abbreviation == "Mt"  # first NT book
    assert books[-1].abbreviation == "Jel"


def test_every_listed_book_has_bundled_data():
    bundled = set(list_book_names())
    for book in get_bible_books():
        assert book.abbreviation in bundled, f"missing data for {book.abbreviation}"


def test_get_book_details_psalms():
    details = get_book_details("Zsolt")
    assert details.name == "A Zsoltárok könyve"
    assert details.abbreviation == "Zsolt"
    assert details.abbreviation_eng == "PSA"
    assert details.chapters == 150
    assert details.verses[1] == 6  # Psalm 1 has 6 verses
    assert len(details.verses) == 150


def test_get_book_details_john():
    details = get_book_details("Jn")
    assert details.name == "János evangéliuma"
    assert details.chapters == 21
    assert details.verses[3] == 36  # John 3 has 36 verses


def test_get_book_details_unknown_raises():
    try:
        get_book_details("Nope")
    except (ValueError, FileNotFoundError):
        pass
    else:
        raise AssertionError("expected an error for unknown book")
