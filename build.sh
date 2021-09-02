#!/bin/bash

export TK_LIBRARY=/usr/lib/tk8.6
export TCL_LIBRARY=/usr/lib/tcl8.6

python -m venv .
source bin/activate
pip install -r requirements.txt
pip install pyinstaller
pyinstaller -y --clean --onefile --noconsole --add-data "icon/RB.png:icon" --icon icon/RB.xpm retroboard.py
#pip install nuitka
#python -m nuitka --onefile --remove-output --assume-yes-for-downloads --follow-imports --plugin-enable=tk-inter --plugin-enable=numpy --include-package pynput --include-package Xlib --include-data-file=icon/RB.png=icon/RB.png --linux-onefile-icon=icon/RB.xpm retroboard.py