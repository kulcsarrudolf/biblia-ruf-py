import pytest

from biblia_ruf import get_bible_passage, parse_passage
from biblia_ruf.models import ParsedPassage


def test_parse_single_verse():
    assert parse_passage("Jn 3:16") == [ParsedPassage("Jn", 3, 16, 16)]


def test_parse_range():
    assert parse_passage("Zsolt 139:23-24") == [ParsedPassage("Zsolt", 139, 23, 24)]


def test_parse_comma_list():
    assert parse_passage("Zsolt 139:3,23-24") == [
        ParsedPassage("Zsolt", 139, 3, 3),
        ParsedPassage("Zsolt", 139, 23, 24),
    ]


def test_parse_full_chapter_uses_verse_count():
    # Psalm 100 has 5 verses.
    assert parse_passage("Zsolt 100") == [ParsedPassage("Zsolt", 100, 1, 5)]


def test_parse_multiple_passages():
    parsed = parse_passage("Zsolt 1;Péld 10")
    assert parsed[0].book == "Zsolt" and parsed[0].chapter == 1
    assert parsed[1].book == "Péld" and parsed[1].chapter == 10


def test_parse_multiple_passages_with_space_after_semicolon():
    parsed = parse_passage("Jn 3:16; Róm 8:28")
    assert parsed == [
        ParsedPassage("Jn", 3, 16, 16),
        ParsedPassage("Róm", 8, 28, 28),
    ]


def test_get_passage_single_verse():
    verses = get_bible_passage("Jn 3:16")
    assert len(verses) == 1
    assert verses[0].verse == "16"
    assert "Isten" in verses[0].text


def test_get_passage_range():
    verses = get_bible_passage("Zsolt 139:23-24")
    assert [v.verse for v in verses] == ["23", "24"]


def test_get_passage_full_chapter():
    verses = get_bible_passage("Zsolt 100")
    assert [v.verse for v in verses] == ["1", "2", "3", "4", "5"]


def test_get_passage_uses_only_first_parsed_passage():
    # Mirrors JS: only parsed[0] is used, so the second passage is ignored.
    verses = get_bible_passage("Jn 3:16;Róm 8:28")
    assert [v.verse for v in verses] == ["16"]


def test_get_passage_missing_chapter_raises():
    with pytest.raises(ValueError):
        get_bible_passage("Jn 99:1")
