# -*- coding: utf-8 -*-

import functools
import threading

from .. import context


__all__ = ['Context']

_DEFAULT_SCRIPT_NAME = '<anonymous>'


class Context(context.Context):
    """
    A Context providing asyncio support.

    This class is not thread safe.
    """
    def __init__(self, vm):
        super().__init__(vm=vm)
        self._workers_count = 0
        self._worker_cond = threading.Condition()

    def __exit__(self, *_, **__):
        """
        Wait for all workers to exit to prevent crashes
        """
        with self._worker_cond:
            # todo: terminate current script
            self._worker_cond.wait_for(
                lambda: not self._workers_count)

            return super().__exit__()

    def _run_script_worker(self, *args, **kwargs):
        with self._worker_cond:
            if not self.is_alive():
                return

            self._workers_count += 1

        try:
            return super().run_script(*args, **kwargs)
        finally:
            with self._worker_cond:
                self._workers_count -= 1
                self._worker_cond.notify_all()

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
        assert self.is_alive(), (
            'run_script was scheduled but '
            'async.Context has already exited')

        return self._vm._loop.run_in_executor(
            self._vm._executor,
            functools.partial(
                self._run_script_worker,
                script=script,
                identifier=_DEFAULT_SCRIPT_NAME))
