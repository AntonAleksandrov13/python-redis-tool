#!/usr/bin/env python
# coding=utf-8

from setuptools import setup


package_name = 'redis-tool'
filename = 'redis-tool.py'


def get_version():
    import ast

    with open(filename) as input_file:
        for line in input_file:
            if line.startswith('__version__'):
                return ast.parse(line).body[0].value.s


def get_long_description():
    try:
        with open('README.md', 'r') as f:
            return f.read()
    except IOError:
        return ''


setup(
    name=package_name,
    version=get_version(),
    author='AntonAleksandrov',
    author_email='antonaleksandrov24@gmail.com',
    description='redis-cluster administration made easy',
    url='https://github.com/AntonAleksandrov13/python-redis-tool',
    long_description=get_long_description(),
    py_modules=[package_name],
    entry_points={
        'console_scripts': [
            'redis-tool- = redis-tool:main'
        ]
    },
    license='License :: OSI Approved :: MIT License',
)