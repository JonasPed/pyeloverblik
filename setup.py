'''
setup.py
'''
from os import path
from setuptools import setup
import pyeloverblik

THIS_DIRECTORY = path.abspath(path.dirname(__file__))

with open(path.join(THIS_DIRECTORY, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='pyeloverblik',
    version=pyeloverblik.__version__,
    description='Python wrapper for eloverblik.dk API.',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/JonasPed/pyeloverblik',
    author='Jonas Pedersen',
    author_email='jonas@pedersen.ninja',
    license='Apache 2.0',
    packages=['pyeloverblik'],
    install_requires=['requests']
    )
