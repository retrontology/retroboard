import tkinter as tk

class ErrorWindow(tk.Toplevel):

    def __init__(self, message, master=None, cnf={}, **kw):
        super().__init__(master)
        self.master = master
        self.title('Error')
        self.setup_widgets(message)

    def setup_widgets(self, message):
        self.minsize(100,50)
        self.grab_set()
        self.focus_force()

        # Top level frame
        topframe = tk.Frame(self)
        topframe.pack(padx=5, pady=5, fill='both', expand=True)

        # Message
        tk.Label(topframe, text=message, justify='center').pack(side='top', padx=5, pady=5)

        # Button
        tk.Button(topframe, command=self.destroy, text='OK').pack(side='bottom', padx=5, pady=5)

        # Disable resize
        self.resizable(width=False, height=False)

