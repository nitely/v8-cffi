#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unittest

from v8cffi.platform import platform


def start():
    with platform as _:
        unittest.main(
            module=None,
            argv=['v8cffi', 'discover'])


if __name__ == '__main__':
    start()
