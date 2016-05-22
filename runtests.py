#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import sys

from v8cffi.platform import platform


def start():
    with platform as _:
        unittest.main(
            module=None,
            argv=['v8cffi', 'discover'])


if __name__ == '__main__':
    start()
