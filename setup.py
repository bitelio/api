#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup


__version__ = '0.0.1'


setup(name='api',
      packages=['server'],
      version=__version__,
      author='Guillermo Guirao Aguilar',
      author_email='info@bitelio.com',
      url='https://github.com/bitelio/api',
      install_requires=['flask', 'flask_restful', 'pymongo', 'pytz'],
      tests_require={'test': ['nose', 'rednose']},
      classifiers=['Programming Language :: Python :: 3.5'],
      entry_points={'console_scripts': ['api = server:run']})
