import tkinter as tk
from threading import Thread
from time import sleep
from pynput import keyboard
from enum import Enum

class HotkeyEntry(tk.Entry):
    def __init__(self, master=None, cnf={}, **kw):
        kw['state'] = 'disabled'
        kw['disabledbackground'] = 'light gray'
        tk.Widget.__init__(self, master, 'entry', cnf, kw)
        self.hotkey_combo = KeyCombo()
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
        listener = keyboard.Listener(on_press=self.hotkey_combo.key_press_callback, on_release=self.hotkey_combo.key_release_callback)
        listener.start()
        while self.capture:
            sleep(1)
        listener.stop()
        self.capture = False
        self.config({"disabledbackground": "light gray"})

    def clear_hotkeys(self):
        pass

class KeyCombo():
    
    def __init__(self, textvar = None):
        pass

    def key_press_callback(self, key):
        pass

    def key_release_callback(self, key):
        pass