from __future__ import annotations

import csv
from pathlib import Path

import pytest

from rome_search import NoSearchResultsError, search_in_appellations, search_rome

appellations = [
    {
        "libelle_appellation_long": "Ingénieur DevOps",
        "libelle_appellation_court": "DevOps",
        "code_rome": "M1827",
    },
    {
        "libelle_appellation_long": "Plombier",
        "libelle_appellation_court": "Plombier",
        "code_rome": "F1234",
    },
]


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    """Helper used to produce deterministic CSV fixtures."""

    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_enrichment_csvs(data_dir: Path, code: str | None) -> None:
    """Create the enrichment CSV files required by ``search_rome``."""

    rows = (
        [{"code_rome": code, "libelle_texte": "Ingénieur DevOps cloud."}]
        if code
        else []
    )
    write_csv(
        data_dir / "unix_texte_v460_utf8.csv",
        ["code_rome", "libelle_texte"],
        rows,
    )

    competence_rows = (
        [
            {"code_rome": code, "libelle_competence": "Automatiser les déploiements"},
            {"code_rome": code, "libelle_competence": "Superviser les infrastructures"},
        ]
        if code
        else []
    )
    write_csv(
        data_dir / "unix_referentiel_competence_v460_utf8.csv",
        ["code_rome", "libelle_competence"],
        competence_rows,
    )

    savoir_rows = (
        [
            {"code_rome": code, "libelle_savoir": "Savoir configurer un pipeline CI/CD"},
        ]
        if code
        else []
    )
    write_csv(
        data_dir / "unix_referentiel_savoir_v460_utf8.csv",
        ["code_rome", "libelle_savoir"],
        savoir_rows,
    )

    contexte_rows = (
        [
            {
                "code_rome": code,
                "libelle_contexte_travail": "Travail en équipe produit",
            }
        ]
        if code
        else []
    )
    write_csv(
        data_dir / "unix_referentiel_contexte_travail_v460_utf8.csv",
        ["code_rome", "libelle_contexte_travail"],
        contexte_rows,
    )

    mobilite_rows = (
        [
            {
                "code_rome": code,
                "libelle_mobilite": "Mobilité vers ingénieur systèmes",
            }
        ]
        if code
        else []
    )
    write_csv(
        data_dir / "unix_rubrique_mobilite_v460_utf8.csv",
        ["code_rome", "libelle_mobilite"],
        mobilite_rows,
    )

    centres_rows = (
        [
            {
                "code_rome": code,
                "code_centre_interet": "CI01",
                "libelle_centre_interet": "Technologies innovantes",
                "code_arborescence": "ARB01",
            },
            {
                "code_rome": code,
                "code_centre_interet": "CI02",
                "libelle_centre_interet": "Résolution de problèmes",
                "code_arborescence": "ARB02",
            },
        ]
        if code
        else []
    )
    write_csv(
        data_dir / "unix_centre_interet_v460_utf8.csv",
        [
            "code_rome",
            "code_centre_interet",
            "libelle_centre_interet",
            "code_arborescence",
        ],
        centres_rows,
    )

    arbo_rows = (
        [
            {"code_arborescence": "ARB01", "libelle_arborescence": "Innovation"},
            {"code_arborescence": "ARB02", "libelle_arborescence": "Analyse"},
        ]
        if code
        else []
    )
    write_csv(
        data_dir / "unix_arborescence_centre_interet_v460_utf8.csv",
        ["code_arborescence", "libelle_arborescence"],
        arbo_rows,
    )


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
    write_enrichment_csvs(data_dir, "M1827")

    results = search_rome("devops", data_dir)

    assert results == [
        {
            "code_rome": "M1827",
            "libelle": "Ingénierie DevOps",
            "code_rome_parent": "M1800",
            "libelle_parent": "Systèmes d'information",
            "description": "Ingénieur DevOps cloud.",
            "competences": [
                "Automatiser les déploiements",
                "Superviser les infrastructures",
            ],
            "savoirs": ["Savoir configurer un pipeline CI/CD"],
            "contextes_travail": ["Travail en équipe produit"],
            "mobilites": ["Mobilité vers ingénieur systèmes"],
            "centres_interet": [
                "Innovation — Technologies innovantes",
                "Analyse — Résolution de problèmes",
            ],
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
    write_enrichment_csvs(data_dir, None)

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
    write_enrichment_csvs(data_dir, None)

    with pytest.raises(ValueError):
        search_rome("   ", data_dir)

