from os import path
from setuptools import setup


def version():
    init = path.join(path.dirname(__file__), 'api', '__init__.py')
    line = list(filter(lambda l: l.startswith('__version__'), open(init)))[0]
    return line.split('=')[-1].strip(" '\"\n")


setup(name='api',
      packages=['api'],
      version=version(),
      author='Guillermo Guirao Aguilar',
      author_email='info@bitelio.com',
      url='https://github.com/bitelio/backend',
      classifiers=['Programming Language :: Python :: 3.8'])
