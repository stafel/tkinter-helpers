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
from tkinter.constants import *
from scrollframe import ScrolledFrame
from table import (
    Table,
    get_title_row_generator,
    get_readonly_row_generator,
    get_input_row_generator_centered,
)

__doc__ = """
Simple table for data
"""


class SimpleTable(ScrolledFrame):
    """
    Simple scrollable table
    """

    def __init__(self, parent, read_only: bool = True):
        ScrolledFrame.__init__(self, parent)

        self.table = Table(self.interior)
        self.table.pack()

        self.read_only = read_only

    def set_title(self, title_texts):
        """
        Generates title row with title texts
        """

        self.table.add_row(get_title_row_generator(len(title_texts)))
        self.table.set_row(self.table.rows - 1, title_texts)

    def set_data(self, data_rows):
        """
        Generates read only rows for data rows
        """

        for row in data_rows:
            columns = len(row)
            if self.read_only:
                self.table.add_row(get_readonly_row_generator(columns))
            else:
                self.table.add_row(get_input_row_generator_centered(columns))
            self.table.set_row(self.table.rows - 1, row)


if __name__ == "__main__":

    class SampleApp(tk.Tk):
        """
        Sample tkinter app to demonstrate simple table
        """

        def __init__(self, *args, **kwargs):
            tk.Tk.__init__(self, *args, **kwargs)

            self.table = SimpleTable(self, read_only=False)
            self.table.pack()

            self.table.set_title(["a", "b", "c"])
            self.table.set_data(
                [["one", "two", "three"], ["eins", "zwei", "drei"], ["I", "II", "III"]]
            )

    app = SampleApp()
    app.mainloop()
