import csv, os

def _detect_delimiter(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        sample = f.read(2048)
    if not sample.strip():
        return ","
    import csv
    return csv.Sniffer().sniff(sample).delimiter

def load_csv(path: str) -> list[dict]:
    """Load a ROME CSV file and return it as a list of dicts."""
#    raise NotImplementedError("load_csv not implemented yet")
    if not os.path.exists(path):
        raise FileNotFoundError(f"No such file: {path}")
    with open(path, mode='r', errors='ignore') as csvfile:
        delimiter = _detect_delimiter(path)
        reader = csv.DictReader(csvfile, delimiter=delimiter)
        if not reader.fieldnames:
            return []
        required_columns = {"code_rome"}
        if not required_columns.issubset(reader.fieldnames):
            raise ValueError(f"Invalid CSV structure: missing {required_columns - set(reader.fieldnames)}")
        rows = list(reader)
        if not rows:
            return []
        return rows


