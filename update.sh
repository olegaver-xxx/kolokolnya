#!/bin/bash

git fetch --all
git reset --hard origin/master
docker-compose build app
docker-compose up -d
