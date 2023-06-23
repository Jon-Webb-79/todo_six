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

#. Navigate to the correct installation directory.
   #. For zshell navigate to ``cd scripts/zsh``
   #. For bash navigate to ``cd scripts/bash``
#. Run the installation script.
   #. For zshell ``zsh install.zsh``
   #. For bash ``bash install.sh``
#. The script will run and create another directory at the root directory for the repository
   titled ``dist``.  A copy of the executable will be stored in the ``dist`` directory.
   If you are running Mac OS, the executable will be titled ``todo.app``, if you are running
   linux the directory will be titled ``todo``.
#. Despite the fact that the executable is stored in the ``dist`` directory, a copy is installed
   in ``~/bin`` if you are running Linux or ``~/Applications`` if you are running Mac OS.
   Furthermore, if you are running a Linux distribution, a ``todo.desktop`` file is copied
   to your ``~/.local/share/applications/`` directory.  At this point, the executable
   should be visible in teh application menu if running Linux, or LaunchPad if using Mac.
#. If the application is not visible in LaunchPad for Mac users, then type ``killall Dock``
   into the termal to restart the dock.

For PC Users (**NOTE:** This process is not tested yet for PC users)

#. Navigate to ``cd scripts/DOS``
#. Run ``install.cmd``
#. The script will run and create another directory at the root of the directory for the
   repository titled ``dist``.  A copy of the executable will be stored in ``dist``.
#. Despite hte fact that hte executable is stored in ``dist``, a copy is installed in
   ``~\Program Files\ ``.
#. The executable should be visible in your list of applications

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
