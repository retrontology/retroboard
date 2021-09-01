import tkinter as tk
from hotkeyentry import HotkeyEntry
from hotkeylistener import HotkeyScope

class SettingsWindow(tk.Toplevel):
    
    def __init__(self, master=None):
        super().__init__(master)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.master = master
        self.minsize(450,80)
        self.setup_widgets()
        self.resizable(False, False)
        self.focus()

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
        # Stop All
        tk.Label(hotkey_frame, text="'Stop All Sounds' hotkey(s):", justify='left').grid(column=0, row=0, sticky='w')
        self.stopall = HotkeyEntry(hotkey_frame, clearable=False, stored=self.master.hotkey_listener.get_hotkey('stop_all', HotkeyScope.GLOBAL)._keys, stop_callback=lambda x: self.bind_global_hotkey('stop_all', x, self.master.stop_all), textvariable=self.master.stopall_var)
        self.stopall.grid(column=1, row=0, sticky='ew')
        self.stopall.bind('<Button>', lambda x: self.stop_other_entries(self.stopall), '+')
        # Push To Talk
        tk.Label(hotkey_frame, text="VoIP 'Push To Talk' enabled:", justify='left').grid(column=0, row=1, sticky='w')
        self.ptt_enable = tk.Checkbutton(hotkey_frame, variable=self.master.ptt_enable_var, command=self.master.toggle_ptt_enable)
        self.ptt_enable.grid(column=1, row=1, sticky='w')
        self.master.toggle_ptt_enable()
        tk.Label(hotkey_frame, text="VoIP 'Push To Talk' hotkey(s):", justify='left').grid(column=0, row=2, sticky='w')
        self.ptt = HotkeyEntry(hotkey_frame, clearable=True, stored=self.master.hotkey_listener.get_hotkey('ptt', HotkeyScope.GLOBAL)._keys, stop_callback=lambda x: self.bind_global_hotkey('ptt', x, None), textvariable=self.master.ptt_var)
        self.ptt.grid(column=1, row=2, sticky='ew')
        self.ptt.bind('<Button>', lambda x: self.stop_other_entries(self.ptt), '+')

    def stop_other_entries(self, selected):
        for entry in {self.ptt, self.stopall}:
            if entry is not selected:
                entry.stop()

    def bind_global_hotkey(self, index, hkentry:HotkeyEntry, command):
        hotkey = hkentry.get_hotkey(command)
        self.master.hotkey_listener.set_hotkey(index, hotkey, HotkeyScope.GLOBAL)
        self.master.prefs[index] = hotkey._keys
    
    def on_closing(self):
        self.stopall.stop()
        self.ptt.stop()
        self.destroy()
        self.master.settings_window = None
