import requests
import time
import aiohttp
import asyncio


async def Gerreur(session,url,params,max_retries=5):
 for attemp in range(max_retries):
  try:
      async with session.get(url,params=params) as response:
        
        status=response.status
        if status==200:
            return await response.json()
            # Gestion des erreurs API
        elif status == 400:
            return {"error": "400 Bad Request - Requête invalide. Vérifiez les paramètres envoyés."}
        elif status == 401:
            return {"error": "401 Unauthorized - Clé API manquante ou invalide."}
        elif status == 403:
            return {"error": "403 Forbidden - Accès interdit, peut-être dû à un quota dépassé."}
        elif status == 404:
            return {"error": "404 Not Found - Ressource non trouvée. Vérifiez l'ID du film."}    
        elif status==429:
            wait_time=2**attemp
            print(f"🚨 429 Too Many Requests - Attente de {wait_time} secondes avant retry...") 
            time.sleep(wait_time)
        elif status in [500,503]:
            wait_time=2**attemp
            print(f"⚠️ {status} Erreur serveur - Tentative {attemp+1}/{max_retries}, attente {wait_time}s...")
            time.sleep(wait_time)
        else:
            print(f'{status} erreur veuillez ressyer')
  except aiohttp.ClientError as e:
     print(f"🔴 Erreur de connexion : {e}. Retrying...")
     await asyncio.sleep(2 ** attemp)  # Attente exponentielle

 return {"error": f"Échec après {max_retries} tentatives."}