import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog

class EntryFrame(tk.Toplevel):

    def __init__(self, master=None, filename=None, hotkeys=None):
        super().__init__(master)
        self.master = master
        self.setup_widgets()
    
    def setup_widgets(self):
        # Create new window
        self.geometry('500x170')
        self.resizable(width=False, height=False)
        self.grab_set()
        popup_frame = tk.Frame(self)
        popup_frame.pack(padx=10, pady=10, fill='both')
        popup_frame.columnconfigure(0, weight=1)

        # Browse for file
        file_frame = tk.Frame(popup_frame)
        file_frame.grid(column=0, row=0, sticky='w')
        browse_frame = tk.Frame(file_frame)
        browse_frame.grid(column=0, row=0, sticky='w')
        self.filename_var = tk.StringVar(popup_frame, 'None Selected', 'filename')
        tk.Label(browse_frame, text='Sound clip:').pack(side='left',pady=5)
        tk.Button(browse_frame, text='Select', command=self.browse_files).pack(side='left')
        filename_label = tk.Label(file_frame, textvariable=self.filename_var)
        filename_label.grid(column=0, row=1, sticky='w')
        ttk.Separator(popup_frame, orient='horizontal').grid(column=0, row=1, sticky='ew', pady=5)

        # Hotkeys
        hotkey_frame = tk.Frame(popup_frame)
        hotkey_frame.columnconfigure(0, weight=1)
        hotkey_frame.grid(column=0, row=2, sticky='we')
        hotkey_var = tk.StringVar(self, '', 'hotkey_var')
        tk.Label(hotkey_frame, text='HotKeys:').grid(column=0, row=0, sticky='w')
        tk.Entry(hotkey_frame, state='disabled', textvariable=hotkey_var).grid(column=0, row=1, sticky='we')
        tk.Label(hotkey_frame, text='* Right-click to clear hotkeys').grid(column=0, row=2, sticky='w')

        # Done button
        tk.Button(popup_frame, text='Done', command=self.submit_new).grid(column=0, row=3, sticky='se')
    
    def browse_files(self):
        filenames = filedialog.askopenfilenames()
        if len(filenames) == 1:
            self.filename_var.set(filenames[0])
        elif len(filenames) > 1:
            for file in filenames:
                self.master.add_to_table(file)
            self.destroy()
    
    def submit_new(self):
        filename = self.filename_var.get()
        if filename and filename != 'None Selected':
            self.master.add_to_table(filename)
        self.destroy()