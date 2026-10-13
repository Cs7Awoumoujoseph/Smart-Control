# Smart-Control

**Smart-Control** est une application de bureau Python avec interface graphique Tkinter, conçue autour de la gestion et de l'analyse de données de patients. Le dépôt contient une interface graphique, des fichiers CSV d'exemple, un logo et un document de confidentialité.

> **Statut : prototype pédagogique.** Le code actuel lit les paramètres PostgreSQL depuis des variables d’environnement. Le fichier `patient_csv.csv` contient des données synthétiques de démonstration ; n’ajoutez jamais de données réelles de patients à ce dépôt. Une ancienne révision contenait des paramètres de connexion codés en dur : si ces paramètres correspondent à un compte réel, son mot de passe doit être renouvelé. La modification du fichier courant ne retire pas cette ancienne révision de l’historique Git.

## Fonctionnalités repérées

- Interface de bureau construite avec Tkinter.
- Connexion à une base de données PostgreSQL et récupération de données de patients.
- Sélection de fichiers CSV depuis une boîte de dialogue.
- Visualisation de distributions statistiques, notamment la loi de Benford, la loi binomiale et la loi normale.
- Utilisation de modèles de régression linéaire et logistique et d'outils de visualisation de résultats statistiques.
- Fenêtre d'information de l'application et accès à un document de confidentialité.

Ces éléments sont décrits à partir du code présent dans le dépôt ; ils ne constituent pas une validation du fonctionnement complet ni de la pertinence médicale des analyses.

## Technologies

- **Python 3**
- **Tkinter** — interface graphique
- **PostgreSQL** et **psycopg2** — accès à la base de données
- **Pandas**, **NumPy** et **SciPy** — traitement et calculs numériques
- **Matplotlib** et **Seaborn** — graphiques
- **scikit-learn** — modèles et métriques d'apprentissage automatique
- **Pillow** — gestion d'images

## Fichiers du dépôt

| Fichier | Rôle |
|---|---|
| `gui.py` | Application de bureau et logique de l'interface. |
| `logo.png` | Logo utilisé dans l'interface. |
| `contrat.txt` | Modèle de contrat de confidentialité. |
| `patient_csv.csv` | Jeu de données fictives destiné à la démonstration ; ne pas y ajouter de données réelles. |
| `NH.csv`, `other.csv`, `valeur.csv` | Fichiers CSV utilisés pour les données ou les analyses. |

## Prérequis

- Python 3.10 ou version compatible avec les dépendances choisies.
- PostgreSQL, si les fonctions de base de données sont utilisées.
- Une session graphique pour afficher Tkinter.

## Installation

Clonez le dépôt et entrez dans le dossier :

```bash
git clone https://github.com/Cs7Awoumoujoseph/Smart-Control.git
cd Smart-Control
```

Créez et activez un environnement virtuel :

```bash
python -m venv .venv
```

Sous Windows :

```powershell
.venv\Scripts\Activate.ps1
```

Sous macOS ou Linux :

```bash
source .venv/bin/activate
```

Installez les bibliothèques Python utilisées par le code :

```bash
python -m pip install pillow psycopg2-binary numpy pandas matplotlib scikit-learn seaborn scipy
```

Tkinter est généralement inclus dans les installations Python pour Windows ; sur certaines distributions Linux, il doit être installé séparément via le gestionnaire de paquets du système.

## Configuration de la base de données

Le code actuel attend une base PostgreSQL locale nommée `gestion_patient` et une table `patients`. Le schéma de base de données n'est pas documenté dans le dépôt consulté.

Avant de lancer l'application :

1. Créez et configurez la base de données et la table attendue.
2. Configurez `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER` et `DB_PASSWORD` dans l'environnement avant de lancer l'application. Un modèle est fourni dans `.env.example` ; recopiez-le en `.env` si vous utilisez un outil qui charge ce fichier, puis gardez `.env` hors de Git.
3. N'utilisez pas de compte PostgreSQL superutilisateur pour l'application ; créez un compte dédié avec les permissions minimales.
4. Ne publiez jamais de mot de passe ou de données réelles de patients dans Git.

## Lancement

Depuis le dossier du projet et avec l'environnement virtuel activé :

```bash
python gui.py
```

Le lancement effectif dépend de la disponibilité de PostgreSQL, de la configuration locale et des bibliothèques installées.

## Sécurité et confidentialité — actions prioritaires

- Si les paramètres de connexion présents dans une ancienne révision correspondent à un compte réel, renouveler ce mot de passe et vérifier les journaux d’accès.
- Retirer du dépôt les données identifiantes et utiliser des données synthétiques pour les exemples.
- Charger les secrets depuis l'environnement ; ne pas les coder en dur.
- Le fichier `.gitignore` exclut les environnements virtuels et les fichiers de configuration locaux ; vérifiez aussi les exports et jeux de données avant chaque commit.
- Définir des règles de contrôle d'accès, de sauvegarde et de conservation des données avant tout usage avec de vrais patients.
- Faire vérifier le contrat de confidentialité par un professionnel compétent avant de le présenter comme un document juridique final.

## Limites connues

- Aucun fichier `requirements.txt` n'a été identifié ; la liste d'installation ci-dessus est indicative et déduite des imports.
- Le schéma SQL complet et les instructions de création de la base ne sont pas fournis.
- La validité des modèles statistiques et leur aptitude à un usage médical ne sont pas évaluées par cette documentation.

## Auteur et dépôt

Projet hébergé sur GitHub : [Cs7Awoumoujoseph/Smart-Control](https://github.com/Cs7Awoumoujoseph/Smart-Control).
