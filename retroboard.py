import tkinter as tk
import tkinter.ttk as ttk
import sounddevice

class retroboard(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill='both', expand=True)
        self.columnconfigure(0, weight=1)
        self.setup_widgets()

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
        file_menu = tk.Menu(self.menubar)
        file_menu.add_command(label='Save', command=self.file_save_callback)
        file_menu.add_command(label='Load', command=self.file_load_callback)
        file_menu.add_command(label='Exit', command=self.on_exit)
        self.menubar.add_cascade(label = "File", menu=file_menu)

    def create_audio_table(self):
        # Top Level frame for table of audio clips
        table_frame = tk.Frame(self)
        table_frame.grid(column=0, row=0, sticky='nsew')
        self.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        # Audio clip table
        table_headings = ['File','Hotkey']
        self.audio_table = ttk.Treeview(table_frame, show="headings", height=10, columns=table_headings)
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
        table_button_frame.pack(side='left')
        add_button = tk.Button(table_button_frame, text='Add', command=self.add_button_callback)
        add_button.grid(column=0, row=0, sticky='w', in_=table_button_frame)
        remove_button = tk.Button(table_button_frame, text='Remove', command=self.remove_button_callback)
        remove_button.grid(column=1, row=0, sticky='w', in_=table_button_frame)
        edit_button = tk.Button(table_button_frame, text='Edit', command=self.edit_button_callback)
        edit_button.grid(column=2, row=0, sticky='w', in_=table_button_frame)

        # buttons for playback
        playback_button_frame = tk.Frame(button_frame)
        playback_button_frame.pack(side='right')
        play_button = tk.Button(playback_button_frame, text='Play', command=self.play_button_callback)
        play_button.grid(column=0, row=0, sticky='w', in_=playback_button_frame)
        stop_button = tk.Button(playback_button_frame, text='Stop All', command=self.stop_button_callback)
        stop_button.grid(column=1, row=0, sticky='w', in_=playback_button_frame)

    def create_device_selection(self):
        # Device selection frame
        device_frame = tk.Frame(self)
        device_frame.grid(column=0, row=2, sticky='nsew')
        device_frame.columnconfigure(0, weight=1)
        
        # Get device info
        devices = sounddevice.query_devices()
        device_names = [x['name'] for x in devices]
        default_device = sounddevice.query_devices(kind='output')['name']

        # Primary output
        self.primary_device = tk.StringVar(self, default_device, 'primary_device')
        primary_device_menu = tk.OptionMenu(device_frame, self.primary_device, *device_names)
        primary_device_menu.grid(column=0, row=0, sticky='nsew', in_=device_frame)

        # Secondary output
        self.secondary_device = tk.StringVar(self, default_device, 'secondary_device')
        secondary_device_frame = tk.Frame(device_frame)
        secondary_device_frame.columnconfigure(0, weight=1)
        secondary_device_frame.grid(column=0, row=1, sticky='nsew', in_=device_frame)
        secondary_device_menu = tk.OptionMenu(secondary_device_frame, self.secondary_device, *device_names)
        secondary_device_menu.grid(column=0, row=0, sticky='nsew')
        secondary_device_enable = tk.BooleanVar(self, False, 'secondary_device_enable')
        secondary_device_enable_box = tk.Checkbutton(secondary_device_frame, text='Use', variable=secondary_device_enable)
        secondary_device_enable_box.grid(column=1, row=0, sticky='nsew')

    def add_button_callback(self):
        pass

    def remove_button_callback(self):
        pass

    def edit_button_callback(self):
        pass

    def play_button_callback(self):
        pass

    def stop_button_callback(self):
        pass

    def file_save_callback(self):
        pass

    def file_load_callback(self):
        pass

def main():
    root = tk.Tk()
    root.geometry("500x600")
    root.title('retroboard')
    app = retroboard(root)
    app.mainloop()

if __name__ == '__main__':
    main()