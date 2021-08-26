import tkinter as tk
from tkinter import Toplevel, ttk

GAIN_MIN = -66
GAIN_MAX = 6

class GainWindow(tk.Toplevel):
    
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.minsize(450,80)
        self.setup_widgets()
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_widgets(self):
        topframe = tk.Frame(self)
        topframe.pack(fill='both', expand=True, padx=10, pady=10)
        topframe.columnconfigure(0, weight=1)
        primary_gain_slider = tk.Scale(topframe, from_=GAIN_MIN, to=GAIN_MAX, variable=self.master.primary_gain, orient='horizontal', tickinterval=6, resolution=0.1, label='Primary Output Gain:', takefocus=1)
        primary_gain_slider.grid(column=0, row=0, sticky='ew')
        primary_gain_slider.bind('<Button-1>', lambda x: primary_gain_slider.focus())
        secondary_gain_slider = tk.Scale(topframe, from_=GAIN_MIN, to=GAIN_MAX, variable=self.master.secondary_gain, orient='horizontal', tickinterval=6, resolution=0.1, label='Secondary Output Gain:', takefocus=1)
        secondary_gain_slider.grid(column=0, row=1, sticky='ew')
        secondary_gain_slider.bind('<Button-1>', lambda x: secondary_gain_slider.focus())
    
    def on_closing(self):
        self.master.prefs['primary_gain'] = self.master.primary_gain.get()
        self.master.prefs['secondary_gain'] = self.master.secondary_gain.get()
        self.destroy()
        self.master.gain_window = None