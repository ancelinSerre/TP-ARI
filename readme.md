#  Accès et recherche d'information
**Auteurs** : Baptiste Bouvier et Ancelin Serre\
**Date** : 27/02/2019\
*POLYTECH GRENOBLE - INFO4*

## Arborescence du projet
```bash
.
├── readme.md
└── search_engine
    ├── engine
    │   ├── config.json
    │   ├── DataPreprocessor.py
    │   ├── main.py
    │   ├── Request.py
    │   ├── Search.py
    │   └── Utils.py
    ├── preparation
    │   ├── split_cacm.py
    │   ├── tokenize_cacm.py
    │   └── zipf.py
    └── resources
        ├── cacm
        │   ├── cacm.all
        │   ├── cite.info
        │   ├── common_words
        │   ├── qrels.text
        │   ├── query.text
        │   └── README
        ├── generated_files
        │   ├── inverted_index.json
        │   ├── norms.json
        │   ├── salton_representation.json
        │   └── vocabulary.json
        ├── results [3204 entries exceeds filelimit, not opening dir]
        ├── stop_words_filtered [3204 entries exceeds filelimit, not opening dir]
        └── tokenized [3204 entries exceeds filelimit, not opening dir]
```

Dans le dossier `search_engine` on trouve les dossiers suivants :
- `preparation` : contient le code *Python* utilisé pour préparer le corpus de fichiers à manipuler par la suite. Cela correspond au premier TP situé [ici](https://hmul8r6b.imag.fr/doku.php?id=tp_loi_de_zipf).
- `engine` : contient le code *Python* permettant de générer et calculer le vocabulaire du corpus, les normes de ses documents, l'index inversé ainsi que la [représentation vectorielle](https://hmul8r6b.imag.fr/lib/exe/fetch.php?media=accesinfoi-ii.pdf) de **Salton** (plus d'infos [ici](https://fr.wikipedia.org/wiki/Mod%C3%A8le_vectoriel)). Ce répertoire contient également le nécesssaire pour effectuer une recherche au sein du corpus. Cet ensemble de scripts *Python* correspond aux [deuxième](https://hmul8r6b.imag.fr/doku.php?id=tp_constitution_de_vocabulaire_et_representation) et [troisième](https://hmul8r6b.imag.fr/doku.php?id=tp_recherche_et_evaluation) TP.
- `resources` : contient l'ensemble des fichiers manipulés tout au long du projet. Le corpus est basé sur le fichier nommé `cacm.all` situé dans le sous-dossier `cacm`. Ce fichier est découpé en **3204** parties traitées au fur et à mesure par les différents scripts du projet.

## Notice d'utilisation

Pour faire fonctionner ce programme, il est nécessaire d'effectuer les étapes ci-dessous dans l'ordre indiqué : 
- Placez-vous dans le dossier 