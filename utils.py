def build_referentiel(data: list[dict])-> dict[str, dict]:
    """Transform the CSV data into into a mapping {code_rome: {...fields..}}"""
    ref = {}
    for row in data:
        ref[row["code_rome"]] = {"libelle":row["libelle_rome"], "code_rome_parent": row["code_rome_parent"]}
#    print("TEST : K1511 ->", ref["K1511"]["libelle"])
    return ref

