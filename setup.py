import pyeloverblik
from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='pyeloverblik',
    version=pyeloverblik.__version__,
    description='Python wrapper for eloverblik.dk API.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/JonasPed/pyeloverblik',
    author='Jonas Pedersen',
    author_email='jonas@pedersen.ninja',
    license='Apache 2.0',
    packages=['pyeloverblik'])
