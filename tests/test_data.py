import json

from biblia_ruf import validate_all_books, validate_book
from biblia_ruf.data_loader import list_book_names, load_json


def test_all_66_books_are_bundled():
    assert len(list_book_names()) == 66


def test_metadata_is_bundled_and_not_listed_as_a_book():
    metadata = load_json("biblia")
    assert isinstance(metadata, list)
    assert all(entry["toc3"] for entry in metadata)
    assert "biblia" not in list_book_names()


def test_missing_data_raises():
    try:
        load_json("DoesNotExist")
    except FileNotFoundError:
        pass
    else:
        raise AssertionError("expected FileNotFoundError")


def test_every_book_loads_as_utf8_with_expected_shape():
    for name in list_book_names():
        chapters = load_json(name)
        assert isinstance(chapters, list) and chapters
        first = chapters[0]
        assert isinstance(first["chapter"], int)
        assert isinstance(first["verses"], list) and first["verses"]
        assert isinstance(first["verses"][0]["verse"], str)
        assert isinstance(first["verses"][0]["text"], str)


def test_hungarian_diacritics_preserved():
    # Genesis 1:1 in RÚF — the é/á/ö must survive the round-trip.
    gen = load_json("1Móz")
    verse1 = gen[0]["verses"][0]["text"]
    assert "teremtette Isten" in verse1
    assert any(c in verse1 for c in "áéíóöőúüű")


def test_json_files_are_valid_utf8_encoded_json():
    # Belt-and-suspenders: raw bytes parse cleanly as UTF-8 JSON.
    for name in list_book_names():
        raw = load_json(name)
        assert json.loads(json.dumps(raw)) == raw


def test_validate_book_reports_no_errors_for_a_real_book():
    assert validate_book("Jn") == []


def test_validate_all_books_reports_no_errors():
    errors = validate_all_books()
    assert errors == [], f"unexpected validation errors: {errors[:5]}"
