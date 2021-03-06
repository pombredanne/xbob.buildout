==========================
 Buildout Recipes for Bob
==========================

This package contains a number of recipes to be used to build `Satellite
Packages <http://www.idiap.ch/software/bob/docs/releases/last/sphinx/html/OrganizeYourCode.html>`_ for `Bob <http://idiap.github.com/bob/>`_, a signal-processing and machine learning toolbox originally developed by the Biometrics Group at Idiap, in Switzerland.

.. note::

  You normally don't need to download this package directly. It will be done by
  ``zc.buildout`` automatically, if you followed our recipe to build `Satellite
  Packages`_.

C++/Python Package Builder
--------------------------

This recipe can build C++/Python extensions that link against Bob using
``pkg-config``. This recipe will look at the ``buildout`` section entry called
``prefixes``, that potentially lists prefixes that should be **prepended** to
the default ``pkg-config`` environment::

  [mycxx]
  recipe = xbob.buildout:develop

This recipe also, indirectly, generates a python interpreter named (by default)
``xpython.builder``. This program allows you to build the package using
installed or development eggs. Our build therefore by-passes the normal package
building via setuptools/distribute and use buildout for finding the eggs which
are required for the build. Note this has *nothing* to do with package
use, for which you can use the recipes below.

Supported Options
=================

debug
  If set, the module will be compiled with debugging symbols and with
  optimization turned off.

verbose
  If set, it will output the compilation commands while compiling the module.

eggs
  The eggs option specifies a list of eggs to use for **building** this
  package. Each string must be given on a separate line. If you don't specify
  anything, at least ``xbob.extension`` is included. Otherwise, we will add
  that one to your list, if not yet available.

interpreter
  The name of the interpreter that is generated for **building** this package.
  If you don't set it, it is by default called ``xpython.builder``.

buildout.prefixes
  A list of directories where this recipe will look for subdirectories with
  the stem ``lib/pkgconfig``. All directories matching this condition are
  appended to the ``pkg-config`` environment using the environment variable
  ``PKG_CONFIG_PATH``.

Multi-Script Installer
----------------------

This recipe installs **all** most used scripts and interpreter proxies for your
package. It will look at the ``buildout`` section entry called ``prefixes``,
that potentially lists prefixes that should be **prepended** to the default
python environment. In these prefixes, it will look for standard python
directories. If one or more are found, these paths are **prepended** into
the resulting scripts generated by this recipe and eggs will be searched on
those locations prioritarily.

By default, this recipe will use the eggs defined at the ``buildout`` section
called ``eggs``, but that can be overriden locally. It generates these scripts:

python
  A pre-configured python interpreter

ipython
  If the package ``ipython`` is installed, a pre-configured ipython interpreter
  will also be created

nosetests
  If the package ``nose`` is installed, a test runner called ``nosetests`` will
  be created on the bin directory of buildout.

sphinx- *utils*
  If the package ``sphinx`` is installed, several sphinx utilities will be
  created on the bin directory of buildout.

package scripts
  Package scripts will be created taking into account the ``prefixes``
  established for this section or globally (as a second priority).

To use this recipe, you just have to simply do::

  [scripts]
  recipe = xbob.buildout:scripts

Supported Options
=================

The recipe supports the following options:

prefixes
  A list of directories where this recipe will look for subdirectories with
  the stem ``lib/python*/site-packages``. All directories matching this
  condition are appended to the search paths. If not given, the value of this
  property defaults to ``buildout.prefixes``. Both can be empty, which makes
  this recipe default to using standard available paths.

eggs
  The eggs option specifies a list of eggs to use for **building** this
  package. Each string must be given on a separate line. If not given, the
  value of this property defaults to ``buildout.eggs``.

dependent-scripts
  If set to the string ``true``, scripts will be generated for all required
  eggs in addition to the eggs specifically named.

interpreter
  The name of a script to generate that allows access to a Python interpreter
  that has the path set based on the eggs installed. If you don't specify
  anything, the default value ``python`` will be used.

extra-paths
  Extra paths to be appended in a generated script. To prepend, using the
  ``prefixes`` entry.

nose-flags
  These are extra flags that are **appended** to the given ``nosetests``
  command line, automatically. Use this to preset arguments you like running
  all the time like ``-v``, for example.

Other Recipes
-------------

This package also provides recipes that allow for the discrete installation of
interpreters and support programs, lumped together with the ``scripts`` recipe
described above. You can use some of the options described above with these
recipes. For example, the ``prefixes``, ``eggs`` and ``extra-paths`` are
considered by all these recipes.

.. note::

  Use of these individual recipes should be done with care. The ``scripts``
  recipe should be used by default, unless you have a special requirement that
  is not covered by that recipe.

python
  This recipe generates **just** a python interpreter on the binary directory.
  Extra options considered: ``interpreter``.

ipython
  This recipe generates an IPython interpreter on the binary directory.
  Extra options considered: ``interpreter``.

egg.scripts
  This recipe generates only the scripts (and dependent scripts) for the
  package. Extra options considered: ``dependent-scripts``.

nose
  This recipe generates only the ``nosetests`` program. Extra options
  considered are:``nose-flags``.

sphinx
  This recipe generates only the Sphinx documentation generator applications.
  Extra options considered: none.

gdb-python
  This recipe generates a gdb launcher using the python interpreter so you can
  start your scripts directly typing ``gdb-python myscript.py``.
