FROM python:3.10-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo de dependencias
COPY requirements.txt .

# Instalar las dependencias
RUN pip install -r requirements.txt

# Copiar el código fuente
COPY app.py utils.py ./

# Comando por defecto
CMD ["python", "app.py"]