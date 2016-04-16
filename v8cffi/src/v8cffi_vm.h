#ifndef V8CFFI_VM_H_INCLUDED
#define V8CFFI_VM_H_INCLUDED

#include "include/libplatform/libplatform.h"
#include "include/v8.h"


namespace v8cffi_vm
{

  class ArrayBufferAllocator : public v8::ArrayBuffer::Allocator
  {
    public:
      virtual void *Allocate(size_t length);
      virtual void *AllocateUninitialized(size_t length);
      virtual void Free(void *data, size_t);
  };


  class VM
  {
    public:
      VM();
      ~VM();
      v8::Isolate *getIsolate();

    private:
      // Prevent copying. Not implemented.
      VM(const VM&);
      VM& operator=(const VM&);

      ArrayBufferAllocator m_allocator;
      v8::Isolate *m_isolate = nullptr;
  };

}


#endif
