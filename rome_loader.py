import csv, os

def load_csv(path: str) -> list[dict]:
    """Load a ROME CSV file and return it as a list of dicts."""
#    raise NotImplementedError("load_csv not implemented yet")
    if not os.path.exists(path):
        raise FileNotFoundError(f"No such file: {path}")
    with open(path, mode='r', errors='ignore') as csvfile:
        reader = csv.DictReader(csvfile)
        if not reader.fieldnames:
            return []
        required_columns = {"code_rome"}
        if not required_columns.issubset(reader.fieldnames):
            raise ValueError(f"Invalid CSV structure: missing {required_columns - set(reader.fieldnames)}")
        rows = list(reader)
        if not rows:
            return []
        return rows


