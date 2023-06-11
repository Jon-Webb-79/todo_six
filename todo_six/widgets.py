# Import necessary packages here
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QFont, QKeySequence, QShortcut
from PyQt6.QtWidgets import (
    QButtonGroup,
    QCalendarWidget,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMessageBox,
    QPushButton,
    QRadioButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from todo_six.database import ToDoDatabase

# ==========================================================================================
# ==========================================================================================

# File:    widgets.py
# Date:    June 01, 2023
# Author:  Jonathan A. Webb
# Purpose: This file contains classes that implement widgets to be used in the todo_six
#          code base.  In most cases the classes act as warappers around widgets
#          implemented in the PyQt6 library.
# ==========================================================================================
# ==========================================================================================
# Insert Code here


class DayNightRadioButton(QWidget):
    """
    Custom QWidget that contains two QRadioButtons for selecting Day or Night themes.

    :param active_widget: Widget is active when created if set to True, inactive
                          if set to false
    """

    def __init__(self, active_widget: bool = True):
        super().__init__()

        self.form = QHBoxLayout(self)
        self.button_group = QButtonGroup(self)

        self.day_button = QRadioButton("Day")
        self.night_button = QRadioButton("Night")

        self.form.addWidget(self.day_button)
        self.form.addWidget(self.night_button)

        self.button_group.addButton(self.day_button)
        self.button_group.addButton(self.night_button)

        # Set the day theme as default
        self.day_button.setChecked(True)
        self.setEnabled(active_widget)


# ==========================================================================================
# ==========================================================================================


class DropDownMenu(QComboBox):
    """
    Class to create a drop down menu

    :param options: A list of text strings describing possible options for drop
                    down menu
    :param active_widget: Widget is active when created if set to True, inactive
                          if set to false
    """

    def __init__(self, options: list[str], active_widget: bool = True):
        super().__init__()
        self.addItems(options)
        self.setCurrentIndex(0)  # Set default selection to the first item
        self.setEnabled(active_widget)

    # ------------------------------------------------------------------------------------------

    def get_selected_option(self) -> str:
        """
        Method to return the selected options

        :return option: The selected option as a string
        """
        return self.currentText()

    # ------------------------------------------------------------------------------------------

    def set_selected_option(self, option: str) -> None:
        """
        Method that allows a user to enter an option as a text string

        :param option: A text string describing the options
        """
        index = self.findText(option)
        if index >= 0:
            self.setCurrentIndex(index)


# ==========================================================================================
# ==========================================================================================


class LineEdit(QLineEdit):
    """
    Custom QLineEdit with specific text and font

    :param font: A QFont object with font type and font size
    :param active_widget: Widget is active when created if set to True, inactive
                          if set to false
    """

    def __init__(self, font: QFont, active_widget: bool = True):
        super().__init__()
        self.setFont(font)
        self.setEnabled(active_widget)

    # ------------------------------------------------------------------------------------------

    def set_text(self, text: str) -> None:
        """
        Method to set the text in the QLineEdit

        :param text: The text to be set
        """
        self.setText(text)

    # ------------------------------------------------------------------------------------------

    def get_text(self) -> str:
        """
        Method to get the text in the QLineEdit

        :return: The text in the QLineEdit
        """
        return self.text()


# ==========================================================================================
# ==========================================================================================


class ListWidget(QListWidget):
    """
    Custom QListWidget with specific text and font

    :param font: A QFont object with font type and font size
    :param active_widget: Widget is active when created if set to True, inactive
                          if set to false
    """

    def __init__(self, font: QFont, active_widget: bool = True):
        super().__init__()
        self.setFont(font)
        self.setEnabled(active_widget)

    # ------------------------------------------------------------------------------------------

    def add_item(self, item: str) -> None:
        """
        Method to add an item to the QListWidget

        :param item: The item to be added
        """
        self.addItem(item)

    # ------------------------------------------------------------------------------------------

    def remove_item(self, item: str) -> None:
        """
        Method to remove an item from the QListWidget

        :param item: The item to be removed
        """
        items = self.findItems(item, Qt.MatchExactly)
        if not items:
            return  # No item found to be removed
        for item in items:
            self.takeItem(self.row(item))

    # ------------------------------------------------------------------------------------------

    def get_selected_item(self) -> str:
        """
        Method to get the currently selected item in the QListWidget

        :return: The currently selected item
        """
        return self.currentItem().text() if self.currentItem() else None


# ==========================================================================================
# ==========================================================================================


class OpacitySlider(QWidget):
    """
    Custom QWidget that contains a QLabel and a QSlider for setting the opacity.

    :param active_widget: Widget is active when created if set to True, inactive
                          if set to false
    """

    def __init__(self, active_widget: bool = True):
        super().__init__()

        # Create a QHBoxLayout
        layout = QHBoxLayout()

        # Create a QLabel with a default opacity of 100
        self.label = QLabel("Opacity: 100")

        # Create a QSlider
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 100)  # Opacity range from 0% to 100%
        self.slider.setValue(100)  # Default opacity is 100%

        # Connect slider's value change signal to update_label function
        self.slider.valueChanged.connect(self.update_label)

        # Add the QLabel and QSlider to the QHBoxLayout
        layout.addWidget(self.label)
        layout.addWidget(self.slider)

        # Set the QHBoxLayout as the layout for this widget
        self.setLayout(layout)
        self.setEnabled(active_widget)

    # ------------------------------------------------------------------------------------------

    def update_label(self, value: float) -> None:
        """
        Updates the QLabel text with the current slider value.

        :param value: The current value of the slider.
        """
        # Update the label text with the new slider value
        self.label.setText(f"Opacity: {value}")

    # ------------------------------------------------------------------------------------------

    def set_opacity(self, value: int) -> None:
        """
        Method to set the opacity

        :param value: The opacity value to be set
        """
        self.slider.setValue(value)

    # ------------------------------------------------------------------------------------------

    def get_opacity(self) -> int:
        """
        Method to get the current opacity value

        :return: The current opacity value
        """
        return self.slider.value()


# ==========================================================================================
# ==========================================================================================


class PushButton(QPushButton):
    """
    Custom QPushButton with specific text and font.

    :param text: The text to be displayed on a button
    :param: font: A QFont object with font type and font size
    :param active_widget: Widget is active when created if set to True, inactive
                          if set to false
    """

    def __init__(self, text: str, font: QFont, active_widget: bool = True):
        super().__init__(text)
        self.setFont(font)
        self.setEnabled(active_widget)


# ==========================================================================================
# ==========================================================================================


class Calendar(QCalendarWidget):
    """
    Custom calendar widget with specified start and end dats as well as gird pattern

    :param start_date: A QDate object representing the first acceptable date in
                       the calendar
    :param end_date: A QDate object representing the last acceptable date in the
                     calendar
    :param grid: True if a grid around the dates is to be displayed, False otherwise.
    :param active_widget: Widget is active when created if set to True, inactive
                          if set to false
    """

    def __init__(
        self,
        start_date: QDate,
        end_date: QDate,
        grid: bool = True,
        active_widget: bool = True,
    ):
        super().__init__()
        self.setMinimumDate(start_date)
        self.setMaximumDate(end_date)
        self.setEnabled(active_widget)
        self.setGridVisible(grid)

    # ------------------------------------------------------------------------------------------

    def get_selected_date(self) -> QDate:
        """
        Method to get the currently selected date.

        :return: The currently selected date.
        """
        return self.selectedDate()

    # ------------------------------------------------------------------------------------------

    def set_selected_date(self, date: QDate) -> None:
        """
        Method to set the selected date.

        :param date: The date to select.
        """
        self.setSelectedDate(date)


# ==========================================================================================
# ==========================================================================================


class Tab:
    """
    Class to set a tab instantiation for the todo_six application.

    :param fnt: A QFont object
    :param tab_name: A string character name for the object
    :param db: A ToDoDatabase object
    """

    def __init__(self, fnt: QFont, tab_name: str, db: ToDoDatabase):
        self.tab_name = tab_name
        self.tab_widget = QWidget()
        self.tab_layout = QVBoxLayout(self.tab_widget)
        self.db = db

        self.widgets = {
            "entry_field": LineEdit(fnt),
            "todo_list": ListWidget(fnt),
            "todo_list_label": QLabel("Todo List"),
            "completed_list_label": QLabel("Completed List"),
            "completed_list": ListWidget(fnt),
            "add_task_button": PushButton("Add Task", fnt),
            "retire_task_button": PushButton("Retire Task", fnt),
            "delete_task_button": PushButton("Delete Task", fnt),
            "drop_down_menu": DropDownMenu(["Day", "Week", "Month", "Year", "All"]),
        }

        self.tab_layout.addWidget(self.widgets["entry_field"])
        self.tab_layout.addWidget(self.widgets["todo_list_label"])
        self.tab_layout.addWidget(self.widgets["todo_list"])
        self.tab_layout.addWidget(self.widgets["completed_list_label"])
        self.tab_layout.addWidget(self.widgets["completed_list"])
        self.tab_layout.addWidget(self.widgets["add_task_button"])
        self.tab_layout.addWidget(self.widgets["retire_task_button"])
        self.tab_layout.addWidget(self.widgets["delete_task_button"])
        self.tab_layout.addWidget(self.widgets["drop_down_menu"])

        self.widgets["add_task_button"].clicked.connect(self._add_task)
        self.shortcut = QShortcut(QKeySequence(Qt.Key.Key_Return), self.tab_widget)
        self.shortcut.activated.connect(self._add_task)

    # ------------------------------------------------------------------------------------------

    def _add_task(self):
        """
        Method to add a task to the todo_list window of the appropriate tab
        """
        task_text = self.widgets["entry_field"].text()
        if task_text:
            success, message = self.db.insert_task(task_text)
            if not success:
                # Display a message box if there's an error
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Critical)
                msg.setText("Error")
                msg.setInformativeText(message)
                msg.setWindowTitle("Error")
                msg.exec()
                return
            # Get the last inserted id from the database
            last_id = self._get_largest_id_in_todo_list()
            new_id = last_id + 1
            self.widgets["todo_list"].addItem(f"{new_id}. {task_text}")
            self.widgets["entry_field"].setText("")  # clear the entry field

    # ------------------------------------------------------------------------------------------

    def _get_largest_id_in_todo_list(self) -> int:
        """
        Return the largest ID currently in the todo_list.
        """
        max_id = 0
        for i in range(self.widgets["todo_list"].count()):
            item_text = self.widgets["todo_list"].item(i).text()
            item_id = int(
                item_text.split(".")[0]
            )  # assuming item_text is in "id: text" format
            if item_id > max_id:
                max_id = item_id
        return max_id


# ==========================================================================================
# ==========================================================================================
# eof
