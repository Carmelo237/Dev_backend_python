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
  - Stock les collections : customers, orders, products, locations
  - Permet des requêtes complexes et agrégations
  - Offre de bonnes performances pour les grands volumes de données
  - Flexible pour les schémas de données évolutifs

2. **FastAPI** (Framework API)
- **Rôle** : Serveur d'API REST
- **Avantages** :
  - Performances élevées (asynchrone)
  - Documentation automatique (Swagger/OpenAPI)
  - Validation des données intégrée



3. **PyMongo** (Driver MongoDB pour Python)
- **Rôle** : Connection Python-MongoDB
- **Utilisation** :
  - Exécute les requêtes MongoDB
  - Gère les connexions à la base
  

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
  - Graphiques en barres 
  - Camemberts 
  - Graphiques linéaires 
  - Cartes pour les données géographiques

### Flux de données

# Comparaison des Stacks Technologiques

## Stack Actuelle du Projet

| Couche | Composant | Technologie | Rôle | Avantages |
|--------|-----------|-------------|------|-----------|
| Backend | Base de données | MongoDB | Stockage NoSQL | • Flexibilité du schéma<br>• Bonnes performances en lecture<br>• Requêtes complexes faciles |
| Backend | API Framework | FastAPI | Serveur API REST | • Haute performance<br>• Documentation auto (Swagger)<br>• Support async natif |
| Backend | Serveur | Uvicorn | Serveur ASGI | • Très performant<br>• Rechargement auto<br>• Simple à configurer |
| Frontend | Interface | Streamlit | Dashboard UI | • Développement rapide<br>• Widgets intégrés<br>• Interface Python native |
| Frontend | Visualisation | Plotly | Graphiques | • Interactif<br>• Nombreux graphiques<br>• Personnalisable |

## Alternatives Possibles

### Stack Entreprise

| Couche | Composant | Technologie | Rôle | Avantages |
|--------|-----------|-------------|------|-----------|
| Backend | Base de données | PostgreSQL | SGBD relationnel | • Transactions ACID<br>• Mature et stable<br>• Support JSON |
| Backend | API Framework | Django REST | Framework web | • Écosystème complet<br>• Admin inclus<br>• Sécurité robuste |
| Backend | Serveur | Gunicorn | Serveur WSGI | • Production-ready<br>• Performant<br>• Configurable |
| Frontend | Interface | Dash | Application web | • Pro-grade<br>• Composants React<br>• Hautement configurable |
| Frontend | Visualisation | Bokeh | Graphiques avancés | • Interactivité poussée<br>• Grands volumes<br>• Personnalisation fine |

### Stack Microservices

| Couche | Composant | Technologie | Rôle | Avantages |
|--------|-----------|-------------|------|-----------|
| Backend | Base de données | Cassandra | DB distribuée | • Scalabilité horizontale<br>• Haute disponibilité<br>• Performance en écriture |
| Backend | API Framework | Flask | Microservices | • Léger<br>• Flexible<br>• Simple |
| Backend | Serveur | Hypercorn | Serveur HTTP/2 | • Support HTTP/2<br>• TLS avancé<br>• Compatible ASGI/WSGI |
| Frontend | Interface | Gradio | UI simple | • Rapide à déployer<br>• Interface moderne<br>• Intégration ML |
| Frontend | Visualisation | Altair | Graphiques déclaratifs | • Syntaxe élégante<br>• Vega-Lite<br>• Intégration facile |

## Guide de Choix

| Stack | Cas d'Usage | Points Forts |
|-------|-------------|--------------|
| Actuelle | • Startups<br>• Projets moyens<br>• Data science | • Développement rapide<br>• Focus Python<br>• Flexible |
| Entreprise | • Grandes entreprises<br>• Applications critiques | • Robuste<br>• Sécurisé<br>• Maintenable |
| Microservices | • Architecture distribuée<br>• Forte charge | • Scalable<br>• Modulaire<br>• Performant |
