#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0', ]

setup_requirements = []

test_requirements = [
"pip==18.1",
"bumpversion==0.5.3",
"wheel==0.32.1",
"watchdog==0.9.0",
"flake8==3.5.0",
"tox==3.5.2",
"coverage==4.5.1",
"Sphinx==1.8.1",
"twine==1.12.1",]

setup(
    author="Lingyun Chen",
    author_email='geekchenlingyun@outlook.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Lox language implemented inn Python",
    entry_points={
        'console_scripts': [
            'pylox=pylox.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='pylox',
    name='pylox',
    packages=find_packages(include=['pylox']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/excited-ccccly/pylox',
    version='0.1.0',
    zip_safe=False,
)
