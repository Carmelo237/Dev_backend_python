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
- ![Uvicorn](https://img.shields.io/badge/Uvicorn-FF9500?style=for-the-badge&logo=uvicorn&logoColor=white) - [Uvicorn](https://www.uvicorn.org/) - Serveur ASGI performant



# Comparaison des Architectures Web pour l'Analytics E-commerce

## Architecture Actuelle du Projet

### Backend
| Composant | Technologie | Rôle | Avantages |
|-----------|-------------|------|-----------|
| Base de données | MongoDB | Stockage NoSQL | • Flexibilité du schéma<br>• Bonnes performances en lecture<br>• Facilité des requêtes complexes |
| API Framework | FastAPI | Serveur API REST | • Performance élevée<br>• Documentation automatique<br>• Support async natif |
| Serveur ASGI | Uvicorn | Serveur d'application | • Très performant<br>• Support async<br>• Rechargement automatique |
| ORM/Driver | PyMongo | Connexion DB | • Interface native MongoDB<br>• Support async<br>• Simple d'utilisation |

### Frontend
| Composant | Technologie | Rôle | Avantages |
|-----------|-------------|------|-----------|
| Framework UI | Streamlit | Interface utilisateur | • Développement rapide<br>• Widgets prêts à l'emploi<br>• Intégration Python native |
| Visualisation | Plotly | Graphiques | • Interactivité<br>• Nombreux types de graphiques<br>• Personnalisation poussée |
| HTTP Client | Requests | Appels API | • Simple d'utilisation<br>• Standard de facto<br>• Bonne documentation |

## Architecture Alternative

#### Backend
| Composant | Technologie | Rôle | Avantages |
|-----------|-------------|------|-----------|
| Base de données | PostgreSQL | SGBD relationnel | • ACID compliant<br>• Mature et stable<br>• Support JSON natif |
| API Framework | Django REST | Framework complet | • Écosystème riche<br>• Admin interface<br>• Sécurité robuste |
| Serveur WSGI | Gunicorn | Serveur production | • Stable<br>• Facile à configurer<br>• Performant |
| ORM | Django ORM | Couche d'abstraction DB | • Intégration native<br>• Migrations automatiques<br>• Requêtes puissantes |

#### Frontend
| Composant | Technologie | Rôle | Avantages |
|-----------|-------------|------|-----------|
| Framework UI | Dash | Application web | • Composants professionnels<br>• Hautement personnalisable<br>• Basé sur React |
| Visualisation | Bokeh | Graphiques avancés | • Visualisations complexes<br>• Grande interactivité<br>• Support grands volumes |
| HTTP Client | Axios | Appels API | • Promesses<br>• Intercepteurs<br>• Gestion erreurs avancée |




## Descrption du projet

## Pré-requis‼️ 

⚠️ **Utilisation avancée (Git - Gestion des branches)**
Travailler avec des branches Git

Ces commandes permettent de créer, basculer sur une branche, ajouter des modifications, les valider et les pousser vers un dépôt distant.

1. Créer une nouvelle branche ou basculer sur une branche existante**
   ```bash
   git branch <nom-de-la-branche>
   git checkout <nom-de-la-branche>

2. Ajouter les nouveaux fichiers ou fichiers modifiés
    ```bash
    git add 

3. Valider les changements avec un message de commit
   ```bash
   git commit -m "Message de commit pour indiquer l'ajout ou la modification »

4. Pousser les modifications vers le dépôt distant
   ```bash
   git push origin <nom-de-la-branche>
## Installation⚙️
  ```bash
pip install pymongo
pip install  pandas 
