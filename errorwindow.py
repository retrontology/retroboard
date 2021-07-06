import tkinter as tk

class ErrorWindow(tk.Toplevel):

    def __init__(self, message, master=None, cnf={}, **kw):
        tk.Widget.__init__(self, master, 'entry', cnf, kw)
        self.master = master
        self.title = 'Error'
        self.setup_widgets(message)

    def setup_widgets(self, message):
        # Top level frame
        topframe = tk.Frame(self)
        topframe.pack(padx=10, pady=10, fill='both', expand=True)

        # Message
        tk.Label(topframe, text=message, justify='center')
