"""Interactive CLI tests for Code ROME."""

from __future__ import annotations

import os
import shutil
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from code_rome import main  # noqa: E402  pylint: disable=wrong-import-position
from rome_search import NoSearchResultsError  # noqa: E402  pylint: disable=wrong-import-position


@pytest.fixture()
def interactive_workspace(tmp_path, monkeypatch):
    """Run interactive CLI tests from an isolated working directory."""

    monkeypatch.chdir(tmp_path)
    yield tmp_path
    output_dir = tmp_path / "output"
    if output_dir.exists():
        shutil.rmtree(output_dir)


def _set_inputs(monkeypatch, values: list[str]) -> None:
    """Provide deterministic responses for input prompts."""

    iterator = iter(values)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(iterator))


def test_interactive_generates_markdown(interactive_workspace, monkeypatch, capsys):
    """Interactive run should create a Markdown export when requested."""

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

    _set_inputs(monkeypatch, ["developpeur", "md", ""])
    monkeypatch.setattr(sys, "argv", [sys.argv[0]])

    main()

    captured = capsys.readouterr()
    assert "Mode interactif activé." in captured.out
    assert "Fichier généré : output/developpeur.md (2 résultats)" in captured.out
    assert "Fin du mode interactif." in captured.out

    output_path = interactive_workspace / "output" / "developpeur.md"
    assert output_path.exists()
    content = output_path.read_text(encoding="utf-8").splitlines()
    assert content[0] == "## Résultats de la recherche ROME"
    assert content[1].startswith("- [M1805]")


def test_interactive_no_results(interactive_workspace, monkeypatch, capsys):
    """No results should avoid creating exports and notify the user."""

    def _raise_no_results(term: str) -> list[dict]:  # noqa: D401
        raise NoSearchResultsError("nothing found")

    monkeypatch.setattr("code_rome.search_rome", _raise_no_results)
    monkeypatch.setattr("code_rome._configure_logger", lambda verbose: None)

    _set_inputs(monkeypatch, ["astronaute", "md", ""])
    monkeypatch.setattr(sys, "argv", [sys.argv[0]])

    main()

    captured = capsys.readouterr()
    assert "Aucun résultat trouvé pour astronaute" in captured.out
    output_dir = interactive_workspace / "output"
    assert not output_dir.exists()


def test_interactive_format_none_skips_file(interactive_workspace, monkeypatch, capsys):
    """Format none should keep results in memory without writing a file."""

    fake_results = [
        {
            "code_rome": "F1103",
            "libelle": "Plombier",
            "libelle_parent": "Installation d'équipements sanitaires",
        }
    ]
    monkeypatch.setattr("code_rome.search_rome", lambda term: fake_results)
    monkeypatch.setattr("code_rome._configure_logger", lambda verbose: None)

    _set_inputs(monkeypatch, ["plombier", "none", ""])
    monkeypatch.setattr(sys, "argv", [sys.argv[0]])

    main()

    captured = capsys.readouterr()
    assert "Aucun fichier généré pour plombier (format none, 1 résultat)" in captured.out
    output_dir = interactive_workspace / "output"
    assert not output_dir.exists()

