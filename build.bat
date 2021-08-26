python -m venv .
.\Scripts\activate
pip install -r requirements.txt
pip install nuitka zstandard
python -m nuitka --onefile --mingw64 --windows-disable-console --remove-output --assume-yes-for-downloads --follow-imports --plugin-enable=tk-inter --plugin-enable=numpy --include-package pynput --include-data-file=lib\site-packages\_sounddevice_data\portaudio-binaries\libportaudio64bit.dll=_sounddevice_data/portaudio-binaries/ --include-data-file=icon/RB.png=icon/RB.png --windows-icon-from-ico=icon/RB.ico retroboard.py
