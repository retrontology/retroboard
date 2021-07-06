import tkinter as tk

class SettingsWindow(tk.Toplevel):
    
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master