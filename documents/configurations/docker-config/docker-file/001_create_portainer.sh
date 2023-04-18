
docker volume create --driver local --name portainer_data

docker run -d \
  --name portainer \
  -p 0:9000 \
  -p 0:9443 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  -v /etc/letsencrypt:/certs \
  --network proxy_net \
  -e "VIRTUAL_HOST=portainer.${DOMINIO}" \
  -e "VIRTUAL_PORT=9000" \
  -e "LETSENCRYPT_HOST=portainer.${DOMINIO}" \
  -e "LETSENCRYPT_EMAIL=${EMAIL}" \
  --label "traefik.enable=true" \
  --label "traefik.http.routers.portainer.rule=Host(\`portainer.${DOMINIO}\`)" \
  --label "traefik.http.routers.portainer.entrypoints=https" \
  --label "traefik.http.routers.portainer.tls.certresolver=http" \
  --label "traefik.http.services.portainer.loadbalancer.server.port=9000" \
  portainer/portainer-ce:latest \
  --sslcert /certs/live/${DOMINIO}/fullchain.pem \
  --sslkey /certs/live/${DOMINIO}/privkey.pem
