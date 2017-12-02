#!/bin/bash
clear

FILE=docker-compose-prod.yml

docker-compose -f $FILE kill
docker-compose -f $FILE down
docker-compose -f $FILE up -d nginx
docker-compose -f $FILE up -d fixture
