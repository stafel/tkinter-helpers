#!/usr/bin/env python3
#
# tkinter-helpers: enhance your tkinter expirience
# Copyright (C) 2023 Rafael Stauffer
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import tkinter as tk
from tkinter import ttk
from tkinter.constants import *

__doc__ = """
Simple table for data
"""


def get_readonly_row_generator(columns: int):
    """
    returns generator method for a read only row consisting of labels
    """

    def _generate_row(parent, row_position):
        widgets = []
        for column_position in range(columns):
            label = tk.Label(parent)
            label.grid(
                row=row_position, column=column_position, sticky=NSEW, padx=1, pady=1
            )
            widgets.append(label)
        return widgets

    return _generate_row


def get_input_row_generator(columns: int):
    """
    returns generator method for a input row consisting of entry text boxes
    """

    def _generate_row(parent, row_position):
        widgets = []
        for column_position in range(columns):
            label = tk.Entry(parent, justify="center")
            label.grid(
                row=row_position, column=column_position, sticky=NSEW, padx=1, pady=1
            )
            widgets.append(label)
        return widgets

    return _generate_row


class Table(tk.Frame):
    """
    Simple table for data
    """

    def __init__(self, parent, rows: int, row_generator):
        tk.Frame.__init__(self, parent)

        self.widgets = []
        self.rows = rows
        for row in range(rows):
            self.widgets.append(row_generator(parent=self, row_position=row))

    def add_row(self, row_generator):
        """
        Adds new row to table end from generator
        """

        self.rows += 1
        self.widgets.append(row_generator(parent=self, row_position=self.rows))

    def set(self, row: int, column: int, value):
        """
        Sets cell on position row column to value
        """

        widget = self.widgets[row][column]
        if isinstance(widget, tk.Label):
            widget.configure(text=value)
        elif isinstance(widget, tk.Entry):
            widget.delete(0, END)
            widget.insert(0, value)

    def get(self, row: int, column: int):
        """
        Returns value from cell on position row column
        """

        widget = self.widgets[row][column]
        if isinstance(widget, tk.Label):
            return widget.cget("text")
        if isinstance(widget, tk.Entry):
            return widget.get()

    def get_row(self, row: int):
        """
        Returns values as list for row
        """

        values = []
        for column in range(len(self.widgets[row])):
            values.append(self.get(row, column))
        return values


if __name__ == "__main__":

    class SampleApp(tk.Tk):
        """
        Sample tkinter app to demonstrate table
        """

        def __init__(self, *args, **kwargs):
            tk.Tk.__init__(self, *args, **kwargs)

            self.table = Table(self, 15, get_readonly_row_generator(3))
            self.table.add_row(get_input_row_generator(3))
            self.table.pack()
            self.label = ttk.Label(
                self, text="Buttons output values to console."
            )
            self.label.pack()

            for row in range(16):
                for column in range(3):
                    self.table.set(row, column, f"test {row} {column}")

            self.button = tk.Button(
                self, text="get pos 1,1", command=lambda: print(self.table.get(1, 1))
            )
            self.button.pack()

            self.button_end = tk.Button(
                self,
                text="get last row",
                command=lambda: print(self.table.get_row(self.table.rows - 1)),
            )
            self.button_end.pack()

    app = SampleApp()
    app.mainloop()
