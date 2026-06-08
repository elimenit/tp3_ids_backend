FROM python:latest

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 15000

ENV PYTHONUNBUFFERED=1

# Ejecutar la aplicación
CMD ["python3", "app.py"]