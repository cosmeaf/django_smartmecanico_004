# set image name
ARG image_name

# pull the official base image
FROM python:3

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Image Name
LABEL image_name=${image_name}

# set work directory
WORKDIR /app

RUN apt update
RUN apt install -y cron && touch /var/log/cron.log
RUN apt-get install -yq tzdata
RUN apt autoclean

# TIME ZONE
ENV TZ="America/Sao_Paulo"

# install dependencies
RUN pip install --upgrade pip

COPY ./requirements.txt /app

RUN pip install --no-cache-dir -r /app/requirements.txt

# copy project
COPY . /app

EXPOSE 443

CMD ["gunicorn", "--workers", "2", "smartMecanico.wsgi", "-b", "0.0.0.0:443", "--certfile", "fullchain.pem", "--keyfile", "privkey.pem", "--log-level", "debug"]