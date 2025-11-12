"""CLI integration tests for the Code ROME tool."""

from __future__ import annotations

import json
import os
import shutil
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from code_rome import main  # noqa: E402  pylint: disable=wrong-import-position
from rome_search import NoSearchResultsError  # noqa: E402  pylint: disable=wrong-import-position


@pytest.fixture()
def cli_workspace(tmp_path, monkeypatch):
    """Run CLI tests from an isolated temporary directory."""

    monkeypatch.chdir(tmp_path)
    yield tmp_path
    output_dir = tmp_path / "output"
    if output_dir.exists():
        shutil.rmtree(output_dir)


def test_cli_generates_markdown(cli_workspace, monkeypatch, capsys):
    """Default run should export Markdown with the heading and bullet list."""

    fake_results = [
        {
            "code_rome": "M1805",
            "libelle": "Ingénieur DevOps",
            "libelle_parent": "Études et développement informatique",
        },
        {
            "code_rome": "M1806",
            "libelle": "Ingénieur Cloud",
            "libelle_parent": "Études et développement informatique",
        },
    ]
    monkeypatch.setattr("code_rome.search_rome", lambda term: fake_results)
    monkeypatch.setattr("code_rome._configure_logger", lambda verbose: None)

    monkeypatch.setattr(sys, "argv", [sys.argv[0], "devops"])
    main()

    captured = capsys.readouterr()
    assert captured.out == "Selected job is devops and output file is output/devops.md\n"

    output_path = cli_workspace / "output" / "devops.md"
    expected = "\n".join(
        [
            "## Résultats de la recherche ROME",
            "- [M1805] Ingénieur DevOps (parent: Études et développement informatique)",
            "- [M1806] Ingénieur Cloud (parent: Études et développement informatique)",
        ]
    )
    assert output_path.read_text(encoding="utf-8") == expected


def test_cli_generates_json(cli_workspace, monkeypatch, capsys):
    """JSON format flag should create an indented JSON export."""

    fake_results = [
        {
            "code_rome": "M1805",
            "libelle": "Ingénieur DevOps",
            "libelle_parent": "Études et développement informatique",
        }
    ]
    monkeypatch.setattr("code_rome.search_rome", lambda term: fake_results)
    monkeypatch.setattr("code_rome._configure_logger", lambda verbose: None)

    monkeypatch.setattr(sys, "argv", [sys.argv[0], "devops", "--format", "json"])
    main()

    captured = capsys.readouterr()
    assert captured.out == "Selected job is devops and output file is output/devops.json\n"

    output_path = cli_workspace / "output" / "devops.json"
    assert json.loads(output_path.read_text(encoding="utf-8")) == fake_results


def test_cli_no_results_avoids_creating_file(cli_workspace, monkeypatch, capsys):
    """The CLI should not create any export when no result is found."""

    def _raise_no_results(term: str):  # noqa: D401
        raise NoSearchResultsError("nothing")

    monkeypatch.setattr("code_rome.search_rome", _raise_no_results)
    monkeypatch.setattr("code_rome._configure_logger", lambda verbose: None)

    monkeypatch.setattr(sys, "argv", [sys.argv[0], "devops"])
    main()

    captured = capsys.readouterr()
    assert captured.out == "Aucun résultat trouvé pour devops\n"

    output_dir = cli_workspace / "output"
    assert not output_dir.exists()


def test_cli_unknown_format(monkeypatch, capsys):
    """Unknown format value should trigger argparse validation error."""

    monkeypatch.setattr(sys, "argv", [sys.argv[0], "devops", "--format", "xml"])
    with pytest.raises(SystemExit):
        main()

    captured = capsys.readouterr()
    assert "invalid choice" in captured.err
    assert "(choose from 'md', 'json')" in captured.err
