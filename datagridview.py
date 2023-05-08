import tkinter as tk
from CTkMessagebox import CTkMessagebox
from datasource import DataSourceVar
from typing import List


class DataGridView(tk.Frame):
    def __init__(self, master, data: DataSourceVar, max_rows: int, read_only=False,
                 headers_bg='#000000', headers_fg='#ffffff',
                 even_row_bg='#ffffff', even_row_fg='#000000',
                 odd_row_bg='#eeeeee', odd_row_fg='#000000',
                 true_string='True', false_string='False'):
        super().__init__(master)
        self._headers = list(data[0].keys())
        self.master = master
        self._max_rows = max_rows
        self._read_only = read_only
        self._data = data
        self._data.callable(self.update, 'all', True)
        self._num_rows = len(data)
        self._num_cols = len(data[0])
        self._true_string = true_string
        self._false_string = false_string
        self._cells = []

        # style variables:
        self._headers_bg = headers_bg
        self._headers_fg = headers_fg
        self._even_row_bg = even_row_bg
        self._even_row_fg = even_row_fg
        self._odd_row_bg = odd_row_bg
        self._odd_row_fg = odd_row_fg
        self._font_family = 'Arial'
        self._font_size = 10
        self._font_weight = 'normal'
        self._border_width = 1
        self._border_color = 'black'

        self._sort_order = None

        # Create the table header
        for col, key in enumerate(self._data[0].keys()):
            label = tk.Label(self,
                             text=key,
                             font=(self._font_family, self._font_size, self._font_weight),
                             bg=self._headers_bg,
                             fg=self._headers_fg,
                             highlightthickness=self._border_width,
                             highlightcolor=self._border_color,
                             relief='raised')
            label.grid(row=0, column=col, sticky='nswe')
            label.bind('<Button-1>', lambda event, col_=col: self.sort_column(col_))

        self._create_table()

        # Set the row and column weights
        self.columnconfigure(0, weight=1)
        for i in range(1, self._num_cols):
            self.columnconfigure(i, weight=2)
        for i in range(self._max_rows + 1):
            self.rowconfigure(i, weight=1)

    def _create_table(self):
        self._cells = []
        # Create the table _cells
        for row in range(self._max_rows):
            _test_ = row < self._num_rows
            row_cells = []
            is_even = row % 2 == 0
            for col in range(self._num_cols):
                cell_value = tk.StringVar(
                    value=self._revise_values(self._data[row][list(self._data[row].keys())[col]]) if _test_ else None)
                cell_entry = tk.Entry(self, textvariable=cell_value, justify='center',
                                      font=(self._font_family, self._font_size, self._font_weight),
                                      bg=self._even_row_bg if is_even else self._odd_row_bg,
                                      fg=self._even_row_fg if is_even else self._odd_row_fg,
                                      highlightthickness=self._border_width,
                                      highlightcolor=self._border_color,
                                      state=tk.DISABLED if self._read_only or not _test_ else tk.NORMAL)
                cell_entry.grid(row=row + 1, column=col, sticky='nswe')
                cell_entry.bind('<Return>', lambda event, row_=row, col_=col: self.save_cell(event, row_, col_))
                cell_entry.bind('<Escape>', lambda event, row_=row, col_=col: self.cancel_edit(event, row_, col_))
                row_cells.append(cell_value)
            self._cells.append(row_cells)

    def _revise_values(self, value, reverse=False):
        if not reverse:
            if isinstance(value, bool):
                return self._true_string if value else self._false_string
            if value is None:
                return ''
            return value
        else:
            if value is None or value.strip() == '':
                return None
            elif isinstance(value, str) and value.strip().lower() == self._true_string.lower():
                return True
            elif isinstance(value, str) and value.strip().lower() == self._false_string.lower():
                return False
            else:
                try:
                    return int(value)
                except:
                    return value

    def save_cell(self, event, row, col):
        value = self._revise_values(self._cells[row][col].get(), True)
        __value = self._data[row][self._headers[col]]
        if type(value) != type(__value):
            CTkMessagebox(title="Warning!",
                          message=f"Incorrect type! Please insert a valid value.\n\nCOD: <{type(value)}{type(__value)}>"
                          , icon="warning", option_1="Cancel")
            return
        self._data[row][list(self._data[row].keys())[col]] = value
        self.master.focus()

    def cancel_edit(self, event, row, col):
        value = self._data[row][list(self._data[row].keys())[col]]
        self._cells[row][col].set(self._revise_values(value))
        self.master.focus()

    def clear(self) -> None:
        for row in range(self._max_rows):
            for col in range(self._num_cols):
                cell_value = self._cells[row][col]
                cell_value.set('')
        if not self._read_only:
            __widget = self.grid_slaves()
            for widget in __widget:
                if isinstance(widget, tk.Entry):
                    widget.configure(state=tk.DISABLED)

    def _return_cells(self) -> List[tk.Entry]:
        __widget = self.grid_slaves()
        __entry_list = []
        for widget in __widget:
            if isinstance(widget, tk.Entry):
                __entry_list.append(widget)
        __entry_list.reverse()
        return __entry_list

    def update(self, event_arg1=None, event_arg2=None, event_arg3=None) -> None:
        self._num_rows = len(self._data)
        self.clear()
        entry_list = self._return_cells()
        for row in range(self._max_rows):
            _test_ = row < self._num_rows
            for col in range(self._num_cols):
                this_entry = entry_list[row * self._num_cols + col]
                this_entry.configure(state=tk.NORMAL)
                self._cells[row][col].set(
                    self._revise_values(self._data[row][list(self._data[row].keys())[col]]) if _test_ else '')
                this_entry.configure(state=tk.DISABLED if self._read_only or not _test_ else tk.NORMAL)

    def sort_column(self, col):
        if self._sort_order == col:
            self._sort_order = None
            reverse = True
        else:
            self._sort_order = col
            reverse = False
        # Sort the _data by the selected column
        __the_data = self._data
        __the_data.sort(key=lambda row_: row_[self._headers[col]], reverse=reverse)

        # Re-create the cell widgets with the sorted _data
        for row, row_data in enumerate(__the_data):
            for col, key in enumerate(self._headers):
                self._cells[row][col].set(row_data[key])

    def update_cells(self, sort_by=None):
        if sort_by:
            self._data.sort(key=sort_by)
        for row, row_data in enumerate(self._data):
            for col, cell_value in enumerate(row_data.values()):
                self._cells[row][col].set(cell_value)

    def cget(self, key: str):
        return getattr(self, '_' + key)

    def configure(self, **kwargs):
        for key, value in kwargs.items():
            # get the current value of the variable
            current_value = getattr(self, key)
            # check if the new value is different from the current value
            if current_value != value:
                # update the variable with the new value
                setattr(self, key, value)

                # update the table widget based on the variable that was changed
                if key == '_read_only':
                    # update the state of the Entry widgets
                    for i in range(1, self._num_rows):
                        for j in range(self._num_cols):
                            cell = self.grid_slaves(i, j)[0]
                            if isinstance(cell, tk.Entry):
                                if value:
                                    cell.config(state='readonly')
                                    cell.unbind('<Return>')
                                    cell.unbind('<Escape>')
                                else:
                                    cell.config(state='normal')
                                    cell.bind('<Return>', lambda event, row=i, col=j: self.save_cell(event, row, col))
                                    cell.bind('<Escape>', lambda event, row=i, col=j: self.cancel_edit(event, row, col))
                elif key == '_data':
                    # update the number of rows and columns
                    self._num_rows = len(value)
                    self._num_cols = len(self._headers)
                    # update the table widget with the new data
                    self.update_cells()
                elif key == '_headers':
                    # update the number of rows and columns
                    self._num_rows = len(self._data)
                    self._num_cols = len(value)
                    # update the table widget with the new headers
                    self.update_cells()
                elif key == '_sort_order':
                    self._sort_order = value
                    # sort the data based on the new sort order
                    self.sort_column(self._sort_order)
                    # update the table widget with the sorted data
                    self.update_cells()

    def _style_font(self, family=None, size=None, weight=None):
        if family:
            self._font_family = family
        if size:
            self._font_size = size
        if weight:
            self._font_weight = weight
        for row in range(1, self._num_rows):
            for col in range(self._num_cols):
                cell = self.grid_slaves(row, col)[0]
                if isinstance(cell, (tk.Entry, tk.Label)):
                    cell.configure(font=(self._font_family, self._font_size, self._font_weight))

    def _style_border(self, width=None, color=None):
        if width:
            self._border_width = width
        if color:
            self._border_color = color
        for row in range(1, self._num_rows):
            for col in range(self._num_cols):
                cell = self.grid_slaves(row, col)[0]
                if isinstance(cell, (tk.Entry, tk.Label)):
                    cell.configure(highlightthickness=self._border_width, highlightcolor=self._border_color)

    def style(self, **kwargs):
        for key, value in kwargs:
            if 'headers_bg' in key:
                self._headers_bg = value
            if 'headers_fg' in key:
                self._headers_fg = value
            if 'even_bg' in key:
                self._even_row_bg = value
            if 'even_fg' in key:
                self._even_row_fg = value
            if 'odd_bg' in key:
                self._odd_row_bg = value
            if 'odd_fg' in key:
                self._odd_row_fg = value
            if 'font' in key:
                self._style_font(**value)
            if 'border' in key:
                self._style_border(**value)

    def _update_style_config(self):
        for col in range(self._num_cols):
            cell = self.grid_slaves(0, col)[0]
            if isinstance(cell, tk.Label):
                cell.configure(bg=self._headers_bg, fg=self._headers_fg)

        for row in range(1, self._num_rows):
            for col in range(self._num_cols):
                cell = self.grid_slaves(row, col)[0]
                if isinstance(cell, tk.Entry):
                    if row % 2 == 0:
                        cell.configure(bg=self._even_row_bg, fg=self._even_row_bg)
                    else:
                        cell.configure(bg=self._odd_row_bg, fg=self._odd_row_bg)

    def index(self, row):
        # Get all the widgets in the grid
        slaves = self.grid_slaves()
        slaves.reverse()

        # Loop over all the widgets in the grid
        __will_return = []
        for i, widget in enumerate(slaves):
            j = i
            while j >= len(self._headers):
                j -= len(self._headers)
            # Check if the widget is an Entry widget and has the same values as the given row
            if isinstance(widget, tk.Entry) and self._revise_values(widget.get(), True) == row[self._headers[j]]:
                __will_return.append(True)
            else:
                __will_return.append(False)
            if len(__will_return) == len(self._headers):
                if False not in __will_return:
                    return (i // len(self._headers)) - 1  # Return the index of the row if it exists
                else:
                    __will_return.clear()

        # Return -1 if the row doesn't exist
        return -1

    def find(self, index):
        if not 0 <= index < self._num_rows:
            return None
        values = {}
        for i, header in enumerate(self._headers):
            cell = self.grid_slaves(row=index + 1, column=i)[0]
            if isinstance(cell, tk.Entry):
                values[header] = self._revise_values(cell.get(), True)
        return values


# Example usage
if __name__ == '__main__':
    root = tk.Tk()
    root.title('Data Grid View')

    __data = DataSourceVar(value=[{'name': 'example', 'age': 15, 'marriage': False}, {'name': 'Fulan', 'age': None, 'marriage': True}])
    table = DataGridView(root, __data, 10)
    table.pack(expand=True, fill='both')
    mynewrow = {'name': 'new name', 'age': 0, 'marriage': True}
    for x in range(10):
        __data.append(mynewrow)
    __index = table.index(mynewrow)

    root.mainloop()
