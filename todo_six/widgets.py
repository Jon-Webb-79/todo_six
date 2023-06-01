# Import necessary packages here
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QButtonGroup,
    QCalendarWidget,
    QComboBox,
    QDate,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QPushButton,
    QRadioButton,
    QSlider,
    QWidget,
)

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


# ==========================================================================================
# ==========================================================================================
# eof
