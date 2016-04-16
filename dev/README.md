# Output

After building the V8, files are copied into the project,
the output will look like this:

```bash
$ cd ./v8cffi/lib/v8
$ tree --charset=ascii

.
|-- include
|   |-- libplatform
|   |   `-- libplatform.h
|   |-- OWNERS
|   |-- v8config.h
|   |-- v8-debug.h
|   |-- v8-experimental.h
|   |-- v8.h
|   |-- v8-platform.h
|   |-- v8-profiler.h
|   |-- v8-testing.h
|   |-- v8-util.h
|   `-- v8-version.h
|-- LICENSE.v8
|-- natives_blob.bin
|-- release
|   |-- libicudata.a
|   |-- libicui18n.a
|   |-- libicuuc.a
|   |-- libv8_base.a
|   |-- libv8_external_snapshot.a
|   |-- libv8_libbase.a
|   `-- libv8_libplatform.a
`-- snapshot_blob.bin
```


# Building

It currently builds Linux_x64 libraries.

1. Install [Docker Compose](https://docs.docker.com/compose/install/)
2. Run `$ bash ./up.sh`
