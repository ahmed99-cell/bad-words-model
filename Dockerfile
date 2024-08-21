# Utiliser une image de base légère avec Python 3.9
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier requirements.txt dans le conteneur
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier tous les fichiers dans le conteneur
COPY . .

# Exposer le port sur lequel l'application va tourner
EXPOSE 8000

# Commande pour lancer l'application FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
