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


v8::Local<v8::String> Context::toV8String(const std::string &str)
{
  return v8::String::NewFromUtf8(
    m_isolate,
    str.c_str(),
    v8::NewStringType::kNormal,
    str.length()).ToLocalChecked();
}


std::string Context::toCString(const v8::String::Utf8Value &str_utf8)
{
  return std::string(*str_utf8, str_utf8.length());
}


// todo: refactor
std::string Context::prettyTraceBack(const v8::TryCatch &try_catch)
{
  std::string trace_back = "";
  v8::String::Utf8Value error_utf8_str(try_catch.Exception());
  v8::MaybeLocal<v8::Message> message_maybe = try_catch.Message();

  // Error line with wavy underline indicator
  if (!message_maybe.IsEmpty())
  {
    v8::Local<v8::Message> message = message_maybe.ToLocalChecked();

    // Error source <file_name:line_num>
    v8::String::Utf8Value origin_str(
        message->GetScriptResourceName());
    int line_num_default = 0;
    int line_num = message->GetLineNumber(
        m_isolate->GetCurrentContext()).FromMaybe(line_num_default);
    trace_back += toCString(origin_str) +
      ":" +
      std::to_string(line_num) +
      "\n";

    v8::MaybeLocal<v8::String> source_line_maybe = message->GetSourceLine(
      m_isolate->GetCurrentContext());

    // Error line
    if (!source_line_maybe.IsEmpty())
    {
        v8::Local<v8::Value> source_line =
          source_line_maybe.ToLocalChecked();
        std::string padding = "    ";

        if (source_line->IsString())
          trace_back += padding +
            toCString(v8::String::Utf8Value(source_line)) +
            "\n" +
            padding;
    }

    // Wavy underline
    int source_col_start_default = 0;
    int source_col_start = message->GetStartColumn(
      m_isolate->GetCurrentContext()).FromMaybe(source_col_start_default);

    for (int i = 0; i < source_col_start; i++)
      trace_back += " ";

    int source_col_end_default = 0;
    int source_col_end = message->GetEndColumn(
      m_isolate->GetCurrentContext()).FromMaybe(source_col_end_default);

    for (int i = source_col_start; i < source_col_end; i++)
      trace_back += "^";

    trace_back += "\n";
  }

  v8::MaybeLocal<v8::Value> stack_trace_maybe = try_catch.StackTrace();

  if (!stack_trace_maybe.IsEmpty())
  {
    v8::Local<v8::Value> stack_trace = stack_trace_maybe.ToLocalChecked();

    if (stack_trace->IsString())
      trace_back += toCString(v8::String::Utf8Value(stack_trace));
  }
  else
    trace_back += toCString(error_utf8_str);

  return trace_back;
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
  v8::Local<v8::String> source = toV8String(input_script);
  v8::ScriptOrigin origin(toV8String(identifier));
  v8::TryCatch try_catch;
  v8::MaybeLocal<v8::Script> script_maybe = v8::Script::Compile(
    context, source, &origin);

  if (script_maybe.IsEmpty())
    throw v8cffi_exceptions::JSError(prettyTraceBack(try_catch));

  v8::Local<v8::Script> script = script_maybe.ToLocalChecked();
  v8::MaybeLocal<v8::Value> result_maybe = script->Run(context);

  if (result_maybe.IsEmpty())
    throw v8cffi_exceptions::JSError(prettyTraceBack(try_catch));

  v8::Local<v8::Value> result = result_maybe.ToLocalChecked();
  v8::String::Utf8Value result_utf8_str(result);
  return toCString(result_utf8_str);
}
