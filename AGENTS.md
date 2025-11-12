# Code ROME Agent Guide

## 1. Setup
- **Python**: 3.11+
- **Dépendances**: voir `requirements.txt` (standard library uniquement si le fichier est vide).
- **Commandes**
  - **Run**: `python code_rome.py --help` ou `python code_rome.py <term>`
  - **Dev**: activer un environnement virtuel, installer les dépendances `pip install -r requirements.txt`.
- **Tests**:
  - `pytest`
  - `pytest -q`
  - `pytest --maxfail=1 --disable-warnings --cov=.`
  - `PYTHONPATH=. pytest`
- **Structure**
  - `code_rome.py` — point d'entrée CLI
  - `rome_loader.py` — chargement des jeux de données CSV
  - `rome_search.py` — logique de recherche
  - `formatter.py` — formattage des résultats
  - `api.py` — intégrations externes éventuelles
  - `utils.py` — helpers transverses
  - `tests/` — tests automatisés
  - `data/` et `docs/` — ressources et documentation

## 2. Directives de style
- Respecter PEP 8 pour le formatage et l'ordre des imports (`stdlib`, `third-party`, `local`).
- Utiliser des docstrings claires au format **Google docstring style** pour les fonctions publiques.
- Exemple :

  ```python
  def fetch_job_titles(term: str, limit: int = 10) -> list[str]:
      """Return the top job titles matching a search term.

      Args:
          term: Search term provided by the user.
          limit: Maximum number of job titles to return.

      Returns:
          A list of job titles sorted by relevance.
      """
      ...
  ```
- Nommage descriptif et cohérent (snake_case pour fonctions/variables, PascalCase pour classes, CONSTANTE pour consts).
- Préserver des fonctions pures dès que possible ; le CLI ne doit contenir que l'orchestration et la gestion d'I/O.
- Lever des exceptions métier dédiées pour la gestion d'erreurs, éviter les `print` ou `sys.exit` directs en logique cœur.

## 3. Project Map
- **Entrée**: `code_rome.py` (CLI).
- **Modules**: `rome_loader`, `rome_search`, `utils`, `formatter`, `api`.
- **Flux**: chargement CSV → recherche → formatage → export.
- **Tests**: placer les tests unitaires dans `tests/` en miroir de la structure des modules.

## 4. Missions Codex types
Pour chaque mission, respecter le cycle _plan → diff → tests → commandes_.
- **Mini-refactor ciblé**: identifier la zone, appliquer les changements minimaux, couvrir par tests.
- **Implémenter une petite feature**: décrire la fonctionnalité, modifier modules concernés, ajouter tests et docs si nécessaire.
- **Ajouter un test unitaire**: expliciter le comportement validé, mettre le test dans `tests/`, exécuter `pytest`.
- **Debug guidé**: reproduire, isoler la cause, patcher avec diagnostics, valider par tests.
- **Code review PR**: analyser diff, commenter en se basant sur les règles ci-dessus, proposer corrections et vérifier tests.

## 5. Interdits
- Éviter toute dépendance lourde ou inutile.
- Ne pas modifier l'API publique sans plan de migration validé.
- Ne jamais introduire de secrets ou credentials en clair.

## 6. Sécurité
- Toujours valider et assainir les chemins fichiers reçus en entrée.
- Utiliser l'encodage UTF-8 et ouvrir les CSV avec `newline=''` pour éviter les corruptions.
- N'écrire aucun fichier en dehors du dossier autorisé du projet.

## 7. Documentation
- Maintenir le `README.md` à jour pour toute fonctionnalité visible.
- Documenter les évolutions de ce `AGENTS.md` en gardant le format et la numérotation.

## 8. Workflow Codex
- Créer des branches dédiées sous la forme `codex/<mission-name>` pour chaque mission.
- Réaliser un commit après chaque mission aboutie avec tests passants.
- Une PR doit couvrir un objectif cohérent, entièrement testé et documenté si nécessaire.
- Fusionner les PR via l'option « Squash & Merge » pour conserver un historique propre.
