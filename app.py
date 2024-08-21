from dotenv import load_dotenv
import os
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer la clé API des variables d'environnement
api_key = os.getenv('GOOGLE_API_KEY')

if not api_key:
    raise ValueError("Clé API non trouvée. Assurez-vous qu'elle est définie dans le fichier .env.")

# Configurer l'API
genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-pro')

# Application FastAPI
app = FastAPI()

# Modèle de requête pour FastAPI
class BadWordsRequest(BaseModel):
    input: str

# Endpoint pour classifier les mots offensants
@app.post("/detect")
def bad_words_classifier(request: BadWordsRequest):
    input_text = request.input
    response = model.generate_content(f"""
    Vous recevez une phrase en entrée. Votre tâche est de déterminer si la phrase contient un langage inapproprié ou offensant en anglais ou en français. Si la phrase contient des mots offensants, répondez par "Oui". Si la phrase ne contient aucun mot offensant, répondez par "Non".

    Input: {input_text}
    """)
    if "Oui" in response.text:
        return {"result": True}
    return {"result": False}

# Gestion des erreurs
@app.exception_handler(HTTPException)
def http_exception_handler(request, exc):
    return {"detail": exc.detail}
