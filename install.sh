#!/bin/bash

[[ $# == 5 ]] || {
    echo "Usage: $0 user password host email gandiv5_api_key"; exit 1
}

mkdir data
touch data/.env_jackett_sync
touch data/create_db.sh 

ip=$(curl ifconfig.co)

cat << EOL >.env
NEXTCLOUD_ADMIN_USER=$1
NEXTCLOUD_ADMIN_PASSWORD=$2
host=$3
email=$4
public_ip=$ip
GANDIV5_API_KEY=$5

dns_provider=gandiv5
dns_provider_credentials=--api-protocol rest --auth-token ${GANDIV5_API_KEY} 

COMPOSE_PROJECT_NAME=bacchus
PEERS=2
PID=1000
PUID=1000
PGID=1000
POSTGRES_PASSWORD=pgpw
POSTGRES_USER=pguser
POSTGRES_DB=pguser
POSTGRES_HOST=postgres
NEXTCLOUD_TRUSTED_DOMAINS=cloud.\${host}
OVERWRITEPROTOCOL=https
extra_params=--o:ssl.enable=false --o:ssl.termination=true
NEXTCLOUD_UPDATE=1
SERVERURL=public.\${host}
private_ip=172.29.0.32
PEERDNS=172.29.0.4
ALLOWEDIPS=172.29.0.0/24
SERVERURL=public.\${host}
SERVERPORT=51820
step=first
SYNAPSE_CONFIG_DIR="/data"
SYNAPSE_CONFIG_PATH="/data/homeserver.yaml"
SYNAPSE_REPORT_STATS="no"
SYNAPSE_SERVER_NAME=\${host}
EOL


#step=web_env docker run xayon/bacchus
docker-compose -pbacchus up -d
