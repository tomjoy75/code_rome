"""Utilities for enriching ROME search results with contextual data."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable

EnrichmentData = dict[str, list[dict]]


ENRICHMENT_FILES: dict[str, tuple[str, bool]] = {
    "texte": ("unix_texte_v460_utf8.csv", True),
    "competences": ("unix_referentiel_competence_v460_utf8.csv", True),
    "savoirs": ("unix_referentiel_savoir_v460_utf8.csv", True),
    "contextes": ("unix_referentiel_contexte_travail_v460_utf8.csv", True),
    "mobilites": ("unix_rubrique_mobilite_v460_utf8.csv", True),
    "centres_interet": ("unix_centre_interet_v460_utf8.csv", True),
    "arborescence_centres": ("unix_arborescence_centre_interet_v460_utf8.csv", False),
}


def _read_csv(path: Path, require_code: bool) -> list[dict]:
    """Return a list of dictionaries loaded from ``path``.

    Args:
        path: CSV file to load.
        require_code: Whether a ``code_rome`` column must be present.

    Returns:
        Parsed rows as dictionaries preserving the file order.
    """

    with path.open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        fieldnames = reader.fieldnames or []
        if require_code and "code_rome" not in fieldnames:
            raise ValueError(f"Missing 'code_rome' column in {path.name}")
        return [row for row in reader]


def load_enrichment_data(base_path: Path) -> EnrichmentData:
    """Load all datasets required to enrich a ROME entry.

    Args:
        base_path: Directory where enrichment CSV files are stored.

    Returns:
        A mapping containing the enrichment datasets.
    """

    data: EnrichmentData = {}
    for key, (filename, require_code) in ENRICHMENT_FILES.items():
        dataset_path = base_path / filename
        data[key] = _read_csv(dataset_path, require_code)
    return data


def _first_matching(rows: Iterable[dict], code: str, column: str) -> str:
    """Return the first non-empty value for ``column`` matching ``code``."""

    for row in rows:
        if row.get("code_rome") == code:
            value = (row.get(column) or "").strip()
            if value:
                return value
    return ""


def _collect_values(rows: Iterable[dict], code: str, column: str) -> list[str]:
    """Collect all non-empty ``column`` values for ``code`` preserving order."""

    values: list[str] = []
    for row in rows:
        if row.get("code_rome") != code:
            continue
        value = (row.get(column) or "").strip()
        if value:
            values.append(value)
    return values


def enrich_rome_entry(entry: dict, data: EnrichmentData) -> dict:
    """Return a copy of ``entry`` enriched with contextual ROME data.

    Args:
        entry: Base ROME entry containing at least ``code_rome``.
        data: Enrichment datasets previously loaded.

    Returns:
        A new dictionary merging the base entry with enrichment values.
    """

    code = entry.get("code_rome")
    if not code:
        raise ValueError("ROME entry must define 'code_rome'.")

    enriched = dict(entry)
    enriched["description"] = _first_matching(data.get("texte", []), code, "libelle_texte")
    enriched["competences"] = _collect_values(
        data.get("competences", []), code, "libelle_competence"
    )
    enriched["savoirs"] = _collect_values(data.get("savoirs", []), code, "libelle_savoir")
    enriched["contextes_travail"] = _collect_values(
        data.get("contextes", []), code, "libelle_contexte_travail"
    )
    enriched["mobilites"] = _collect_values(
        data.get("mobilites", []), code, "libelle_mobilite"
    )

    arbo_lookup = {
        row.get("code_arborescence"): (row.get("libelle_arborescence") or "").strip()
        for row in data.get("arborescence_centres", [])
    }
    centres: list[str] = []
    for row in data.get("centres_interet", []):
        if row.get("code_rome") != code:
            continue
        centre_label = (row.get("libelle_centre_interet") or "").strip()
        arbo_label = arbo_lookup.get(row.get("code_arborescence"), "")
        if arbo_label and centre_label:
            centres.append(f"{arbo_label} — {centre_label}")
        elif centre_label:
            centres.append(centre_label)
        elif arbo_label:
            centres.append(arbo_label)
    enriched["centres_interet"] = centres

    return enriched
