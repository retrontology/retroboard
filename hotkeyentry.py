import tkinter as tk

class HotkeyEntry(tk.Widget, tk.XView):
    def __init__(self, master=None, cnf={}, **kw):
        tk.Widget.__init__(self, master, 'entry', cnf, kw)
