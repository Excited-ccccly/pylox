#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('requirements.txt') as f:
    reqs = f.read().split('\n')

with open('requirements.dev.txt') as f:
    dev_reqs = f.read().split('\n')

install_requires = [x.strip() for x in reqs if 'git+' not in x]
dev_requires = [x.strip() for x in dev_reqs if 'git+' not in x]

setup(
    author="Lingyun Chen",
    author_email='geekchenlingyun@outlook.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    description="Lox language implemented in Python",
    entry_points={
        'console_scripts': [
            'pylox=pylox.cli:main',
        ],
    },
    install_requires=install_requires,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='pylox',
    name='pylox',
    packages=find_packages(include=['pylox']),
    test_suite='tests',
    tests_require=dev_requires,
    url='https://github.com/excited-ccccly/pylox',
    version='0.1.0',
    zip_safe=False,
)
