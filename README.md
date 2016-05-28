# V8-CFFI

[![Build Status](https://img.shields.io/travis/nitely/v8-cffi.svg?style=flat-square)](https://travis-ci.org/nitely/v8-cffi)
[![Coverage Status](https://img.shields.io/coveralls/nitely/v8-cffi.svg?style=flat-square)](https://coveralls.io/r/nitely/v8-cffi)
[![pypi](https://img.shields.io/pypi/v/v8-cffi.svg?style=flat-square)](https://pypi.python.org/pypi/v8-cffi)
[![licence](https://img.shields.io/pypi/l/v8-cffi.svg?style=flat-square)](https://raw.githubusercontent.com/nitely/v8-cffi/master/LICENSE)

Embed the V8 Javascript engine into Python.

> *Note: The initial purpose of this library is to render React components server side.*


## Compatibility

* GCC +4.8
* G++ +4.8
* Python 3.4 and 3.5

> *Note:* ***Linux-x64*** *is the only (officially) supported platform.
  To build the binaries for other platforms, the `./dev` steps
  must be adapted (probably to vagrant instead of docker) accordingly.
  PRs are welcome.*


## Usage

```python
from v8cffi import shortcuts
shortcuts.set_up()

ctx = shortcuts.get_context()
ctx.load_libs(['./foo_bundled.js'])
ctx.run_script('foo.render("hola mundo");')
# "hola mundo"
```

Read the [docs](http://v8-cffi.readthedocs.org/en/latest/).


## Notes

* Currently ships with V8 4.9.385.33 (stable).
* This repo contains V8 static files for Linux-x64,
  built with CentOS 6.7 (glibc 2.12),
  it's known to work in Ubuntu 12.04/14.04/16.04.


## Resources

* [How does NodeJS works?](https://medium.com/@ghaiklor/how-nodejs-works-bfe09efc80ca#.antxxwpsv)
* [Beautiful Native Libraries](http://lucumr.pocoo.org/2013/8/18/beautiful-native-libraries/)
or [alt](https://github.com/mitsuhiko/lucumr/blob/master/2013/8/18/beautiful-native-libraries.rst)
* [V8 Custom Snapshots](http://v8project.blogspot.com.ar/2015/09/custom-startup-snapshots.html)
* [V8 Cache Code](http://v8project.blogspot.com.ar/2015/07/code-caching.html)
* [Latest stable V8](https://gist.github.com/nitely/9668d9feab88644148a1e62322ff11c5)
* [V8 Wiki](https://github.com/v8/v8/wiki)
* [V8 Embedder's Guide](https://developers.google.com/v8/embed)
* [V8 users group](https://groups.google.com/forum/#!forum/v8-users)
* [CFFI user group](https://groups.google.com/forum/#!forum/python-cffi)
* [CFFI - Distribute including a (pre-)compiled library](https://groups.google.com/forum/#!topic/python-cffi/y5iNsezOlVs)


## Devs

[Devs](https://github.com/nitely/v8-cffi/tree/master/dev)


## Benchmarks

This will run some silly benchmarks.
It runs about ~110k ops/s on a 1.8GHz CPU.

```
$ make benchmarks
```


## License

MIT
