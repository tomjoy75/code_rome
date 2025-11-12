"""Business logic helpers for searching ROME datasets."""

from __future__ import annotations

from pathlib import Path

from rome_loader import load_csv
from utils import build_referentiel


class NoSearchResultsError(Exception):
    """Raised when a ROME search finishes without any matching entries."""


DEFAULT_DATA_DIR = Path("data/RefRomeCsv")
APPELLATIONS_FILENAME = "unix_referentiel_appellation_v460_utf8.csv"
ROME_CODES_FILENAME = "unix_referentiel_code_rome_v460_utf8.csv"


def _coerce_directory(data_dir: str | Path | None) -> Path:
    """Return a concrete directory path, defaulting to the bundled dataset."""

    if data_dir is None:
        return DEFAULT_DATA_DIR
    if isinstance(data_dir, Path):
        return data_dir
    return Path(data_dir)


def search_in_appellations(keyword: str, appellations: list[dict]) -> set[str]:
    """Return a set of code_rome values where the keyword matches
    an appellation (libelle_appellation_long or libelle_appellation_court).
    """
    codes = set()
    for row in appellations:
        if keyword.casefold() in row.get("libelle_appellation_long").casefold() or keyword.casefold() in row.get("libelle_appellation_court").casefold():
            codes.add(row["code_rome"])
    return codes

def get_rome_details(codes: set[str], referentiel: dict[str, dict]) -> list[dict]:
    """Return detailed ROME entries (code + libelle) for given code_rome values.
    """
    details = []
    for code in codes:
        if code in referentiel:
            code_parent = referentiel[code]["code_rome_parent"]
            if code_parent != code:
                libelle_parent = referentiel[code_parent]["libelle"] 
            else:
                libelle_parent = "N/A"
            details.append({"code_rome": code, "libelle": referentiel[code]["libelle"], "code_rome_parent": code_parent, "libelle_parent": libelle_parent})
    return details

def _load_appellations(directory: Path) -> list[dict]:
    """Load the appellations referential from the provided directory."""

    return load_csv(str(directory / APPELLATIONS_FILENAME))


def _load_referentiel(directory: Path) -> dict[str, dict]:
    """Load and transform the ROME referential."""

    raw_codes = load_csv(str(directory / ROME_CODES_FILENAME))
    return build_referentiel(raw_codes)


def search_rome(keyword: str, data: str | Path | None = None) -> list[dict]:
    """Return matching ROME entries for a given keyword.

    Args:
        keyword: Term provided by the user.
        data: Optional directory overriding the default referential location.

    Returns:
        A list of dictionaries containing enriched ROME data.

    Raises:
        ValueError: When ``keyword`` is empty or blank.
        NoSearchResultsError: If no ROME entry matches the keyword.
    """

    if not keyword or not keyword.strip():
        raise ValueError("Keyword must be a non-empty string.")

    directory = _coerce_directory(data)
    appellations = _load_appellations(directory)
    referentiel = _load_referentiel(directory)

    matching_codes = search_in_appellations(keyword, appellations)
    if not matching_codes:
        raise NoSearchResultsError(f"No ROME entry matches keyword '{keyword}'.")

    return get_rome_details(matching_codes, referentiel)
