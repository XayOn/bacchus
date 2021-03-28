#!/bin/bash

#step=web_env docker run xayon/bacchus

for step in first second third; do 
  step=${step} docker-compose -pbacchus up
  while read i; do if [ "$i" = bacchus_install_${step} ]; then break; fi; done < <(inotifywait  -e create,open --format '%f' --quiet ./data/bacchus --monitor)
  docker-compose -pbacchus stop
done
