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


class Tab(QWidget):
    """
    Class to set a tab instantiation for the todo_six application.

    :param fnt: A QFont object
    :param tab_name: A string character name for the object
    :param db: A ToDoDatabase object
    """

    def __init__(self, fnt: QFont, tab_name: str, db: ToDoDatabase):
        super().__init__()
        self.tab_name = tab_name
        self.tab_layout = QVBoxLayout(self)
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
        self.shortcut = QShortcut(QKeySequence(Qt.Key.Key_Return), self)
        self.shortcut.activated.connect(self._add_task)

        self.widgets["retire_task_button"].clicked.connect(self._retire_task)
        self.shortcut = QShortcut(QKeySequence(Qt.Key.Key_Delete), self)
        self.shortcut.activated.connect(self._retire_task)

        self.widgets["delete_task_button"].clicked.connect(self._delete_task)
        self.delete_all_shortcut = QShortcut(QKeySequence("Shift+Delete"), self)
        self.delete_all_shortcut.activated.connect(self._delete_task)

        self.widgets["drop_down_menu"].currentTextChanged.connect(
            self._update_completed_tasks
        )

        self.widgets["todo_list"].itemSelectionChanged.connect(
            self._clear_other_selections
        )
        self.widgets["completed_list"].itemSelectionChanged.connect(
            self._clear_other_selections
        )
        self.delete_mode = False

        self.todo_tasks = {}
        self.completed_tasks = {}

        self._load_tasks_from_database()

    # ------------------------------------------------------------------------------------------

    def _load_tasks_from_database(self):
        """
        A method to load tasks from the database. The tasks will be added to the
        appropriate task list and also to the corresponding task dictionary.
        """

        # Query the database for open tasks
        success, open_tasks, _ = self.db.select_open_tasks()

        # Iterate over the open tasks and add them to the todo list and dictionary
        if success:
            for _, row in open_tasks.iterrows():
                task_id = row["task_id"]
                task_name = row["task"]
                self.widgets["todo_list"].addItem(task_name)
                self.todo_tasks[task_id] = task_name

        time_frame = self.widgets["drop_down_menu"].currentText().upper()
        success, closed_tasks, _ = self.db.select_closed_tasks(time_frame)

        # Iterate over the closed tasks and add them to the completed list and dictionary
        if success:
            for _, row in closed_tasks.iterrows():
                task_id = row["task_id"]
                task_name = row["task"]
                self.widgets["completed_list"].addItem(task_name)
                self.completed_tasks[task_id] = task_name

    # ------------------------------------------------------------------------------------------

    def _add_task(self):
        """
        Method to add a task to the todo_list window of the appropriate tab
        """
        task_text = self.widgets["entry_field"].text()
        if task_text:
            success, message, task_id = self.db.insert_task(task_text)
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
            self.todo_tasks[new_id] = task_id
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

    # ------------------------------------------------------------------------------------------

    def _retire_task(self) -> None:
        """
        Method to retire a task from the todo_list window of the appropriate tab
        """
        # 1. Retire the selected task
        current_task = self.widgets["todo_list"].currentItem()
        if not current_task:
            return  # If no item selected, do nothing
        task_id, _ = current_task.text().split(". ", 1)
        db_task_id = self.todo_tasks[int(task_id)]
        success, message = self.db.complete_task(db_task_id)
        if not success:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("Error")
            msg.setInformativeText(message)
            msg.setWindowTitle("Error")
            msg.exec()
            return

        # 4. Remove the updated task from the todo list
        self.widgets["todo_list"].takeItem(self.widgets["todo_list"].row(current_task))
        del self.todo_tasks[int(task_id)]  # remove from our tracking dictionary

        # 2. Clear the completed list
        self.widgets["completed_list"].clear()

        # 3. Query the database for completed tasks
        if success:
            self._refresh_tasks()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("Error")
            msg.setInformativeText(message)
            msg.setWindowTitle("Error")
            msg.exec()

    # ------------------------------------------------------------------------------------------

    def _clear_other_selections(self):
        """
        Method to ensure that only one task can be highlighted at a time.
        """
        if not self.delete_mode:  # Skip clearing if we're in delete mode
            sender = self.sender()
            if sender is self.widgets["todo_list"]:
                self.widgets["completed_list"].clearSelection()
        else:
            self.widgets["todo_list"].clearSelection()

    # ------------------------------------------------------------------------------------------

    def _delete_task(self) -> None:
        """
        Method to delete the selected task from the database and the respective list
        window.
        """
        # 1. Determine which list the user is interacting with
        selected_list = None
        selected_item = None
        task_dict = None
        if self.widgets["todo_list"].selectedItems():
            selected_list = self.widgets["todo_list"]
            selected_item = selected_list.currentItem()
            task_dict = self.todo_tasks
        elif self.widgets["completed_list"].selectedItems():
            selected_list = self.widgets["completed_list"]
            selected_item = selected_list.currentItem()
            task_dict = self.completed_tasks

        if selected_item is None:
            QMessageBox.warning(self, "Error", "No task selected.")
            return

        # 2. Determine the task id
        task_id, _ = selected_item.text().split(". ", 1)
        db_task_id = task_dict[int(task_id)]

        # 3. Confirmation window
        confirm = QMessageBox.question(
            self,
            "Confirm Deletion",
            "Are you sure you want to delete the selected task?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        # 4. Delete the task from the database
        if confirm == QMessageBox.StandardButton.Yes:
            success, message = self.db.delete_task(db_task_id)
            if not success:
                QMessageBox.warning(self, "Error", f"Failed to delete task: {message}")
                return

            # 5. Refresh the tasks
            self._refresh_tasks()

    # ------------------------------------------------------------------------------------------

    def _update_completed_tasks(self):
        """
        Method to refresh the completed tasks list based on the selected time frame
        from the drop_down_menu.
        """
        time_frame = self.widgets["drop_down_menu"].currentText().upper()
        success, df, message = self.db.select_closed_tasks(time_frame)
        if success:
            self._populate_tasks(
                df, self.widgets["completed_tasks"], self.completed_tasks
            )
        else:
            msg = f"Failed to query completed tasks: {message}"
            QMessageBox.warning(self, "Error", msg)

    # ------------------------------------------------------------------------------------------

    def _refresh_tasks(self):
        """
        Method to refresh the tasks from the database.
        """
        # Refresh the todo tasks
        success, df, message = self.db.select_open_tasks()
        if success:
            self._populate_tasks(df, self.widgets["todo_list"], self.todo_tasks)
        else:
            QMessageBox.warning(self, "Error", f"Failed to query open tasks: {message}")

        # Refresh the completed tasks
        time_frame = self.widgets["drop_down_menu"].currentText().upper()
        success, df, message = self.db.select_closed_tasks(time_frame)
        if success:
            self._populate_tasks(df, self.widgets["completed_list"], self.completed_tasks)
        else:
            QMessageBox.warning(
                self, "Error", f"Failed to query completed tasks: {message}"
            )

    # ------------------------------------------------------------------------------------------

    def _populate_tasks(self, df, list_widget, task_dict):
        """
        Method to populate a list widget with tasks from a DataFrame and update a
        corresponding task dictionary.
        """
        list_widget.clear()
        task_dict.clear()
        for idx, row in enumerate(df.iterrows(), start=1):
            task_id = row[1]["task_id"]
            task = row[1]["task"]
            list_widget.addItem(f"{idx}. {task}")
            task_dict[idx] = task_id


# ==========================================================================================
# ==========================================================================================
# eof
