#ifndef V8CFFI_PLATFORM_H_INCLUDED
#define V8CFFI_PLATFORM_H_INCLUDED

#include <string>

#include "include/libplatform/libplatform.h"
#include "include/v8.h"


namespace v8cffi_platform
{

  class Platform
  {
    public:
      Platform(
        const std::string &natives_blob,
        const std::string &snapshot_blob);
      ~Platform();

    private:
      // Prevent copying. Not implemented.
      Platform(const Platform&);
      Platform& operator=(const Platform&);

      v8::Platform *m_platform = nullptr;
      v8::StartupData m_natives;
      v8::StartupData m_snapshot;
      std::string m_natives_blob;
      std::string m_snapshot_blob;
  };

}


#endif
