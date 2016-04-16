#ifndef V8CFFI_EXCEPTIONS_H_INCLUDED
#define V8CFFI_EXCEPTIONS_H_INCLUDED

#include <stdexcept>
#include <string>


namespace v8cffi_exceptions
{

  class JSError : public std::exception
  {
    public:
      explicit JSError() : m_message("") {}
      explicit JSError(const std::string &message) : m_message(message) {}
      virtual ~JSError() throw() {}
      virtual const char *what() const throw()
      {
        return m_message.c_str();
      }
      virtual std::string getMessage() const throw()
      {
        return m_message;
      }

    protected:
      std::string m_message;
  };

}


#endif
