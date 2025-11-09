"""code_rome.py - minimal CLI to question the France Travail Code ROME"""
import argparse

"""Parse command-line arguments and print selected job/output."""
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("job", help="job you're making an api request to obtain the ROME code")
    parser.add_argument("-o", "--output", type=str, help="output file name")
    args = parser.parse_args()
#    if len(sys.argv) not in [2,4]:
#        print("Usage: python3 code_rome.py devops -o devops.md")
#        sys.exit(1)
    if args.output is None:
        args.output = args.job + ".md"
    print(f"Selected job is {args.job} and output file is {args.output}")

if __name__=="__main__":
    main()
