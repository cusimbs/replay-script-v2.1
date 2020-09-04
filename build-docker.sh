#!/bin/bash
set -e
cp replay-data.py docker
docker build -t replay-data docker