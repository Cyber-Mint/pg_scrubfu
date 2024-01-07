pg_scrubfu Developer Documentation
==================================

Table of Contents
-----------------

1. Contributing
   * Types of Contributions
   * Getting Started
   * Pull Request Guidelines
   * Publishing
   * Publish to PyPi
   * Testing Installation

2. Developer's Guide
   * Installation Tips
   * Installation
   * Unit Tests

3. Copyright

Contributing
=============

Contributions are welcome, and they are greatly appreciated! Every little bit helps, and credit will always be given.

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at `https://github.com/Cyber-Mint/py_app_package/issues`

If you are reporting a bug, please include:

- Your operating system name and version.
- Any details about your local setup that might be helpful in troubleshooting.
- Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement" and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

We could always use more documentation, whether as part of the official docs, in docstrings, or even on the web in blog posts, articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at `https://github.com/Cyber-Mint/py_app_package/issues`.

If you are proposing a feature:

- Explain in detail how it would work.
- Keep the scope as narrow as possible, to make it easier to implement.
- Remember that this is a volunteer-driven project, and that contributions are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up for local development.

1. Fork the repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:Cyber-Mint/py_app_package.git

3. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development::

    $ python3 -m venv ./py_app_package 
    $ cd ./py_app_package
    $ source bin/activate
    $ pip install -e .

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass the test cases, fixup your PEP8 compliance, and check for any code style issues:

    $ pip3 install tox autopep8 flake8 black
    $ tox
    $ autopep8 -r -i app
    $ flake8 app
    $ python -m black app

   To get autopep8 and black, just pip install them into your virtualenv.

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git tag -a vX.Y.Z -m "Release Tag"
    $ git push origin name-of-your-bugfix-or-feature --follow-tags

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put your new functionality into a function with a docstring, and add the feature to the list in CHANGELOG.rst.
3. The pull request should work for Python 3.8+

Publish to PyPi
---------------

Some notes on publishing to PyPi. Always publish to testpypi first!

    $ rm -rf dist/ build/
    $ git status   # to make sure you have committed the latest version
    $ python3 setup.py sdist bdist_wheel
    $ twine check dist/*
    $ python3 -m twine upload --repository testpypi dist/* --verbose

Tips
----

To run the tests::

    $ tox

Deploying
---------

A reminder for the maintainers on how to deploy.

1. Update CHANGELOG.rst with the intended release number Z.Y.X and commit to git.

2. Bump the version number X.Y.Z in setup.py according to Major.Minor.Patch::

    $ git tag -a vX.Y.Z -m "Initial commit"

3. Push the release commit and new tag up::

       $ git push --follow-tags

4. Th CI tool (once you have set one up) should automatically deploy the tagged release to PyPI if the automated tests pass.

Publishing to PyPi
------------------

First perform all your tests on test.pypi.org by registering there. The create a token and save it safely somewhere.

    # After the build steps above you may upload your dist/* files
    # CHANGELOG and setup.py are the only two files which refer to a version.

    $ python3 -m twine upload --repository testpypi dist/* --verbose
    # this will ask you for a username: enter __token__
    # and it will ask for a password: paste the long token string (in full)

Testing the install will require the use of specifying the testpypi repo as follows::

    sudo pip install --extra-index-url https://test.pypi.org/simple/ py-app-package

This will fetch the dependencies from the main pypi repo and your package from the specified pypi repo.

Developer's Guide
=================

Installation Tips
-----------------

Install the following in your development environment:

.. code-block:: bash

   sudo apt install pre-commit


Installation
------------

``pg_scrubfu`` is easy to install. Simply run the following command:

.. code-block:: bash

   pip install pg_scrubfu


Unit Tests
----------

To run the unit tests:

.. code-block:: bash

   pip3 install tox
   tox



Copyright
=================
Copyright © 2020, Cyber-Mint (Pty) Ltd—all rights reserved.

