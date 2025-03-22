import datetime
import requests
import os
import json

def download_film():
    #recup la date actuel
    
    
    #construire lurl du ficher
    file_name = "adult_movie_ids_01_30_2025.json"
    file_path = os.path.join("C:/Users/pc/Desktop/Ftest/", file_name)
    

    if not os.path.exists(file_path):
        print(f"❌ Fichier introuvable : {file_path}")
        print("ℹ️ Télécharge-le ici : https://developer.themoviedb.org/docs/daily-id-exports")
        return None

    print(f"📂 Chargement du fichier JSON : {file_path}")

    
    try:
        # ✅ Lire le fichier JSON ligne par ligne
        movies = []
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                movies.append(json.loads(line))  # ✅ Lire chaque ligne comme un objet JSON
        
        print(f"✅ {len(movies)} films chargés avec succès !")
        return movies

    except json.JSONDecodeError as e:
        print(f"⚠️ Erreur de lecture du fichier JSON : {e}")
        return None