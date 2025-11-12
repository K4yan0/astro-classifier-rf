# 🚀 Astro-Classifier RF : Classification d'Astéroïdes Potentiellement Dangereux

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Libraries](https://img.shields.io/badge/Bibliothèques-Pandas_|_Scikit--learn_|_Seaborn-orange)
![License](https://img.shields.io/badge/License-MIT-green)

Ce projet utilise un modèle de Machine Learning **Random Forest** pour classifier les astéroïdes comme "Potentiellement Dangereux" (Potentially Hazardous Asteroid - PHA) ou non, en se basant sur leurs données orbitales et physiques extraites de la base de données JPL de la NASA.

---

## 🎯 Objectif et Découverte Scientifique

Le but de ce projet était triple :
1.  **IA :** Mettre en œuvre un modèle `RandomForestClassifier` de Scikit-learn sur un problème de classification concret.
2.  **Portfolio :** Construire un projet de data science de A à Z en suivant les meilleures pratiques (GitFlow, architecture de dossiers, notebooks séparés).
3.  **Science :** Non seulement prédire le statut PHA, mais aussi **confirmer scientifiquement** quelles caractéristiques sont les plus déterminantes pour définir un astéroïde comme "dangereux".

### 1. Performance du Modèle : Précision de 99.86%

Le modèle final, entraîné sur 80% des données et testé sur 20% de données inconnues, atteint une précision globale de 99.86%.

La métrique la plus importante est le **Rappel (Recall)** pour les PHA : **notre modèle a réussi à identifier 98.8% de toutes les menaces réelles (497 sur 503)** dans l'ensemble de test, avec un nombre de fausses alertes (5) et de menaces manquées (6) extrêmement faible.

![Matrice de Confusion](results/figures/04_confusion_matrix.png)

### 2. La Découverte : Le Modèle a "Redécouvert" la Science

L'objectif scientifique a été atteint. En demandant au modèle quelles caractéristiques il a jugées les plus importantes pour prendre sa décision, il a **confirmé de manière autonome la définition officielle d'un PHA**.

Le modèle a identifié `H` (la magnitude, liée à la **taille**) et `moid` (la distance orbitale minimale, liée à la **proximité**) comme étant les deux facteurs prédictifs les plus importants, loin devant tous les autres paramètres orbitaux.

![Importance des Caractéristiques](results/figures/05_feature_importance.png)

---

## 💻 Installation et Utilisation

Ce projet utilise `Python 3.10` et un environnement virtuel est recommandé.

1.  **Cloner le dépôt :**
    ```bash
    git clone [https://github.com/](https://github.com/)[TON_NOM_UTILISATEUR]/[TON_NOM_DE_PROJET].git
    cd [TON_NOM_DE_PROJET]
    ```

2.  **Créer un environnement virtuel et l'activer :**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Sur Windows: .\venv\Scripts\activate
    ```

3.  **Installer les dépendances :**
    ```bash
    pip install -r requirements.txt
    ```

---

## 📖 Processus (Les Notebooks)

Le projet est divisé en trois notebooks séquentiels situés dans le dossier `/notebooks/` :

* **`01_Data_Acquisition_and_Cleaning.ipynb`**
    * Interroge la base de données JPL Small-Body de la NASA.
    * Filtre pour obtenir tous les Objets Proches de la Terre (NEOs).
    * Nettoie les données : gère les valeurs `NaN` et convertit la cible `pha` en format binaire (0/1).
    * Sauvegarde un fichier `asteroids_cleaned.csv` propre.

* **`02_Exploratory_Data_Analysis.ipynb`**
    * Analyse le déséquilibre des classes (la grande majorité des objets sont non-dangereux).
    * Visualise les distributions des caractéristiques (`H`, `moid`, etc.).
    * Génère une matrice de corrélation pour identifier les relations entre les variables.

* **`03_Model_Training_and_Evaluation.ipynb`**
    * Divise les données en ensembles d'entraînement (80%) et de test (20%).
    * Entraîne un `RandomForestClassifier` en utilisant `class_weight='balanced'` pour gérer le déséquilibre.
    * Évalue le modèle, génère la matrice de confusion et le rapport de classification.
    * Extrait et trace l'importance des caractéristiques.
    * Sauvegarde le modèle final entraîné dans `/results/models/`.

---

## 🗂️ Structure du Dépôt
astro-classifier-rf/
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
│
├── data/
│   ├── raw/
│   │   └── .gitkeep        (Les données brutes sont ignorées par .gitignore)
│   └── processed/
│       └── .gitkeep        (Les données nettoyées sont ignorées par .gitignore)
│
├── notebooks/
│   ├── 01_Data_Acquisition_and_Cleaning.ipynb
│   ├── 02_Exploratory_Data_Analysis.ipynb
│   └── 03_Model_Training_and_Evaluation.ipynb
│
├── results/
│   ├── figures/
│   │   ├── 01_class_distribution.png
│   │   ├── 02_h_moid_distributions.png
│   │   ├── 03_correlation_heatmap.png
│   │   ├── 04_confusion_matrix.png
│   │   └── 05_feature_importance.png
│   └── models/
│       └── rf_pha_classifier.joblib
│
└── src/
└── .gitkeep

---

## 📄 Licence

Ce projet est publié sous la licence MIT.
