


docker network create proxy_net
docker volume create --driver local --name traefik_data
source .env
docker run -d \
  --name traefik \
  -p 80:80 \
  -p 443:443 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v traefik_data:/data \
  -v $(pwd)/traefik.toml:/traefik.toml:ro \
  -v $(pwd)/acme.json:/acme.json \
  --label "traefik.enable=true" \
  --label "traefik.http.routers.traefik.rule=Host(\`traefik.${DOMINIO}\`)" \
  --label "traefik.http.routers.traefik.entrypoints=https" \
  --label "traefik.http.routers.traefik.tls.certresolver=http" \
  --label "traefik.http.routers.traefik.service=api@internal" \
  --label "traefik.http.services.traefik.loadbalancer.server.port=8080" \
  --network proxy_net \
  traefik:v2.4 \
  --log.level=DEBUG \
  --api.insecure=true \
  --providers.docker=true \
  --providers.docker.exposedbydefault=false \
  --entrypoints.http.address=:80 \
  --entrypoints.https.address=:443 \
  --certificatesresolvers.http.acme.email=${EMAIL} \
  --certificatesresolvers.http.acme.storage=/acme.json \
  --certificatesresolvers.http.acme.httpchallenge=true \
  --certificatesresolvers.http.acme.httpchallenge.entrypoint=http
