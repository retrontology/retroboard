from pynput.keyboard import KeyCode, Key, HotKey, Listener, _NORMAL_MODIFIERS

class RetroHotKey(HotKey):

    def __init__(self, keys, on_activate):
        self._state = set()
        self._keys = set(keys)
        self._vks = set()
        for key in self._keys:
            if type(key) == KeyCode:
                self._vks.add(key.vk)
            else:
                self._vks.add(key.value.vk)
        self._on_activate = on_activate

    def press(self, key):
        if type(key) == KeyCode:
            value = key.vk
        else:
            value = key.value.vk
        if value in self._vks and value not in self._state:
            self._state.add(value)
            if self._state == self._vks:
                self._on_activate()

    def release(self, key):
        if type(key) == KeyCode:
            value = key.vk
        else:
            value = key.value.vk
        if value in self._state:
            self._state.remove(value)


class RetroListener(Listener):
    def canonical(self, key):
        from pynput.keyboard import Key, KeyCode, _NORMAL_MODIFIERS
        if isinstance(key, KeyCode) and key.char is not None:
            return KeyCode(char=key.char.lower(), vk=key.vk)
        elif isinstance(key, Key) and key.value in _NORMAL_MODIFIERS:
            return key.value
        else:
            return key
