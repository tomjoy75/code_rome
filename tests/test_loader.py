from rome_loader import load_csv

"""def test_load_csv():
    try:
        load_csv("data/RefRomeCsv/unix_referentiel_code_rome_v460_utf8.csv")
    except NotImplementedError:
        assert False
    assert True
"""

def test_load_csv():
    load_csv("data/RefRomeCsv/unix_referentiel_code_rome_v460_utf8.csv")
