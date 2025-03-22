import streamlit as st
import requests

# 🎨 Personnalisation du style
st.set_page_config(page_title="Recherche de Films TMDB", page_icon="🎬", layout="wide")

# 🌟 Titre principal
st.title("🎬 Recherche de Films")

# 🔎 Champ de recherche
movie_name = st.text_input("Entrez le nom du film 🎥", "")

# 🎬 URLs de l'API backend
API_BASE_URL = "http://127.0.0.1:8000"
SEARCH_URL = f"{API_BASE_URL}/search/"
TOP_MOVIES_URL = f"{API_BASE_URL}/top_movies"

# 🎯 Fonction d'affichage des films en grille
def display_movies(movies, section_title):
    if not movies:
        st.error("Aucun film trouvé !")
    else:
        st.subheader(section_title)
        cols = st.columns(3)  # 3 films par ligne
        for index, movie in enumerate(movies):
            with cols[index % 3]:  # Alterne les colonnes
                if movie.get("poster"):
                    st.image(movie["poster"], width=200, caption=movie["title"])
                else:
                    st.warning(f"🚫 Pas d'image disponible pour {movie['title']}")
                st.write(f"**📅 Date de sortie :** {movie.get('release_date', 'Inconnue')}")
                st.write(f"**🔥 Popularité :** {movie.get('popularity', 'N/A')}")
                st.write(f"**⭐ Note :** {movie.get('vote_average', 'N/A')}/10")

# 🔍 Recherche d'un film
if st.button("🔍 Rechercher"):
    if not movie_name:
        st.warning("Veuillez entrer un nom de film !")
    else:
        with st.spinner("Recherche en cours..."):
            response = requests.get(SEARCH_URL + movie_name)
            if response.status_code == 200:
                movies = response.json()
                display_movies(movies, "🔎 Résultats de la recherche")
            else:
                st.error("❌ Erreur lors de la récupération des films !")

# 🎥 Charger et afficher les 20 films les plus populaires au démarrage
try:
    with st.spinner("Chargement des films populaires..."):
        response = requests.get(TOP_MOVIES_URL)
        if response.status_code == 200:
            top_movies = response.json()
            display_movies(top_movies, "🎥 Top 20 des films populaires")
        else:
            st.error(f"❌ Erreur lors du chargement des films populaires. (Code: {response.status_code})")
except requests.exceptions.RequestException as e:
    st.error(f"❌ Erreur de connexion au serveur: {str(e)}")
    st.info("👉 Assurez-vous que le serveur backend est en cours d'exécution sur http://127.0.0.1:8000")
