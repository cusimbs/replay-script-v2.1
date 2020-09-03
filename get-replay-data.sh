#!/bin/sh
set -e

mkdir -p logfiles
#docker run --rm --name replay-data  -v logfiles:/logfiles replay-data python3 ../replay-data.py "$@"
docker start replay-data
echo "Procesing files"
docker exec -w /logfiles replay-data python3 /replay-data.py "$@"
docker stop replay-data