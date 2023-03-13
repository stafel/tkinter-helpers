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
Table base functionality
"""

ROW = "row"


def get_readonly_row_generator(columns: int, **kwargs):
    """
    returns generator method for a read only row consisting of labels
    """

    def _generate_row(parent, row_position):
        widgets = []
        for column_position in range(columns):
            label = tk.Label(parent, **kwargs)
            label.grid(
                row=row_position, column=column_position, sticky=NSEW, padx=1, pady=1
            )
            widgets.append(label)
        return widgets

    return _generate_row


def get_title_row_generator(columns: int, **kwargs):
    """
    returns generator method for title row
    """

    return get_readonly_row_generator(columns, font=("Helvetica", 14, "bold"), **kwargs)


def get_input_row_generator(columns: int, **kwargs):
    """
    returns generator method for a input row consisting of entry text boxes
    """

    def _generate_row(parent, row_position):
        widgets = []
        for column_position in range(columns):
            label = tk.Entry(parent, **kwargs)
            label.grid(
                row=row_position, column=column_position, sticky=NSEW, padx=1, pady=1
            )
            widgets.append(label)
        return widgets

    return _generate_row


def get_input_row_generator_centered(columns: int, **kwargs):
    """
    returns generator method for a input row consisting of centered text entry text boxes
    """

    return get_input_row_generator(columns, justify="center", **kwargs)


class Table(tk.Frame):
    """
    Simple table for data
    """

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.widgets = []

    def get_row_count(self):
        """
        Returns number of rows
        """

        return len(self.widgets)

    def add_row(self, row_generator):
        """
        Adds new row to table end from generator
        """

        self.widgets.append(
            row_generator(parent=self, row_position=self.get_row_count() + 1)
        )

    def add_rows(self, number_of_rows: int, row_generator):
        """
        Adds a number of rows at the end of the table from generator
        """

        for _ in range(number_of_rows):
            self.add_row(row_generator)

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

        return ""

    def get_row(self, row: int):
        """
        Returns values as list for row
        """

        values = []
        for column in range(len(self.widgets[row])):
            values.append(self.get(row, column))
        return values

    def set_row(self, row: int, values):
        """
        Sets cells on row
        """

        for column, value in enumerate(values):
            self.set(row, column, value)

    def remove_row(self, row: int):
        """
        Deletes row and closes gap
        """

        for column in range(len(self.widgets[row])):
            self.widgets[row][column].destroy()

        del self.widgets[row]

        for follow_up_row in range(row, self.get_row_count()):
            for widget in self.widgets[
                follow_up_row
            ]:  # regrid all widgets to close gap in grid
                widget_position = widget.grid_info()
                widget_position[ROW] = (
                    follow_up_row + 1
                )  # remember tkinter grid begins at one
                widget.grid_forget()
                widget.grid(**widget_position)

    def insert_row(self, row: int, row_generator):
        """
        Inserts a row onto the position
        """

        for follow_up_row in range(row, self.get_row_count()):
            for widget in self.widgets[
                follow_up_row
            ]:  # regrid all widgets to close gap in grid
                widget_position = widget.grid_info()
                widget_position[ROW] = (
                    follow_up_row + 2
                )  # remember tkinter grid begins at one
                widget.grid_forget()
                widget.grid(**widget_position)

        new_row = row_generator(parent=self, row_position=row + 1)  # insert at grid pos
        self.widgets.insert(row, new_row)  # insert in our table

    def replace_row(self, row: int, row_generator):
        """
        Replaces row with another generated row
        """

        for column in range(len(self.widgets[row])):
            self.widgets[row][column].destroy()

        self.widgets[row] = row_generator(parent=self, row_position=row + 1)


if __name__ == "__main__":

    class SampleApp(tk.Tk):
        """
        Sample tkinter app to demonstrate table
        """

        def __init__(self, *args, **kwargs):
            tk.Tk.__init__(self, *args, **kwargs)

            self.table = Table(self)
            self.table.add_row(get_title_row_generator(3))
            self.table.add_rows(15, get_readonly_row_generator(3))
            self.table.add_row(get_input_row_generator_centered(3))
            self.table.pack()
            self.label = ttk.Label(self, text="Buttons output values to console.")
            self.label.pack()

            for row in range(17):
                for column in range(3):
                    self.table.set(row, column, f"test {row} {column}")

            self.button = tk.Button(
                self, text="get pos 1,1", command=lambda: print(self.table.get(1, 1))
            )
            self.button.pack()

            self.button_end = tk.Button(
                self,
                text="get last row",
                command=lambda: print(self.table.get_row(self.table.get_row_count() - 1)),
            )
            self.button_end.pack()

            self.button_del = tk.Button(
                self,
                text="delete row 2",
                command=lambda: self.table.remove_row(2),
            )
            self.button_del.pack()

    app = SampleApp()
    app.mainloop()
