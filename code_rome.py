"""Command-line interface to search and export France Travail ROME data."""

from __future__ import annotations

import argparse
import logging
import os
from pathlib import Path
from typing import Callable

from formatter import format_as_json, format_as_markdown
from rome_search import NoSearchResultsError, search_rome


logger = logging.getLogger(__name__)


def _configure_logger(verbose: bool) -> None:
    """Configure module logger according to verbosity flag."""
    level = logging.INFO if verbose else logging.WARNING
    logger.setLevel(level)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(handler)
    logger.propagate = False


def _ensure_output_directory() -> Path:
    """Create the output directory if it does not exist and return its path."""

    os.makedirs("output", exist_ok=True)
    return Path("output")


def _resolve_output_path(job: str, explicit: str | None, chosen_format: str) -> Path:
    """Return the output path based on user arguments."""

    base_name = explicit or job
    sanitized_name = Path(base_name).stem or job
    extension = "md" if chosen_format == "md" else "json"
    file_name = f"{sanitized_name}.{extension}"
    return Path(os.path.join("output", file_name))


def _select_formatter(chosen_format: str) -> Callable[[list[dict]], str]:
    """Return the formatter function matching the CLI flag."""

    if chosen_format == "json":
        return format_as_json
    return format_as_markdown


def main() -> None:
    """Parse command-line arguments, orchestrate search, and export results."""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "job",
        help="job you're making an api request to obtain the ROME code",
    )
    parser.add_argument("-o", "--output", type=str, help="output file name")
    parser.add_argument(
        "-f",
        "--format",
        choices=("md", "json"),
        default="md",
        help="output format: md (default) or json",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="enable verbose output")
    args = parser.parse_args()

    _configure_logger(args.verbose)

    formatter = _select_formatter(args.format)

    try:
        results = search_rome(args.job)
    except NoSearchResultsError as error:
        logger.info("No results found for '%s': %s", args.job, error)
        print(f"Aucun résultat trouvé pour {args.job}")
        return

    if not results:
        logger.info("Search returned an empty result set for '%s'.", args.job)
        print(f"Aucun résultat trouvé pour {args.job}")
        return

    _ensure_output_directory()
    output_path = _resolve_output_path(args.job, args.output, args.format)
    content = formatter(results)
    logger.info("Prepared %d results for export.", len(results))
    output_path.write_text(content, encoding="utf-8")

    print(f"Selected job is {args.job} and output file is {output_path}")

if __name__=="__main__":
    main()
