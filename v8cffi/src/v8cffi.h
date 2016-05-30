// This public header exposes a bunch
// of C APIs hiding all the C++ stuff,
// it's a layer bridging C to C++

#ifndef V8CFFI_H_INCLUDED
#define V8CFFI_H_INCLUDED

#ifndef V8CFFI_API
#  ifdef _WIN32
#     if defined(V8CFFI_SHARED) /* build dll */
#         define V8CFFI_API __declspec(dllexport)
#     elif !defined(V8CFFI_BUILD_STATIC) /* use dll */
#         define V8CFFI_API __declspec(dllimport)
#     else /* static library */
#         define V8CFFI_API
#     endif
#  else
#     define V8CFFI_API
#  endif
#endif

#ifdef __cplusplus
extern "C"
{
#endif


typedef enum
{
  E_V8_OK = 0,
  E_V8_OUT_OF_MEM_ERROR,
  E_V8_JS_ERROR,
  E_V8_UNKNOWN_ERROR
} v8_code;

V8CFFI_API void v8cffi_free(void *ptr);

typedef struct v8cffi_platform_s v8cffi_platform_t;

V8CFFI_API v8_code v8cffi_platform_new(
  v8cffi_platform_t **platform,
  const char *natives_blob,
  size_t natives_blob_len,
  const char *snapshot_blob,
  size_t snapshot_blob_len);
V8CFFI_API void v8cffi_platform_free(v8cffi_platform_t *platform);

typedef struct v8cffi_vm_s v8cffi_vm_t;

V8CFFI_API v8_code v8cffi_vm_new(v8cffi_vm_t **vm);
V8CFFI_API void v8cffi_vm_free(v8cffi_vm_t *vm);

typedef struct v8cffi_context_s v8cffi_context_t;

V8CFFI_API v8_code v8cffi_context_new(v8cffi_context_t **ctx, v8cffi_vm_t *vm);
V8CFFI_API void v8cffi_context_free(v8cffi_context_t *ctx);

V8CFFI_API v8_code v8cffi_run_script(
  v8cffi_context_t *ctx,
  const char *input_script,
  size_t input_script_len,
  const char *identifier,
  size_t identifier_len,
  char **output,
  size_t *output_len,
  char **error,
  size_t *error_len);

#ifdef __cplusplus
}
#endif

#endif
