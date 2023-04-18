#!/bin/bash

# Função para exibir status ok
status_ok() {
  echo -e "[\e[32mstatus ok\e[0m] $1"
}

# Função para exibir status failed
status_failed() {
  echo -e "[\e[31mstatus failed\e[0m] $1"
}

# Verifica se o IP já está presente no arquivo hosts
if grep -q "173.224.117.181" /etc/hosts; then
  # Comenta a linha existente
  sudo sed -i 's/173.224.117.181/#173.224.117.181/' /etc/hosts
  status_ok "IP comentado no arquivo hosts"
else
  # Adiciona nova linha
  echo "173.224.117.181    dockersky.com    dockersky" | sudo tee -a /etc/hosts > /dev/null
  status_ok "Nova linha adicionada no arquivo hosts"
fi

# Adiciona DNS do Google ao arquivo resolv.conf
if sudo grep -q "nameserver 8.8.8.8" /etc/resolv.conf; then
  status_ok "DNS do Google já presente no arquivo resolv.conf"
else
  sudo sh -c 'echo "nameserver 8.8.8.8" >> /etc/resolv.conf'
  sudo sh -c 'echo "nameserver 8.8.4.4" >> /etc/resolv.conf'
  status_ok "DNS do Google adicionado ao arquivo resolv.conf"
fi

# Altera o nome do hostname
if [ "$(hostname)" == "dockersky" ]; then
  status_ok "Nome do hostname já está correto"
else
  sudo hostnamectl set-hostname dockersky
  sudo hostnamectl set-hostname "Dockersky Server" --pretty
  status_ok "Nome do hostname alterado"
fi

# Cria um novo usuário com privilégios sudo
if id "cosmeaf" >/dev/null 2>&1; then
  status_ok "Usuário cosmeaf já existe"
else
  sudo useradd -s /bin/bash -c "Support Administrator" -d /home/cosmeaf/ -m cosmeaf
  echo 'cosmeaf:qweasd32' | sudo chpasswd
  status_ok "Novo usuário cosmeaf criado com sucesso"
fi

# Adiciona o novo usuário ao grupo sudo
if groups cosmeaf | grep &>/dev/null '\bsudo\b'; then
  status_ok "Usuário cosmeaf já está no grupo sudo"
else
  sudo usermod -aG sudo cosmeaf
  status_ok "Usuário cosmeaf adicionado ao grupo sudo"
fi

# Adiciona permissão para o usuário cosmeaf no sudoers
if sudo grep -q "^cosmeaf.*NOPASSWD:ALL$" /etc/sudoers; then
  status_ok "Usuário cosmeaf já tem permissão no sudoers"
else
  echo "cosmeaf ALL=(ALL) NOPASSWD:ALL" | sudo tee -a /etc/sudoers.d/cosmeaf > /dev/null
  status_ok "Usuário cosmeaf adicionado às permissões do sudoers"
fi

# Exibe mensagem de status failed caso algum comando tenha falhado
if [ $? -ne 0 ]; then
  status_failed "Erro ao executar algum comando"
fi
