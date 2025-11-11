from rome_search import search_in_appellations
appellations = [
    {"libelle_appellation_long": "Ingénieur DevOps", "libelle_appellation_court": "DevOps", "code_rome": "M1827"},
    {"libelle_appellation_long": "Plombier", "libelle_appellation_court": "Plombier", "code_rome": "F1234"},
]

def test_search_in_appellations_found():
    result = search_in_appellations("devops", appellations)
    assert result == {"M1827"}

def test_search_in_appellations_not_found():
    result = search_in_appellations("astronaut", appellations)
    assert result == set()

