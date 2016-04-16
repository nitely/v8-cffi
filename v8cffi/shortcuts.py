# -*- coding: utf-8 -*-

import atexit

from .platform import platform


__all__ = ['set_up', 'get_context']


_context = None


def _tear_down():
    global _context

    _context.tear_down()
    _context._vm.tear_down()  # no-qa
    platform.tear_down()


def set_up():
    """
    Set ups the V8 machinery:\
    platform, VM and context.

    This function is not thread-safe,\
    it must be called from a place\
    where is guaranteed it will be\
    called once and only once.\
    Probably within the main-thread\
    at import time.
    """
    global _context

    if _context is not None:
        raise AssertionError(
            'This function must only be called '
            'once in an application lifetime')

    platform.set_up()
    vm = platform.create_vm()
    vm.set_up()
    _context = vm.create_context()
    _context.set_up()
    atexit.register(_tear_down)


def get_context():
    """
    Return a global V8 context.

    :py:func:`.set_up` must has been called

    :return: Global V8 context
    :rtype: :py:class:`.Context`
    """
    global _context

    if _context is None:
        raise AssertionError(
            'No context found. '
            'Did you call shortcuts.set_up()?')

    return _context
