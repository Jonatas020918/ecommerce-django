# Dockerfile
# Imagem base do Python
FROM python:3.10-slim

# Defina o diretório de trabalho
WORKDIR /app

# Copie o requirements.txt e instale as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código do projeto
COPY . .

# Defina a variável de ambiente do Django
ENV DJANGO_SETTINGS_MODULE=ecommerce_django.settings

# Comando para rodar o Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
