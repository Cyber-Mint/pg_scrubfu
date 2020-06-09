==============
py_app_package
==============
-------------------------------------------------
A Python3 template for packaging your application
-------------------------------------------------

This package is a working template/example of a python3 project ready for 
packaging and distributing via PyPi.


Cloning source
--------------

Get this package by::

    git clone git@github.com:Cyber-Mint/py_app_package.git

Activate the virtual environment with venv before coding, testing & packaging::

    $ cd py_app_package
    $ python3 -m venv ~/dev/py_app_package 
    $ source bin/activate
  
A packaging template for a package-able python application.

    >>> import app
    >>> print app.say_hello()

Installing
----------

To install source (development)::

    $ pip3 install -e .
   
But, to install from wheel binary::

    $ pip3 install wheel
    $ pip3 install .

Once it is installed you can run the command line interface defined in setup.py::

    $ app-cli

which will yield something like::

    Hello World
    From : Kara Mclaughlin 
    
Unit Tests
----------

To run the unit tests::

    $ pip3 install tox
    $ tox

====================================

Copyright |copy| 2020, Cyber-Mint (Pty) Ltd |---| all rights reserved.

.. |copy| unicode:: 0xA9 .. copyright sign
.. |---| unicode:: U+02014 .. em dash
   :trim: 

