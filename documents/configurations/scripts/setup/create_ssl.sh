#!/bin/bash

# Defina as informações da empresa
CN="dockersky.com"
C="BR"
ST="Rio de Janeiro"
L="Macaé"
O="Docker Sky Ltda"
OU="Tecnologia"
EMAIL="cosme.alex@gmail.com"
EAB_KEY_ID="e50796983b5b16cb18a68604bd1ccd34"
EAB_HMAC_KEY="YI5PXZb8Cs-9hkfXvs5QrFK4MX_mYDWpdblQGOLmLiyuYVvCWNr5FCzkI8BZBW83rSSwRQYQLJoSYVA1Mhn1Xg"


# Instala o Certbot e o plugin do Google
sudo apt-get update -y
sudo apt-get install certbot python3-certbot-nginx python3-certbot-dns-google -y


# Crie o diretório para armazenar as chaves
if test -d /etc/ssl/private; then
    echo "O diretório /etc/ssl/private já existe."
else
    echo "Criando o diretório /etc/ssl/private..."
    sudo mkdir -p /etc/ssl/private
fi

if test -d /etc/ssl/certs; then
    echo "O diretório /etc/ssl/certs já existe."
else
    echo "Criando o diretório /etc/ssl/certs..."
    sudo mkdir -p /etc/ssl/certs
fi

# Testa se o arquivo existe e remove caso exista
if test -f /etc/ssl/private/dockersky.com.key; then
    echo "O arquivo /etc/ssl/private/dockersky.com.key já existe. Removendo..."
    sudo rm /etc/ssl/private/dockersky.com.key
fi

# Testa se o arquivo existe e remove caso exista
if test -f /etc/ssl/certs/dockersky.com.crt; then
    echo "O arquivo /etc/ssl/certs/dockersky.com.crt já existe. Removendo..."
    sudo rm /etc/ssl/certs/dockersky.com.crt
fi


# Gere a chave privada
sudo openssl genrsa -out /etc/ssl/private/$CN.key 4096

# Gere o certificado autoassinado usando a chave privada e as informações da empresa
sudo openssl req -new -x509 -key /etc/ssl/private/$CN.key -out /etc/ssl/certs/$CN.crt -days 365 -subj "/C=$C/ST=$ST/L=$L/O=$O/OU=$OU/CN=$CN/emailAddress=$EMAIL"

# Registre seu e-mail com a Let's Encrypt e crie uma chave de API
sudo certbot register --email $EMAIL --no-eff-email --server "https://dv.acme-v02.api.pki.goog/directory" --eab-kid $EAB_KEY_ID --eab-hmac-key $EAB_HMAC_KEY

# Solicite um novo certificado SSL para o seu domínio usando o certbot
sudo certbot certonly -d $CN --server "https://dv.acme-v02.api.pki.goog/directory" --standalone

# Exiba informações sobre o certificado
sudo openssl x509 -in /etc/letsencrypt/live/$CN/fullchain.pem -text -noout
