import asyncio
from pprint import pprint
from Gestion_erreur import Gerreur
import requests
from dotenv import load_dotenv
import os
import aiohttp
from aiocache import Cache
from downoaldFILM import download_film

load_dotenv() #charger lenvi

#recup la cle
TMDB_API_KEY=os.getenv("TMDB_API_KEY")

#verifer si la cle est bien charge
if not TMDB_API_KEY:
    raise ValueError ("Cle non defini dans .env")


# Initialisation du cache avec une expiration d’1 heure (3600 sec)
cache = Cache(Cache.MEMORY, ttl=3600)  # Stocke en mémoire avec expiratio


async def get_movie_details(movie_id):

    cache_key=(f"movie_{movie_id}")  # Clé unique pour stocker la réponse en cache

    cached_response= await cache.get(cache_key)# Vérifier si la réponse est déjà en cache

    if cached_response:
        print(f"🟢 Résultat en cache trouvé pour le film {movie_id}")
        return cached_response
    #appel avec url et param
    url=f"https://api.themoviedb.org/3/movie/{movie_id}"
    params={"api_key":TMDB_API_KEY,"language":"fr-FR"}
  
    #    data=response.json()
    async with aiohttp.ClientSession() as session:
      data= await Gerreur(session,url,params)
    if 'error' in data:
        return data
    
    # Stocker le résultat en cache pour 1 heure
    await cache.set(cache_key,data)

    return {
           'title':data.get("title"),
            'genres':[genre['name']for genre in data.get('genres',[])],
            'popularity':data.get('popularity'),
            'vote_average':data.get('vote_average'),
            }
    