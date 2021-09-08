from pynput import keyboard
from hotkey import RetroListener
from enum import Enum

class HotkeyScope(Enum):
    SETTINGS = 0
    TABLE = 1

class HotkeyListener():

    def __init__(self, parent):
        self.parent = parent
        self._global_hotkeys = dict()
        self._global_listeners = dict()
        self._table_hotkeys = dict()
        self._table_listeners = dict()
        
    def get_hotkey(self, index, scope):
        if scope == HotkeyScope.SETTINGS:
            hotkeys = self._global_hotkeys
        elif scope == HotkeyScope.TABLE:
            hotkeys = self._table_hotkeys
        if index in hotkeys:
            return hotkeys[index]
        else:
            return None
    
    def set_hotkey(self, index, hotkey, scope:HotkeyScope):
        if scope == HotkeyScope.SETTINGS:
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
            if hotkey._on_activate is not None:
                listeners[index] = RetroListener(on_press=self.for_canonical(hotkeys[index].press, index, scope), on_release=self.for_canonical(hotkeys[index].release, index, scope))
                listeners[index].start()
            else:
                listeners[index] = None
        else:
            listeners[index] = None
    
    def remove_hotkey(self, index, scope:HotkeyScope):
        if scope == HotkeyScope.SETTINGS:
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
        if scope == HotkeyScope.SETTINGS:
            listeners = self._global_listeners
        elif scope == HotkeyScope.TABLE:
            listeners = self._table_listeners
        return lambda k: f(listeners[index].canonical(k))