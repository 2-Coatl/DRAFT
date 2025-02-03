import tkinter as tk
from tkinter import ttk


class ScrolledFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        # Create a canvas
        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)

        # Create the scrollable frame inside the canvas
        self.scrollable_frame = ttk.Frame(self.canvas)

        # Configure the canvas
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Add the frame to the canvas
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Configure canvas scroll area when window is resized
        self.canvas.bind('<Configure>', self._on_canvas_configure)

        # Configure mouse wheel scrolling
        self.scrollable_frame.bind('<Enter>', self._bind_mouse_scroll)
        self.scrollable_frame.bind('<Leave>', self._unbind_mouse_scroll)

        # Layout
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Configure the canvas to update the scroll region
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

    def _on_canvas_configure(self, event):
        # Update the width of the frame to fill the canvas
        self.canvas.itemconfig(self.canvas_frame, width=event.width)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _bind_mouse_scroll(self, event):
        # Bind for Windows and MacOS
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        # Bind for Linux
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

    def _unbind_mouse_scroll(self, event):
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")