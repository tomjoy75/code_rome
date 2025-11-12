"""code_rome.py - minimal CLI to question the France Travail Code ROME"""
import argparse
import logging

from utils import build_referentiel
from rome_loader import load_csv
from rome_search import search_in_appellations, get_rome_details


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


def main():
    """Parse command-line arguments and print selected job/output."""
    parser = argparse.ArgumentParser()
    parser.add_argument("job", help="job you're making an api request to obtain the ROME code")
    parser.add_argument("-o", "--output", type=str, help="output file name")
    parser.add_argument("-v", "--verbose", action="store_true", help="enable verbose output")
    args = parser.parse_args()
    if args.output is None:
        args.output = args.job + ".md"
    _configure_logger(args.verbose)
    # print(f"Selected job is {args.job} and output file is {args.output}")
    # Construct the code ROME referentiel
    referentiel = build_referentiel(load_csv("data/RefRomeCsv/unix_referentiel_code_rome_v460_utf8.csv"))
    logger.info("Referentiel loaded with %d entries.", len(referentiel))
    # Search for the job in the appelation data
    matching_codes = search_in_appellations(args.job, load_csv("data/RefRomeCsv/unix_referentiel_appellation_v460_utf8.csv"))
    logger.info("Found %d matching ROME codes for job '%s'.", len(matching_codes), args.job)
    # Get the details for the matching codes
    matching_details = get_rome_details(matching_codes, referentiel)
    logger.info("Retrieved details for %d ROME codes.", len(matching_details))
    # Print the results to the output file
    with open(args.output, "w", encoding="utf-8") as f:
        for entry in matching_details:
            logger.info("Entry written: %s", entry)
            f.write(f"## {entry['code_rome']} - {entry['libelle']}\n")
            f.write(f"- Code ROME parent: {entry['code_rome_parent']} - {entry['libelle_parent']}\n\n")
    print(f"Selected job is {args.job} and output file is {args.output}")

if __name__=="__main__":
    main()
