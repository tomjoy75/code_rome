# 🧭 Code ROME CLI – France Travail (Local CSV Version)

## 📘 Overview

**Code ROME CLI** is a lightweight Python command-line tool that lets you search for French job classifications (ROME codes) by keyword — e.g. `devops`, `plumber`, `teacher`.
Instead of calling France Travail’s API (which is not publicly available), it uses **official CSV datasets** published by France Travail.

This approach ensures full offline functionality and avoids OAuth2 authentication or API downtime issues.

---

## 🎯 Goals

- Parse and index official France Travail ROME CSV files
- Search locally by keyword in job titles or appellations
- Return results as structured JSON
- Optionally export them to a Markdown file

Example output:

```json
{
  "query": "devops",
  "results": [
    {
      "code": "M1805",
      "libelle": "Études et développement informatique"
    }
  ]
}
```

---

## 🧱 Project Structure

```bash
code_rome/
├── code_rome.py         # CLI entry point
├── rome_loader.py       # CSV loading and validation
├── rome_search.py       # Keyword search logic
├── formatter.py         # Markdown formatting
├── data/                # Official France Travail CSV files
│   ├── rome_metiers.csv
│   └── rome_appellations.csv
├── tests/
│   ├── test_cli.py
│   ├── test_loader.py
│   └── test_search.py
└── README.md
```

---

## 🚀 Usage

```bash
# Basic usage
python3 code_rome.py devops

# Custom output file
python3 code_rome.py devops -o my_results.md
```

---

## 🧩 Missions (Development Steps)

```
Mission	Description	Output
1	Initialize the project and pytest	✅
2	Implement CLI with argparse and tests	✅
2.5	Explore and validate France Travail data sources	✅
3	Implement CSV loader (rome_loader.py)	CSV read & validation
4	Implement local search (rome_search.py)	JSON search result
5	Integrate search into CLI	Printed or saved results
6	Add Markdown export (formatter.py)	.md file output
```

---

## 🧠 Design Notes

- **No external API calls.**
The France Travail ROME endpoints (api.pole-emploi.io, api.francetravail.io/partenaire/rome-metiers) are not exposed.

- **Data source:**
https://francetravail.io/produits-partages/rome

- **Error handling:**
Gracefully handle missing data, empty results, or malformed CSV lines.

---

## 🧪 Testing

All tests are handled through ##pytest##.
Each module has its own dedicated test file, following the TDD approach:
```bash
pytest -v
```

---

## 🗂 Commit Philosophy
This project follows atomic commits — one logical change per commit:

```git
add: create rome_loader skeleton
test: add failing test for search_rome()
feat: implement CSV search logic
fix: handle missing CSV or invalid keyword
refactor: clean up CLI integration
```

---

## 📄 License

MIT License © 2025 – Open educational project based on public France Travail datasets.
https://www.data.gouv.fr/datasets/repertoire-operationnel-des-metiers-et-des-emplois-rome/
