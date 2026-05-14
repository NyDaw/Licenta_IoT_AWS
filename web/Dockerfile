# Folosim o imagine oficială și ușoară de Python
FROM python:3.9-slim

# Setăm folderul de lucru în container
WORKDIR /app

# Copiem fișierele noastre web în container
COPY app.py .
COPY templates/ templates/

# Instalăm bibliotecile necesare
RUN pip install flask paho-mqtt

# Expunem portul pe care rulează Flask
EXPOSE 5000

# Comanda de pornire a site-ului
CMD ["python", "app.py"]