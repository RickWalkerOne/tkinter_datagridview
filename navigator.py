import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from typing import Callable, Optional


class Navigator(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self._callbacks = []

        self._last_page_var = tk.StringVar()
        self._begin_page_var = tk.StringVar()
        self._current_page_var = tk.StringVar()

        self._begin_label = ttk.Label(self, textvariable=self._begin_page_var)
        self._begin_button = ttk.Button(self, text='|<', command=self.goto_beginning)
        self._previous_button = ttk.Button(self, text='<', command=self.goto_previous)
        self._entry = ttk.Entry(self, textvariable=self._current_page_var)
        self._next_button = ttk.Button(self, text='>', command=self.goto_next)
        self._end_button = ttk.Button(self, text='>|', command=self.goto_end)
        self._end_label = ttk.Label(self, textvariable=self._last_page_var)

        self._entry.bind('<Return>', self.goto_page)

    def goto_beginning(self):
        self._current_page_var.set(self._begin_page_var.get())
        self._refresh()

    def goto_previous(self):
        current_page = int(self._current_page_var.get())
        if current_page > 1:
            self._current_page_var.set(str(current_page - 1))
            self._refresh()

    def goto_next(self):
        current_page = int(self._current_page_var.get())
        if current_page < int(self._last_page_var.get()):
            self._current_page_var.set(str(current_page + 1))
            self._refresh()

    def goto_end(self):
        self._current_page_var.set(self._last_page_var.get())
        self._refresh()

    def goto_page(self, event=None):
        try:
            page = int(self._current_page_var.get())
            if page < 1 or page > int(self._last_page_var.get()):
                raise ValueError
            self._refresh()
        except ValueError:
            messagebox.showerror('Invalid Page', 'Please enter a valid page number.')

    def _refresh(self):
        for func in self._callbacks:
            func()

    def trace(self, func: Callable[[...], ...], add: Optional[bool] = False):
        if add:
            self._callbacks.append(func)
        else:
            self._callbacks = [func]