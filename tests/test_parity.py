"""Byte-for-byte parity with the JS `biblia-ruf` package.

Fixtures in tests/golden/ are produced by scripts/gen_golden.mjs running the JS lib.
Regenerate them with:  node scripts/gen_golden.mjs  (see that script for the env var).
"""

import json
from dataclasses import asdict
from datetime import date
from pathlib import Path

import pytest

from biblia_ruf import get_bible_passage, get_daily_verse, search_bible

GOLDEN = Path(__file__).parent / "golden"


def _load(name):
    return json.loads((GOLDEN / name).read_text(encoding="utf-8"))


@pytest.mark.parametrize("ref, expected", _load("passages.json").items())
def test_passage_parity(ref, expected):
    actual = [asdict(v) for v in get_bible_passage(ref)]
    assert actual == expected


@pytest.mark.parametrize("case", _load("searches.json"))
def test_search_parity(case):
    opts = case["options"]
    actual = [
        asdict(r)
        for r in search_bible(
            case["query"],
            testament=opts.get("testament"),
            book=opts.get("book"),
            case_sensitive=opts.get("caseSensitive", False),
            limit=opts.get("limit", 100),
        )
    ]
    assert actual == case["results"]


@pytest.mark.parametrize("case", _load("daily.json"))
def test_daily_verse_parity(case):
    y, m, d = case["date"]
    actual = asdict(get_daily_verse(date(y, m, d)))
    assert actual == case["result"]
