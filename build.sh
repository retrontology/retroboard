#!/bin/bash

export TK_LIBRARY=/usr/lib/tk8.6
export TCL_LIBRARY=/usr/lib/tcl8.6

declare -a build_dirs=('bin' 'build' 'dist' 'include' 'Include' 'lib' 'lib64' 'Lib' 'Lib64' 'Scripts' 'share')

for i in "${build_dirs[@]}"
do
    if [ -d "$i" ]; then
        rm -r "$i"
    fi
done

python -m venv .
source bin/activate
pip install -r requirements.txt
pip install pyinstaller
pyinstaller -y --clean --onefile --noconsole --collect-binaries av --add-data "icon/RB.png:icon" --icon icon/RB.xpm retroboard.py
#pip install nuitka
#python -m nuitka --onefile --remove-output --assume-yes-for-downloads --follow-imports --plugin-enable=tk-inter --plugin-enable=numpy --include-package pynput --include-package Xlib --include-data-file=icon/RB.png=icon/RB.png --linux-onefile-icon=icon/RB.xpm retroboard.py