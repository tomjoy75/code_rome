1. Cartographie des modules et points d’entrée

    code_rome.py : point d’entrée CLI, parse les arguments, charge les deux CSV, cherche les correspondances et écrit un fichier Markdown simple.

rome_loader.py : fournit _detect_delimiter pour deviner le séparateur et load_csv qui valide la présence de la colonne code_rome et retourne les lignes du CSV.

rome_search.py : expose search_in_appellations (filtre par mot-clé dans les intitulés) et get_rome_details (assemble les détails à partir du référentiel) ; search_rome est déclaré mais pas implémenté.

utils.py : construit un dictionnaire de référence {code_rome: {...}} à partir des lignes du CSV métier.

Ressources : jeux de données CSV officiels dans data/RefRomeCsv/ (codes ROME et appellations).

formatter.py et api.py sont des coquilles vides (0 ligne chacune), signes de fonctionnalités prévues mais absentes.
2. Dettes techniques principales

    Le CLI charge et ouvre les CSV à chaque exécution sans mutualiser les lectures ni gérer finement les erreurs (pas de gestion des exceptions de parsing ni de retour utilisateur en cas de 0 résultat).

search_in_appellations suppose que les champs libelle_appellation_long et libelle_appellation_court existent et sont non vides ; un champ manquant déclencherait un AttributeError (absence de valeur par défaut avant .casefold()).

get_rome_details présume que tout code parent est déjà présent dans le référentiel ; une incohérence de données entraînerait une KeyError sans garde-fou.

search_rome est laissé vide, empêchant une API interne cohérente pour regrouper chargement, recherche et formatage.

Les modules formatter.py et api.py manquent totalement, laissant les fonctionnalités d’export Markdown et d’API locale inachevées.

Les tests CLI sont obsolètes : ils attendent uniquement un message récapitulatif alors que le CLI courant produit plusieurs impressions et écrit un fichier.
3. Tests manquants et zones non couvertes

    Aucune couverture pour _detect_delimiter, la validation des colonnes supplémentaires, ni la gestion des lignes vides dans load_csv au-delà des cas unitaires simples.

Absence totale de tests pour get_rome_details et pour le flux complet (chargement → recherche → formatage) qui garantirait l’intégration entre modules.

Pas de tests autour de la création du fichier de sortie, de la gestion des chemins personnalisés ou de la situation “aucun résultat” dans le CLI.

Aucun test ne couvre les colonnes facultatives du CSV (libellés, parent) ni la robustesse face aux caractères spéciaux présents dans les données réelles.

Les modules formatter.py et api.py n’étant pas implémentés, aucune stratégie de test n’est posée pour ces futurs composants.
4. Risques sécurité, complexité ou duplication

    Le chemin de sortie est directement dérivé de l’entrée utilisateur sans normalisation ni restriction, ouvrant la porte à l’écriture dans un emplacement inattendu (ex. ../../tmp/foo).

L’absence de valeurs par défaut dans search_in_appellations peut provoquer une interruption brutale si un champ est manquant, ce qui compromet la robustesse du CLI sur des données imparfaites.

Répétition des lectures de CSV (aucun cache ni injection de dépendance) augmente le temps d’exécution et la complexité lorsque l’on voudra réutiliser les référentiels dans une API ou un service long-vivant.

Pas de contrôle sur la taille mémoire : tout le CSV est chargé en mémoire, ce qui peut devenir problématique sur des machines modestes si les fichiers grandissent.
5. Quick wins et chantiers prioritaires
Quick wins (≤1 jour)

    Sécuriser search_in_appellations en fournissant des valeurs par défaut (row.get(..., \"\")) et en harmonisant la casse du mot-clé une seule fois.

Mettre à jour les tests CLI pour refléter les sorties actuelles ou, mieux, convertir les impressions “debug” en logs optionnels afin de stabiliser la sortie attendue.

Centraliser le chargement des CSV et gérer proprement l’absence de résultat (message utilisateur + fichier vide explicite) pour offrir une UX cohérente.
Chantiers prioritaires (structurants)

    Implémenter search_rome comme façade unique (chargement, indexation, recherche, formatage) afin de séparer la logique métier du CLI, préparer l’API et faciliter les tests d’intégration.

Concevoir un module formatter.py complet (Markdown et JSON) et l’intégrer via une architecture pluggable ; documenter et tester ces formats pour assurer la pérennité des exports.

Bâtir une API (ou service) réutilisable dans api.py, possiblement avec FastAPI/Flask, en mutualisant les jeux de données chargés et en ajoutant des caches pour réduire la complexité et préparer un usage serveur.
6. Règles de style/structure à formaliser dans un futur AGENTS.md

    Imposer l’écriture de fonctions pures réutilisables (chargement, recherche, formatage) et interdire la logique métier dans le CLI ; documenter clairement le point d’entrée (main() dans code_rome.py).

Standardiser l’utilisation des annotations de type et docstrings pour chaque fonction publique (déjà amorcé dans rome_loader.py, rome_search.py, utils.py).

Définir des conventions de gestion d’erreurs : lever des exceptions métier explicites dans les modules et ne gérer/afficher les messages qu’au niveau CLI/API.

Exiger des tests unitaires pour chaque module ainsi que des tests d’intégration pour les flux critiques (chargement → recherche → export), avec utilisation de fixtures temporaires pour isoler les cas de données.

Documenter la structure des données attendues (schéma des CSV) et imposer des valeurs par défaut non nulles avant tout appel à des méthodes de chaîne pour éviter les plantages silencieux.

Clarifier les règles d’E/S fichiers : encodage UTF-8, ouverture avec newline='', et validation/sanitation des chemins générés à partir des entrées utilisateur.
