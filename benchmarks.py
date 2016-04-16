# -*- coding: utf-8 -*-


if __name__ == "__main__":
    import time
    import gc
    import timeit
    import functools
    from v8cffi.platform import platform

    OPS_NUMBER = 110000


    def do_all():

        with platform as pm:
            with pm.create_vm() as vm:
                with vm.create_context() as context:
                    # hello = b'hi' * 10000
                    hello = b'hi'
                    context.run_script(b"var hello = '" + hello + b"';")
                    # 110000 ops/s on a 1.8Ghz CPU
                    print(timeit.timeit(functools.partial(context.run_script, b"hello"), number=OPS_NUMBER))

                    print('ok')

    do_all()
    #gc.collect()
    #time.sleep(30)
