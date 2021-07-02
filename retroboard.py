import tkinter as tk
import tkinter.ttk as ttk
import sounddevice
from audioentry import AudioEntry
from entryframe import EntryFrame
import os.path

class RetroBoard(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.playing = []
        self.pack(fill='both', expand=True)
        self.columnconfigure(0, weight=1)
        self.setup_widgets()
        self.add_tests()
    
    def add_tests(self):
        self.audio_table.insert('', 'end', None, values=('test.mp3', '', 'test.mp3'))

    def on_exit(self):
        self.winfo_toplevel().destroy()

    def setup_widgets(self):
        self.create_menu()
        self.create_audio_table()
        self.create_buttons()
        self.create_device_selection()

    def create_menu(self):
        # Top Level menubar
        self.menubar = tk.Menu(self.winfo_toplevel())
        self.winfo_toplevel().config(menu=self.menubar)

        # File Menu
        file_menu = tk.Menu(self.menubar, tearoff=0)
        file_menu.add_command(label='Save', command=self.file_save_callback)
        file_menu.add_command(label='Load', command=self.file_load_callback)
        file_menu.add_command(label='Exit', command=self.on_exit)
        self.menubar.add_cascade(label = "File", menu=file_menu)

    def create_audio_table(self):
        # Top Level frame for table of audio clips
        table_frame = tk.Frame(self)
        table_frame.grid(column=0, row=0, sticky='nsew', padx=8, pady=5)
        self.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        # Audio clip table
        table_headings = ['Sound Clip','HotKeys', 'path']
        self.audio_table = ttk.Treeview(table_frame, show="headings", height=10, columns=table_headings, displaycolumns=table_headings[:2])
        self.audio_table.columnconfigure(0, weight=10)
        self.audio_table.columnconfigure(1, weight=1)
        self.audio_table.grid(column=0, row=0, sticky='nsew', in_=table_frame)
        for column in table_headings:
            self.audio_table.heading(column, text=column.title())

        # Scroll bar for table
        scrollbar = tk.Scrollbar(orient="vertical", command=self.audio_table.yview)
        self.audio_table.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(column=1, row=0, sticky='ns', in_=table_frame)
    
    def create_buttons(self):
        # Top level button frame
        button_frame = tk.Frame(self)
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

    def create_device_selection(self):
        # Device selection frame
        device_frame = tk.Frame(self)
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
    
    def play_file(self, filename):
        af = AudioEntry(filename, self)
        af.play()
        self.playing.append(af)

    def get_devices(self):
        out = [self.primary_device.get()]
        if self.secondary_device_enable.get():
            out.append(self.secondary_device.get())
        return out
    
    def add_to_table(self, filename, hotkeys=''):
        name = os.path.basename(filename)
        self.audio_table.insert('', 'end', values=(name, hotkeys, filename))

    def add_button_callback(self):
        EntryFrame(self)

    def remove_button_callback(self):
        item = self.audio_table.focus()
        if item:
            self.audio_table.delete(item)

    def edit_button_callback(self):
        pass

    def play_button_callback(self):
        item = self.audio_table.focus()
        if item:
            item = self.audio_table.item(item)
            self.play_file(item['values'][2])

    def stop_button_callback(self):
        self.stop_all()
    
    def stop_all(self):
        while len(self.playing) > 0:
            self.playing[0].stop()

    def file_save_callback(self):
        pass

    def file_load_callback(self):
        pass

def main():
    root = tk.Tk()
    root.geometry("500x600")
    root.title('retroboard')
    app = RetroBoard(root)
    app.mainloop()

if __name__ == '__main__':
    main()