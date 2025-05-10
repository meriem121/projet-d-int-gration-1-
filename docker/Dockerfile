FROM python:3.9-slim

WORKDIR /app

# Copie avec vérification explicite
COPY requirements.txt .
COPY src/monitor.py ./src/monitor.py

# Installation des dépendances avec vérification
RUN pip install --no-cache-dir -r requirements.txt && \
    [ -f "/app/src/monitor.py" ] || { echo "ERREUR: monitor.py non trouvé"; exit 1; }

CMD ["python", "./src/monitor.py"]
