#!/usr/bin/env python3
"""Refresh the vendored Bible JSON in ``src/biblia_ruf/data`` from the JS repo.

Two sources are supported:

  * ``--source <path>``   copy ``*.json`` from a local checkout of the JS
                          ``biblia-ruf`` repo's ``json/`` directory.
  * ``--from-github``     download every book file (plus ``biblia.json``) from
                          ``raw.githubusercontent.com`` using only the stdlib.

Run manually whenever the upstream Hungarian text is corrected, then commit the diff.

    python scripts/sync_data.py --source ../biblia-ruf/json
    python scripts/sync_data.py --from-github
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import urllib.parse
import urllib.request
from pathlib import Path

RAW_BASE = "https://raw.githubusercontent.com/kulcsarrudolf/biblia-ruf/main/json"
DATA_DIR = Path(__file__).resolve().parent.parent / "src" / "biblia_ruf" / "data"


def _fetch(url: str) -> bytes:
    with urllib.request.urlopen(url) as resp:  # noqa: S310 - fixed, trusted host
        return resp.read()


def sync_from_local(source: Path) -> int:
    if not source.is_dir():
        print(f"error: source directory not found: {source}", file=sys.stderr)
        return 1
    files = sorted(source.glob("*.json"))
    if not files:
        print(f"error: no *.json files in {source}", file=sys.stderr)
        return 1
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    for f in files:
        shutil.copy2(f, DATA_DIR / f.name)
    print(f"Copied {len(files)} JSON files from {source} -> {DATA_DIR}")
    return 0


def sync_from_github() -> int:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    metadata = _fetch(f"{RAW_BASE}/biblia.json")
    (DATA_DIR / "biblia.json").write_bytes(metadata)
    books = [entry["toc3"] for entry in json.loads(metadata)]
    for abbrev in books:
        url = f"{RAW_BASE}/{urllib.parse.quote(abbrev)}.json"
        (DATA_DIR / f"{abbrev}.json").write_bytes(_fetch(url))
    print(f"Downloaded {len(books)} books + metadata from GitHub -> {DATA_DIR}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--source", type=Path, help="local biblia-ruf json/ directory")
    group.add_argument("--from-github", action="store_true", help="download from GitHub raw")
    args = parser.parse_args()

    if args.from_github:
        return sync_from_github()
    return sync_from_local(args.source)


if __name__ == "__main__":
    raise SystemExit(main())
