$build_dirs = @('bin', 'build', 'dist', 'include', 'Include', 'lib', 'lib64', 'Lib', 'Lib64', 'Scripts', 'share')
for($i=0; $i -lt $build_dirs.length; $i++)
{
    if (Test-Path -Path $build_dirs[$i])
    {
        rm -r -Force $build_dirs[$i]
    }
}
python -m venv .
. .\Scripts\Activate.ps1
pip install -r requirements.txt
pip install pyinstaller
pyinstaller -y --clean --onefile --noconsole --collect-binaries av --add-data "icon\RB.png;icon" --icon icon\RB.ico retroboard.py
#pip install nuitka zstandard
#python -m nuitka --onefile --mingw64 --remove-output --assume-yes-for-downloads --follow-imports --plugin-enable=tk-inter --plugin-enable=numpy --include-package pynput --include-package av --include-package-data av --include-data-file=lib\site-packages\_sounddevice_data\portaudio-binaries\libportaudio64bit.dll=_sounddevice_data\portaudio-binaries\ --include-data-file=icon\RB.png=icon\RB.png --windows-icon-from-ico=icon\RB.ico retroboard.py
#--windows-disable-console 