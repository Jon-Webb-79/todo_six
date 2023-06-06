# Import necessary packages here
import pytest
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QLineEdit, QListWidgetItem

from todo_six.widgets import (
    Calendar,
    DayNightRadioButton,
    DropDownMenu,
    LineEdit,
    ListWidget,
    OpacitySlider,
    PushButton,
)

# ==========================================================================================
# ==========================================================================================
# File:    test.py
# Date:    June 01, 2023
# Author:  Jonathan A. Webb
# Purpose: This file tests the methods and classes in the widgets.py file
# Instruction: This code can be run in hte following ways
#              - pytest # runs all functions beginnning with the word test in the
#                         directory
#              - pytest file_name.py # Runs all functions in file_name beginning
#                                      with the word test
#              - pytest file_name.py::test_func_name # Runs only the function
#                                                      titled test_func_name in
#                                                      the file_name.py file
#              - pytest -s # Runs tests and displays when a specific file
#                            has completed testing, and what functions failed.
#                            Also displays print statments
#              - pytest -v # Displays test results on a function by function
#              - pytest -p no:warnings # Runs tests and does not display warning
#                          messages
#              - pytest -s -v -p no:warnings # Displays relevant information and
#                                supports debugging
#              - pytest -s -p no:warnings # Run for record
# ==========================================================================================
# ==========================================================================================
# Insert Code here


@pytest.fixture(scope="module")
def app():
    return QApplication([])


# ==========================================================================================
# ==========================================================================================
# Test DayNightRadioButton


@pytest.fixture
def widget(app):  # Pass the app fixture as a parameter to ensure it's created first
    return DayNightRadioButton()


# ------------------------------------------------------------------------------------------


@pytest.mark.daynightradiobutton
def test_daynight_creation(widget):
    """
    Test whether the widget is created properly
    """
    assert widget.day_button is not None
    assert widget.night_button is not None


# ------------------------------------------------------------------------------------------


@pytest.mark.daynightradiobutton
def test_default(widget):
    """
    Test whether the Day button is selected by default
    """
    assert widget.day_button.isChecked()
    assert not widget.night_button.isChecked()


# ------------------------------------------------------------------------------------------


@pytest.mark.daynightradiobutton
def test_select_night(widget):
    """
    Test whether the Night button can be selected
    """
    widget.night_button.setChecked(True)
    assert not widget.day_button.isChecked()
    assert widget.night_button.isChecked()


# ------------------------------------------------------------------------------------------


@pytest.mark.daynightradiobutton
def test_select_day(widget):
    """
    Test whether the Day button can be selected
    """
    widget.night_button.setChecked(True)  # Select night
    widget.day_button.setChecked(True)  # Select day
    assert widget.day_button.isChecked()
    assert not widget.night_button.isChecked()


# ==========================================================================================
# ==========================================================================================
# Test DropDownMenu class


@pytest.fixture
def dropdown(app):
    options = ["Option1", "Option2", "Option3"]
    return DropDownMenu(options)


# ------------------------------------------------------------------------------------------


@pytest.mark.dropdownmenu
def test_dropdown_creation(dropdown):
    """
    Test whether the widget is created properly
    """
    assert dropdown.count() == 3  # We should have 3 options


# ------------------------------------------------------------------------------------------


@pytest.mark.dropdownmenu
def test_default_selection(dropdown):
    """
    Test whether the first item is selected by default
    """
    assert dropdown.currentText() == "Option1"


# ------------------------------------------------------------------------------------------


@pytest.mark.dropdownmenu
def test_select_option(dropdown):
    """
    Test whether a specific option can be selected
    """
    dropdown.set_selected_option("Option2")
    assert dropdown.currentText() == "Option2"


# ------------------------------------------------------------------------------------------


@pytest.mark.dropdownmenu
def test_get_selected_option(dropdown):
    """
    Test whether the correct selected option is returned
    """
    dropdown.set_selected_option("Option3")
    assert dropdown.get_selected_option() == "Option3"


# ------------------------------------------------------------------------------------------


@pytest.mark.dropdownmenu
def test_select_invalid_option(dropdown):
    """
    Test the behavior when an invalid option is selected
    """
    dropdown.set_selected_option("InvalidOption")
    assert dropdown.currentText() != "InvalidOption"


# ==========================================================================================
# ==========================================================================================
# Test LineEdit class


@pytest.fixture
def line_edit(app):
    font = QFont("Arial", 14)
    return LineEdit(font)


# ------------------------------------------------------------------------------------------


@pytest.mark.lineedit
def test_lineedit_creation(line_edit):
    """
    Test whether the LineEdit widget is created properly
    """
    assert isinstance(line_edit, QLineEdit)
    assert line_edit.text() == ""


# ------------------------------------------------------------------------------------------


@pytest.mark.lineedit
def test_font(line_edit):
    """
    Test the font of the LineEdit widget
    """
    font = line_edit.font()
    assert font.family() == "Arial"
    assert font.pointSize() == 14


# ------------------------------------------------------------------------------------------


@pytest.mark.lineedit
def test_set_text(line_edit):
    """
    Test setting text on the LineEdit widget
    """
    line_edit.setText("Testing")
    assert line_edit.text() == "Testing"


# ------------------------------------------------------------------------------------------


@pytest.mark.lineedit
def test_clear_text(line_edit):
    """
    Test clearing text on the LineEdit widget
    """
    line_edit.setText("Testing")
    line_edit.clear()
    assert line_edit.text() == ""


# ==========================================================================================
# ==========================================================================================
# Test ListWidget class


@pytest.fixture
def list_widget(app):
    font = QFont("Arial", 14)
    return ListWidget(font)


# ------------------------------------------------------------------------------------------


@pytest.mark.listwidget
def test_listwidget_creation(list_widget):
    """
    Test whether the ListWidget is created properly
    """
    assert list_widget.count() == 0  # Initially, there should be no items in the list


# ------------------------------------------------------------------------------------------


@pytest.mark.listwidget
def test_listwidget_font(list_widget):
    """
    Test the font of the ListWidget
    """
    font = list_widget.font()
    assert font.family() == "Arial"
    assert font.pointSize() == 14


# ------------------------------------------------------------------------------------------


@pytest.mark.listwidget
def test_add_item(list_widget):
    """
    Test adding an item to the ListWidget
    """
    item = QListWidgetItem("Item 1")
    list_widget.addItem(item)
    assert list_widget.count() == 1  # Now there should be one item in the list
    assert list_widget.item(0).text() == "Item 1"  # And its text should be 'Item 1'


# ------------------------------------------------------------------------------------------


@pytest.mark.listwidget
def test_remove_item(list_widget):
    """
    Test removing an item from the ListWidget
    """
    item = QListWidgetItem("Item 2")
    list_widget.addItem(item)
    item = QListWidgetItem("Item 3")
    list_widget.addItem(item)
    assert list_widget.count() == 2  # Now there should be two items in the list
    list_widget.takeItem(1)  # Remove the second item
    assert list_widget.count() == 1  # Now there should be one item in the list


# ==========================================================================================
# ==========================================================================================
# Test OpacitySlider class


@pytest.fixture
def opacity_slider(app):
    return OpacitySlider()


# ------------------------------------------------------------------------------------------


@pytest.mark.opacityslider
def test_opacityslider_creation(opacity_slider):
    """
    Test whether the OpacitySlider widget is created properly
    """
    assert opacity_slider.slider.value() == 100  # Initial value should be 100
    assert opacity_slider.label.text() == "Opacity: 100"


# ------------------------------------------------------------------------------------------


@pytest.mark.opacityslider
def test_set_value(opacity_slider):
    """
    Test setting a value on the OpacitySlider widget
    """
    opacity_slider.slider.setValue(80)  # Change the value to 80
    assert opacity_slider.slider.value() == 80  # The slider value should now be 80
    assert (
        opacity_slider.label.text() == "Opacity: 80"
    )  # Label should reflect the new value


# ------------------------------------------------------------------------------------------


@pytest.mark.opacityslider
def test_update_label(opacity_slider):
    """
    Test the update_label method of the OpacitySlider widget
    """
    opacity_slider.update_label(50)  # Update the label with a value of 50
    assert opacity_slider.label.text() == "Opacity: 50"


# ------------------------------------------------------------------------------------------


@pytest.mark.opacityslider
def test_update_opacity(opacity_slider):
    """
    Test the update_opacity method of the OpacitySlider widget
    """
    opacity_slider.set_opacity(50)  # Update the opacity to 0.5
    assert opacity_slider.slider.value() == 50  # The slider value should now be 50
    assert opacity_slider.label.text() == "Opacity: 50"


# ==========================================================================================
# ==========================================================================================
# Test PushButton class


@pytest.fixture
def push_button(app):
    return PushButton("test text", QFont("Arial", 12), True)


# ------------------------------------------------------------------------------------------


@pytest.mark.pushbutton
def test_button_text(push_button):
    """
    Test if button text is correctly set
    """
    assert push_button.text() == "test text"


# ------------------------------------------------------------------------------------------


@pytest.mark.pushbutton
def test_button_font(push_button):
    """
    Test if button font is correctly set
    """
    assert push_button.font().family() == "Arial"
    assert push_button.font().pointSize() == 12


# ------------------------------------------------------------------------------------------


@pytest.mark.pushbutton
def test_button_enabled(push_button):
    """
    Test if button enabled status is correctly set
    """
    assert push_button.isEnabled()


# ==========================================================================================
# ==========================================================================================
# Test Calendar class


@pytest.fixture
def calendar(app):
    start_date = QDate(2023, 1, 1)
    end_date = QDate(2024, 12, 31)
    return Calendar(start_date, end_date, True, True)


# ------------------------------------------------------------------------------------------


@pytest.mark.calendar
def test_selected_date(calendar):
    """
    Test the get_selected_date and set_selected_date methods of the Calendar widget
    """
    new_date = QDate(2023, 6, 4)

    # Verify the initial selected date
    assert calendar.get_selected_date() == QDate.currentDate()

    # Set the selected date to a new value
    calendar.set_selected_date(new_date)

    # Verify the new selected date
    assert calendar.get_selected_date() == new_date


# ==========================================================================================
# ==========================================================================================
# eof
