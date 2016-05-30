# -*- coding: utf-8 -*-

from _v8 import ffi, lib

from . import exceptions


__all__ = ['Context']

_DEFAULT_SCRIPT_NAME = '<anonymous>'


def _read_file(path):
    with open(path, 'rb') as fh:
        return fh.read()


def _is_utf_8(txt):
    """
    Check a string is utf-8 encoded

    :param bytes txt: utf-8 string
    :return: Whether the string\
    is utf-8 encoded or not
    :rtype: bool
    """
    assert isinstance(txt, bytes)

    try:
        _ = str(txt, 'utf-8')
    except (TypeError, UnicodeEncodeError):
        return False
    else:
        return True


class _String:
    """
    A wrapper for C(ffi) strings

    Usage::

        with String() as s:
            lib.my_cffi_foo(s.string_ptr, s.len_ptr)
            result = str(s)

    :ivar string_ptr: String pointer,\
    default: :py:data:`cffi.NULL`
    :type string_ptr: :py:class:`ffi.CData<char **>`
    :ivar len_ptr: String length, default: 0
    :type len_ptr: :py:class:`ffi.CData<size_t *>`
    """
    def __init__(self):
        self.string_ptr = None
        self.len_ptr = None

    def __enter__(self):
        """
        Instantiate string_ptr and len_ptr
        """
        assert self.string_ptr is None
        assert self.len_ptr is None

        self.string_ptr = ffi.new('char **')
        self.string_ptr[0] = ffi.NULL
        self.len_ptr = ffi.new('size_t *', 0)

        return self

    def __exit__(self, *_, **__):
        """
        Clean up string_ptr and len_ptr
        """
        assert self.string_ptr is not None
        assert self.len_ptr is not None

        lib.v8cffi_free(self.string_ptr[0])
        self.string_ptr = None
        self.len_ptr = None

    def __str__(self):
        """
        :return: Representation of the string
        :rtype: str
        """
        return str(self.to_bytes(), 'utf-8')

    def to_bytes(self):
        """
        :return: Representation of the string, utf-8 encoded
        :rtype: bytes
        """
        return ffi.buffer(self.string_ptr[0], self.len_ptr[0])[:]


class Context:
    """
    An execution environment that allows\
    separate, unrelated, JS applications\
    to run in a single instance of V8.\
    It may be thought as a browser tab.

    Running scripts within the same Context\
    is thread-safe.

    There may be many Contexts per VM

    :param vm: Initialized VM
    :type vm: :py:class:`.VM`
    """
    def __init__(self, vm):
        self._vm = vm
        self._c_context = None

    def __enter__(self):
        """
        See :py:func:`set_up` method for docs
        """
        assert self._c_context is None
        assert self._vm.is_alive()

        self._c_context = ffi.new('v8cffi_context_t **')
        self._c_context[0] = ffi.NULL
        code = lib.v8cffi_context_new(self._c_context, self._vm.get_c_vm()[0])

        if code != lib.E_V8_OK:
            raise exceptions.get_exception(code)

        return self

    def __exit__(self, *_, **__):
        """
        See :py:func:`tear_down` method for docs
        """
        assert self._c_context is not None
        assert self._vm.is_alive()

        lib.v8cffi_context_free(self._c_context[0])
        self._c_context = None

    def set_up(self):
        """
        Initialize the context.\
        Remember to call :py:func:`tear_down`\
        before exiting the application.\
        It's recommended to use a ``with``\
        statement instead of this method\
        to ensure clean up

        :raises V8MemoryError: if there\
        is no memory for allocating it,\
        the process should die afterwards anyway,\
        there is little point in catching this
        """
        return self.__enter__()

    def tear_down(self):
        """
        Destructs the context
        """
        return self.__exit__()

    def load_libs(self, scripts_paths):
        """
        Load script files into the context.\
        This can be thought as the HTML script tag.\
        The files content must be utf-8 encoded.

        This is a shortcut for reading the files\
        and pass the content to :py:func:`run_script`

        :param list scripts_paths: Script file paths.
        :raises OSError: If there was an error\
        manipulating the files. This should not\
        normally be caught
        :raises V8Error: if there was\
        an error running the JS script
        """
        for path in scripts_paths:
            self.run_script(_read_file(path), identifier=path)

    def run_script(self, script, identifier=_DEFAULT_SCRIPT_NAME):
        """
        Run a JS script within the context.\
        All code is ran synchronously,\
        there is no event loop. It's thread-safe

        :param script: utf-8 encoded or unicode string
        :type script: bytes or str
        :param identifier: utf-8 encoded or unicode string.\
        This is used as the name of the script\
        (ie: in stack-traces)
        :type identifier: bytes or str
        :return: Result of running the JS script
        :rtype: str
        :raises V8Error: if there was\
        an error running the JS script
        """
        assert isinstance(script, str) or _is_utf_8(script)
        assert isinstance(identifier, str) or _is_utf_8(identifier)

        if isinstance(script, str):
            script = bytes(script, 'utf-8')

        if isinstance(identifier, str):
            identifier = bytes(identifier, 'utf-8')

        with _String() as output:
            with _String() as error:
                code = lib.v8cffi_run_script(
                    self._c_context[0],
                    script,
                    len(script),
                    identifier,
                    len(identifier),
                    output.string_ptr,
                    output.len_ptr,
                    error.string_ptr,
                    error.len_ptr)

                if code != lib.E_V8_OK:
                    raise exceptions.get_exception(code)(str(error))

                return str(output)
