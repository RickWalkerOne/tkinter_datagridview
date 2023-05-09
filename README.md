# tkinter_datagridview

tkinter_datagridview is a library for Python with a DataGridView

## Installation Avise

Don't have a pip installation

## Usage

```python
from datagridview import DataGridView, DataSourceVar
from tkinter import Tk


DataGridView
root = Tk()
root.title('Data Grid View')
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

__data = DataSourceVar(value=[{'name': 'example', 'age': 15, 'marriage': False},
                              {'name': 'Fulan', 'age': None, 'marriage': True}])
table = DataGridView(root, __data, 10)
table.grid(row=0, column=0, sticky='nsew')
mynewrow = {'name': 'new name', 'age': 0, 'marriage': True}
for x in range(10):
    __data.append(mynewrow)
__index = table.index(mynewrow)

root.mainloop()
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
