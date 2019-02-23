=====
pylox
=====

.. image:: https://travis-ci.org/Excited-ccccly/pylox.svg?branch=master
        :target: https://travis-ci.org/Excited-ccccly/pylox
.. image:: https://sonarcloud.io/api/project_badges/measure?project=Excited-ccccly_pylox&metric=sqale_rating
        :target: https://sonarcloud.io/dashboard?id=Excited-ccccly_pylox
.. image:: https://sonarcloud.io/api/project_badges/measure?project=Excited-ccccly_pylox&metric=coverage
        :target: https://sonarcloud.io/dashboard?id=Excited-ccccly_pylox
.. image:: https://sonarcloud.io/api/project_badges/measure?project=Excited-ccccly_pylox&metric=reliability_rating
        :target: https://sonarcloud.io/dashboard?id=Excited-ccccly_pylox
.. image:: https://sonarcloud.io/api/project_badges/measure?project=Excited-ccccly_pylox&metric=bugs
        :target: https://sonarcloud.io/dashboard?id=Excited-ccccly_pylox
.. image:: https://sonarcloud.io/api/project_badges/measure?project=Excited-ccccly_pylox&metric=code_smells
        :target: https://sonarcloud.io/dashboard?id=Excited-ccccly_pylox
.. image:: https://sonarcloud.io/api/project_badges/measure?project=Excited-ccccly_pylox&metric=sqale_index
        :target: https://sonarcloud.io/dashboard?id=Excited-ccccly_pylox
.. image:: https://sonarcloud.io/api/project_badges/measure?project=Excited-ccccly_pylox&metric=security_rating
        :target: https://sonarcloud.io/dashboard?id=Excited-ccccly_pylox
.. image:: https://sonarcloud.io/api/project_badges/measure?project=Excited-ccccly_pylox&metric=ncloc
        :target: https://sonarcloud.io/dashboard?id=Excited-ccccly_pylox

Lox language implemented in Python. Inspired by `Bob Nystrom`_'s `Crafting Interpreters`_

.. _Bob Nystrom: https://github.com/munificent
.. _Crafting Interpreters: http://craftinginterpreters.com/

Features
--------

* booleans, numbers, strings and nil datatypes
* dynamic typing
* control flow. if, while, for statement
* closures
* recursion
* class
* inheritance

more at `examples <https://github.com/Excited-ccccly/pylox/tree/master/tests/data/interpreter>`_

Developer Guide
_______________

Make sure you have python 3.7 installed, other versions are not tested.
Here I use python venv, and I highly suggest you do also::

    $ git clone https://github.com/Excited-ccccly/pylox
    $ cd pylox/
    $ mkdir .venv
    $ python -m venv .venv
    $ source .venv/bin/activate
    $ pip install -r requirements.txt & pip install -r requirements.dev.txt
    $ python setup.py develop

more at `CONTRIBUTING <https://github.com/Excited-ccccly/pylox/blob/master/CONTRIBUTING.rst>`_

Usage
-----

This project will register a command, **pylox**, in your environment(venv or system).
If you use venv as I suggested, **pylox** will only be avaliable in venv and you
have to activate venv before use **pylox** to interpret

Execute **pylox** with a script filepath argument to interpret it ::

    $ pylox tests/data/interpreter/visitor_pattern_in_lox.lox

or without a argument to enter REPL mode ::

    $ pylox

Know Issues
-----------

* In REPL mode, user have to input a blank line to get code interpreted.