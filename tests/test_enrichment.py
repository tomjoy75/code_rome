from __future__ import annotations

from rome_enrichment import enrich_rome_entry, load_enrichment_data
from rome_search import DEFAULT_DATA_DIR, search_rome


def test_enrichment_for_known_job() -> None:
    """Ensure enrichment works for a known ROME job using official datasets."""
    results = search_rome("engins agricoles")
    matching = [entry for entry in results if entry["code_rome"] == "A1101"]
    assert matching, "Expected at least one entry for code A1101"

    enriched = matching[0]
    assert enriched["description"]

    # Les compétences peuvent être vides selon le dataset officiel
    assert isinstance(enriched["competences"], list)
    assert isinstance(enriched["savoirs"], list)
    assert isinstance(enriched["contextes_travail"], list)

    # On vérifie simplement que la structure d'enrichissement reste cohérente
    for field in ["mobilites", "centres_interet"]:
        assert field in enriched


def test_enrichment_returns_empty_values_when_missing() -> None:
    """Ensure enrichment returns empty structures when data is missing."""
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
    assert isinstance(enriched["competences"], list)
    assert isinstance(enriched["savoirs"], list)
    assert isinstance(enriched["contextes_travail"], list)
    assert isinstance(enriched["mobilites"], list)
    assert isinstance(enriched["centres_interet"], list)
