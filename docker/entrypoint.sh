#!/bin/sh
set -e

cd /logfiles
echo python3 ../replay-data.py "$@"
exec python3 ../replay-data.py "$@"