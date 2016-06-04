# -*- coding: utf-8 -*-

from _v8 import ffi, lib

from . import exceptions
from . import context


__all__ = ['VM']


class VM:
    """
    Holds the VM state (V8 isolate).\
    Running scripts within a VM is thread-safe,\
    but only a single thread will execute code\
    at a given time (there is a Global Lock).\
    It's feasible to run one VM per thread\
    or to have a pre-initialized pool.

    There may be many VMs per platform

    :param platform: Initialized platform
    :type platform: :py:class:`._Platform`
    """
    def __init__(self, platform):
        self._platform = platform
        self._c_vm = None

    def __enter__(self):
        """
        See :py:func:`set_up` method for docs
        """
        assert not self.is_alive()
        assert self._platform.is_alive()

        self._c_vm = ffi.new('v8cffi_vm_t **')
        self._c_vm[0] = ffi.NULL
        code = lib.v8cffi_vm_new(self._c_vm)

        if code != lib.E_V8_OK:
            raise exceptions.get_exception(code)

        return self

    def __exit__(self, *_, **__):
        """
        See :py:func:`tear_down` method for docs
        """
        assert self.is_alive()
        assert self._platform.is_alive()

        lib.v8cffi_vm_free(self._c_vm[0])
        self._c_vm = None

    def is_alive(self):
        """
        Check the vm is initialized and was not exited

        :return: Whether the vm is alive or not
        :rtype: bool
        """
        return self._c_vm is not None

    def create_context(self):
        """
        Create a :py:class:`.Context` for running\
        JS scripts

        :return: Instance of :py:class:`.Context`
        :rtype: :py:class:`.Context`
        """
        return context.Context(self)

    def get_c_vm(self):
        """
        @Private
        Return the underlying C VM

        :return: struct cdata
        :rtype: :py:class:`ffi.CData<struct **>`
        """
        return self._c_vm

    def set_up(self):
        """
        Initialize the VM.\
        Remember to call :py:func:`tear_down`\
        before exiting the application.\
        It's recommended to use a ``with``\
        statement instead of this method\
        to ensure clean up

        :raise V8MemoryError: if there\
        is no memory for allocating it,\
        the process should die afterwards anyway,\
        there is little point in catching this
        """
        return self.__enter__()

    def tear_down(self):
        """
        Destructs the VM
        """
        return self.__exit__()
