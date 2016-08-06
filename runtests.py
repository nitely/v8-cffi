#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unittest

import six

from v8cffi.platform import platform

if six.PY2:
    PATTERN = 'test*_py2*.py'
else:
    PATTERN = 'test*_py3*.py'


def start():
    unittest.defaultTestLoader.discover('tests')

    with platform as _:
        unittest.main(
            module=None,
            argv=[
                'v8cffi', 'discover',
                '-s', 'tests',
                '-p', PATTERN])


if __name__ == '__main__':
    start()
