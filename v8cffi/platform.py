# -*- coding: utf-8 -*-

import os

from _v8 import ffi, lib

from . import exceptions
from . import vm


__all__ = ['platform']


_BLOBS_PATH = os.path.join(os.path.dirname(__file__), 'src', 'v8')
_NATIVES_BLOB_PATH = os.path.join(_BLOBS_PATH, 'natives_blob.bin')
_SNAPSHOT_BLOB_PATH = os.path.join(_BLOBS_PATH, 'snapshot_blob.bin')


def _read_file(path):
    with open(path, 'rb') as fh:
        return fh.read()


class _Platform:
    """
    V8 platform environment. The underlying\
    platform is a singleton that must only\
    be initialized once per process.

    Should be used through :py:data:`platform`

    :ivar str natives_path: Path to natives_blob.bin
    :ivar str snapshot_path: Path to snapshot_blob.bin
    """
    def __init__(self):
        self.natives_path = _NATIVES_BLOB_PATH
        self.snapshot_path = _SNAPSHOT_BLOB_PATH
        self._c_platform = None
        self._is_dead = False  # Irreversible state, once it's dead

    def __enter__(self):
        """
        See :py:func:`set_up` method for docs
        """
        assert not self.is_alive()
        assert not self._is_dead

        self._c_platform = ffi.new('v8cffi_platform_t **')  # initialized to NULL ?
        self._c_platform[0] = ffi.NULL
        natives_blob = _read_file(self.natives_path)
        snapshot_blob = _read_file(self.snapshot_path)
        code = lib.v8cffi_platform_new(
            self._c_platform,
            natives_blob,
            len(natives_blob),
            snapshot_blob,
            len(snapshot_blob))

        if code != lib.E_V8_OK:
            raise exceptions.get_exception(code)

        return self

    def __exit__(self, *_, **__):
        """
        See :py:func:`tear_down` method for docs
        """
        assert self.is_alive()

        lib.v8cffi_platform_free(self._c_platform[0])
        self._c_platform = None
        self._is_dead = True

    def is_alive(self):
        """
        Check is initialized and was not exited

        :return: Whether the platform is alive or not
        :rtype: bool
        """
        return self._c_platform is not None

    def create_vm(self):
        """
        Create a :py:class:`.VM` for running\
        JS scripts within an isolated environment

        :return: Instance of :py:class:`.VM`
        :rtype: :py:class:`.VM`
        """
        return vm.VM(self)

    def set_up(self):
        """
        Initialize the V8 platform.\
        Remember to call :py:func:`tear_down`\
        before exiting the application.\
        It's recommended to use a ``with``\
        statement instead of this method\
        to ensure clean up.

        This must only be called once\
        in an application lifetime

        :raises V8MemoryError: if there\
        is no memory for allocating it,\
        the process should die afterwards anyway,\
        there is little point in catching this
        """
        return self.__enter__()

    def tear_down(self):
        """
        Destructs the V8 platform
        """
        return self.__exit__()


platform = _Platform()
