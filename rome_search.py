def search_in_appellations(keyword: str, appellations: list[dict]) -> set[str]:
    """Return a set of code_rome values where the keyword matches
    an appellation (libelle_appellation_long or libelle_appellation_court).
    """
    codes = set()
    keyword_lower = keyword.casefold()
    for row in appellations:
        libelle_long = row.get("libelle_appellation_long", "")
        libelle_short = row.get("libelle_appellation_court", "")
        if keyword_lower in libelle_long.casefold() or keyword_lower in libelle_short.casefold():
            codes.add(row["code_rome"])
    return codes

def get_rome_details(codes: set[str], referentiel: dict[str,dict]) -> list[dict]:
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

def search_rome(keyword: str, data: list[dict]) -> list[dict]:
    """Return matching ROME entries for a given keyword."""
