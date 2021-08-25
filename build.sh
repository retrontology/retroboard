set TK_LIBRARY=/usr/lib/tk8.6
set TCL_LIBRARY=/usr/lib/tcl8.6

python -m venv .
source bin/activate
pip install -r requirements.txt
pip install nuitka
python -m nuitka --onefile --follow-imports --plugin-enable=tk-inter --plugin-enable=numpy --linux-onefile-icon=RB.ico retroboard.py
