# retroboard

## THIS BRANCH IS NOT STABLE AT THE MOMENT

## Description
Python recreation of EXP Soundboard. It uses pydub (with ffmpeg) to read the audio files, sounddevice (python PortAudio bindings) to play them, and pynput for the hotkeys.

## Requirements
Requires ffmpeg if audio is a format other than WAV or RAW. The python requirements are listed in ```requirements.txt```

## Installation
### Clone the repo
```
git clone https://github.com/retrontology/retroboard
```
### Install the requirements

```
cd retroboard
python -m pip install -r requirements.txt
```
## Runing the Program
```
python retroboard.py
```