from pynput import keyboard
from enum import Enum

DEFAULT_STOP_ALL = set([keyboard.Key.pause])

class HotkeyScope(Enum):
    GLOBAL = 0
    TABLE = 1

class HotkeyListener():

    def __init__(self, parent):
        self.parent = parent
        self._global_hotkeys = dict()
        self._global_listeners = dict()
        self._table_hotkeys = dict()
        self._table_listeners = dict()
        self.set_global_hotkeys()

    def set_global_hotkeys(self):
        self.set_hotkey('stop_all', keyboard.HotKey(DEFAULT_STOP_ALL, self.parent.stop_all), HotkeyScope.GLOBAL)
    
    def get_hotkey_keys(self, index, scope):
        if scope == HotkeyScope.GLOBAL:
            hotkeys = self._global_hotkeys
        elif scope == HotkeyScope.TABLE:
            hotkeys = self._table_hotkeys
        return hotkeys[index]._keys
    
    def set_hotkey(self, index, hotkey, scope:HotkeyScope):
        if scope == HotkeyScope.GLOBAL:
            hotkeys = self._global_hotkeys
            listeners = self._global_listeners
        elif scope == HotkeyScope.TABLE:
            hotkeys = self._table_hotkeys
            listeners = self._table_listeners
        if index in hotkeys:
            self.remove_hotkey(index, scope)
        hotkeys[index] = hotkey
        if hotkey != None:
            if hotkey._on_activate is None and scope == HotkeyScope.TABLE:
                hotkey._on_activate = lambda: self.parent.play_entry(index)
            listeners[index] = keyboard.Listener(on_press=self.for_canonical(hotkeys[index].press, index, scope), on_release=self.for_canonical(hotkeys[index].release, index, scope))
            listeners[index].start()
        else:
            listeners[index] = None
    
    def remove_hotkey(self, index, scope:HotkeyScope):
        if scope == HotkeyScope.GLOBAL:
            hotkeys = self._global_hotkeys
            listeners = self._global_listeners
        elif scope == HotkeyScope.TABLE:
            hotkeys = self._table_hotkeys
            listeners = self._table_listeners
        if index in listeners:
            if listeners[index] is not None:
                listeners[index].stop()
            listeners.pop(index)
        if index in hotkeys:
            hotkeys.pop(index)

    def for_canonical(self, f, index, scope:HotkeyScope):
        if scope == HotkeyScope.GLOBAL:
            listeners = self._global_listeners
        elif scope == HotkeyScope.TABLE:
            listeners = self._table_listeners
        return lambda k: f(listeners[index].canonical(k))