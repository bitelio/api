#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from setuptools import setup


def version():
    init = path.join(path.dirname(__file__), 'server', '__init__.py')
    line = list(filter(lambda l: l.startswith('__version__'), open(init)))[0]
    return line.split('=')[-1].strip(" '\"\n")


setup(name='api',
      packages=['server'],
      version=version(),
      author='Guillermo Guirao Aguilar',
      author_email='info@bitelio.com',
      url='https://github.com/bitelio/api',
      install_requires=['flask_restful', 'pymongo', 'pytz', 'flask'],
      setup_requires=['nose', 'rednose', 'coverage'],
      classifiers=['Programming Language :: Python :: 3.5'],
      entry_points={'console_scripts': ['api = server:run']})
