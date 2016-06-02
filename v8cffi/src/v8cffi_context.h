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

      v8::Isolate *m_isolate = nullptr;
      v8::Persistent<v8::Context> m_pers_context;
  };

}


#endif
