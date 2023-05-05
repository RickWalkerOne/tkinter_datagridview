import tkinter as tk


class DataSourceVar(tk.Variable):
    def __init__(self, master=None, value=None, name=None):
        super().__init__(master, value, name)
        self._value = value if value is not None else []
        self.trace("w", self._update_observers)

    def get(self):
        return self._value

    def set(self, value):
        self._value = value
        self._update_observers('set', None)

    def append(self, item):
        self._value.append(item)
        self._update_observers('append', item)

    def remove(self, item):
        self._value.remove(item)
        self._update_observers('remove', item)

    def insert(self, index, item):
        self._value.insert(index, item)
        self._update_observers('insert', item)

    def _update_observers(self, operation, item):
        message = f'{operation} was performed'
        if item:
            message += f' on item {item}'
        self._tk.call(*(self._w, 'set', self._value, message))


if __name__ == '__main__':
    root = tk.Tk()
