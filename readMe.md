# Prédiction Météo
Ce projet contient un modèle de prédiction météo développé en Python, utilisant des techniques d'apprentissage automatique pour prédire les conditions météorologiques futures basées sur un ensemble de données historiques.

### Structure du Projet
Le modèle de prédiction est situé dans le sous-dossier apprentissage, sous le nom de fichier apprentissage.py. C'est le cœur de notre système de prédiction, où les algorithmes d'apprentissage automatique sont entraînés et testés pour prédire les conditions météorologiques.

### Emplacement des MLruns
Les informations concernant les exécutions de MLflow (MLruns) sont également stockées dans le même dossier apprentissage. MLflow est utilisé pour suivre les expériences, enregistrer les résultats des différents entraînements, et versionner les modèles. Cela permet une analyse approfondie des performances des modèles et une comparaison facile entre différentes configurations.

### Utilisation
assurez-vous d'avoir installé Python et les dépendances nécessaires listées dans requirements.txt. Ensuite, naviguez dans le dossier apprentissage et exécutez la commande suivante : mlflow ui

### Problème possible
Il est possible que les modèles soient associés à un emplacement spécifique sur mon ordinateur. Pour résoudre ce problème et utiliser notre API, vous devrez effectuer un nouvel apprentissage (environ 3 minutes). Cela générera un nouvel identifiant de modèle, que vous devrez ensuite mettre à jour dans le fichier routes/predictionRoute.py.