# Tableau de bord Dash (Ventes)

Application Dash interactive pour l'analyse des ventes à partir d'un dataset public. Elle affiche des KPI (chiffre d'affaires, commandes, panier moyen, régions), des courbes d'évolution mensuelle, des tops par états/villes/sous-catégories, et des heatmaps. Filtres par période et par région inclus.

## Prérequis
- Python 3.9+
- pip

## Installation
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Lancement
```bash
python .\Aïcha_Mbaye_DIT_L3_Projet_Dash.py
```
L'application démarre sur `http://127.0.0.1:8050`.

## Données
- Source chargée depuis: `https://raw.githubusercontent.com/OusmanHamit/datasets/refs/heads/main/L3_Project.csv`

## Structure
- `Aïcha_Mbaye_DIT_L3_Projet_Dash.py`: code principal Dash
- `requirements.txt`: dépendances Python
- `.gitignore`: exclusions Git
- `README.md`: ce fichier

## Déploiement rapide sur GitHub
Après création d'un dépôt vide sur GitHub:
```bash
git remote add origin <URL_DU_DEPOT>
git branch -M main
git push -u origin main
```
