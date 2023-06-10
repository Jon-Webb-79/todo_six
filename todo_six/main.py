# Import necessary packages here
import os
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QGridLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from todo_six.database import ToDoDatabase
from todo_six.menu_bar import MenuBar
from todo_six.widgets import (
    DayNightRadioButton,
    DropDownMenu,
    LineEdit,
    ListWidget,
    OpacitySlider,
    PushButton,
)

# ==========================================================================================
# ==========================================================================================

# File:    main.py
# Date:    June 01, 2023
# Author:  Jonathan A. Webb
# Purpose: This file contains the functions and classes that integrate the todo_six
#          application into a Model, View, Controller architecture
# ==========================================================================================
# ==========================================================================================
# Insert Code here


class ToDoListModel:
    """
    The ToDoListModel class handles all data manipulation for the todo_six
    application
    """

    def __init__(self):
        # Initialize your model data here
        self.tasks = []
        self.tasks_id = []

    # ------------------------------------------------------------------------------------------

    def add_task(self, task: str, task_id: int) -> None:
        """
        Adds an item to the tasks list

        :param task: The task to be added
        """
        self.tasks.append(task)
        self.tasks_id.append(task_id)

    # ------------------------------------------------------------------------------------------

    def remove_task(self, task_id: int) -> bool:
        """
        This method will remove items from the tasks and tasks_id lists

        :param task_id: The unique id of the item to be removed
        """
        if task_id not in self.tasks_id:
            sys.stderr.write(f"Task id {task_id} not in list")
            return False
        index = self.tasks_id.index(task_id)
        self.tasks.pop(index)
        self.tasks_id.pop(index)
        return True


# ==========================================================================================
# ==========================================================================================


class ToDoListView(QMainWindow, QWidget, ToDoListModel):
    """
    Class that integrates the application into a main window with tabs. This tab
    will also act as the View class in a Model, View, Controller architecture

    :param day_theme: The title and path length to the .qss file containing the day
                      time theme for the application
    :param night_theme: The title and path length to the .qss file containing the night
                        time theme for the application
    """

    def __init__(self, day_theme: str, night_theme: str):
        super().__init__()
        self.day_theme = day_theme
        self.night_theme = night_theme

        # Set layout structure for application
        self.grid = QGridLayout()
        self.vert = QVBoxLayout()

        # IMport menu options
        self.menu_bar = MenuBar(self.create_new_database)
        self.setMenuBar(self.menu_bar)

        # Set window properties
        self.setWindowTitle("Todo List")
        self.resize(951, 1022)

        # Set GUI font
        self.fnt = QFont()
        # Was Cantrell
        self.fnt.setFamily("Verdana")
        self.fnt.setPointSize(18)

        # set Central Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Add widgets
        self._create_initial_widgets()
        self._arrange_widgets()

    # ------------------------------------------------------------------------------------------

    def set_day_theme(self) -> None:
        """
        Toggles the application to the day time style sheet
        """
        with open(self.day_theme) as file:
            self.setStyleSheet(file.read())

    # ------------------------------------------------------------------------------------------

    def set_night_theme(self) -> None:
        """
        Toggles the application to the night time style sheet
        """
        with open(self.night_theme) as file:
            self.setStyleSheet(file.read())

    # ------------------------------------------------------------------------------------------

    def add_new_tab(self, tab_name, ok) -> None:
        if ok and tab_name != "":
            new_tab = QWidget()
            new_tab_layout = QVBoxLayout(new_tab)

            # Instantiate Widgets and add them to the layout
            entry_field = LineEdit(self.fnt)
            todo_list = ListWidget(self.fnt)
            todo_list_label = QLabel("Todo List")
            completed_list_label = QLabel("Completed List")
            completed_list = ListWidget(self.fnt)
            add_task_button = PushButton("Add Task", self.fnt)
            retire_task_button = PushButton("Retire Task", self.fnt)
            delete_task_button = PushButton("Delete Task", self.fnt)
            drop_down_menu = DropDownMenu(["Day", "Week", "Month", "Year", "All"])

            new_tab_layout.addWidget(entry_field)
            new_tab_layout.addWidget(todo_list_label)
            new_tab_layout.addWidget(todo_list)
            new_tab_layout.addWidget(completed_list_label)
            new_tab_layout.addWidget(completed_list)
            new_tab_layout.addWidget(add_task_button)
            new_tab_layout.addWidget(retire_task_button)
            new_tab_layout.addWidget(delete_task_button)
            new_tab_layout.addWidget(drop_down_menu)

            # Add the new tab to the tab widget
            self.tabs.addTab(new_tab, tab_name)

    # ------------------------------------------------------------------------------------------

    def set_opacity(self, value) -> None:
        """
        Changes the opacity of the application
        """
        # Convert the slider value (0-100) to opacity value (0.0-1.0)
        opacity = value / 100.0
        self.setWindowOpacity(opacity)

    # ==========================================================================================
    # PRIVATE-LIKE METHODS

    def _create_initial_widgets(self) -> None:
        """
        This method instantiates all widgets for the todo_list application
        """
        # Set control actuators that are persistent (not related to tabs)
        self.day_night_radio_button = DayNightRadioButton()
        self.opacity_slider = OpacitySlider()

        # Setup Tab widget
        self.tabs = QTabWidget(self.central_widget)

    # ------------------------------------------------------------------------------------------

    def _arrange_widgets(self) -> None:
        """
        This method arranges all of the widgets for the todo_list application
        """
        # Add day night radio button and opacity slider
        self.grid.addWidget(self.day_night_radio_button, 0, 0)
        self.grid.addWidget(
            self.opacity_slider, 0, 1, alignment=Qt.AlignmentFlag.AlignRight
        )

        # Add the tab widget
        self.grid.addWidget(self.tabs, 1, 0, 1, 2)

        self.central_widget.setLayout(self.grid)


# ==========================================================================================
# ==========================================================================================


class ToDoListController(ToDoListView):
    """
    Class to control all aspects of the todo_six application

    :param day_theme: The title and path length to the .qss file containing the day
                      time theme for the application
    :param night_theme: The title and path length to the .qss file containing the night
                        time theme for the application
    """

    def __init__(self, day_sheet: str, night_sheet: str):
        super().__init__(day_sheet, night_sheet)

        self.day_night_radio_button.day_button.clicked.connect(self.set_day_theme)
        self.day_night_radio_button.night_button.clicked.connect(self.set_night_theme)
        self.opacity_slider.slider.valueChanged.connect(self.set_opacity)

        self.database = None
        self.tab_database_map = {}

    # ------------------------------------------------------------------------------------------

    def create_new_database(self) -> None:
        """
        Method that is connected to the New button and is used to create a new database
        """
        response = False
        while response is False:
            msg1 = "Create New Database"
            msg2 = "SQLite Databases (*.db);;All Files (*)"
            file_name, _ = QFileDialog.getSaveFileName(None, msg1, "", msg2)
            if file_name:
                if not file_name.endswith(".db"):  # ensure the file has .db extension
                    file_name += ".db"
            if os.path.exists(file_name):
                msg1 = f"A database named '{file_name}' already exists. "
                msg1 += "Please choose a different name."
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Critical)
                msg.setText("Database Already Exists")
                msg.setInformativeText(msg1)
                msg.setWindowTitle("Error")
                msg.exec()
            else:
                response = True
                self.database = ToDoDatabase(file_name)
                success, message = self.database.open_db()
                if not success:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Icon.Critical)
                    msg.setText(message)
                    msg.setWindowTitle("Error")
                    msg.exec()
                    break
                else:
                    success, message = self.database.create_tasks_table()
                if success:
                    file_name_only = os.path.splitext(os.path.basename(file_name))[0]
                    if file_name_only in self.tab_database_map:
                        file_name_only += "-1"
                    self.add_new_tab(file_name_only, success)
                    self.tab_database_map[file_name_only] = self.database
                    print(f"Database '{file_name}' and task table created successfully.")
                    break
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Icon.Critical)
                    msg.setText(message)
                    msg.setWindowTitle("Error")
                    msg.exec()


# ==========================================================================================
# ==========================================================================================


def main(day_sheet: str, night_sheet: str) -> None:
    """
    Integrates and executes all necessary code

    :param day_sheet: The location and title of the daytime .qss style sheet
    :param night_sheet: The location and title of the night time .qss style sheet
    """
    app = QApplication(sys.argv)
    view = ToDoListController(day_sheet, night_sheet)
    view.set_day_theme()
    view.show()
    sys.exit(app.exec())


# ==========================================================================================
# ==========================================================================================

if __name__ == "__main__":
    day = "../data/style_sheets/night.qss"
    night = "../data/style_sheets/night.qss"
    main(day, night)

# TODO move create_new_database from ToDoListView to ToDoListController class
# TODO implement a dictionary of databases
# eof
