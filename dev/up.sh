#!/bin/bash

set -o pipefail
set -e

echo "Running docker-compose up"
docker-compose up -d

echo "Copying compiled files"
docker cp dev_v8cffi_1:/code/out ../v8cffi/src/v8

