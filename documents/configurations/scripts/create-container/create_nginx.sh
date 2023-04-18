#!/bin/bash

# Carrega as variáveis de ambiente do arquivo .env
source .env

if [ $# -lt 1 ]; then
    echo "Uso: $0 <container name>"
    exit 1
fi

CONTAINER_NAME=$1
CONTAINER_VOLUME="${CONTAINER_NAME}_vol"

echo "Criando container ${CONTAINER_NAME}"

# Cria o volume
docker volume create ${CONTAINER_VOLUME}

# Inicia o container
docker run -d \
  --name ${CONTAINER_NAME} \
  -p 0:80 \
  -v ${CONTAINER_VOLUME}:/usr/share/nginx/html \
  --network=proxy_net \
  -e "VIRTUAL_HOST=${CONTAINER_NAME}.${DOMINIO}" \
  -e "VIRTUAL_PORT=80" \
  -e "LETSENCRYPT_HOST=${CONTAINER_NAME}.${DOMINIO}" \
  -e "LETSENCRYPT_EMAIL=${LETSENCRYPT_EMAIL}" \
  --label "traefik.enable=true" \
  --label "traefik.http.routers.${CONTAINER_NAME}.rule=Host(\`${CONTAINER_NAME}.${DOMINIO}\`)" \
  --label "traefik.http.routers.${CONTAINER_NAME}.entrypoints=https" \
  --label "traefik.http.routers.${CONTAINER_NAME}.tls.certresolver=http" \
  --label "traefik.http.routers.${CONTAINER_NAME}.service=${CONTAINER_NAME}" \
  --label "traefik.http.services.${CONTAINER_NAME}.loadbalancer.server.port=80" \
  nginx:latest

echo "Container ${CONTAINER_NAME} criado com sucesso e disponível em https://${CONTAINER_NAME}.${DOMINIO}"
