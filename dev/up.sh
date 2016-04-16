#!/bin/bash

set -o pipefail
set -e

echo "Running docker-compose up"
docker-compose up -d

echo "Copying compiled files"

org_path="/code/build/v8"
dest_path="../v8cffi/src/v8"
statics_gyp_path="$org_path/out/x64.release/obj.target/tools/gyp"
statics_tp_path="$org_path/out/x64.release/obj.target/third_party/icu"

mkdir -p $dest_path/release

req_files_paths=(
    "$org_path/LICENSE.v8"
    "$org_path/include"
    "$org_path/out/x64.release/natives_blob.bin"
    "$org_path/out/x64.release/snapshot_blob.bin"
)
archives_paths=(
    "$statics_gyp_path/libv8_base.a"
    "$statics_gyp_path/libv8_libbase.a"
    "$statics_gyp_path/libv8_external_snapshot.a"
    "$statics_gyp_path/libv8_libplatform.a"
    "$statics_tp_path/libicuuc.a"
    "$statics_tp_path/libicui18n.a"
    "$statics_tp_path/libicudata.a"
)

for path in ${req_files_paths[*]}
do
    docker cp dev_v8cffi_1:$path $dest_path
done

for path in ${archives_paths[*]}
do
    docker cp dev_v8cffi_1:$path $dest_path/release
done

