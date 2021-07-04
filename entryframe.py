import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
from hotkeyentry import HotkeyEntry
from pynput.keyboard import HotKey

class EntryFrame(tk.Toplevel):

    def __init__(self, master=None, filename=None, hotkeys=None, iid=None):
        super().__init__(master)
        self.master = master
        self.iid = iid
        self.setup_variables(filename, hotkeys)
        self.setup_widgets()
        self.setup_binds()
    
    def setup_variables(self, filename=None, hotkeys=None):
        if not filename:
            filename = 'None Selected'
        if not hotkeys:
            hotkeys = ''
        self.filename_var = tk.StringVar(self, filename, 'filename')
        self.hotkey_var = tk.StringVar(self, hotkeys, 'hotkey_var')

    def setup_widgets(self):
        # Create new window
        self.geometry('500x170')
        self.resizable(width=False, height=False)
        self.grab_set()
        self.focus_force()
        popup_frame = tk.Frame(self)
        popup_frame.pack(padx=10, pady=10, fill='both')
        popup_frame.columnconfigure(0, weight=1)

        # Browse for file
        file_frame = tk.Frame(popup_frame)
        file_frame.grid(column=0, row=0, sticky='w')
        browse_frame = tk.Frame(file_frame)
        browse_frame.grid(column=0, row=0, sticky='w')
        tk.Label(browse_frame, text='Sound clip:').pack(side='left',pady=5)
        tk.Button(browse_frame, text='Select', command=self.browse_files).pack(side='left')
        filename_label = tk.Label(file_frame, textvariable=self.filename_var)
        filename_label.grid(column=0, row=1, sticky='w')
        ttk.Separator(popup_frame, orient='horizontal').grid(column=0, row=1, sticky='ew', pady=5)

        # Hotkeys
        hotkey_frame = tk.Frame(popup_frame)
        hotkey_frame.columnconfigure(0, weight=1)
        hotkey_frame.grid(column=0, row=2, sticky='we')
        tk.Label(hotkey_frame, text='HotKeys:').grid(column=0, row=0, sticky='w')
        self.hotkey_entry = HotkeyEntry(hotkey_frame, textvariable=self.hotkey_var)
        self.hotkey_entry.grid(column=0, row=1, sticky='we')
        tk.Label(hotkey_frame, text='* Right-click to clear hotkeys').grid(column=0, row=2, sticky='w')

        # Done button
        done = tk.Button(popup_frame, text='Done', command=self.submit)
        done.grid(column=0, row=3, sticky='se')
    
    def setup_binds(self):
        self.bind('<Return>', lambda x: self.submit())
        self.bind('<ButtonRelease-1>', lambda x: self.hotkey_entry.stop())
        self.bind('<ButtonRelease-3>', lambda x: self.hotkey_entry.stop())

    def browse_files(self):
        filenames = filedialog.askopenfilenames()
        if len(filenames) == 1:
            self.filename_var.set(filenames[0])
        elif len(filenames) > 1:
            for file in filenames:
                self.master.add_entry(file)
            self.destroy()
    
    def submit(self):
        self.hotkey_entry.stop()
        filename = self.filename_var.get()
        hotkeys_str = self.hotkey_var.get()
        hotkey = HotKey(self.hotkey_entry.keys_stored, None)
        if self.iid:
            self.master.edit_entry(self.iid, filename, hotkeys_str, hotkey)
        elif filename and filename != 'None Selected':
            self.iid = self.master.add_entry(filename, hotkeys_str, hotkey)
        hotkey._on_activate = lambda: self.master.play_entry(self.iid)
        self.destroy()