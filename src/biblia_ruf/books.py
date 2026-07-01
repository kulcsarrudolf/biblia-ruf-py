"""The RÚF book list, split by testament. Ported verbatim from ``books.ts``.

Order matters: it defines the canonical iteration order used by search and by the
full-Bible book list, so it must match the JS package exactly.
"""

from __future__ import annotations

from .models import BibleBook

_OLD_TESTAMENT: list[BibleBook] = [
    BibleBook("1Móz", "Mózes első könyve"),
    BibleBook("2Móz", "Mózes második könyve"),
    BibleBook("3Móz", "Mózes harmadik könyve"),
    BibleBook("4Móz", "Mózes negyedik könyve"),
    BibleBook("5Móz", "Mózes ötödik könyve"),
    BibleBook("Józs", "Józsué könyve"),
    BibleBook("Bír", "A bírák könyve"),
    BibleBook("Ruth", "Ruth könyve"),
    BibleBook("1Sám", "Sámuel első könyve"),
    BibleBook("2Sám", "Sámuel második könyve"),
    BibleBook("1Kir", "A királyok első könyve"),
    BibleBook("2Kir", "A királyok második könyve"),
    BibleBook("1Krón", "A krónikák első könyve"),
    BibleBook("2Krón", "A krónikák második könyve"),
    BibleBook("Ezsd", "Ezsdrás könyve"),
    BibleBook("Neh", "Nehémiás könyve"),
    BibleBook("Eszt", "Eszter könyve"),
    BibleBook("Jób", "Jób könyve"),
    BibleBook("Zsolt", "A Zsoltárok könyve"),
    BibleBook("Péld", "A példabeszédek könyve"),
    BibleBook("Préd", "A prédikátor könyve"),
    BibleBook("Énekek", "Énekek éneke"),
    BibleBook("Ézs", "Ézsaiás próféta könyve"),
    BibleBook("Jer", "Jeremiás próféta könyve"),
    BibleBook("JSir", "Jeremiás siralmai"),
    BibleBook("Ez", "Ezékiel próféta könyve"),
    BibleBook("Dán", "Dániel próféta könyve"),
    BibleBook("Hós", "Hóseás próféta könyve"),
    BibleBook("Jóel", "Jóel próféta könyve"),
    BibleBook("Ám", "Ámósz próféta könyve"),
    BibleBook("Abd", "Abdiás próféta könyve"),
    BibleBook("Jón", "Jónás próféta könyve"),
    BibleBook("Mik", "Mikeás próféta könyve"),
    BibleBook("Náh", "Náhum próféta könyve"),
    BibleBook("Hab", "Habakuk próféta könyve"),
    BibleBook("Zof", "Zofóniás próféta könyve"),
    BibleBook("Hag", "Haggeus próféta könyve"),
    BibleBook("Zak", "Zakariás próféta könyve"),
    BibleBook("Mal", "Malakiás próféta könyve"),
]

_NEW_TESTAMENT: list[BibleBook] = [
    BibleBook("Mt", "Máté evangéliuma"),
    BibleBook("Mk", "Márk evangéliuma"),
    BibleBook("Lk", "Lukács evangéliuma"),
    BibleBook("Jn", "János evangéliuma"),
    BibleBook("ApCsel", "Az apostolok cselekedetei"),
    BibleBook("Róm", "Pál levele a rómaiakhoz"),
    BibleBook("1Kor", "Pál első levele a korinthusiakhoz"),
    BibleBook("2Kor", "Pál második levele a korinthusiakhoz"),
    BibleBook("Gal", "Pál levele a galatákhoz"),
    BibleBook("Ef", "Pál levele az efezusiakkoz"),
    BibleBook("Fil", "Pál levele a filippiekhez"),
    BibleBook("Kol", "Pál levele a kolosséiakhoz"),
    BibleBook("1Thessz", "Pál első levele a thesszalonikaiakhoz"),
    BibleBook("2Thessz", "Pál második levele a thesszalonikaiakhoz"),
    BibleBook("1Tim", "Pál első levele Timóteushoz"),
    BibleBook("2Tim", "Pál második levele Timóteushoz"),
    BibleBook("Tit", "Pál levele Tituszhoz"),
    BibleBook("Filem", "Pál levele Filemonhoz"),
    BibleBook("Zsid", "A zsidókhoz írt levél"),
    BibleBook("Jak", "Jakab levele"),
    BibleBook("1Pt", "Péter első levele"),
    BibleBook("2Pt", "Péter második levele"),
    BibleBook("1Jn", "János első levele"),
    BibleBook("2Jn", "János második levele"),
    BibleBook("3Jn", "János harmadik levele"),
    BibleBook("Júd", "Júdás levele"),
    BibleBook("Jel", "A jelenések könyve"),
]


def get_bible_books() -> list[BibleBook]:
    """All 66 books in canonical order (Old Testament then New Testament)."""
    return [*_OLD_TESTAMENT, *_NEW_TESTAMENT]


def get_bible_books_old_testament() -> list[BibleBook]:
    """The 39 Old Testament books."""
    return list(_OLD_TESTAMENT)


def get_bible_books_new_testament() -> list[BibleBook]:
    """The 27 New Testament books."""
    return list(_NEW_TESTAMENT)
