from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize(["hello.py", 'main.py'], build_dir="build"),
    #cythonize("objects/Position.py")
)