# set image name
ARG image_name

# pull the official base image
FROM python:3.9

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Image Name
LABEL image_name=${image_name}

# set work directory
WORKDIR /usr/src/app/

RUN apt update
RUN apt install -y cron && touch /var/log/cron.log
RUN apt-get install -yq tzdata
RUN apt autoclean

# TIME ZONE
ENV TZ="America/Sao_Paulo"

# install dependencies
RUN pip install --upgrade pip

COPY ./requirements.txt /usr/src/app/

RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

# copy project
COPY . /usr/src/app/
COPY .env /usr/src/app/
RUN python manage.py collectstatic --no-input

EXPOSE 8000

CMD ["gunicorn", "--workers", "2", "api.wsgi", "-b", "0.0.0.0:8000", "--certfile", "fullchain.pem", "--keyfile", "privkey.pem", "--log-level", "debug"]

