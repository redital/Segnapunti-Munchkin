# Immagine base
FROM python:3.11-slim

# Impostazioni di lavoro
WORKDIR /app

# Copia i file necessari
COPY . /app

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# Espone la porta 5000
EXPOSE 5000

# Avvia l'app Flask
CMD ["python", "app.py"]

