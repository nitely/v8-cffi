#ifndef V8CFFI_TRACE_BACK_H_INCLUDED
#define V8CFFI_TRACE_BACK_H_INCLUDED

#include <string.h>
#include <string>

#include "include/libplatform/libplatform.h"
#include "include/v8.h"


namespace v8cffi_trace_back
{
  std::string prettyTraceBack(
    v8::Isolate *isolate,
    const v8::TryCatch &try_catch);
}


#endif
