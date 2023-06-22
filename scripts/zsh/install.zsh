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
	if [ ! -f ~/.icons/todo.png ]; then
		rm ~/.icons/todo.png
	fi
    cp data/icon.png ~/.icons/todo.png

	# Check to see if todo.desktop already exists
	if [ -f ~/.local/share/applications/todo.desktop ]; then
		rm ~/.local/share/applications/todo.desktop
	fi

	# Copy scripts/zsh/todo.desktop to ~/.local/share/applications/todo.desktop
	cp scripts/zsh/todo.desktop ~/.local/share/applications/todo.desktop
	exec_path=$HOME"/bin/todo"
	icon_path=$HOME"/.icons/todo.png"

	sed -i "s|^Exec=.*|Exec=$exec_path|" ~/.local/share/applications/todo.desktop

	sed -i "s|^Icon=.*|Icon=$icon_path|" ~/.local/share/applications/todo.desktop

elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Detected OS: macOS"
    cp data/icon.icns todo.icns
    ICONFILE=todo.icns
elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "Detected OS: Windows"
    cp data/icon.ico todo.ico
    ICONFILE=todo.ico
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
    todo.py
fi

if [[ "$OSTYPE" == "darwin"* ]]; then
	cp -R dist/todo.app ~/Applications
fi

# Return control
echo "Returning to scripts/zsh directory"
cd scripts/zsh
