.. _usage:

Usage
=====

Quick-start
-----------

::

    from v8cffi import shortcuts
    shortcuts.set_up()

    ctx = shortcuts.get_context()
    ctx.load_libs(['./foo_bundled.js'])
    ctx.run_script('foo.render("hola mundo");')
    # "hola mundo"

This is the most simple and limited form of usage.
A platform, VM and global context are created when
calling ``set_up``, then the global context can be
retrieve by calling ``get_context`` from anywhere
within the application, even from other threads.

The normal usage is to ``set_up`` and ``load_libs``
at the start of the application, then call
``run_script`` in many other places.

One thing to have in mind is the context is `global`,
this means any modification to the global scope will
persist.

.. Tip::

    The API section contains useful information about:
    :ref:`platform <platform_obj>`, :ref:`vm <vm_obj>`
    and :ref:`context <context_obj>`.

Multiple VMs & contexts
-----------------------

::

    from v8cffi.platform import platform

    with platform as p:
        with p.create_vm() as vm:
            with vm.create_context() as ctx:
                ctx.load_libs(['./foo_bundled.js'])
                res = ctx.run_script('foo.render("hola mundo");')

            with vm.create_context() as ctx_b:
                ctx_b.load_libs(['./bar.js', './baz.js'])
                res_b = ctx_b.run_script('baz.render("hello world");')

        with p.create_vm() as vm_b:
            # ...

Or alternatively, without ``with`` statement:

::

    from v8cffi.platform import platform

    p = platform
    p.set_up()
    vm = p.create_vm()
    vm.set_up()
    ctx = vm.create_context()

    try:
        # ...
    finally:
        ctx.tear_down()
        vm.tear_down()
        p.tear_down()

This allows much greater flexibility than
the previous ``shortcuts`` example.

As you may have read in the API section,
the first thing is to create a V8 platform,
there must be one and only one per process
(python instance).

Creating many VMs allows to run JS
code in parallel. Every VM takes about ~1MB
of RAM. It should be possible to spawn
a fixed pool of them with loaded libs to
reuse and obtain N times the number of opts/s
(where N is the number of VMs).

Every VM should run in a different
python thread, so when calling ``run_script``,
the thread blocks (the GIL is released) and
another python thread can run code in a different VM.

In case two python threads are using the `same` VM,
the VM will prevent them from running at the same time.
But both will block and release the GIL,
allowing other python threads to run.

At last, creating many Context allows JS code run without
sharing the same global scope.

