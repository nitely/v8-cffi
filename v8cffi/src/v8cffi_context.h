#ifndef V8CFFI_CONTEXT_H_INCLUDED
#define V8CFFI_CONTEXT_H_INCLUDED

#include <string.h>
#include <string>

#include "include/libplatform/libplatform.h"
#include "include/v8.h"


namespace v8cffi_context
{

  class Context
  {
    public:
      Context(v8::Isolate *isolate);
      ~Context();
      std::string runScript(
        const std::string &input_script,
        const std::string &identifier);

    private:
      // Prevent copying. Not implemented.
      Context(const Context&);
      Context& operator=(const Context&);

      v8::Local<v8::String> toV8String(const std::string &str);
      std::string toCString(const v8::String::Utf8Value &str_utf8);

      std::string paddingOf(int padding_len);
      std::string errorSource(const v8::Local<v8::Message> &message);
      std::string sourceLine(const v8::Local<v8::Message> &message);
      std::string wavyLine(const v8::Local<v8::Message> &message);
      std::string stackTrace(const v8::TryCatch &try_catch);
      std::string prettyTraceBack(const v8::TryCatch &try_catch);

      v8::Isolate *m_isolate = nullptr;
      v8::Persistent<v8::Context> m_pers_context;
  };

}


#endif
