import tkinter as tk
from threading import Thread
from time import sleep
from pynput import keyboard
from hotkey import RetroHotKey
import win_workaround
import os


class HotkeyEntry(tk.Entry):
    def __init__(self, master=None, clearable:bool=True, stored=None, stop_callback=None, cnf={}, **kw):
        kw['state'] = 'disabled'
        kw['disabledbackground'] = 'light gray'
        tk.Widget.__init__(self, master, 'entry', cnf, kw)
        self.stop_callback = stop_callback
        self.clearable = clearable
        self.hotkey_var: tk.StringVar = kw['textvariable']
        self.keys_pressed = set()
        if stored != None:
            self.keys_stored = stored._keys
        else:
            self.keys_stored = set()
            self.clear_hotkeys()
        self.capture = False
        self.capture_process = None
        self.bind('<ButtonRelease-1>', self.left_click_callback, '+')
        self.bind('<ButtonRelease-3>', self.right_click_callback, '+')
    
    def left_click_callback(self, key):
        if not self.capture:
            self.capture_process = Thread(target=self.capture_hotkeys, daemon=True)
            self.capture_process.start()

    def right_click_callback(self, key):
        self.stop()
        if self.clearable:
            self.clear_hotkeys()
    
    def stop(self):
        if self.capture:
            self.capture = False
    
    def capture_hotkeys(self):
        self.capture = True
        self.config({"disabledbackground": "deep sky blue"})
        listener = keyboard.Listener(on_press=self.key_press_callback, on_release=self.key_release_callback)
        listener.start()
        binds = [self.winfo_toplevel().bind('<ButtonRelease-1>', lambda x: self.stop(), '+'),
                 self.winfo_toplevel().bind('<ButtonRelease-3>', lambda x: self.stop(), '+')]
        while self.capture:
            sleep(.1)
        listener.stop()
        self.capture = False
        if self.winfo_exists():
            self.winfo_toplevel().unbind('<ButtonRelease-1>', binds[0])
            self.winfo_toplevel().unbind('<ButtonRelease-3>', binds[1])
            self.config({"disabledbackground": "light gray"})
        if self.stop_callback is not None:
            self.stop_callback(self)

    def clear_hotkeys(self):
        self.keys_pressed.clear()
        self.keys_stored.clear()
        self.hotkey_var.set('')
        if self.stop_callback:
            self.stop_callback(self)
    
    def key_press_callback(self, key):
        if not key in self.keys_pressed and key in self.keys_stored:
            self.keys_stored = self.keys_pressed.copy()
        self.keys_pressed.add(key)
        for key in self.keys_pressed:
            if not key in self.keys_stored:
                self.keys_stored = self.keys_pressed.copy()
                break
        self.hotkey_var.set(self.set_to_string(self.keys_stored))

    def key_release_callback(self, key):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)
        self.hotkey_var.set(self.set_to_string(self.keys_stored))
    
    def get_hotkey(self, on_activate=None):
        if len(self.keys_stored) == 0:
            return None
        else:
            out = RetroHotKey(self.keys_stored, on_activate)
            return out
    
    @staticmethod
    def set_to_string(keys: set):
        out = ''
        for key in keys:
            if out != '':
                out += '+'
            if type(key) == keyboard.Key:
                out += f'<{key._name_}>'
            elif type(key) == keyboard.KeyCode:
                if key.char:
                    out += key.char
                else:
                    if os.name == 'nt':
                        out += win_workaround.WINDOWS_SCANCODES[key.vk]
                    else:
                        out += '?'
        return out
    
    @staticmethod
    def hotkey_to_string(key):
        if key != None:
            return HotkeyEntry.set_to_string(key._keys)
        else:
            return set()