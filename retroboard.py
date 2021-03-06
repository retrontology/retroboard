from tkinter.constants import E
from hotkeyentry import HotkeyEntry
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as filedialog
import sounddevice
from audioentry import AudioEntry
from hotkeylistener import HotkeyListener, HotkeyScope
from entrywindow import EntryWindow
from hotkeytree import HotKeyTree
from errorwindow import ErrorWindow
from settingswindow import SettingsWindow
from gainwindow import GainWindow
from pynput import keyboard
from hotkey import RetroHotKey
import os
import pickle
import webbrowser
from time import sleep, time
from threading import Thread
from preferences import *
import sys

VERSION_MAJOR = 1
VERSION_MINOR = 2
VERSION_PATCH = 2
VERSION = f'{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}'
GITHUB_URL = 'https://github.com/retrontology/retroboard'
ICON_FILE = os.path.join(os.path.dirname(__file__), 'icon/RB.png')

class RetroBoard(tk.Tk):

    def __init__(self, master=None):
        super().__init__(master)
        self.iconphoto(True, tk.PhotoImage(file=ICON_FILE))
        self.geometry("500x600")
        self.title(f'retroboard | {VERSION}')
        self.playing = []
        self.setup_variables()
        self.setup_widgets()
        self.setup_binds()
        self.load_default_file()
    
    def setup_binds(self):
        self.bind('<Control-s>', lambda x: self.file_save_callback())
        self.bind('<Return>', self.enter_callback)
        self.bind('<KP_Enter>', self.enter_callback)
    
    def setup_variables(self):
        # Hidden Application Variables
        self.prefs = Preferences()
        self.hotkey_listener = HotkeyListener(self)
        self._savefile = tk.StringVar(self, self.prefs['savefile'], 'savefile')
        self.settings_window = None
        self.gain_window = None

        # Device Variables
        devices = sounddevice.query_devices()
        device_names = [f'{i+1}. {x["name"]}' for i, x in enumerate(devices)]
        odev = sounddevice._get_device_id(sounddevice.default.device['output'], 'output')
        default_device = device_names[odev]
        self.primary_device = tk.StringVar(self, default_device, 'primary_device')
        self.primary_gain = tk.DoubleVar(self, self.prefs['primary_gain'], 'primary_gain')
        self.secondary_device = tk.StringVar(self, default_device, 'secondary_device')
        self.secondary_gain = tk.DoubleVar(self, self.prefs['secondary_gain'], 'secondary_gain')
        self.secondary_device_enable = tk.BooleanVar(self, False, 'secondary_device_enable')

        # Global Hotkey Variables
        if self.prefs['pause_all_hotkey'] != None:
            pause_all_hotkey = RetroHotKey(self.prefs['pause_all_hotkey'], self.pause_toggle_all)
        else:
            pause_all_hotkey = None
        self.hotkey_listener.set_hotkey('pause_all_hotkey', pause_all_hotkey, HotkeyScope.SETTINGS)
        self.pause_all_var = tk.StringVar(self, HotkeyEntry.hotkey_to_string(pause_all_hotkey), 'hotkey_pause_all')

        if self.prefs['stop_all'] != None:
            stop_all_hotkey =  RetroHotKey(self.prefs['stop_all'], self.stop_all)
        else:
            stop_all_hotkey = None
        self.hotkey_listener.set_hotkey('stop_all', stop_all_hotkey, HotkeyScope.SETTINGS)
        self.stopall_var = tk.StringVar(self, HotkeyEntry.hotkey_to_string(stop_all_hotkey), 'hotkey_stop_all')

        self.ptt_pre_time = tk.DoubleVar(self, self.prefs['ptt_pre_time'], 'ptt_pre_time')
        self.ptt_post_time = tk.DoubleVar(self, self.prefs['ptt_post_time'], 'ptt_post_time')
        if self.prefs['ptt'] != None:
            ptt_hotkey = RetroHotKey(self.prefs['ptt'], None)
        else:
            ptt_hotkey = None
        self.hotkey_listener.set_hotkey('ptt', ptt_hotkey, HotkeyScope.SETTINGS)
        self.ptt_pressed = False
        self.ptt_enable_var = tk.BooleanVar(self, self.prefs['ptt_enable'], 'ptt_enable')
        self.ptt_var = tk.StringVar(self, HotkeyEntry.hotkey_to_string(ptt_hotkey), 'ptt_hotkey')

        self.overlap = tk.BooleanVar(self, self.prefs['overlap'], 'overlap')
        if self.prefs['overlap_hotkey'] != None:
            overlap_hotkey = RetroHotKey(self.prefs['overlap_hotkey'], self.toggle_overlap)
        else:
            overlap_hotkey = None
        self.hotkey_listener.set_hotkey('overlap_hotkey', overlap_hotkey, HotkeyScope.SETTINGS)
        self.overlap_var = tk.StringVar(self, HotkeyEntry.hotkey_to_string(overlap_hotkey), 'overlap_hotkey')

    def on_exit(self):
        self.destroy()

    def setup_widgets(self):
        topframe = tk.Frame()
        topframe.pack(fill='both', expand=True)
        topframe.columnconfigure(0, weight=1)
        topframe.rowconfigure(0, weight=1)
        self.create_audio_table(topframe)
        self.create_menu()
        self.create_buttons(topframe)
        self.create_device_selection(topframe)
    
    def spawn_settings(self):
        if self.settings_window:
            self.settings_window.focus()
            self.settings_window.lift(self)
        else:
            self.settings_window = SettingsWindow(self)

    def spawn_gain(self):
        if self.gain_window:
            self.gain_window.focus()
            self.gain_window.lift(self)
        else:
            self.gain_window = GainWindow(self)

    def create_menu(self):
        # Top Level menubar
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)

        # File Menu
        file_menu = tk.Menu(self.menubar, tearoff=0)
        file_menu.add_command(label='New', command=self.audio_table.clear)
        file_menu.add_command(label='Open', command=self.file_load_callback)
        file_menu.add_separator()
        file_menu.add_command(label='Save        Ctrl+S', command=self.file_save_callback)
        file_menu.add_command(label='Save As', command=self.file_save_as_callback)
        file_menu.add_separator()
        file_menu.add_command(label='GitHub Page', command=lambda: webbrowser.open(GITHUB_URL))
        file_menu.add_separator()
        file_menu.add_command(label='Quit', command=self.on_exit)
        self.menubar.add_cascade(label = "File", menu=file_menu)

        # Option Menu
        settings_menu = tk.Menu(self.menubar, tearoff=0)
        settings_menu.add_command(label='Gain Levels', command = self.spawn_gain)
        settings_menu.add_command(label='Settings', command=self.spawn_settings)
        self.menubar.add_cascade(label = 'Option', menu=settings_menu)

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
        play_button.grid(column=0, row=0, sticky='w', in_=playback_button_frame, padx=5)
        pause_button = tk.Button(playback_button_frame, text='Pause All', command=self.pause_button_callback)
        pause_button.grid(column=1, row=0, sticky='w', in_=playback_button_frame, padx=5)
        stop_button = tk.Button(playback_button_frame, text='Stop All', command=self.stop_button_callback)
        stop_button.grid(column=3, row=0, sticky='w', in_=playback_button_frame, padx=5)

    def create_device_selection(self, frame):
        # Device selection frame
        device_frame = tk.Frame(frame)
        device_frame.grid(column=0, row=2, sticky='nsew', padx=8, pady=5)
        device_frame.columnconfigure(0, weight=1)
        
        # Get device info
        devices = sounddevice.query_devices()
        device_names = [f'{i+1}. {x["name"]}' for i, x in enumerate(devices) if x['max_output_channels'] > 0]

        # Primary output
        primary_device_label = tk.Label(device_frame, text='Primary Output Device')
        primary_device_label.grid(column=0, row=0, sticky='w')
        primary_device_menu = ttk.Combobox(device_frame, textvariable=self.primary_device, values=device_names, state='readonly', background='light gray')
        primary_device_menu.grid(column=0, row=1, sticky='nsew', in_=device_frame)

        # Secondary output
        secondary_device_label = tk.Label(device_frame, text='Secondary Output Device')
        secondary_device_label.grid(column=0, row=2, sticky='w')
        secondary_device_frame = tk.Frame(device_frame)
        secondary_device_frame.columnconfigure(0, weight=1)
        secondary_device_frame.grid(column=0, row=3, sticky='nsew', in_=device_frame)
        self.secondary_device_menu = ttk.Combobox(secondary_device_frame, textvariable=self.secondary_device, values=device_names, state='readonly', background='light gray')
        self.secondary_device_menu.grid(column=0, row=0, sticky='nsew')
        secondary_device_enable_button = tk.Checkbutton(secondary_device_frame, text='Use', variable=self.secondary_device_enable, command=self.toggle_secondary_device_enable)
        self.toggle_secondary_device_enable()
        secondary_device_enable_button.grid(column=1, row=0, sticky='nsew')
        
    def toggle_secondary_device_enable(self):
        if self.secondary_device_enable.get():
            self.secondary_device_menu.configure(state='readonly')
        else:
            self.secondary_device_menu.configure(state='disabled')
    
    def ptt_press(self):
        hotkey = self.hotkey_listener.get_hotkey('ptt', HotkeyScope.SETTINGS)
        if hotkey != None and self.ptt_enable_var.get() and not self.ptt_pressed:
            self.ptt_pressed = True
            keys = hotkey._keys
            kbc = keyboard.Controller()
            end_time = time() + self.ptt_pre_time.get() + 0.1
            while time() < end_time:
                for key in keys:
                    kbc.press(key)
                sleep(0.1)
            while len(self.playing) > 0 and any([not x.pause for x in self.playing]):
                for key in keys:
                    kbc.press(key)
                sleep(0.1)
            if self.ptt_post_time.get():
                end_time = time() + self.ptt_post_time.get()
                while time() < end_time:
                    for key in keys:
                        kbc.press(key)
                    sleep(0.1)
            for key in keys:
                kbc.release(key)
            self.ptt_pressed = False
                
    def toggle_ptt_enable(self):
        self.prefs['ptt_enable'] = self.ptt_enable_var.get()
    
    def toggle_overlap(self):
        self.overlap.set(not self.overlap.get())
        self.prefs['overlap'] = self.overlap.get()
    
    def play_entry(self, item):
        if not self.ptt_pressed:
            Thread(target=self.ptt_press, daemon=True).start()
            sleep(self.ptt_pre_time.get())
        filename = self.audio_table.item(item)['values'][2]
        if not self.overlap.get():
            for audio in self.playing:
                if audio.item == item:
                    audio.stop = True
        af = AudioEntry(filename, item, self)
        self.playing.append(af)
        af.play()
        

    def get_devices(self):
        primary_index = int(self.primary_device.get().split('.', 1)[0]) - 1
        primary_info = sounddevice.query_devices(primary_index)
        out = [(primary_index, primary_info['default_samplerate'], primary_info['max_output_channels'], self.primary_gain)]
        if self.secondary_device_enable.get():
            secondary_index = int(self.secondary_device.get().split('.', 1)[0]) - 1
            secondary_info = sounddevice.query_devices(secondary_index)
            out.append((secondary_index, secondary_info['default_samplerate'], secondary_info['max_output_channels'], self.secondary_gain))
        return out
    
    def add_entry(self, filename, hotkeys_str='', hotkey=None):
        name = os.path.basename(filename)
        return self.audio_table.insert('', 'end', values=(name, hotkeys_str, filename), hotkey=hotkey)
    
    def edit_entry(self, iid, filename, hotkeys_str='', hotkey=None):
        name = os.path.basename(filename)
        self.audio_table.set(iid, column='Sound Clip', value=name)
        self.audio_table.set(iid, column='HotKeys', value=hotkeys_str)
        self.audio_table.set(iid, column='path', value=filename)
        self.hotkey_listener.set_hotkey(iid, hotkey, HotkeyScope.TABLE)
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
        for index in self.audio_table.selection():
            self.audio_table.delete(index)

    def edit_button_callback(self):
        for index in self.audio_table.selection():
            item = self.audio_table.item(index)
            EntryWindow(self, item['values'][2], item['values'][1], index)

    def play_button_callback(self):
        item = self.audio_table.focus()
        if item:
            self.play_entry(item)

    def stop_button_callback(self):
        self.stop_all()
    
    def pause_button_callback(self):
        self.pause_toggle_all()
    
    def stop_all(self):
        for clip in self.playing.copy():
            clip.stop = True
    
    def pause_toggle_all(self):
        if any([not x.pause for x in self.playing]):
            self.pause_all()
        else:
            self.resume_all()

    def pause_all(self):
        for clip in self.playing:
            clip.pause = True
    
    def resume_all(self):
        if not self.ptt_pressed:
            Thread(target=self.ptt_press, daemon=True).start()
            sleep(self.ptt_pre_time.get())
        for clip in self.playing:
            clip.resume()
        
    
    def file_save_callback(self):
        default_file = self._savefile.get()
        if os.path.isfile(default_file):
            self.save_file(default_file)
        else:
            self.file_save_as_callback()

    def file_save_as_callback(self):
        filename = filedialog.asksaveasfilename(initialfile=DEFAULT_SAVE, initialdir=os.path.dirname(os.path.abspath(sys.argv[0])))
        if filename:
            self.save_file(filename)

    def file_load_callback(self):
        filename = filedialog.askopenfilename(initialfile=DEFAULT_SAVE)
        if filename:
            self.load_file(filename)

    def save_file(self, filename):
        data = []
        for iid in self.audio_table.get_children():
            item = self.audio_table.item(iid).copy()
            if item['hotkey']:
                hotkey = item['hotkey']._keys.copy()
            else:
                hotkey = None
            data.append((item['values'].copy(), hotkey))
        with open(filename, 'wb') as outfile:
            pickle.dump(data, outfile)
        self._savefile.set(filename)
    
    def load_file(self, filename):
        with open(filename, 'rb') as infile:
            data = pickle.load(infile)
        self.audio_table.clear()
        for d in data:
            if d[1]:
                hotkey = RetroHotKey(d[1], None)
            else:
                hotkey = None
            self.audio_table.insert('', 'end', None, hotkey, values=d[0].copy())
        self._savefile.set(filename)
    
    def load_default_file(self):
        default_file = self._savefile.get()
        if os.path.isfile(default_file):
            self.load_file(default_file)
    
    def error(self, message):
        ErrorWindow(message, self)

def main():
    app = RetroBoard()
    app.mainloop()

if __name__ == '__main__':
    main()