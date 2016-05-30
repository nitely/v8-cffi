#include "v8cffi_exceptions.h"
#include "v8cffi_context.h"

using namespace v8cffi_context;


Context::Context(v8::Isolate *isolate)
{
  m_isolate = isolate;

  v8::Locker l(m_isolate);
  v8::Isolate::Scope isolate_scope(m_isolate);
  v8::HandleScope handle_scope(m_isolate);
  m_pers_context.Reset(m_isolate, v8::Context::New(m_isolate));
}


Context::~Context() {
  m_pers_context.Reset();
  // isolate gets disposed elsewhere
}


std::string Context::runScript(const std::string &input_script)
{
  v8::Locker l(m_isolate);
  v8::Isolate::Scope isolate_scope(m_isolate);
  v8::HandleScope handle_scope(m_isolate);
  v8::Local<v8::Context> context = v8::Local<v8::Context>::New(
    m_isolate, m_pers_context);  // Materialize the persistent context
  v8::Context::Scope context_scope(context);
  v8::Local<v8::String> source = v8::String::NewFromUtf8(
    m_isolate,
    input_script.c_str(),
    v8::NewStringType::kNormal,
    input_script.length()).ToLocalChecked();
  v8::TryCatch try_catch;
  v8::MaybeLocal<v8::Script> script_maybe = v8::Script::Compile(context, source);

  if (script_maybe.IsEmpty())
  {
    v8::String::Utf8Value error_utf8_str(try_catch.Exception());
    throw v8cffi_exceptions::JSError(
      std::string(*error_utf8_str, error_utf8_str.length()));
  }

  v8::Local<v8::Script> script = script_maybe.ToLocalChecked();
  v8::MaybeLocal<v8::Value> result_maybe = script->Run(context);

  if (result_maybe.IsEmpty())
  {
    v8::String::Utf8Value error_utf8_str(try_catch.StackTrace());
    throw v8cffi_exceptions::JSError(
      std::string(*error_utf8_str, error_utf8_str.length()));
  }

  v8::Local<v8::Value> result = result_maybe.ToLocalChecked();
  v8::String::Utf8Value result_utf8_str(result);
  return std::string(*result_utf8_str, result_utf8_str.length());
}
