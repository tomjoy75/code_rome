"""Utilities to format search results for export."""

from __future__ import annotations

import json
from typing import Sequence


def format_as_markdown(results: Sequence[dict]) -> str:
    """Return the ROME search results as a Markdown bullet list.

    Args:
        results: Sequence of dictionaries returned by ``search_rome``. Each
            dictionary must expose the keys ``code_rome``, ``libelle``, and
            ``libelle_parent``.

    Returns:
        A Markdown string with a heading and bullet list representation of the
        search results. When ``results`` is empty, a placeholder bullet is
        emitted to keep the output explicit.
    """

    lines: list[str] = ["## Résultats de la recherche ROME"]
    if not results:
        lines.append("- Aucun résultat")
        return "\n".join(lines)

    for entry in results:
        code = entry.get("code_rome", "?")
        label = entry.get("libelle", "")
        parent_label = entry.get("libelle_parent", "")
        lines.append(f"- [{code}] {label} (parent: {parent_label})")
    return "\n".join(lines)


def format_as_json(results: Sequence[dict]) -> str:
    """Return the ROME search results encoded as JSON.

    Args:
        results: Sequence of dictionaries returned by ``search_rome``.

    Returns:
        A JSON string with UTF-8 friendly characters and deterministic
        indentation to ease storage or diffing.
    """

    return json.dumps(list(results), ensure_ascii=False, indent=2)
