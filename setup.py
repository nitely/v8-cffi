#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages


README = open(
    os.path.join(os.path.dirname(__file__), 'README.md'),
    encoding='utf-8').read()
REQUIREMENTS = open(
    os.path.join(os.path.dirname(__file__), 'requirements.txt'),
    encoding='utf-8').read()
VERSION = __import__('v8cffi').__version__

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='v8-cffi',
    version=VERSION,
    description='Embed the V8 Javascript engine into Python.',
    author='Esteban Castro Borsani',
    author_email='ecastroborsani@gmail.com',
    long_description=README,
    url='https://github.com/nitely/v8-cffi',
    packages=find_packages(exclude=['dev']),
    test_suite="runtests.start",
    package_data={'v8cffi': ['src/*.*', 'src/v8/*.*']},
    zip_safe=False,
    install_requires=REQUIREMENTS,
    setup_requires=REQUIREMENTS,
    cffi_modules=["v8cffi/v8_build.py:ffi"],
    license='MIT License',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content'])
