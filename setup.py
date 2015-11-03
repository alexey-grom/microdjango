#!/usr/bin/env python

from setuptools import setup

from microdjango import __version__


setup(
    name='microdjango',
    version='.'.join(map(str, __version__)),
    description='Single file django project with models',
    author='alxgrmv@gmail.com',
    py_modules=['microdjango'],
    install_requires=(
        'django>=1.7',
    ),
)
