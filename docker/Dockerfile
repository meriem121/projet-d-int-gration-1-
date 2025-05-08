# Utiliser une image Python officielle
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires
COPY requirements.txt .
COPY src/ ./src/

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Définir la commande par défaut
CMD ["python", "./src/monitor.py"]
