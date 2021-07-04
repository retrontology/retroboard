from typing import ClassVar
from pynput.keyboard import Key, KeyCode

class KeyCombo():
    
    def __init__(self, textvar = None):
        self.textvar = textvar
        self.keys_pressed = set()
        self.keys_stored = set()

    def key_press_callback(self, key):
        if type(key) == KeyCode:
            key = KeyCode(char=key.char.upper())
        self.keys_pressed.add(key)
        if not key in self.keys_stored:
            self.keys_stored = self.keys_pressed.copy()
        self.textvar.set(self.string(self.keys_stored))

    def key_release_callback(self, key):
        if type(key) == KeyCode:
            key = KeyCode(char=key.char.upper())
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)
        self.textvar.set(self.string(self.keys_stored))
    
    @staticmethod
    def string(keys: set):
        out = ''
        for key in keys:
            if out != '':
                out += '+'
            if type(key) == Key:
                out += key._name_
            elif type(key) == KeyCode:
                out += key.char
        return out