import tkinter as tk
from tkinter import ttk
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
        self.hotkey_entries = set()
        hotkey_row_index = 0

        # Pause All
        tk.Label(hotkey_frame, text="'Pause/Resume All Sounds' hotkey(s):", justify='left').grid(column=0, row=hotkey_row_index, sticky='w')
        self.pause_all = HotkeyEntry(hotkey_frame, clearable=True, stored=self.master.hotkey_listener.get_hotkey('pause_all_hotkey', HotkeyScope.SETTINGS), stop_callback=lambda x: self.bind_global_hotkey('pause_all_hotkey', x, self.master.pause_all_toggle), textvariable=self.master.pause_all_var)
        self.pause_all.grid(column=1, row=hotkey_row_index, sticky='ew')
        self.pause_all.bind('<Button>', lambda x: self.stop_other_entries(self.pause_all), '+')
        self.hotkey_entries.add(self.pause_all)
        hotkey_row_index += 1

        # Stop All
        tk.Label(hotkey_frame, text="'Stop All Sounds' hotkey(s):", justify='left').grid(column=0, row=hotkey_row_index, sticky='w')
        self.stopall = HotkeyEntry(hotkey_frame, clearable=True, stored=self.master.hotkey_listener.get_hotkey('stop_all', HotkeyScope.SETTINGS), stop_callback=lambda x: self.bind_global_hotkey('stop_all', x, self.master.stop_all), textvariable=self.master.stopall_var)
        self.stopall.grid(column=1, row=hotkey_row_index, sticky='ew')
        self.stopall.bind('<Button>', lambda x: self.stop_other_entries(self.stopall), '+')
        self.hotkey_entries.add(self.stopall)
        hotkey_row_index += 1

        ttk.Separator(hotkey_frame, orient='horizontal').grid(column=0, columnspan=2, row=hotkey_row_index, sticky='ew', pady=5)
        hotkey_row_index += 1

        # Push To Talk
        tk.Label(hotkey_frame, text="VoIP 'Push To Talk' enabled:", justify='left').grid(column=0, row=hotkey_row_index, sticky='w')
        self.ptt_enable = tk.Checkbutton(hotkey_frame, variable=self.master.ptt_enable_var, command=self.master.toggle_ptt_enable)
        self.ptt_enable.grid(column=1, row=hotkey_row_index, sticky='w')
        hotkey_row_index += 1
        tk.Label(hotkey_frame, text="VoIP 'Push To Talk' hotkey(s):", justify='left').grid(column=0, row=hotkey_row_index, sticky='w')
        self.ptt = HotkeyEntry(hotkey_frame, clearable=True, stored=self.master.hotkey_listener.get_hotkey('ptt', HotkeyScope.SETTINGS), stop_callback=lambda x: self.bind_global_hotkey('ptt', x, None), textvariable=self.master.ptt_var)
        self.ptt.grid(column=1, row=hotkey_row_index, sticky='ew')
        self.ptt.bind('<Button>', lambda x: self.stop_other_entries(self.ptt), '+')
        self.hotkey_entries.add(self.ptt)
        hotkey_row_index += 1

        ttk.Separator(hotkey_frame, orient='horizontal').grid(column=0, columnspan=2, row=hotkey_row_index, sticky='ew', pady=5)
        hotkey_row_index += 1

        # Overlap
        tk.Label(hotkey_frame, text="Overlap Same File:", justify='left').grid(column=0, row=hotkey_row_index, sticky='w')
        self.overlap_enable = tk.Checkbutton(hotkey_frame, variable=self.master.overlap, command=lambda: self.master.prefs.__setitem__('overlap', self.master.overlap.get()))
        self.overlap_enable.grid(column=1, row=hotkey_row_index, sticky='w')
        hotkey_row_index += 1
        tk.Label(hotkey_frame, text='Overlap Hotkey(s):', justify='left').grid(column=0, row=hotkey_row_index, sticky='w')
        self.overlap_hotkey = HotkeyEntry(hotkey_frame, clearable=True, stored=self.master.hotkey_listener.get_hotkey('overlap_hotkey', HotkeyScope.SETTINGS), stop_callback=lambda x:self.bind_global_hotkey('overlap_hotkey', x, self.master.toggle_overlap), textvariable=self.master.overlap_var)
        self.overlap_hotkey.grid(column=1, row=hotkey_row_index, sticky='ew')
        self.overlap_hotkey.bind('<Button>', lambda x: self.stop_other_entries(self.overlap_hotkey), '+')
        self.hotkey_entries.add(self.overlap_hotkey)
        hotkey_row_index += 1

    def stop_other_entries(self, selected):
        for entry in self.hotkey_entries:
            if entry is not selected:
                entry.stop()

    def bind_global_hotkey(self, index, hkentry:HotkeyEntry, command):
        hotkey = hkentry.get_hotkey(command)
        self.master.hotkey_listener.set_hotkey(index, hotkey, HotkeyScope.SETTINGS)
        if hotkey != None:
            self.master.prefs[index] = hotkey._keys
        else:
            self.master.prefs[index] = None
    
    def on_closing(self):
        self.stopall.stop()
        self.ptt.stop()
        self.destroy()
        self.master.settings_window = None
