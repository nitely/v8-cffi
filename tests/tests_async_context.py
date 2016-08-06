# -*- coding: utf-8 -*-

import unittest
import logging
import asyncio

from v8cffi.platform import platform
from v8cffi import exceptions
from v8cffi.async.vm import VM
from v8cffi.async.context import Context


logging.disable(logging.CRITICAL)


def async_test(func):
    def wrapper(test_klass, *args, **kwargs):
        coro = asyncio.coroutine(func)
        future = coro(test_klass, *args, **kwargs)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)
        test_klass.loop = loop

        try:
            loop.run_until_complete(future)
        finally:
            loop.close()

    return wrapper


class ContextTest(unittest.TestCase):

    @async_test
    def test_run_script_async(self):
        """
        It should run the script on V8 asynchronously
        """
        script_foo = b'var foo = "foo!";'

        with VM(platform, loop=self.loop) as vm:
            with vm.create_context() as ctx:
                yield from ctx.run_script(script_foo)
                self.assertEqual("foo!", (yield from ctx.run_script(b'foo')))

                try:
                    yield from ctx.run_script('baz')
                    raise AssertionError('V8JSError was expected')
                except exceptions.V8JSError:
                    pass

            with vm.create_context() as ctx:
                try:
                    yield from ctx.run_script('foo')
                    raise AssertionError('V8JSError was expected')
                except exceptions.V8JSError:
                    pass

    @async_test
    def test_run_script_async_wait(self):
        """
        It should run the script on V8 asynchronously
        """
        try:
            ensure_future = asyncio.ensure_future
        except AttributeError:
            ensure_future = asyncio.async

        script_foo = b'var foo = "foo!";'

        with VM(platform, loop=self.loop) as vm:
            with vm.create_context() as ctx:
                yield from ctx.run_script(script_foo)

                done, pending = yield from asyncio.wait(
                    fs=[
                        ensure_future(ctx.run_script(b"foo"), loop=self.loop)
                        for _ in range(10)],
                    loop=self.loop)
                self.assertEqual(list(pending), [])
                self.assertEqual(
                    [f.result() for f in done],
                    ['foo!' for _ in range(10)])

    @async_test
    def test_run_script_async_wait_timeout(self):
        """
        It should timeout script
        """
        # todo: implement ctx.terminate()
        # This should block for ever
        with VM(platform, loop=self.loop) as vm:
            with vm.create_context() as ctx:
                pass
                # yield from asyncio.wait_for(
                #    ctx.run_script(b"while (true){}"), timeout=1, loop=self.loop)
