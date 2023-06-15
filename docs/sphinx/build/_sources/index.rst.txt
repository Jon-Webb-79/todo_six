.. Core Utilities documentation master file, created by
   sphinx-quickstart
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the Todo List documentation!
==========================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   UsersManual <UsersManual>
   DevelopersManual <DevelopersManual>


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Installation
============
To install todo_six application as a developer, follow these steps.

.. rst-class:: numbered-list

#. Install poetry globally on your computer. Follow the instructions from `Poetry <https://python-poetry.org/docs/>`_
#. Set the poetry virtual environment with the following command ``poetry config virtualenvs.in-project true``
#. Ensure you have .git installed on your computer.
#. At your desired location create a directory titled ``todo_six``
#. Open a terminal (Bash, zsh or DOS) and cd to the ``todo_six`` directory
#. Type ``git clone https://github.com/Jon-Webb-79/todo_six.git todo_six``
#. Install packages with ``poetry install``

To install the package as an executable complete the developer installation process,
and complete the following steps.

Usage
=====
The user instructions for this application is shown in :doc:`UsersManual`.


Developers Documentation
========================
For detailed documentation on developing with Todo List, please refer to the :doc:`DevelopersManual`.

Contributing
============
Pull requests are welcome.  For major changes, please open an issue first to discuss what
you would like to change.  Please make sure to include and update tests as well
as relevant cod-strings and sphinx updates.

License
=======
This project uses a basic MIT license
