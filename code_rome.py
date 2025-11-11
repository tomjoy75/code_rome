"""code_rome.py - minimal CLI to question the France Travail Code ROME"""
import argparse
from utils import build_referentiel
from rome_loader import load_csv
from rome_search import search_in_appellations, get_rome_details

def main():
    """Parse command-line arguments and print selected job/output."""
    parser = argparse.ArgumentParser()
    parser.add_argument("job", help="job you're making an api request to obtain the ROME code")
    parser.add_argument("-o", "--output", type=str, help="output file name")
    args = parser.parse_args()
    if args.output is None:
        args.output = args.job + ".md"
    # print(f"Selected job is {args.job} and output file is {args.output}")
    # Construct the code ROME referentiel
    referentiel = build_referentiel(load_csv("data/RefRomeCsv/unix_referentiel_code_rome_v460_utf8.csv"))
    print(f"Referentiel loaded with {len(referentiel)} entries.")
    # Search for the job in the appelation data
    matching_codes = search_in_appellations(args.job, load_csv("data/RefRomeCsv/unix_referentiel_appellation_v460_utf8.csv"))
    print(f"Found {len(matching_codes)} matching ROME codes for job '{args.job}'.")
    # Get the details for the matching codes
    matching_details = get_rome_details(matching_codes, referentiel)
    print(f"Retrieved details for {len(matching_details)} ROME codes.")
    # Print the results to the output file
    with open(args.output, "w", encoding="utf-8") as f:
        for entry in matching_details:
            print(entry)
            f.write(f"## {entry['code_rome']} - {entry['libelle']}\n")
            f.write(f"- Code ROME parent: {entry['code_rome_parent']} - {entry['libelle_parent']}\n\n")

if __name__=="__main__":
    main()
