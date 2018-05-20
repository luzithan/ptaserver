#!/bin/bash

source .env
docker-machine create --driver=digitalocean --digitalocean-access-token=$DO_TOKEN --digitalocean-size=1gb ptaserver
eval $(docker-machine env ptaserver)
docker-compose up -d
