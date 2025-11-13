from __future__ import annotations

from rome_enrichment import enrich_rome_entry, load_enrichment_data
from rome_search import DEFAULT_DATA_DIR, search_rome


def test_enrichment_for_known_job() -> None:
    results = search_rome("engins agricoles")
    matching = [entry for entry in results if entry["code_rome"] == "A1101"]
    assert matching, "Expected at least one entry for code A1101"

    enriched = matching[0]
    assert enriched["description"]
    assert enriched["competences"], "Competences should not be empty"
    assert enriched["savoirs"], "Savoirs should not be empty"
    assert enriched["contextes_travail"], "Contextes de travail should not be empty"


def test_enrichment_returns_empty_values_when_missing() -> None:
    data_dir = DEFAULT_DATA_DIR
    enrichment_data = load_enrichment_data(data_dir)

    base_entry = {
        "code_rome": "Z9999",
        "libelle": "Métier inconnu",
        "code_rome_parent": "Z9999",
        "libelle_parent": "Parent inconnu",
    }

    enriched = enrich_rome_entry(base_entry, enrichment_data)

    assert enriched["description"] == ""
    assert enriched["competences"] == []
    assert enriched["savoirs"] == []
    assert enriched["contextes_travail"] == []
    assert enriched["mobilites"] == []
    assert enriched["centres_interet"] == []
