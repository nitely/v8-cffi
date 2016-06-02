#include "v8cffi_utils.h"
#include "v8cffi_trace_back.h"

using namespace v8cffi_trace_back;


std::string paddingOf(int padding_len)
{
  if (padding_len < 0)
    return "";

  std::string padding = "";

  for (int i = 0; i < padding_len; i++)
    padding += " ";

  return padding;
}


/*
  Return: file_name:line_num
*/
std::string errorSource(
  v8::Isolate *isolate,
  const v8::Local<v8::Message> &message)
{
  v8::String::Utf8Value origin_str(
    message->GetScriptResourceName());
  int line_num_default = 0;
  int line_num = message->GetLineNumber(
    isolate->GetCurrentContext()).FromMaybe(line_num_default);
  return v8cffi_utils::toCString(origin_str) + ":" + std::to_string(line_num);
}


std::string sourceLine(
  v8::Isolate *isolate,
  const v8::Local<v8::Message> &message)
{
  std::string source_line_str = "";

  v8::MaybeLocal<v8::String> source_line_maybe = message->GetSourceLine(
    isolate->GetCurrentContext());

  if (!source_line_maybe.IsEmpty())
  {
    v8::Local<v8::Value> source_line =
      source_line_maybe.ToLocalChecked();

    if (source_line->IsString())
      source_line_str = v8cffi_utils::toCString(
        v8::String::Utf8Value(source_line));
  }

  return source_line_str;
}


std::string wavyLine(
  v8::Isolate *isolate,
  const v8::Local<v8::Message> &message)
{
  std::string wavy_line = "";

  int source_col_start_default = 0;
  int source_col_start = message->GetStartColumn(
    isolate->GetCurrentContext()).FromMaybe(source_col_start_default);

  wavy_line += paddingOf(source_col_start);

  int source_col_end_default = 0;
  int source_col_end = message->GetEndColumn(
    isolate->GetCurrentContext()).FromMaybe(source_col_end_default);

  for (int i = source_col_start; i < source_col_end; i++)
    wavy_line += "^";

  return wavy_line;
}


std::string errorMessage(
  v8::Isolate *isolate,
  const v8::TryCatch &try_catch)
{
  std::string error_message_str = "";

  v8::MaybeLocal<v8::Message> message_maybe = try_catch.Message();

  if (!message_maybe.IsEmpty())
  {
    v8::Local<v8::Message> message = message_maybe.ToLocalChecked();

    error_message_str += errorSource(isolate, message) + "\n";

    std::string source_line = sourceLine(isolate, message);
    std::string padding = paddingOf(4);

    if (source_line.length() <= 240)
      error_message_str += padding + source_line + "\n" +
        padding + wavyLine(isolate, message);
    else
      error_message_str += padding + "~Line too long to display.";
  }

  return error_message_str;
}


std::string stackTrace(const v8::TryCatch &try_catch)
{
  std::string stack_trace_str = "";

  v8::MaybeLocal<v8::Value> stack_trace_maybe = try_catch.StackTrace();

  if (!stack_trace_maybe.IsEmpty())
  {
    v8::Local<v8::Value> stack_trace = stack_trace_maybe.ToLocalChecked();

    if (stack_trace->IsString())
      stack_trace_str = v8cffi_utils::toCString(
        v8::String::Utf8Value(stack_trace));
  }

  return stack_trace_str;
}


std::string v8cffi_trace_back::prettyTraceBack(
  v8::Isolate *isolate,
  const v8::TryCatch &try_catch)
{
  std::string trace_back = "";

  std::string error_message = errorMessage(isolate, try_catch);

  if (!error_message.empty())
    trace_back += error_message + "\n";

  std::string stack_trace = stackTrace(try_catch);

  if (!stack_trace.empty())
    trace_back += stack_trace;
  else
    trace_back += v8cffi_utils::toCString(
      v8::String::Utf8Value(try_catch.Exception()));

  return trace_back;
}
