import os
import asyncio
import aiohttp
from fastapi import FastAPI
from dotenv import load_dotenv
from aiocache import Cache
from fastapi.middleware.cors import CORSMiddleware

from downoaldFILM import download_film

# Charger les variables d'environnement
load_dotenv()

# Récupérer la clé API TMDB
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# Vérifier si la clé API est bien chargée
if not TMDB_API_KEY:
    raise ValueError("TMDB_API_KEY non définie dans le fichier .env")

# Initialisation du cache avec expiration d’1 heure
cache = Cache(Cache.MEMORY, ttl=3600)

# Initialisation de l'application FastAPI
app = FastAPI()

# Autoriser le frontend à faire des requêtes API (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permet d'accéder à l'API depuis n'importe où 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

 #Charger les films au démarrage du serveur
movies_data = download_film()
if not movies_data:
    raise ValueError("❌ Aucun film trouvé dans le fichier JSON.")


@app.get("/top_movies")
async def get_top_movies():
    """
    Récupère les 20 films les plus populaires.
    """
    url = "https://api.themoviedb.org/3/movie/popular"
    params = {"api_key": TMDB_API_KEY, "language": "fr-FR", "page": 1}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                if not data.get("results"):
                    return {"message": "Aucun film trouvé."}

                # Ne récupérer que les 20 premiers films populaires
                top_movies = [
                    {
                        "id": movie.get("id"),
                        "title": movie.get("title", "Titre inconnu"),
                        "release_date": movie.get("release_date", "Inconnue"),
                        "poster": f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}" if movie.get("poster_path") else None,
                        "popularity": movie.get("popularity"),
                        "vote_average": movie.get("vote_average"),
                    }
                    for movie in data["results"][:20]
                ]

                return top_movies
            else:
                return {"error": f"Erreur {response.status}"}



@app.get("/search/{movie_name}")
async def search_movie(movie_name: str):
    """
    Recherche un film par son nom et retourne tous les films contenant ce mot-clé.
    """
    cache_key = f"search_{movie_name.lower()}"
    cached_response = await cache.get(cache_key)

    if cached_response:
        return cached_response  # Retourne les résultats en cache

    url = "https://api.themoviedb.org/3/search/movie"
    params = {"api_key": TMDB_API_KEY, "language": "fr-FR", "query": movie_name}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                if not data.get("results"):
                    return {"message": "Aucun film trouvé."}

                # Formatter les résultats pour n'afficher que les informations utiles
                formatted_results = [
                    {
                        "id": movie.get("id"),
                        "title": movie.get("title", "Titre inconnu"),
                        "release_date": movie.get("release_date", "Inconnue"),
                        "poster": f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}" if movie.get("poster_path") else None,
                        "popularity": movie.get("popularity"),
                        "vote_average": movie.get("vote_average"),
                    }
                    for movie in data["results"]
                ]

                # Stocker en cache pour éviter de refaire la requête
                await cache.set(cache_key, formatted_results)

                return formatted_results
            else:
                return {"error": f"Erreur {response.status}"}

