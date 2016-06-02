#include "v8cffi_exceptions.h"
#include "v8cffi_utils.h"
#include "v8cffi_trace_back.h"
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


std::string Context::runScript(
  const std::string &input_script,
  const std::string &identifier)
{
  v8::Locker l(m_isolate);
  v8::Isolate::Scope isolate_scope(m_isolate);
  v8::HandleScope handle_scope(m_isolate);
  v8::Local<v8::Context> context = v8::Local<v8::Context>::New(
    m_isolate, m_pers_context);  // Materialize the persistent context
  v8::Context::Scope context_scope(context);
  v8::Local<v8::String> source = v8cffi_utils::toV8String(m_isolate, input_script);
  v8::ScriptOrigin origin(v8cffi_utils::toV8String(m_isolate, identifier));
  v8::TryCatch try_catch;
  v8::MaybeLocal<v8::Script> script_maybe = v8::Script::Compile(
    context, source, &origin);

  if (script_maybe.IsEmpty())
    throw v8cffi_exceptions::JSError(
      v8cffi_trace_back::prettyTraceBack(m_isolate, try_catch));

  v8::Local<v8::Script> script = script_maybe.ToLocalChecked();
  v8::MaybeLocal<v8::Value> result_maybe = script->Run(context);

  if (result_maybe.IsEmpty())
    throw v8cffi_exceptions::JSError(
      v8cffi_trace_back::prettyTraceBack(m_isolate, try_catch));

  v8::Local<v8::Value> result = result_maybe.ToLocalChecked();
  v8::String::Utf8Value result_utf8_str(result);
  return v8cffi_utils::toCString(result_utf8_str);
}
