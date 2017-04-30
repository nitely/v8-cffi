# -*- coding: utf-8 -*-

import concurrent.futures
import functools
import asyncio
import os

from .. import context


__all__ = ['Context']

_DEFAULT_SCRIPT_NAME = '<anonymous>'
_MAX_WORKERS = (os.cpu_count() or 1) * 2


class Context:
    """
    A Context providing asyncio\
    support for running scripts.

    This class is not thread safe.
    """
    def __init__(self, vm, max_workers=_MAX_WORKERS, loop=None):
        self.vm = vm
        self.context = context.Context(vm)
        self._loop = loop or asyncio.get_event_loop()
        self._executor = (
            concurrent.futures
            .ThreadPoolExecutor(max_workers=max_workers))

    def __enter__(self):
        self.context.__enter__()
        return self

    def __exit__(self, *args, **kwargs):
        """
        Wait for all workers to exit to prevent crashes
        """
        # todo: terminate current script ?
        # Wait for all workers to exit to prevent crashes
        self._executor.shutdown(wait=True)
        return self.context.__exit__(*args, **kwargs)

    def set_up(self):
        return self.__enter__()

    def tear_down(self):
        return self.__exit__()

    def _run_script_worker(self, *args, **kwargs):
        return self.context.run_script(*args, **kwargs)

    def run_script(self, script, identifier=_DEFAULT_SCRIPT_NAME):
        """
        The first time this method is called,\
        it start a new thread, future calls will\
        enqueue the work to the child thread(s).

        There is no way to stop a script that is running.

        :param script: utf-8 encoded or unicode string
        :type script: bytes or str
        :param identifier: utf-8 encoded or unicode string.\
        This is used as the name of the script\
        (ie: in stack-traces)
        :type identifier: bytes or str
        :return: The script result
        :rtype: coroutine
        """
        assert self.context.is_alive()

        # Passing positional args coz "func"
        # is named "callback" in py3.4
        return self._loop.run_in_executor(
            self._executor,
            functools.partial(
                self._run_script_worker,
                script=script,
                identifier=identifier))
