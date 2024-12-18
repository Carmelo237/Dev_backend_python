# Dev_backend_python


![image](https://github.com/user-attachments/assets/efd86cf2-b6f6-4a85-8a87-e5f970cf62d6)



À propos du Projet

Notre projet est porté sur une  analyse de données e-commerce notre but ici sera de analyser et de visualiser les performances commerciales à travers différents KPIs.Pour ce projet nous utilisons MongoDB pour le stockage des données mais aussi la gestion de données , FastAPI pour le developpement de notre application et interagir avec la base de données 
, et Streamlit pour la visualisation des données.

## Les KPI'S

- [Métriques de Ventes](#métriques-de-ventes)
  - [Total des ventes & Total des bénéfices](#Total-des-ventes-&-Total-des-bénéfices)
  - [Nombre total de commandes](#nombre-total-de-commandes)
  - [Panier moyen](#panier-moyen)
  - [Nombre total de produits vendus](#nombre-total-de-produits-vendus)
  
- [Métriques Clients](#métriques-clients)
  - [Nombre total de clients](#nombre-total-de-clients)
  - [Moyenne de commandes par client](#moyenne-de-commandes-par-client)
  - [Temps moyen entre les commandes](#temps-moyen-entre-les-commandes)
  - [Taux de rétention client](#taux-de-rétention-client)

- [Performance Produits](#performance-produits)
  - [Revenus par produit](#revenus-par-produit)
  - [Quantités vendues par produit](#quantités-vendues-par-produit)
  - [Nombre de commandes par produit](#nombre-de-commandes-par-produit)
  - [Quantité moyenne par commande](#quantité-moyenne-par-commande)

- [Analyses Temporelles](#analyses-temporelles)
  - [Évolution des ventes dans le temps](#évolution-des-ventes-dans-le-temps)
  - [Saisonnalité des ventes](#saisonnalité-des-ventes)
  - [Jours/périodes de forte activité](#jourspériodes-de-forte-activité)

- [Métriques Géographiques](#métriques-géographiques)
  - [Répartition des ventes par région](#répartition-des-ventes-par-région)
  - [Zones les plus rentables](#zones-les-plus-rentables)
  - [Analyse des distances de livraison](#analyse-des-distances-de-livraison)

## Construit avec


- ![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white) - [MongoDB](https://www.mongodb.com/) - Base de données NoSQL
- ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white) - [FastAPI](https://fastapi.tiangolo.com/) - Framework API REST
- ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white) - [Streamlit](https://streamlit.io/) - Framework de visualisation de données
- ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) - [Python](https://www.python.org/) - Langage de programmation
- ![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white) - [Pandas](https://pandas.pydata.org/) - Manipulation de données
- ![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white) - [Plotly](https://plotly.com/) - Création de graphiques

### Architecture Backend

1. **MongoDB** (Base de données)
- **Rôle** : Stockage des données NoSQL
- **Utilisation** : 
  - Stocke les collections : customers, orders, products, locations
  - Permet des requêtes complexes et agrégations
  - Offre de bonnes performances pour les grands volumes de données
  - Flexible pour les schémas de données évolutifs

2. **FastAPI** (Framework API)
- **Rôle** : Serveur d'API REST
- **Avantages** :
  - Performances élevées (asynchrone)
  - Documentation automatique (Swagger/OpenAPI)
  - Validation des données intégrée
  - Typage fort avec Pydantic


3. **PyMongo** (Driver MongoDB pour Python)
- **Rôle** : Connection Python-MongoDB
- **Utilisation** :
  - Exécute les requêtes MongoDB
  - Gère les connexions à la base
  - Transforme les données BSON en objets Python

### Architecture Frontend

1. **Streamlit** (Framework de dashboard)
- **Rôle** : Interface utilisateur web
- **Avantages** :
  - Création rapide d'interfaces
  - Widgets interactifs intégrés
  - Mise à jour en temps réel
  - Intégration facile avec Pandas/Plotly

2. **Plotly** (Bibliothèque de visualisation)
- **Rôle** : Création de graphiques interactifs
- **Types de graphiques** :
  - Graphiques en barres pour les revenus
  - Camemberts pour les distributions
  - Graphiques linéaires pour les tendances
  - Cartes pour les données géographiques

### Flux de données

**Collecte des données et Traitement Backend**
= Avec python

