from os import stat
from tkinter.ttk import Treeview, Widget, _format_optdict, _val_or_dict
from pynput import keyboard
from hotkeylistener import HotkeyScope

class HotKeyTree(Treeview):
    
    def __init__(self, master=None, **kw):
        Widget.__init__(self, master, "ttk::treeview", kw)
        self.root = self.winfo_toplevel()

    def clear(self):
        self.delete(*self.get_children())
    
    def delete(self, *items):
        self.tk.call(self._w, "delete", items)
        for item in items:
            self.root.hotkey_listener.remove_hotkey(item, HotkeyScope.TABLE)
    
    def insert(self, parent, index, iid=None, hotkey=None, **kw):
        opts = _format_optdict(kw)
        if iid is not None:
            res = self.tk.call(self._w, "insert", parent, index,
                "-id", iid, *opts)
        else:
            res = self.tk.call(self._w, "insert", parent, index, *opts)
        self.root.hotkey_listener.set_hotkey(res, hotkey, HotkeyScope.TABLE)
        return res
    
    def item(self, item, option=None, **kw):
        if option is not None:
            kw[option] = None
        out = _val_or_dict(self.tk, kw, self._w, "item", item)
        if option is None:
            out['hotkey'] = self.root.hotkey_listener._table_hotkeys[item]
        return out