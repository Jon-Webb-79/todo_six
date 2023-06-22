#!/usr/bin/zsh

# Navigate to correct directory
echo "Changing to base directory"
cd ../..

# Detect OS and copy the appropriate icon file
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Detected OS: Linux"
	if [ ! -d ~/.icons ]; then
		mkdir -p ~/.icons
	fi
    cp data/icon.png ~/.icons/todo.png

	# Check to see if todo.desktop already exists
	if [ -f ~/.local/share/applications/todo.desktop ]; then
		rm ~/.local/share/applications/todo.desktop
	fi

	# Copy scripts/zsh/todo.desktop to ~/.local/share/applications/todo.desktop
	cp scripts/zsh/todo.desktop ~/.local/share/applications/todo.desktop

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
echo "Providing execute privledges to PyQt libraries"
chmod +x .venv/lib/python3.11/site-packages/PyQt6/QtSql.abi3.so
chmod +x .venv/lib/python3.11/site-packages/PyQt6/QtDBus.abi3.so
chmod +x .venv/lib/python3.11/site-packages/PyQt6/QtWidgets.abi3.so
chmod +x .venv/lib/python3.11/site-packages/PyQt6/QtGui.abi3.so
chmod +x .venv/lib/python3.11/site-packages/PyQt6/QtCore.abi3.so

echo "Initiating executable installation"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Call PyInstaller without the -i option on Linux
    pyinstaller -F -w \
    --add-data "todo_six:todo_six" \
    --hidden-import "jinja2" \
    --add-data "data/style_sheets/day.qss:data/style_sheets" \
    --add-data "data/style_sheets/night.qss:data/style_sheets" \
    --add-binary=".venv/lib/python3.11/site-packages/numpy.libs/libquadmath-96973f99.so.0.0.0:." \
    --add-binary=".venv/lib/python3.11/site-packages/numpy.libs/libgfortran-040039e1.so.5.0.0:." \
    todo.py
	if [ ! -d ~/bin ]; then
		mkdir -p ~/bin
	fi
	cp dist/todo ~/bin/todo
	update-desktop-database ~/.local/share/applications
else
    pyinstaller -F -w -i $ICONFILE \
    --add-data "todo_six:todo_six" \
    --hidden-import "jinja2" \
    --add-data "data/style_sheets/day.qss:data/style_sheets" \
    --add-data "data/style_sheets/night.qss:data/style_sheets" \
    --add-binary=".venv/lib/python3.11/site-packages/numpy.libs/libquadmath-96973f99.so.0.0.0:." \
	--add-binary=".venv/lib/python3.11/site-packages/numpy.libs/libgfortran-040039e1.so.5.0.0:." \
    todo.py

# Return control
echo "Returning to scripts/zsh directory"
cd scripts/zsh
