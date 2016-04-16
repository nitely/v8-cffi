# -*- coding: utf-8 -*-

from unittest.mock import patch, Mock
import unittest
import logging

from v8cffi.platform import platform
from v8cffi import shortcuts


logging.disable(logging.CRITICAL)


class ShortcutsTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        shortcuts._context = None

    def test_set_up(self):
        """
        It should create a global context
        """
        with patch('v8cffi.shortcuts.platform', autospec=True) as rp:
            with patch('v8cffi.vm.VM', autospec=True) as rv:
                with patch('v8cffi.context.Context', autospec=True) as rc:
                    with patch('v8cffi.shortcuts.atexit.register', autospec=True) as rae:
                        rp.set_up = Mock()
                        rp.create_vm = Mock(return_value=rv)
                        rv.set_up = Mock()
                        rv.create_context = Mock(return_value=rc)
                        rc.set_up = Mock()
                        shortcuts.set_up()
                        self.assertTrue(rp.set_up.called)
                        self.assertTrue(rp.create_vm.called)
                        self.assertTrue(rv.set_up.called)
                        self.assertTrue(rv.create_context.called)
                        self.assertTrue(rc.set_up)
                        rae.assert_called_once_with(shortcuts._tear_down)
                        self.assertEqual(shortcuts._context, rc)

    def test_set_up_set_up(self):
        """
        It should not allow to re set up
        """
        shortcuts._context = (platform
            .create_vm()
            .create_context())

        with patch('v8cffi.shortcuts.platform', autospec=True) as rp:
            rp.set_up = Mock()
            self.assertRaises(AssertionError, shortcuts.set_up)
            self.assertFalse(rp.set_up.called)

    def test_get_context(self):
        """
        It should return the global context
        """
        self.assertRaises(AssertionError, shortcuts.get_context)

        shortcuts._context = (platform
            .create_vm()
            .create_context())

        self.assertEqual(shortcuts._context, shortcuts.get_context())
