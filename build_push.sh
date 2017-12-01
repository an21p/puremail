#!/bin/bash
clear

FILE=docker-compose-prod.yml

docker-compose -f $FILE build
docker push espenfolke/puremail_web:latest
docker push espenfolke/puremail_migration:latest
docker push espenfolke/puremail_nginx:latest
