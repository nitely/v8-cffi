# -*- coding: utf-8 -*-

import concurrent.futures
import asyncio
import os

from . import context
from .. import vm


__all__ = ['VM']

_MAX_WORKERS = (os.cpu_count() or 1) * 2


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
    def __init__(self, platform, max_workers=_MAX_WORKERS, loop=None):
        self.vm = vm.VM(platform=platform)
        self._loop = loop or asyncio.get_event_loop()
        self._executor = (
            concurrent.futures
            .ThreadPoolExecutor(max_workers=max_workers))

    def create_context(self):
        """
        Create a :py:class:`.context.Context` for running\
        JS scripts

        :return: Instance of :py:class:`.context.Context`
        :rtype: :py:class:`.context.Context`
        """
        return context.Context(self)

    def set_up(self):
        return self.vm.set_up()

    def tear_down(self):
        return self.vm.tear_down()
