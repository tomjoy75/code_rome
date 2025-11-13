"""Tests for formatter exports."""

import json

from formatter import format_as_json, format_as_markdown


def _sample_results() -> list[dict]:
    return [
        {
            "code_rome": "A1101",
            "libelle": "Conduite d'engins agricoles et forestiers",
            "code_rome_parent": "A110",
            "libelle_parent": "Travaux agricoles et forestiers",
        },
        {
            "code_rome": "B3202",
            "libelle": "Conception de produits industriels",
            "code_rome_parent": "B320",
            "libelle_parent": "Études et conception en mécanique industrielle",
        },
    ]


def test_format_as_markdown_with_results():
    results = _sample_results()

    rendered = format_as_markdown(results)

    expected_lines = ["## Résultats de la recherche ROME"]
    expected_lines.extend(
        [
            "- [A1101] Conduite d'engins agricoles et forestiers (parent: Travaux agricoles et forestiers)",
            "- [B3202] Conception de produits industriels (parent: Études et conception en mécanique industrielle)",
        ]
    )
    assert rendered == "\n".join(expected_lines)


def test_format_as_markdown_without_results():
    rendered = format_as_markdown([])

    assert rendered == "## Résultats de la recherche ROME\n- Aucun résultat"


def test_format_as_json_with_results():
    results = _sample_results()

    rendered = format_as_json(results)

    expected = json.dumps(results, ensure_ascii=False, indent=2)
    assert rendered == expected


def test_format_as_json_without_results():
    rendered = format_as_json([])

    assert rendered == json.dumps([], ensure_ascii=False, indent=2)
