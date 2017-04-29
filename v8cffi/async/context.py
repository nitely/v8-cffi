# -*- coding: utf-8 -*-

import functools

from .. import context


__all__ = ['Context']

_DEFAULT_SCRIPT_NAME = '<anonymous>'


class Context:
    """
    A Context providing asyncio support.

    This class is not thread safe.
    """
    def __init__(self, vm):
        self.vm = vm
        self.context = context.Context(vm)

    def set_up(self):
        return self.context.set_up()

    def tear_down(self):
        """
        Wait for all workers to exit to prevent crashes
        """
        # todo: terminate current script
        self.vm._executor.shutdown(wait=True)
        return self.context.tear_down()

    def _run_script_worker(self, *args, **kwargs):
        if not self.context.is_alive():
            raise RuntimeError(
                'run_script was scheduled but '
                'async.Context has already exited')

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
        # Passing positional args coz "func"
        # is named "callback" in py3.4
        return self.vm._loop.run_in_executor(
            self.vm._executor,
            functools.partial(
                self._run_script_worker,
                script=script,
                identifier=identifier))
