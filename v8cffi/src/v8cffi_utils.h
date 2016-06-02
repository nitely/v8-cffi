#ifndef V8CFFI_UTILS_H_INCLUDED
#define V8CFFI_UTILS_H_INCLUDED

#include <string.h>
#include <string>

#include "include/libplatform/libplatform.h"
#include "include/v8.h"


namespace v8cffi_utils
{
  v8::Local<v8::String> toV8String(
    v8::Isolate *isolate,
    const std::string &str);
  std::string toCString(const v8::String::Utf8Value &str_utf8);
}


#endif
