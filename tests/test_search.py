from __future__ import annotations

import csv
from pathlib import Path

import pytest

from rome_search import NoSearchResultsError, search_in_appellations, search_rome

appellations = [
    {"libelle_appellation_long": "Ingénieur DevOps", "libelle_appellation_court": "DevOps", "code_rome": "M1827"},
    {"libelle_appellation_long": "Plombier", "libelle_appellation_court": "Plombier", "code_rome": "F1234"},
]


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    """Helper used to produce deterministic CSV fixtures."""

    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def test_search_in_appellations_found():
    result = search_in_appellations("devops", appellations)
    assert result == {"M1827"}


def test_search_in_appellations_not_found():
    result = search_in_appellations("astronaut", appellations)
    assert result == set()


def test_search_rome_returns_enriched_results(tmp_path: Path):
    data_dir = tmp_path
    write_csv(
        data_dir / "unix_referentiel_appellation_v460_utf8.csv",
        ["libelle_appellation_long", "libelle_appellation_court", "code_rome"],
        [
            {
                "libelle_appellation_long": "Ingénieur DevOps",
                "libelle_appellation_court": "DevOps",
                "code_rome": "M1827",
            }
        ],
    )
    write_csv(
        data_dir / "unix_referentiel_code_rome_v460_utf8.csv",
        ["code_rome", "libelle_rome", "code_rome_parent"],
        [
            {
                "code_rome": "M1800",
                "libelle_rome": "Systèmes d'information",
                "code_rome_parent": "M1800",
            },
            {
                "code_rome": "M1827",
                "libelle_rome": "Ingénierie DevOps",
                "code_rome_parent": "M1800",
            },
        ],
    )

    results = search_rome("devops", data_dir)

    assert results == [
        {
            "code_rome": "M1827",
            "libelle": "Ingénierie DevOps",
            "code_rome_parent": "M1800",
            "libelle_parent": "Systèmes d'information",
        }
    ]


def test_search_rome_raises_when_no_match(tmp_path: Path):
    data_dir = tmp_path
    write_csv(
        data_dir / "unix_referentiel_appellation_v460_utf8.csv",
        ["libelle_appellation_long", "libelle_appellation_court", "code_rome"],
        [],
    )
    write_csv(
        data_dir / "unix_referentiel_code_rome_v460_utf8.csv",
        ["code_rome", "libelle_rome", "code_rome_parent"],
        [],
    )

    with pytest.raises(NoSearchResultsError):
        search_rome("astronaut", data_dir)


def test_search_rome_rejects_blank_keyword(tmp_path: Path):
    data_dir = tmp_path
    write_csv(
        data_dir / "unix_referentiel_appellation_v460_utf8.csv",
        ["libelle_appellation_long", "libelle_appellation_court", "code_rome"],
        [],
    )
    write_csv(
        data_dir / "unix_referentiel_code_rome_v460_utf8.csv",
        ["code_rome", "libelle_rome", "code_rome_parent"],
        [],
    )

    with pytest.raises(ValueError):
        search_rome("   ", data_dir)

