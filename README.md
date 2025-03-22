# 🎬 TMDB API Search

TMDB API Search est une application **Streamlit** permettant de **rechercher des films et afficher les 20 films les plus populaires** en utilisant **l'API de The Movie Database (TMDB)**.  

🚀 **Objectif** : Offrir une interface rapide et intuitive pour explorer des films avec des affichages optimisés.  

---

## 🌟 Fonctionnalités

✅ **Recherche avancée** : Trouver un film en entrant son titre.  
✅ **Top 20 des films populaires** : Liste des films les plus regardés du moment.  
✅ **Affichage détaillé** : Poster, date de sortie, popularité et note.  
✅ **Gestion des erreurs** : Requêtes robustes avec gestion des codes HTTP et des limites d'API.  
✅ **Performances améliorées** : Mise en cache des résultats pour une navigation fluide.  

---

## 📌 Prérequis

Avant de commencer, assure-toi d'avoir installé :

- **Python 3.x**
- **pip** (installé avec Python)
- **Un compte TMDB** (pour récupérer une clé API)
- **Git** (si tu veux cloner le projet)

---

## 🛠️ Installation et exécution

### 1️⃣ Cloner le projet
```bash
git clone https://github.com/akramCh77/TMDB_API_Search.git
cd TMDB_API_Search
```

### 2️⃣ Créer un environnement virtuel (optionnel mais recommandé)
python -m venv venv
source venv/bin/activate  # Sur macOS/Linux
venv\Scripts\activate  # Sur Windows

### 3️⃣ Installer les dépendances
pip install -r requirements.txt

### 4️⃣ Configurer l'API TMDB
Crée un fichier .env à la racine du projet et ajoute :
TMDB_API_KEY=VOTRE_CLE_API

### 5️⃣ Lancer le backend de l'application
uvicorn main:app --reload

### 6️⃣ Lancer le frontend de l'application (Streamlit)
streamlit run index.py



