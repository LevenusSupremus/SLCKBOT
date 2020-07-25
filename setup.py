from setuptools import setup
from Cython.Build import cythonize

setup(ext_modules = cythonize('bot_functions_aio.py'))