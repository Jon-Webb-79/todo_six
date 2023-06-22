@echo off
REM ==========================================================================================
REM ==========================================================================================

REM File:    install.cmd
REM Date:    June 22, 2023
REM Author:  Jonathan A. Webb
REM Purpose: This file contains a batch script that will install the todo executable on a PC
REM ==========================================================================================
REM ==========================================================================================
REM Navigate to correct directory
echo Changing to base directory
cd ..

REM ==========================================================================================
REM Copy the appropriate icon file
echo Detected OS: Windows
copy data\icon.ico todo.ico

REM Check if the directory already exists
IF EXIST "C:\Program Files\todo" (
    echo Installation directory "C:\Program Files\todo" already exists. Skipping directory creation.
) ELSE (
    echo Creating installation directory: "C:\Program Files\todo"
    mkdir "C:\Program Files\todo"
)

REM Check if the file already exists
IF EXIST "C:\Program Files\todo\todo.exe" (
    echo Existing executable found in installation directory. Removing previous file.
    del "C:\Program Files\todo\todo.exe"
)

REM Copy the executable to the installation directory
copy dist/todo.exe "C:\todo\todo.exe"

REM ==========================================================================================
REM Determine if a virtual environment is active
IF DEFINED VIRTUAL_ENV (
    echo Virtual environment is already active: %VIRTUAL_ENV%
) ELSE (
    REM Specify the path to your virtual environment
    set "VENV_PATH=.venv"

    REM Activate the virtual environment
    call "%VENV_PATH%\Scripts\activate.bat"
    echo Activated virtual environment: %VIRTUAL_ENV%
)

REM ==========================================================================================
REM Ensure permissions to PyQt files
echo Providing execute privileges to PyQt libraries
attrib +x .venv\Lib\site-packages\PyQt6\QtSql.abi3.so
attrib +x .venv\Lib\site-packages\PyQt6\QtDBus.abi3.so
attrib +x .venv\Lib\site-packages\PyQt6\QtWidgets.abi3.so
attrib +x .venv\Lib\site-packages\PyQt6\QtGui.abi3.so
attrib +x .venv\Lib\site-packages\PyQt6\QtCore.abi3.so

REM ==========================================================================================
REM Return control
echo Returning to scripts\zsh directory
cd scripts\zsh
