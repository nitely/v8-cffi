#include <string.h>
#include <string>
#include <memory>

#include "v8cffi_exceptions.h"
#include "v8cffi_vm.h"

using namespace v8cffi_vm;


void *ArrayBufferAllocator::Allocate(size_t length)
{
  void *data = AllocateUninitialized(length);
  return data == NULL ? data : memset(data, 0, length);
}


void *ArrayBufferAllocator::AllocateUninitialized(size_t length)
{
  return malloc(length);
}


void ArrayBufferAllocator::Free(void *data, size_t)
{
  free(data);
}


VM::VM()
{
  v8::Isolate::CreateParams create_params;
  create_params.array_buffer_allocator = &m_allocator;
  m_isolate = v8::Isolate::New(create_params);
}


VM::~VM()
{
  if (!m_isolate)
    return;

  m_isolate->Dispose();

  // delete m_isolate;
  m_isolate = nullptr;
}


v8::Isolate *VM::getIsolate()
{
  return m_isolate;
}
