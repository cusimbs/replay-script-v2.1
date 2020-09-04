#!/bin/sh
set -e
mkdir -p logfiles
docker run -it --mount type=bind,source=$(pwd)/logfiles,destination=/logfiles --name replay-data replay-data  gcloud init --console-only
