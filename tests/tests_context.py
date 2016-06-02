# -*- coding: utf-8 -*-

from unittest.mock import patch, Mock
import unittest
import logging
import os
import tempfile
from contextlib import contextmanager

from v8cffi.platform import platform
from v8cffi.vm import VM
from v8cffi import exceptions
from v8cffi import context


logging.disable(logging.CRITICAL)


class StringTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_with(self):
        """
        It should support with statement
        """
        with context._String() as s:
            self.assertIsInstance(s, context._String)
            self.assertEqual(
                context.ffi.typeof('char **'),
                context.ffi.typeof(s.string_ptr))
            self.assertEqual(
                context.ffi.typeof('size_t *'),
                context.ffi.typeof(s.len_ptr))
            self.assertEqual(s.string_ptr[0], context.ffi.NULL)
            self.assertEqual(s.len_ptr[0], 0)

    def test_to_str(self):
        """
        It should support str call
        """
        with context._String() as s:
            string_ptr = s.string_ptr
            s.string_ptr = [context.ffi.new('char[]', b'foo')]
            s.len_ptr[0] = 3
            self.assertEqual(str(s), 'foo')
            s.string_ptr = string_ptr

    def test_to_bytes(self):
        """
        It should return the string bytes
        """
        with context._String() as s:
            string_ptr = s.string_ptr
            s.string_ptr = [context.ffi.new('char[]', b'foo')]
            s.len_ptr[0] = 3
            self.assertEqual(s.to_bytes(), b'foo')
            s.string_ptr = string_ptr

    def test_free(self):
        """
        It should free the string
        """
        with patch('v8cffi.context.lib', autospec=True) as r:
            s = context._String()
            s.__enter__()

            free = Mock()
            r.v8cffi_free = free
            s.__exit__()
            self.assertTrue(free.called)

    def test_assert_on_re_enter(self):
        """
        It should fail to re enter
        """
        s = context._String()

        with s as _:
            self.assertRaises(AssertionError, s.__enter__)

    def test_assert_on_re_exit(self):
        """
        It should fail to re exit
        """
        s = context._String()

        self.assertRaises(AssertionError, s.__exit__)

        with s as _:
            pass

        self.assertRaises(AssertionError, s.__exit__)

    def test_assert_on_re_create(self):
        """
        It should allow to re create
        """
        s = context._String()

        with s as _:
            self.assertIsNotNone(s.string_ptr)

        self.assertIsNone(s.string_ptr)

        with s as _:
            self.assertIsNotNone(s.string_ptr)


@contextmanager
def js_file(data):
    temp = tempfile.NamedTemporaryFile(delete=False)
    temp.write(data)
    temp.close()

    try:
        yield temp.name
    finally:
        os.remove(temp.name)


class ContextTest(unittest.TestCase):

    def setUp(self):
        self.vm = VM(platform)
        self.vm.set_up()

    def tearDown(self):
        self.vm.tear_down()

    def test_keep_vm(self):
        """
        It should keep a reference to the VM
        """
        ctx = context.Context(self.vm)
        self.assertIsInstance(ctx._vm, VM)

    def test_with(self):
        """
        It should support with statement
        """
        with context.Context(self.vm) as ctx:
            self.assertIsInstance(ctx, context.Context)

    def test_set_up(self):
        """
        It should call __enter__
        """
        ctx = context.Context(self.vm)

        with patch.object(ctx, '__enter__', autospec=True) as r:
            r.return_value = 'foo'
            self.assertEqual(ctx.set_up(), 'foo')
            r.assert_called_once_with()

    def test_tear_down(self):
        """
        It should call __exit__
        """
        ctx = context.Context(self.vm)

        with patch.object(ctx, '__exit__', autospec=True) as r:
            ctx.tear_down()
            r.assert_called_once_with()

    def test_load_libs(self):
        """
        It should run the script file content on V8
        """
        script = b'var foo = "foo";'

        with js_file(script) as path:
            with context.Context(self.vm) as ctx:
                with patch.object(ctx, 'run_script', autospec=True) as r:
                    ctx.load_libs([path])
                    r.assert_called_once_with(script, identifier=path)

    def test_run_script(self):
        """
        It should run the script on V8
        """
        script_foo = b'var foo = "foo!";'
        script_bar = 'var bar = "bar!";'
        script_special = 'var txt = "áéíóú";'

        with context.Context(self.vm) as ctx:
            ctx.run_script(script_foo)
            ctx.run_script(script_bar)
            ctx.run_script(script_special)
            self.assertEqual("foo!", ctx.run_script(b'foo'))
            self.assertEqual("bar!", ctx.run_script('bar'))
            self.assertEqual("áéíóú", ctx.run_script('txt'))
            self.assertRaises(exceptions.V8JSError, ctx.run_script, 'baz')
            self.assertRaises(exceptions.V8JSError, ctx.run_script, 'function[]();')

        with context.Context(self.vm) as ctx:
            self.assertRaises(exceptions.V8JSError, ctx.run_script, 'foo')

    def test_builtin_libs(self):
        """
        It should pre-load builtin libraries
        """
        with context.Context(self.vm) as ctx:
            self.assertEqual("20", ctx.run_script('Math.max(10, 20);'))

    def test_run_script_trace_back(self):
        """
        It should run the script on V8\
        and get a useful traceback
        """
        def get_exception_message(ctx, script):
            try:
                return ctx.run_script(script)
            except exceptions.V8JSError as ex:
                return str(ex)

        script_oops = (
            'function oops() {\n'
            '  thereMayBeErrors();\n'
            '  var my_var_2;\n'
            '}')
        script_oops2 = (
            'function oops2() {\n'
            '  thereMayBeMoreErrors();\n'
            '  var my_var_2;\n'
            '}')
        var_a = 'var a;'
        script_long = (
            'function oops3() {\n' +
            var_a * 100 + 'thereMayBeMoreErrors();' + var_a * 100 + '\n'
            '}')

        # todo: trim source line when too long
        with context.Context(self.vm) as ctx:
            ctx.run_script(script_oops, identifier='my_file_áéíóú.js')
            ctx.run_script(script_oops2, identifier='my_other_file.js')
            ctx.run_script(script_long)
            self.assertEqual(
                'my_file_áéíóú.js:2\n'
                '      thereMayBeErrors();\n'
                '      ^\n'
                'ReferenceError: thereMayBeErrors is not defined\n'
                '    at oops (my_file_áéíóú.js:2:3)\n'
                '    at <anonymous>:1:1',
                get_exception_message(ctx, 'oops()'))
            self.assertEqual(
                'my_other_file.js:2\n'
                '      thereMayBeMoreErrors();\n'
                '      ^\n'
                'ReferenceError: thereMayBeMoreErrors is not defined\n'
                '    at oops2 (my_other_file.js:2:3)\n'
                '    at <anonymous>:1:1',
                get_exception_message(ctx, 'oops2()'))
            self.assertEqual(
                '<anonymous>:2\n'
                '    ~Line too long to display.\n'
                'ReferenceError: thereMayBeMoreErrors is not defined\n'
                '    at oops3 (<anonymous>:2:601)\n'
                '    at <anonymous>:1:1',
                get_exception_message(ctx, 'oops3()'))
            self.assertEqual(
                '<anonymous>:1\n'
                '    nonExistentFunc();\n'
                '    ^\n'
                'ReferenceError: nonExistentFunc is not defined\n'
                '    at <anonymous>:1:1',
                get_exception_message(ctx, 'nonExistentFunc();'))
            self.assertEqual(
                '<anonymous>:1\n'
                '    function[]();\n'
                '            ^\n'
                'SyntaxError: Unexpected token [',
                get_exception_message(ctx, 'function[]();'))
            # Has no .stack property
            self.assertEqual(
                '<anonymous>:2\n'
                '      throw "myException";\n'
                '      ^\n'
                'myException',
                get_exception_message(
                    ctx,
                    '(function() {\n'
                    '  throw "myException";\n'
                    '})();'))
