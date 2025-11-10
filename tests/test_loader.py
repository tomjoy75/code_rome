from rome_loader import load_csv
import pytest

"""def test_load_csv():
    try:
        load_csv("data/RefRomeCsv/unix_referentiel_code_rome_v460_utf8.csv")
    except NotImplementedError:
        assert False
    assert True
"""

def test_load_csv():
    load_csv("data/RefRomeCsv/unix_referentiel_code_rome_v460_utf8.csv")

def test_missing_file():
    with pytest.raises(FileNotFoundError):
        load_csv("data/unix_referentiel_code_rome_v460_utf8.csv")

def test_empty_file():
    assert load_csv("tests/empty.csv") == []

def test_missing_columns(tmp_path):
    fake_csv = tmp_path / "bad.csv"
    fake_csv.write_text("foo,bar\n1,2\n", encoding="utf-8")
    with pytest.raises(ValueError):
        load_csv(str(fake_csv))
