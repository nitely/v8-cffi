#include <string.h>
#include <string>
#include <new>  // std::bad_alloc

#include "v8cffi_platform.h"
#include "v8cffi_vm.h"
#include "v8cffi_context.h"
#include "v8cffi_exceptions.h"
#include "v8cffi.h"

#define AS_TYPE(Type, Obj) reinterpret_cast<Type *>(Obj)
#define AS_CTYPE(Type, Obj) reinterpret_cast<const Type *>(Obj)


/*
 * @brief Wrapper for exposing the C's free function.
 * @param ptr The pointer to free.
 * */
void v8cffi_free(void *ptr)
{
  free(ptr);
  ptr = NULL;
}


/*
 * @brief Instantiate a Platform.
 * It must be instance only once per process,
 * this is enforced by V8.
 * @param platform Opaque type.
 * @param natives_blob Binary data read from the .bin file.
 * @param natives_blob_len Binary data length.
 * @param snapshot_blob Binary data read from the .bin file.
 * @param snapshot_blob_len Binary data length.
 * @return Status code
 * */
v8_code v8cffi_platform_new(
  v8cffi_platform_t **platform,
  const char *natives_blob,
  size_t natives_blob_len,
  const char *snapshot_blob,
  size_t snapshot_blob_len)
{
  try
  {
    *platform = AS_TYPE(v8cffi_platform_t, new v8cffi_platform::Platform(
        std::string(natives_blob, natives_blob_len),
        std::string(snapshot_blob, snapshot_blob_len)));
  }
  catch (const std::bad_alloc &e)
  {
    return E_V8_OUT_OF_MEM_ERROR;
  }
  catch (...)
  {
    return E_V8_UNKNOWN_ERROR;
  }

  return E_V8_OK;
}


/*
 * @brief Destruct the Platform.
 * @param platform Opaque type.
 * */
void v8cffi_platform_free(v8cffi_platform_t *platform)
{
  if (!platform)
    return;

  delete AS_TYPE(v8cffi_platform::Platform, platform);
}


/*
 * @brief Instantiate a VM which is a V8::Isolate manager.
 * @param vm Opaque type.
 * @return Status code
 * */
v8_code v8cffi_vm_new(v8cffi_vm_t **vm)
{
  try
  {
    *vm = AS_TYPE(v8cffi_vm_t, new v8cffi_vm::VM());
  }
  catch (const std::bad_alloc &e)
  {
    return E_V8_OUT_OF_MEM_ERROR;
  }
  catch (...)
  {
    return E_V8_UNKNOWN_ERROR;
  }

  return E_V8_OK;
}


/*
 * @brief Destruct the VM.
 * @param vm Opaque type.
 * */
void v8cffi_vm_free(v8cffi_vm_t *vm)
{
  if (!vm)
    return;

  delete AS_TYPE(v8cffi_vm::VM, vm);
}


/*
 * @brief Instantiate a Context to run JS code.
 * @param ctx Opaque type.
 * @param vm Opaque type, referencing a instantiated VM.
 * @return Status code
 * */
v8_code v8cffi_context_new(v8cffi_context_t **ctx, v8cffi_vm_t *vm)
{
  try
  {
    *ctx = AS_TYPE(
      v8cffi_context_t,
      new v8cffi_context::Context(AS_TYPE(v8cffi_vm::VM, vm)->getIsolate()));
  }
  catch (const std::bad_alloc &e)
  {
    return E_V8_OUT_OF_MEM_ERROR;
  }
  catch (...)
  {
    return E_V8_UNKNOWN_ERROR;
  }

  return E_V8_OK;
}


/*
 * @brief Destruct the Context.
 * @param ctx Opaque type.
 * */
void v8cffi_context_free(v8cffi_context_t *ctx)
{
  if (!ctx)
    return;

  delete AS_TYPE(v8cffi_context::Context, ctx);
}


/*
 * Create a string copy and return it.
 * Caller must free it later.
 * Return NULL when out of memory.
 * */
char *str_dup(const char *s, size_t len) {
  char *d = (char *) malloc(len + 1);  // + null char

  if (d == NULL)
    return NULL;
  else
    return (char *) memcpy(d, s, len + 1);
}


/*
 * Copy a C++ string into a C string destination.
 * Return false when out of memory or true otherwise.
 * */
bool str_copy(const std::string &str, char **out_str, size_t *out_len)
{
  *out_len = str.length();
  *out_str = str_dup(str.c_str(), *out_len);

  if (*out_str == NULL)
    return false;
  else
    return true;
}


/*
 * @brief Run JS code, the JS state is saved across calls.
 * @param ctx Opaque type, instantiated Context.
 * @param input_script JS code to be ran, must be utf-8 encoded.
 * @param input_script_len JS code length.
 * @param output Storage for the JS result, utf-8 encoded.
 * @param output_len JS result length.
 * @param error Message for JS errors.
 * @param error_len Error message length.
 * @return Status code.
 * */
v8_code v8cffi_run_script(
  v8cffi_context_t *ctx,
  const char *input_script,
  size_t input_script_len,
  const char *identifier,
  size_t identifier_len,
  char **output,
  size_t *output_len,
  char **error,
  size_t *error_len)
{
  std::string output_str;

  try
  {
    output_str = AS_TYPE(v8cffi_context::Context, ctx)->runScript(
      std::string(input_script, input_script_len),
      std::string(identifier, identifier_len));
  }
  catch (const v8cffi_exceptions::JSError &e)
  {
    if (!str_copy(e.getMessage(), error, error_len))
      return E_V8_OUT_OF_MEM_ERROR;

    return E_V8_JS_ERROR;
  }
  catch (...)
  {
    return E_V8_UNKNOWN_ERROR;
  }

  if (!str_copy(output_str, output, output_len))
    return E_V8_OUT_OF_MEM_ERROR;

  return E_V8_OK;
}
