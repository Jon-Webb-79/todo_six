# Import necessary packages here
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

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
        self.menu_bar = MenuBar()
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
        self._create_widgets()
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

    def _create_widgets(self) -> None:
        """
        This method instantiates all widgets for the todo_list application
        """
        # Set control actuators that are persistent (not related to tabs)
        self.day_night_radio_button = DayNightRadioButton()
        self.opacity_slider = OpacitySlider()

        self.entry_field = LineEdit(self.fnt)

        self.todo_list = ListWidget(self.fnt)
        self.todo_list_label = QLabel("Todo List")

        self.completed_list_label = QLabel("Completed List")
        self.completed_list = ListWidget(self.fnt)

        # Use the custom Button class
        self.add_task_button = PushButton("Add Task", self.fnt)
        self.retire_task_button = PushButton("Retire Task", self.fnt)
        self.delete_task_button = PushButton("Delete Task", self.fnt)

        self.drop_down_menu = DropDownMenu(["Day", "Week", "Month", "Year", "All"])

    # ------------------------------------------------------------------------------------------

    def _arrange_widgets(self) -> None:
        """
        This method arranges all of the widgets for the todo_list application
        """
        # Add text widgets
        self.grid.addWidget(self.entry_field, 0, 0, 1, 2)
        self.grid.addWidget(self.todo_list_label, 1, 1)
        self.grid.addWidget(self.todo_list, 2, 1)
        self.grid.addWidget(self.completed_list, 4, 1)

        # Place buttons in vertical orientation, from top down
        self.vert.addWidget(self.add_task_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.vert.addWidget(
            self.retire_task_button, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.vert.addWidget(
            self.delete_task_button, alignment=Qt.AlignmentFlag.AlignCenter
        )

        # Calculate the maximum width and height among the buttons
        max_width = max(
            self.add_task_button.sizeHint().width(),
            self.retire_task_button.sizeHint().width(),
            self.delete_task_button.sizeHint().width(),
        )

        max_height = max(
            self.add_task_button.sizeHint().height(),
            self.retire_task_button.sizeHint().height(),
            self.delete_task_button.sizeHint().height(),
        )

        # Set all buttons to the same size
        self.add_task_button.setFixedSize(max_width + 10, max_height + 3)
        self.retire_task_button.setFixedSize(max_width + 10, max_height + 3)
        self.delete_task_button.setFixedSize(max_width + 10, max_height + 3)

        # Add the vertical layout to the grid layout
        self.grid.addLayout(self.vert, 2, 0, 5, 1)

        self.vert.addStretch(2)
        # self.grid.addLayout(self.vert, 1, 0)

        # Add day night radio button and opacity slider
        self.grid.addWidget(self.day_night_radio_button, 5, 0)
        self.grid.addWidget(
            self.opacity_slider, 5, 1, alignment=Qt.AlignmentFlag.AlignRight
        )

        completed_list_layout = QHBoxLayout()

        completed_list_layout.addWidget(self.completed_list_label)
        completed_list_layout.addWidget(self.drop_down_menu)

        # Replace the previous widget (QLabel) with the new layout
        self.grid.addLayout(completed_list_layout, 3, 1)
        self.grid.addWidget(self.completed_list, 4, 1)

        # Adjust ListWidget width
        self.todo_list.setMaximumWidth(700)
        self.completed_list.setMaximumWidth(700)
        self.central_widget.setLayout(self.grid)

    # ------------------------------------------------------------------------------------------

    def set_opacity(self, value):
        """
        Changes the opacity of the application
        """
        # Convert the slider value (0-100) to opacity value (0.0-1.0)
        opacity = value / 100.0
        self.setWindowOpacity(opacity)


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
# eof
