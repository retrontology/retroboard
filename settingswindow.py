import tkinter as tk
from pynput import keyboard
from hotkeyentry import HotkeyEntry

DEFAULT_STOP = set([keyboard.Key.pause])

class SettingsWindow(tk.Toplevel):
    
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.minsize(500,300)
        self.setup_widgets()

    def setup_widgets(self):
        # Top Level Frame
        topframe = tk.Frame(self)
        topframe.pack(fill='both', expand=True, padx=10, pady=10)
        topframe.columnconfigure(0, weight=1)
    
        # Hotkey Settings
        hotkey_frame = tk.Frame(topframe)
        hotkey_frame.grid(column=0, row=0, sticky='nesw')
        hotkey_frame.columnconfigure(0, weight=2)
        hotkey_frame.columnconfigure(1, weight=1)
        tk.Label(hotkey_frame, text="'Stop All Sounds' hotkey:", justify='left').grid(column=0, row=0, sticky='w', padx=5, pady=5)
        self.stopall = HotkeyEntry(hotkey_frame, clearable=False, stored=DEFAULT_STOP, textvariable=self.master.stopall_var)
        self.stopall.grid(column=1, row=0, sticky='ew', padx=5, pady=5)

