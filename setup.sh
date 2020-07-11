#!/bin/bash

docker build --build-arg UID=$UID -t networking_monitor .


docker-compose run --rm monitoring
