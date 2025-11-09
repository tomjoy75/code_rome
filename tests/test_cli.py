import pytest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from code_rome import main

def test_no_output(monkeypatch, capsys):
    monkeypatch.setattr(sys, 'argv', [ sys.argv[0], "devops" ])
    main()
    captured = capsys.readouterr()
    assert captured.out == "Selected job is devops and output file is devops.md\n"

def test_w_output(monkeypatch, capsys):
    monkeypatch.setattr(sys, 'argv', [ sys.argv[0], "devops" , "-o", "dev.md" ])
    main()
    captured = capsys.readouterr()
    assert captured.out == "Selected job is devops and output file is dev.md\n"

def test_no_args(monkeypatch, capsys):
    monkeypatch.setattr(sys, 'argv', [ sys.argv[0] ])
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "the following arguments are required: job" in captured.err

