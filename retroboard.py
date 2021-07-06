import tkinter as tk
import tkinter.filedialog as filedialog
import sounddevice
from audioentry import AudioEntry
from entrywindow import EntryWindow
from hotkeytree import HotKeyTree
from errorwindow import ErrorWindow
import os
import pickle

DEFAULT_SAVE = 'default.rbd'

class RetroBoard(tk.Tk):

    def __init__(self, master=None):
        super().__init__(master)
        self.geometry("500x600")
        self.title('retroboard')
        self.playing = []
        self.setup_widgets()
        self.setup_binds()
    
    def setup_binds(self):
        self.winfo_toplevel().bind('<Return>', self.enter_callback)

    def on_exit(self):
        self.winfo_toplevel().destroy()

    def setup_widgets(self):
        topframe = tk.Frame()
        topframe.pack(fill='both', expand=True)
        topframe.columnconfigure(0, weight=1)
        topframe.rowconfigure(0, weight=1)
        self.create_menu()
        self.create_audio_table(topframe)
        self.create_buttons(topframe)
        self.create_device_selection(topframe)

    def create_menu(self):
        # Top Level menubar
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)

        # File Menu
        file_menu = tk.Menu(self.menubar, tearoff=0)
        file_menu.add_command(label='Save As', command=self.file_save_as_callback)
        file_menu.add_command(label='Load', command=self.file_load_callback)
        file_menu.add_command(label='Exit', command=self.on_exit)
        self.menubar.add_cascade(label = "File", menu=file_menu)

    def create_audio_table(self, frame):
        # Top Level frame for table of audio clips
        table_frame = tk.Frame(frame)
        table_frame.grid(column=0, row=0, sticky='nsew', padx=8, pady=5)
        self.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        # Audio clip table
        table_headings = ['Sound Clip','HotKeys', 'path']
        self.audio_table = HotKeyTree(table_frame, show="headings", height=10, columns=table_headings, displaycolumns=table_headings[:2])
        self.audio_table.columnconfigure(0, weight=1)
        self.audio_table.columnconfigure(1, weight=1)
        self.audio_table.grid(column=0, row=0, sticky='nsew', in_=table_frame)
        for column in table_headings:
            self.audio_table.heading(column, text=column.title())

        # Scroll bar for table
        scrollbar = tk.Scrollbar(orient="vertical", command=self.audio_table.yview)
        self.audio_table.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(column=1, row=0, sticky='ns', in_=table_frame)
    
    def create_buttons(self, frame):
        # Top level button frame
        button_frame = tk.Frame(frame)
        button_frame.grid(column=0, row=1, sticky='nsew')

        # buttons that edit the table
        table_button_frame = tk.Frame(button_frame)
        table_button_frame.pack(side='left', padx=8)
        add_button = tk.Button(table_button_frame, text='Add', command=self.add_button_callback)
        add_button.grid(column=0, row=0, sticky='w', in_=table_button_frame, padx=5)
        remove_button = tk.Button(table_button_frame, text='Remove', command=self.remove_button_callback)
        remove_button.grid(column=1, row=0, sticky='w', in_=table_button_frame, padx=5)
        edit_button = tk.Button(table_button_frame, text='Edit', command=self.edit_button_callback)
        edit_button.grid(column=2, row=0, sticky='w', in_=table_button_frame, padx=5)

        # buttons for playback
        playback_button_frame = tk.Frame(button_frame)
        playback_button_frame.pack(side='right', padx=8)
        play_button = tk.Button(playback_button_frame, text='Play', command=self.play_button_callback)
        play_button.grid(column=0, row=0, sticky='w', in_=playback_button_frame, padx=8)
        stop_button = tk.Button(playback_button_frame, text='Stop All', command=self.stop_button_callback)
        stop_button.grid(column=1, row=0, sticky='w', in_=playback_button_frame, padx=8)

    def create_device_selection(self, frame):
        # Device selection frame
        device_frame = tk.Frame(frame)
        device_frame.grid(column=0, row=2, sticky='nsew', padx=8, pady=5)
        device_frame.columnconfigure(0, weight=1)
        
        # Get device info
        devices = sounddevice.query_devices()
        device_names = [x['name'] for x in devices]
        default_device = sounddevice.query_devices(kind='output')['name']

        # Primary output
        primary_device_label = tk.Label(device_frame, text='Primary Output Device')
        primary_device_label.grid(column=0, row=0, sticky='w')
        self.primary_device = tk.StringVar(self, default_device, 'primary_device')
        primary_device_menu = tk.OptionMenu(device_frame, self.primary_device, *device_names)
        primary_device_menu.grid(column=0, row=1, sticky='nsew', in_=device_frame)

        # Secondary output
        secondary_device_label = tk.Label(device_frame, text='Secondary Output Device')
        secondary_device_label.grid(column=0, row=2, sticky='w')
        self.secondary_device = tk.StringVar(self, default_device, 'secondary_device')
        secondary_device_frame = tk.Frame(device_frame)
        secondary_device_frame.columnconfigure(0, weight=1)
        secondary_device_frame.grid(column=0, row=3, sticky='nsew', in_=device_frame)
        self.secondary_device_menu = tk.OptionMenu(secondary_device_frame, self.secondary_device, *device_names)
        self.secondary_device_menu.grid(column=0, row=0, sticky='nsew')
        self.secondary_device_enable = tk.BooleanVar(self, False, 'secondary_device_enable')
        secondary_device_enable_button = tk.Checkbutton(secondary_device_frame, text='Use', variable=self.secondary_device_enable, command=self.toggle_secondary_device_enable)
        self.toggle_secondary_device_enable()
        secondary_device_enable_button.grid(column=1, row=0, sticky='nsew')
        
    def toggle_secondary_device_enable(self):
        if self.secondary_device_enable.get():
            self.secondary_device_menu.configure(state='normal')
        else:
            self.secondary_device_menu.configure(state='disabled')
    
    def play_entry(self, item):
        filename = self.audio_table.item(item)['values'][2]
        af = AudioEntry(filename, self)
        af.play()
        self.playing.append(af)

    def get_devices(self):
        out = [self.primary_device.get()]
        if self.secondary_device_enable.get():
            out.append(self.secondary_device.get())
        return out
    
    def add_entry(self, filename, hotkeys_str='', hotkey=None):
        name = os.path.basename(filename)
        return self.audio_table.insert('', 'end', values=(name, hotkeys_str, filename), hotkey=hotkey)
    
    def edit_entry(self, iid, filename, hotkeys_str='', hotkey=None):
        name = os.path.basename(filename)
        self.audio_table.set(iid, column='Sound Clip', value=name)
        self.audio_table.set(iid, column='HotKeys', value=hotkeys_str)
        self.audio_table.set(iid, column='path', value=filename)
        self.audio_table.set_hotkey(iid, hotkey)
        return iid
    
    def enter_callback(self, somevar):
        item = self.audio_table.focus()
        if item:
            item = self.audio_table.item(item)
            EntryWindow(self, item['values'][2], item['values'][1], item)
        else:
            EntryWindow(self)

    def add_button_callback(self):
        EntryWindow(self)

    def remove_button_callback(self):
        item = self.audio_table.focus()
        if item:
            self.audio_table.delete(item)

    def edit_button_callback(self):
        index = self.audio_table.focus()
        if index:
            item = self.audio_table.item(index)
            EntryWindow(self, item['values'][2], item['values'][1], index)

    def play_button_callback(self):
        item = self.audio_table.focus()
        if item:
            self.play_entry(item)

    def stop_button_callback(self):
        self.stop_all()
    
    def stop_all(self):
        while len(self.playing) > 0:
            self.playing[0].stop()

    def file_save_as_callback(self):
        filename = filedialog.asksaveasfilename(initialfile=DEFAULT_SAVE)
        self.save_file(filename)

    def file_load_callback(self):
        filename = filedialog.askopenfilename(initialfile=DEFAULT_SAVE)
        self.load_file(filename)

    def save_file(self, filename):
        data = []
        for iid in self.audio_table.get_children():
            item = self.audio_table.item(iid).copy()
            item['hotkey']._on_activate = None
            data.append((item['values'].copy(), item['hotkey']))
        with open(filename, 'wb') as outfile:
            pickle.dump(data, outfile)
    
    def load_file(self, filename):
        with open(filename, 'rb') as infile:
            data = pickle.load(infile)
        self.audio_table.delete(*self.audio_table.get_children())
        for d in data:
            self.audio_table.insert('', 'end', None, d[1], values=d[0].copy())
    
    def error(self, message):
        ErrorWindow(message, self)

def main():
    app = RetroBoard()
    app.mainloop()

if __name__ == '__main__':
    main()