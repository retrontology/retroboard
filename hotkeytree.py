from os import stat
from tkinter.ttk import Treeview, Widget, _format_optdict, _val_or_dict
from pynput import keyboard

class HotKeyTree(Treeview):
    
    def __init__(self, master=None, **kw):
        Widget.__init__(self, master, "ttk::treeview", kw)
        self._hotkeys = dict()
        self._listeners = dict()
    
    def clear(self):
        self.delete(*self.get_children())
    
    def delete(self, *items):
        self.tk.call(self._w, "delete", items)
        for item in items:
            self.remove_hotkey(item)
    
    def insert(self, parent, index, iid=None, hotkey=None, **kw):
        opts = _format_optdict(kw)
        if iid is not None:
            res = self.tk.call(self._w, "insert", parent, index,
                "-id", iid, *opts)
        else:
            res = self.tk.call(self._w, "insert", parent, index, *opts)
        self.set_hotkey(res, hotkey)
        return res
    
    def item(self, item, option=None, **kw):
        if option is not None:
            kw[option] = None
        out = _val_or_dict(self.tk, kw, self._w, "item", item)
        if option is None:
            out['hotkey'] = self._hotkeys[item]
        return out
    
    def set_hotkey(self, iid, hotkey):
        if iid in self._hotkeys:
            self.remove_hotkey(iid)
        self._hotkeys[iid] = hotkey
        if hotkey != None:
            if hotkey._on_activate is None:
                hotkey._on_activate = lambda: self.winfo_toplevel().play_entry(iid)
            self._listeners[iid] = keyboard.Listener(on_press=self.for_canonical(self._hotkeys[iid].press, iid), on_release=self.for_canonical(self._hotkeys[iid].release, iid))
            self._listeners[iid].start()
        else:
            self._listeners[iid] = None
    
    def remove_hotkey(self, iid):
        self._listeners[iid].stop()
        self._listeners.pop(iid)
        self._hotkeys.pop(iid)

    def for_canonical(self, f, iid):
        return lambda k: f(self._listeners[iid].canonical(k))