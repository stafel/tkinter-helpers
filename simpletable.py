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

        self.table.add_row(get_title_row_generator(0))  # to mark the title row

        self.footer = tk.Frame(self.interior)
        self.footer.pack(side=BOTTOM)

        self.new_button = tk.Button(self.footer, text="New", command=self._add_row)
        self.new_button.pack()

        self.right_click_menu = tk.Menu(self.interior)
        self.right_click_menu.add_command(label="New", command=self._add_row)
        self.right_click_menu.add_command(label="Delete", command=self._delete_row)

        # dynamic bind right mouse to open menu
        self.interior.bind(
            "<Enter>", lambda event: self.canvas.bind_all("<Button-3>", self._show_menu)
        )
        self.interior.bind(
            "<Leave>", lambda event: self.canvas.unbind_all("<Button-3>")
        )

        self.read_only = read_only
        self.new_row_generator = None

        self.selected_widget = None

    def _show_menu(self, event):
        self.selected_widget = event.widget  # save widget for later use in delete
        try:
            self.right_click_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.right_click_menu.grab_release()

    def set_title(self, title_texts):
        """
        Generates title row with title texts
        """

        self.table.replace_row(0, get_title_row_generator(len(title_texts)))
        self.table.set_row(0, title_texts)

    def set_data(self, data_rows):
        """
        Generates read only rows for data rows
        """

        columns = len(data_rows[0])

        # we define the row generator here to share with the new button
        def _row_generator():
            if self.read_only:
                self.table.add_row(get_readonly_row_generator(columns))
            else:
                self.table.add_row(get_input_row_generator_centered(columns))

        self.new_row_generator = _row_generator

        for row in data_rows:
            self.new_row_generator()
            self.table.set_row(self.table.rows - 1, row)

    def _add_row(self):
        if self.new_row_generator is None:
            return

        self.new_row_generator()

    def get_selected_row(self):
        """
        Returns selected row
        """

        if self.selected_widget is None:
            return -1

        return (
            self.selected_widget.grid_info()["row"] - 1
        )  # need to subtract one to get the right row in the list

    def _delete_row(self):
        selected_row = self.get_selected_row()

        if selected_row < 1:  # prevent deletion of title
            return

        self.table.remove_row(selected_row)


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
