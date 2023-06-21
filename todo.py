# Import necessary packages here
import os
import sys

from todo_six.main import main

# ==========================================================================================
# ==========================================================================================

# File:    todo.py
# Date:    June 15, 2023
# Author:  Jonathan A. Webb
# Purpose: This file calls the high-level functions necessary to operate the todo_six
#          software package
# ==========================================================================================
# ==========================================================================================
# Insert Code here


if getattr(sys, "frozen", False):
    # If the application is run as a bundle (pyinstaller)
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

day = os.path.join(application_path, "data/style_sheets/day.qss")
night = os.path.join(application_path, "data/style_sheets/night.qss")

if __name__ == "__main__":
    main(day, night)
# ==========================================================================================
# ==========================================================================================
# eof
