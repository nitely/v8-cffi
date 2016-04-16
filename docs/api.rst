.. _api:

API
===

.. _platform_obj:

Platform Object
---------------

.. module:: v8cffi.platform

.. autoclass:: _Platform
   :members: is_alive, create_vm, set_up, tear_down

.. autodata:: platform
   :annotation: – Platform object (singleton)

.. _vm_obj:

VM Object
---------

.. module:: v8cffi.vm

.. autoclass:: VM
   :members:

.. _context_obj:

Context Object
--------------

.. module:: v8cffi.context

.. autoclass:: Context
   :members:

Shortcuts Module
----------------

.. automodule:: v8cffi.shortcuts
   :members: set_up, get_context
