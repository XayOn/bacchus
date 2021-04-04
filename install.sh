#!/bin/bash

#step=web_env docker run xayon/bacchus

docker-compose -pbacchus up -d
docker-compose -pbacchus up bacchus && docker-compose -pbacchus stop
docker-compose -pbacchus up -d
