# -*- coding: utf-8 -*-

from unittest.mock import patch, Mock
import unittest
import logging

from v8cffi.platform import platform
from v8cffi import vm as vm_module
from v8cffi.vm import VM
from v8cffi import exceptions
from v8cffi import context


logging.disable(logging.CRITICAL)


class VMTest(unittest.TestCase):

    def setUp(self):
        self.vm = VM(platform)
        self.vm.set_up()

    def tearDown(self):
        self.vm.tear_down()

    def test_keep_platform(self):
        """
        It should keep a reference to the platform
        """
        self.assertEqual(platform, self.vm._platform)

    def test_with(self):
        """
        It should support with statement
        """
        with VM(platform) as vm:
            self.assertIsInstance(vm, VM)

    def test_is_alive(self):
        """
        It should be alive within a with context
        """
        vm = VM(platform)
        self.assertFalse(vm.is_alive())

        with VM(platform) as vm:
            self.assertTrue(vm.is_alive())

        self.assertFalse(vm.is_alive())

    def test_create_context(self):
        """
        It should create a Context
        """
        self.assertIsInstance(self.vm.create_context(), context.Context)

        with patch('v8cffi.context.Context', autospec=True) as r:
            r.return_value = None
            self.vm.create_context()
            r.assert_called_once_with(self.vm)

    def test_get_c_vm(self):
        """
        It should return the C VM
        """
        self.assertEqual(self.vm._c_vm, self.vm.get_c_vm())

    def test_set_up(self):
        """
        It should call __enter__
        """
        vm = VM(platform)

        with patch.object(vm, '__enter__', autospec=True) as r:
            r.return_value = 'foo'
            self.assertEqual(vm.set_up(), 'foo')
            r.assert_called_once_with()

    def test_tear_down(self):
        """
        It should call __exit__
        """
        vm = VM(platform)

        with patch.object(vm, '__exit__', autospec=True) as r:
            vm.tear_down()
            r.assert_called_once_with()

    def test_allocate_and_free(self):
        """
        It should allocate and free the C VM
        """
        code_ok = vm_module.lib.E_V8_OK

        with patch('v8cffi.vm.lib', autospec=True) as r:
            vm = VM(platform)

            vm_new = Mock(return_value=code_ok)
            r.v8cffi_vm_new = vm_new
            r.E_V8_OK = code_ok
            vm.__enter__()
            self.assertTrue(vm_new.called)

            vm_free = Mock()
            r.v8cffi_vm_free = vm_free
            vm.__exit__()
            self.assertTrue(vm_free.called)

            self.assertFalse(vm.is_alive())
            self.assertRaises(AssertionError, vm.__exit__)

    def test_with_exceptions(self):
        """
        It should raise V8 exceptions
        """
        code_error = vm_module.lib.E_V8_JS_ERROR
        code_ok = vm_module.lib.E_V8_OK

        with patch('v8cffi.vm.lib', autospec=True) as r:
            r.v8cffi_vm_new = Mock(return_value=code_error)
            r.E_V8_OK = code_ok

            self.assertRaises(exceptions.V8JSError, VM(platform).__enter__)

    def test_assert_on_re_enter(self):
        """
        It should fail to re enter
        """
        vm = VM(platform)

        with vm as _:
            self.assertRaises(AssertionError, vm.__enter__)

    def test_assert_on_re_exit(self):
        """
        It should fail to re exit
        """
        vm = VM(platform)

        self.assertRaises(AssertionError, vm.__exit__)

        with vm as _:
            pass

        self.assertRaises(AssertionError, vm.__exit__)

    def test_assert_on_re_create(self):
        """
        It should allow to re create a vm
        """
        vm = VM(platform)

        with vm as _:
            self.assertTrue(vm.is_alive())

        self.assertFalse(vm.is_alive())

        with vm as _:
            self.assertTrue(vm.is_alive())
