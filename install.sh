#!/bin/bash
mkdir data
touch data/.env_jackett_sync
touch data/create_db.sh 
#step=web_env docker run xayon/bacchus
docker-compose -pbacchus up -d
