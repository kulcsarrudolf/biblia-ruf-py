"""Access to the bundled RÚF Bible JSON data.

The data ships inside the package (``biblia_ruf/data``) so the library works fully
offline. This mirrors the JS package's build-time bundling: callers request data by
the base file name (e.g. ``"1Móz"`` for a book, ``"biblia"`` for the metadata), with
no filesystem path or network access involved.
"""

from __future__ import annotations

import json
from functools import cache
from importlib import resources
from typing import Any

_PACKAGE = "biblia_ruf"
_DATA_DIR = "data"
_METADATA_NAME = "biblia"


def _data_dir():
    return resources.files(_PACKAGE).joinpath(_DATA_DIR)


def load_json(name: str) -> Any:
    """Load and parse a bundled JSON file by its base name (without ``.json``).

    Raises ``FileNotFoundError`` if no bundled data exists for ``name`` — matching the
    JS loader, which throws when a key is missing.
    """
    resource = _data_dir().joinpath(f"{name}.json")
    if not resource.is_file():
        raise FileNotFoundError(f'biblia-ruf: no bundled data found for "{name}"')
    return json.loads(resource.read_text(encoding="utf-8"))


@cache
def list_book_names() -> tuple[str, ...]:
    """Return the base names of all bundled book data files (excludes metadata)."""
    names = []
    for entry in _data_dir().iterdir():
        if entry.name.endswith(".json"):
            base = entry.name[: -len(".json")]
            if base != _METADATA_NAME:
                names.append(base)
    return tuple(sorted(names))
