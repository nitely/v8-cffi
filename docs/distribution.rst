.. _distribution:

Distribution decisions
----------------------

There are a couple of ways I could have distributed the library:

1. Distribute a ``libv8cffi.so`` or ``libv8.so`` as a separate
   package, install it into ``LD_LIBRARY_PATH`` and copy
   ``natives_blob.bin`` + ``snapshot_blob.bin`` into somewhere.
2. Compile everything from source at install time.

The second option is probably the worst since the V8 repo
alone is about 800MB and it takes quite a few minutes to
fetch and compile. The first option is ok I guess,
but I'd rather prefer the user compiles the library them-self.

So, I went with some intermediate option: distribute the
V8 static libraries (.a) when possible and compile the
cffi wrapper at install time.
