import tkinter as tk
from threading import Thread
from time import sleep
from pynput import keyboard, mouse
from enum import Enum
from keycombo import KeyCombo

class HotkeyEntry(tk.Entry):
    def __init__(self, master=None, cnf={}, **kw):
        kw['state'] = 'disabled'
        kw['disabledbackground'] = 'light gray'
        tk.Widget.__init__(self, master, 'entry', cnf, kw)
        self.hotkey_var: tk.StringVar = kw['textvariable']
        self.hotkey_combo = KeyCombo(kw['textvariable'])
        self.capture = False
        self.capture_process = None
        self.bind('<ButtonRelease-1>', self.left_click_callback)
        self.bind('<ButtonRelease-3>', self.right_click_callback)
    
    def left_click_callback(self, key):
        if not self.capture:
            self.capture_process = Thread(target=self.capture_hotkeys)
            self.capture_process.start()

    def right_click_callback(self, key):
        self.capture = False
        self.clear_hotkeys()
    
    def stop(self):
        if self.capture:
            self.capture = False
    
    def capture_hotkeys(self):
        self.capture = True
        self.config({"disabledbackground": "deep sky blue"})
        listeners = []
        listeners.append(keyboard.Listener(on_press=self.hotkey_combo.key_press_callback, on_release=self.hotkey_combo.key_release_callback))
        for listener in listeners: listener.start()
        while self.capture:
            sleep(1)
        for listener in listeners: listener.stop()
        self.capture = False
        if self.winfo_exists():
            self.config({"disabledbackground": "light gray"})

    def clear_hotkeys(self):
        self.hotkey_var.set('')