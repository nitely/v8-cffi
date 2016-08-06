# -*- coding: utf-8 -*-


if __name__ == "__main__":
    import time
    import gc
    import timeit
    import functools
    import asyncio
    from v8cffi.platform import platform

    OPS_NUMBER = 40000

    import time


    @asyncio.coroutine
    def do_all(loop):

        with platform as pm:
            with pm.create_vm() as vm:
                with vm.create_context(loop=loop) as context:
                    # hello = b'hi' * 10000
                    hello = b'hi'
                    yield from context.run_script_async(b"var hello = '" + hello + b"';")
                    # 110000 ops/s on a 1.8Ghz CPU

                    futs = []

                    for _ in range(OPS_NUMBER):
                        futs.append(asyncio.ensure_future(context.run_script_async(b"hello")))

                    ts = time.time()
                    yield from asyncio.wait(futs)
                    te = time.time()
                    print('%f sec' % (te - ts))

                    print('ok')

    # do_all()
    #gc.collect()
    #time.sleep(30)



    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(
            do_all(loop=event_loop)
        )
    finally:
        event_loop.close()
