# Utilise une image de base Python
FROM python:3.9

# Définit le dossier de travail
WORKDIR /usr/src/app

# Copie les fichiers nécessaires
COPY . .

# Installe les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Expose le port sur lequel l'application sera exécutée
EXPOSE 80

# Définit la commande pour démarrer l'application
CMD ["python", "./app/app.py" ]