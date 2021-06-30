import tkinter as tk
import tkinter.ttk as ttk

class retroboard(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("600x400")
        self.setup_widgets()

    def setup_widgets(self):
        self.create_menu()
        self.create_audio_table()

    def create_audio_table(self):
        # Top Level frame for table of audio clips
        self.table_frame = ttk.Frame(self)
        self.table_frame.pack(fill='both', expand=True)
        self.table_frame.columnconfigure(0, weight=1)
        self.table_frame.rowconfigure(0, weight=1)

        # Audio clip table
        table_headings = ['File','Hotkey']
        self.audio_table = ttk.Treeview(self, show="headings", height=10, columns=table_headings)
        self.audio_table.columnconfigure(0, weight=10)
        self.audio_table.columnconfigure(1, weight=1)
        self.audio_table.grid(column=0, row=0, sticky='nsew', in_=self.table_frame)
        for column in table_headings:
            self.audio_table.heading(column, text=column.title())

        # Scroll bar for table
        scrollbar = ttk.Scrollbar(orient="vertical", command=self.audio_table.yview)
        self.audio_table.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(column=1, row=0, sticky='ns', in_=self.table_frame)

    def create_menu(self):
        # Top Level menubar
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)
        # File Menu
        file_menu = tk.Menu(self.menubar)
        file_menu.add_command(label='Save', command=self.save)
        file_menu.add_command(label='Load', command=self.load)
        file_menu.add_command(label='Exit', command=self.destroy)
        self.menubar.add_cascade(label = "File", menu=file_menu)
    
    def save(self):
        pass

    def load(self):
        pass

def main():
    app = retroboard()
    app.mainloop()

if __name__ == '__main__':
    main()