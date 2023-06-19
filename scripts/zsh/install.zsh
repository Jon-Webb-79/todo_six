# Navigate to correct directory
cd ../..

# Download ico file
cp data/icon.ico icon.ico

# Deterimine if a virtual environment is active
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
chmod +x /home/jonwebb/Desktop/todo_six/.venv/lib/python3.11/site-packages/PyQt6/QtSql.abi3.so
chmod +x /home/jonwebb/Desktop/todo_six/.venv/lib/python3.11/site-packages/PyQt6/QtDBus.abi3.so
chmod +x /home/jonwebb/Desktop/todo_six/.venv/lib/python3.11/site-packages/PyQt6/QtWidgets.abi3.so
chmod +x /home/jonwebb/Desktop/todo_six/.venv/lib/python3.11/site-packages/PyQt6/QtGui.abi3.so
chmod +x /home/jonwebb/Desktop/todo_six/.venv/lib/python3.11/site-packages/PyQt6/QtCore.abi3.so

# Transform to executable
pyinstaller -F -w -i icon.ico --add-data "todo_six:todo_six" todo.py

# Return control
cd scripts/zsh
