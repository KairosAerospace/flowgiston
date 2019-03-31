from distutils.core import setup

from setuptools import find_packages

setup(
    name='Flowgiston',
    version='0.1',
    packages=find_packages(),
    license='LICENSE.txt',
    long_description=open('README.txt', 'r').read(),
    author_email='matt@kairosaerospace.com',
    author="Matthew P. Gordon",
    maintainer="Matthew P. Gordon",
    maintainer_email="matt@kairosaerospace.com",
    install_requires=['graphviz==0.10.1'],
    tests_require=['pydot==1.4.1'],
)
