#include "v8cffi_utils.h"

using namespace v8cffi_utils;


v8::Local<v8::String> v8cffi_utils::toV8String(
  v8::Isolate *isolate,
  const std::string &str)
{
  return v8::String::NewFromUtf8(
    isolate,
    str.c_str(),
    v8::NewStringType::kNormal,
    str.length()).ToLocalChecked();
}


std::string v8cffi_utils::toCString(const v8::String::Utf8Value &str_utf8)
{
  return std::string(*str_utf8, str_utf8.length());
}
