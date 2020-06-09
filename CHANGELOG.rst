==========
Change Log
==========

0.1.1 - 0.1.9 (2020-06-03)
------------------
* Deploy to pypi
* Added Classifier: Development Status :: 1 - Planning
* Fixed install_requires=['Faker>=4.1.0', ], in setup.py
* Added publishing instructions to CONTRIBUTING.rst

0.1.0 (2020-06-03)
------------------
* py_app_package Initial Commit
* Created file structures & minimum required files for project & app package::

        .
        ├── app
        │   ├── alive.py
        │   ├── app_cli.py
        │   ├── __init__.py
        │   └── tests
        │       ├── test_app_cli.py
        │       └── test_say_hello.py
        ├── CHANGELOG.rst
        ├── config.py
        ├── CONTRIBUTING.rst
        ├── include
        ├── LICENSE
        ├── MANIFEST.in
        ├── pyproject.toml
        ├── pyvenv.cfg
        ├── README.rst
        ├── requirements.txt
        ├── setup.py
        └── tox.ini


* Added demo unit tests with tox
* Added usage documentation
* Added CHANGELOG.rst
* Added CONTRIBUTING.rst
* Added PEP8, flake8 and pystyle guidelines


====================================

Copyright |copy| 2020, Cyber-Mint (Pty) Ltd |---| all rights reserved.

.. |copy| unicode:: 0xA9 .. copyright sign
.. |---| unicode:: U+02014 .. em dash
   :trim: 


