import pickle
from pynput import keyboard
from os.path import isfile, abspath, join, dirname

DEFAULT_DIR = dirname(abspath(__file__))
DEFAULT_PREF = 'pref.rbp'
DEFAULT_SAVE = 'default.rbd'
DEFAULT_STOP_ALL = set([keyboard.Key.pause])
DEFAULT_PTT = set([keyboard.KeyCode(char='v')])
DEFAULT_PTT_ENABLE = False

class Preferences(dict):

    def __init__(self, path=join(DEFAULT_DIR, DEFAULT_PREF)):
        self.path = path
        self.load()

    def __setitem__(self, k, v):
        super().__setitem__(k, v)
        self.save()
    
    def load_defaults(self):
        self.setdefault('savefile', join(DEFAULT_DIR, DEFAULT_SAVE))
        self.setdefault('stop_all', DEFAULT_STOP_ALL)
        self.setdefault('ptt', DEFAULT_PTT)
        self.setdefault('ptt_enable', DEFAULT_PTT_ENABLE)

    def load(self):
        self.clear()
        if isfile(self.path):
            try:
                with open(self.path, 'rb') as f:
                    self.update(pickle.load(f))
            except Exception as e:
                print(e)
        self.load_defaults()
    
    def save(self):
        with open(self.path, 'wb') as f:
            pickle.dump(self.copy(), f)