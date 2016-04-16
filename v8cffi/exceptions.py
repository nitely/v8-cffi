# -*- coding: utf-8 -*-

from _v8 import lib


class V8Error(Exception):
    """
    Base error for all V8\
    related errors
    """

class V8JSError(V8Error):
    """
    Error raised when a JS\
    script fails to compile or run.\
    The message contains an\
    explanation of the cause of the error
    """

class V8MemoryError(V8Error):
    """
    Error raised when an allocation fails,\
    this usually means out of memory
    """

class V8UnknownError(V8Error):
    """
    Unpredicted error
    """


EXCEPT = {
    lib.E_V8_JS_ERROR: V8JSError,
    lib.E_V8_OUT_OF_MEM_ERROR: V8MemoryError,
    lib.E_V8_UNKNOWN_ERROR: V8UnknownError}


def get_exception(code):
    """
    Map C code error to Python exception

    :param int code: V8 C error code
    :return: The exception mapped to the code
    :rtype: :py:class:`.V8Error`
    """
    return EXCEPT.get(code, V8Error)
