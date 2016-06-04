# -*- coding: utf-8 -*-

import os

from cffi import FFI


SRC_PATH = os.path.join('v8cffi', 'src')
STATIC_LIBS_PATH = os.path.join(SRC_PATH, 'v8', 'release')

ffi = FFI()

ffi.set_source(
    "_v8",
    """
    #include "v8cffi.h"
    """,
    language='c++',
    source_extension='.cpp',
    extra_compile_args=['-std=c++11'],
    extra_link_args=['-lrt', '-ldl', '-std=c++11'],
    include_dirs=[
        SRC_PATH,
        os.path.join(SRC_PATH, 'v8')],
    sources=[
        os.path.join(SRC_PATH, 'v8cffi.cpp'),
        os.path.join(SRC_PATH, 'v8cffi_context.cpp'),
        os.path.join(SRC_PATH, 'v8cffi_platform.cpp'),
        os.path.join(SRC_PATH, 'v8cffi_trace_back.cpp'),
        os.path.join(SRC_PATH, 'v8cffi_utils.cpp'),
        os.path.join(SRC_PATH, 'v8cffi_vm.cpp')],
    extra_objects=[
        '-Wl,--start-group',
        os.path.join(STATIC_LIBS_PATH, 'libv8_base.a'),
        os.path.join(STATIC_LIBS_PATH, 'libv8_libbase.a'),
        os.path.join(STATIC_LIBS_PATH, 'libv8_external_snapshot.a'),
        os.path.join(STATIC_LIBS_PATH, 'libv8_libplatform.a'),
        os.path.join(STATIC_LIBS_PATH, 'libicuuc.a'),
        os.path.join(STATIC_LIBS_PATH, 'libicui18n.a'),
        os.path.join(STATIC_LIBS_PATH, 'libicudata.a'),
        '-Wl,--end-group'])


ffi.cdef(
    """
    typedef enum
    {
      E_V8_OK = 0,
      E_V8_OUT_OF_MEM_ERROR,
      E_V8_JS_ERROR,
      E_V8_UNKNOWN_ERROR
    } v8_code;

    void v8cffi_free(void *ptr);

    typedef struct v8cffi_platform_s v8cffi_platform_t;

    v8_code v8cffi_platform_new(
      v8cffi_platform_t **platform,
      const char *natives_blob,
      size_t natives_blob_len,
      const char *snapshot_blob,
      size_t snapshot_blob_len);
    void v8cffi_platform_free(v8cffi_platform_t *platform);

    typedef struct v8cffi_vm_s v8cffi_vm_t;

    v8_code v8cffi_vm_new(v8cffi_vm_t **vm);
    void v8cffi_vm_free(v8cffi_vm_t *vm);

    typedef struct v8cffi_context_s v8cffi_context_t;

    v8_code v8cffi_context_new(v8cffi_context_t **ctx, v8cffi_vm_t *vm);
    void v8cffi_context_free(v8cffi_context_t *ctx);

    v8_code v8cffi_run_script(
      v8cffi_context_t *ctx,
      const char *input_script,
      size_t input_script_len,
      const char *identifier,
      size_t identifier_len,
      char **output,
      size_t *output_len,
      char **error,
      size_t *error_len);
    """)


if __name__ == "__main__":
    ffi.compile(verbose=1)
    print('ok')
