FROM python:3.9-slim

WORKDIR /app

# Copie des fichiers nécessaires
COPY requirements.txt .
COPY src/ ./src/

# Installation des dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Vérification que le fichier principal existe
RUN test -f "/app/src/monitor.py" || { echo "ERREUR: monitor.py non trouvé"; exit 1; }

CMD ["python", "./src/monitor.py"]
