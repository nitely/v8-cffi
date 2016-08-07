# -*- coding: utf-8 -*-


if __name__ == "__main__":
    import time
    import gc
    import timeit
    import functools
    import asyncio
    from v8cffi.platform import platform
    from v8cffi.async.vm import VM

    OPS_NUMBER = 40000

    import time


    @asyncio.coroutine
    def do_all(loop):

        with platform as pm:
            with VM(pm, loop=loop) as vm:
                with vm.create_context() as context:
                    # hello = b'hi' * 10000
                    hello = b'hi'
                    yield from context.run_script(b"var hello = '" + hello + b"';")
                    # 110000 ops/s on a 1.8Ghz CPU

                    futs = [
                        asyncio.ensure_future(context.run_script(b"hello"), loop=loop)
                        for _ in range(OPS_NUMBER)]

                    ts = time.time()
                    yield from asyncio.gather(*futs, loop=loop)
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
