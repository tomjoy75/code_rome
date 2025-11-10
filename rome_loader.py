import csv

def load_csv(path: str) -> list[dict]:
    """Load a ROME CSV file and return it as a list of dicts."""
#    raise NotImplementedError("load_csv not implemented yet")
    with open(path, mode='r', errors='ignore') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)


