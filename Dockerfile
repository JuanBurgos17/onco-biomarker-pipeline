# Usar una imagen oficial de Python ligera y optimizada
FROM python:3.10-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias del sistema necesarias si se requiere compilación
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar el archivo de requerimientos e instalarlos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código fuente, carpetas de modelos y configuración al contenedor
COPY . .

# Exponer el puerto por el que corre FastAPI
EXPOSE 8000

# Comando por defecto para arrancar la API en producción
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]