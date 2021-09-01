python -m venv .
. .\Scripts\Activate.ps1
pip install -r requirements.txt
pip install pyinstaller
pyinstaller -y --clean --onefile --noconsole --add-data "icon\RB.png;icon" --icon icon\RB.ico retroboard.py
# --noconsole
#pip install nuitka zstandard
#python -m nuitka --onefile --mingw64 --remove-output --assume-yes-for-downloads --follow-imports --plugin-enable=tk-inter --plugin-enable=numpy --include-package pynput --include-package av --include-package-data av --include-data-file=lib\site-packages\_sounddevice_data\portaudio-binaries\libportaudio64bit.dll=_sounddevice_data\portaudio-binaries\ --include-data-file=icon\RB.png=icon\RB.png --windows-icon-from-ico=icon\RB.ico retroboard.py
#--windows-disable-console 