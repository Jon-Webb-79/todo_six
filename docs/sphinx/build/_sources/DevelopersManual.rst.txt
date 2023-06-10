****************
Developrs Manual
****************
The todo list application was written as with a Modelv, Viewer, Controller (MVC) architecture.
The Model-View-Controller (MVC) architecture is a design pattern commonly used in software
development to separate the concerns of an application into three distinct components: the Model,
the View, and the Controller. The Model represents the data and logic of the application,
encapsulating its business rules and state. The View is responsible for presenting the data to the
user and displaying the user interface. The Controller acts as an intermediary between the Model
and the View, handling user input, updating the Model, and triggering the appropriate changes in the
View. This architecture promotes the separation of concerns, making the application more modular,
maintainable, and easier to extend or modify.  The MVC classes are stored in the **main.py** file,
their public attributes are shown below.


Widgets
=======
All widgets used in the todo list application are created or encapsulated in the **widgets.py**
file.  In many cases, these are wrappers around the widgets already contained in the PyQt6
library.  The widgets along with their public attributes are shown below.

.. autoclass:: todo_six.widgets.LineEdit
   :members:

.. autoclass:: todo_six.widgets.ListWidget
   :members:

.. autoclass:: todo_six.widgets.PushButton
   :members:

.. autoclass:: todo_six.widgets.DayNightRadioButton
   :members:

.. autoclass:: todo_six.widgets.OpacitySlider
   :members:

.. autoclass:: todo_six.widgets.Calendar
   :members:

.. autoclass:: todo_six.widgets.Tab
   :members:

Menu Bar
========
All menu bar items used in the todo list application are created from the **menu_bar.py**
file.


DatabaseManager
===============
All database actions are controlled from the DatabaseManager class stored in **database.py**.
The database classes are as follows.

.. autoclass:: todo_six.database.SQLiteManager
   :members:

.. autoclass:: todo_six.database.ToDoDatabase
   :members:
