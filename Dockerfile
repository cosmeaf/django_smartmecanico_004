# Use a imagem oficial do Ubuntu como base
FROM ubuntu:20.04

# Definir variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TZ="America/Sao_Paulo"

# Instalar dependências
RUN apt update && \
    apt install -y python3 python3-pip cron tzdata && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
    apt autoclean

# Configurar o diretório de trabalho
WORKDIR /app

# Atualizar pip
RUN pip3 install --upgrade pip

# Copiar e instalar os requisitos do Python
COPY ./requirements.txt /app
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# Copiar o resto do código Django para o diretório de trabalho
COPY . /app
COPY .env /app/
RUN python3 manage.py collectstatic --no-input

# Expor a porta para o aplicativo
EXPOSE 8000

# Definir o comando para executar o aplicativo Django
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
#CMD ["gunicorn", "--workers", "2", "api.wsgi", "-b", "0.0.0.0:8002",  "--log-level", "debug"]
