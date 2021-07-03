import tkinter as tk
from threading import Thread
from time import sleep
from pynput import keyboard

class HotkeyEntry(tk.Entry):
    def __init__(self, master=None, cnf={}, **kw):
        kw['state'] = 'disabled'
        kw['disabledbackground'] = 'light gray'
        tk.Widget.__init__(self, master, 'entry', cnf, kw)
        self.capture = False
        self.capture_process = None
        self.key_pressed = None
        self.bind('<ButtonRelease-1>', self.left_click_callback)
        self.bind('<ButtonRelease-3>', self.right_click_callback)
    
    def left_click_callback(self, key):
        if not self.capture:
            self.capture_process = Thread(target=self.capture_hotkeys)
            self.capture_process.start()

    def right_click_callback(self, key):
        self.capture = False
        self.clear_hotkeys()
    
    def capture_hotkeys(self):
        self.capture = True
        self.config({"disabledbackground": "deep sky blue"})
        listener = keyboard.Listener(on_press=self.key_callback, on_release=self.key_callback)
        listener.start()
        while self.capture:
            sleep(1)
        listener.stop()
        self.capture = False
        self.config({"disabledbackground": "light gray"})

    def clear_hotkeys(self):
        pass

    def key_callback(self, key:keyboard.KeyCode):
        
        """ if key.type == 'KeyPress':
            if not self.key_pressed:
                self.key_pressed = key.keycode
        elif key.type == 'KeyRelease':
            if self.key_pressed == key.keycode:
                pass """