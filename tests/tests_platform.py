# -*- coding: utf-8 -*-

from unittest.mock import patch, Mock
import unittest
import logging
import os

from v8cffi import platform as platform_module
from v8cffi.platform import platform, _Platform
from v8cffi import vm
from v8cffi import exceptions


logging.disable(logging.CRITICAL)


class PlatformTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_is_alive(self):
        """
        It should be initialized for these tests (see runtests.py)
        """
        self.assertTrue(platform.is_alive())
        self.assertFalse(_Platform().is_alive())

    def test_singleton(self):
        """
        It should instantiate a Platform into platform global
        """
        self.assertIsInstance(platform, _Platform)

    def test_bin_blobs(self):
        """
        It should contain the bin's paths by default
        """
        self.assertTrue(os.path.isfile(platform.natives_path))
        self.assertTrue(os.path.isfile(platform.snapshot_path))
        self.assertTrue(platform.natives_path.endswith('natives_blob.bin'))
        self.assertTrue(platform.snapshot_path.endswith('snapshot_blob.bin'))

    def test_is_dead(self):
        """
        It should not be dead by default
        """
        self.assertFalse(platform._is_dead)

    def test_create_vm(self):
        """
        It should create a VM
        """
        self.assertIsInstance(platform.create_vm(), vm.VM)

        with patch('v8cffi.platform.vm.VM', autospec=True) as r:
            r.return_value = None
            platform.create_vm()
            r.assert_called_once_with(platform)

    def test_assert_on_re_enter(self):
        """
        It should fail to re enter (it has enter in the test runner)
        """
        self.assertRaises(AssertionError, platform.__enter__)

    def test_allocate_and_free(self):
        """
        It should allocate and free the C platform
        """
        code_ok = platform_module.lib.E_V8_OK

        with patch('v8cffi.platform.lib', autospec=True) as r:
            platform_ = _Platform()

            platform_new = Mock(return_value=code_ok)
            r.v8cffi_platform_new = platform_new
            r.E_V8_OK = code_ok
            platform_.__enter__()
            self.assertTrue(platform_new.called)

            platform_free = Mock()
            r.v8cffi_platform_free = platform_free
            platform_.__exit__()
            self.assertTrue(platform_free.called)

            self.assertTrue(platform_._is_dead)
            self.assertFalse(platform_.is_alive())
            self.assertRaises(AssertionError, platform_.__exit__)

    def test_with_exceptions(self):
        """
        It should raise V8 exceptions
        """
        code_error = platform_module.lib.E_V8_JS_ERROR
        code_ok = platform_module.lib.E_V8_OK

        with patch('v8cffi.platform.lib', autospec=True) as r:
            r.v8cffi_platform_new = Mock(return_value=code_error)
            r.E_V8_OK = code_ok
            self.assertRaises(exceptions.V8JSError, _Platform().__enter__)

    def test_set_up(self):
        """
        It should call __enter__
        """
        with patch('v8cffi.platform.platform.__enter__', autospec=True) as r:
            r.return_value = 'foo'
            self.assertEqual(platform.set_up(), 'foo')
            r.assert_called_once_with()

    def test_tear_down(self):
        """
        It should call __exit__
        """
        with patch('v8cffi.platform.platform.__exit__', autospec=True) as r:
            platform.tear_down()
            r.assert_called_once_with()
