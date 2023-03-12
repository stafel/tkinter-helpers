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
Scrolled frame based on https://web.archive.org/web/20170514022131id_/http://tkinter.unpythonic.net/wiki/VerticalScrolledFrame
"""


class ScrolledFrame(ttk.Frame):
    """
    Frame with scrollbar
    Use interior to add child elements
    Based on https://web.archive.org/web/20170514022131id_/http://tkinter.unpythonic.net/wiki/VerticalScrolledFrame
    """

    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)

        # create canvas and scrollbar for it
        vertical_scrollbar = ttk.Scrollbar(self, orient=VERTICAL)
        vertical_scrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)

        self.canvas = tk.Canvas(
            self, bd=0, highlightthickness=0, yscrollcommand=vertical_scrollbar.set
        )
        self.canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)

        vertical_scrollbar.config(command=self.canvas.yview)

        # reset the view to pos 0,0
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # create frame inside canvas which will be scrolled
        self.interior = ttk.Frame(self.canvas)
        interior_id = self.canvas.create_window(0, 0, window=self.interior, anchor=NW)

        # track changes to canvas and frame width and sync them, update scrollbar
        def _configure_interior(event):
            # update scrollbar size to match frame
            size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
            self.canvas.config(scrollregion=f"0 0 {size[0]} {size[1]}")

            if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
                # update with of canvas to fit inner frame
                self.canvas.config(width=self.interior.winfo_reqwidth())

        self.interior.bind("<Configure>", _configure_interior)

        def _configure_canvas(event):
            if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
                # update inner frame width to fill canvas
                self.canvas.itemconfigure(interior_id, width=self.canvas.winfo_width())

        self.canvas.bind("<Configure>", _configure_canvas)

        # dynamic bind scroll wheel if mouse over
        self.interior.bind("<Enter>", self._bind_mousewheel)
        self.interior.bind("<Leave>", self._unbind_mousewheel)

    def _on_scroll(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), UNITS)

    def _scroll_down(self, event):
        self.canvas.yview_scroll(1, UNITS)

    def _scroll_up(self, event):
        self.canvas.yview_scroll(-1, UNITS)

    def _bind_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_scroll)

        # X11 compatibility
        self.canvas.bind_all("<Button-4>", self._scroll_up)
        self.canvas.bind_all("<Button-5>", self._scroll_down)

    def _unbind_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

        # X11 compatibility
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")


if __name__ == "__main__":

    class SampleApp(tk.Tk):
        """
        Sample tkinter app to demonstrate scrolling
        """

        def __init__(self, *args, **kwargs):
            tk.Tk.__init__(self, *args, **kwargs)

            self.frame = ScrolledFrame(None)
            self.frame.pack()
            self.label = ttk.Label(
                self, text="Shrink the window to activate the scrollbar."
            )
            self.label.pack()
            buttons = []
            for i in range(10):
                buttons.append(ttk.Button(self.frame.interior, text="Button " + str(i)))
                buttons[-1].pack()

    app = SampleApp()
    app.mainloop()
