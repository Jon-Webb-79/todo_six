#!/usr/bin/zsh

# Navigate to correct directory
cd ../..

# Detect OS and copy the appropriate icon file
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Detected OS: Linux"
    cp data/icon.png icon.png
    ICONFILE=icon.png
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Detected OS: macOS"
    cp data/icon.icns icon.icns
    ICONFILE=icon.icns
elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "Detected OS: Windows"
    cp data/icon.ico icon.ico
    ICONFILE=icon.ico
else
    echo "Unsupported OS detected, cannot copy the icon file"
fi

# Determine if a virtual environment is active
if [[ -n "$VIRTUAL_ENV" ]]; then
    echo "Virtual environment is already active: $VIRTUAL_ENV"
else
    # Specify the path to your virtual environment
    VENV_PATH=".venv"

    # Activate the virtual environment
    source "$VENV_PATH/bin/activate"
    echo "Activated virtual environment: $VIRTUAL_ENV"
fi

# Ensure permissions to PyQt files
chmod +x .venv/lib/python3.11/site-packages/PyQt6/QtSql.abi3.so
chmod +x .venv/lib/python3.11/site-packages/PyQt6/QtDBus.abi3.so
chmod +x .venv/lib/python3.11/site-packages/PyQt6/QtWidgets.abi3.so
chmod +x .venv/lib/python3.11/site-packages/PyQt6/QtGui.abi3.so
chmod +x .venv/lib/python3.11/site-packages/PyQt6/QtCore.abi3.so

pyinstaller -F -w -i $ICONFILE \
--add-data "todo_six:todo_six" \
--hidden-import "jinja2" \
--add-binary=".venv/lib/python3.11/site-packages/numpy.libs/libquadmath-96973f99.so.0.0.0:." \
--add-binary=".venv/lib/python3.11/site-packages/numpy.libs/libgfortran-040039e1.so.5.0.0:." \
todo.py

# Transform to executable
#pyinstaller -F -w -i $ICONFILE --add-data "todo_six:todo_six" todo.py

# Return control
cd scripts/zsh

# # Navigate to correct directory
# cd ../..

# # Download ico file
# cp data/icon.ico icon.ico

# # Deterimine if a virtual environment is active
# if [[ -n "$VIRTUAL_ENV" ]]; then
#     echo "Virtual environment is already active: $VIRTUAL_ENV"
# else
#     # Specify the path to your virtual environment
#     VENV_PATH=".venv"

#     # Activate the virtual environment
#     source "$VENV_PATH/bin/activate"
#     echo "Activated virtual environment: $VIRTUAL_ENV"
# fi

# # Ensure permissions to PyQt files
# chmod +x .venv/lib/python3.11/site-packages/PyQt6/QtSql.abi3.so
# chmod +x .venv/lib/python3.11/site-packages/PyQt6/QtDBus.abi3.so
# chmod +x .venv/lib/python3.11/site-packages/PyQt6/QtWidgets.abi3.so
# chmod +x .venv/lib/python3.11/site-packages/PyQt6/QtGui.abi3.so
# chmod +x .venv/lib/python3.11/site-packages/PyQt6/QtCore.abi3.so

# pyinstaller -F -w -i icon.ico \
# --add-data "todo_six:todo_six" \
# --hidden-import "jinja2" \
# --add-binary=".venv/lib/python3.11/site-packages/numpy.libs/libquadmath-96973f99.so.0.0.0:." \
# --add-binary=".venv/lib/python3.11/site-packages/numpy.libs/libgfortran-040039e1.so.5.0.0:." \
# todo.py

# # Return control
# cd scripts/zsh
