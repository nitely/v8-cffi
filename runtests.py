#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import sys

from v8cffi.platform import platform


def start():
    argv = ['v8cffi', 'discover']

    if len(sys.argv) > 1:
        argv = sys.argv

    with platform as _:
        unittest.main(module=None, argv=argv)


if __name__ == '__main__':
    start()
