#!/bin/bash

set -o pipefail
set -e

echo "Running docker-compose up"
docker-compose up -d

echo "Copying compiled files"
docker cp v8cffi_master:/code/v8 ../v8cffi/src

