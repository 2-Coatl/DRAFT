import tkinter as tk
from tkinter import ttk
from ui.config.settings import AppSettings


class ColumnHeader(tk.Frame):
    def __init__(
            self,
            parent,
            text,
            sortable=False,
            sort_command=None,
            width=None,
            **kwargs
    ):
        super().__init__(parent, **kwargs)

        # Store attributes
        self.sort_command = sort_command
        self.sort_direction = None  # None, 'asc', or 'desc'

        # Configure frame
        self.configure(
            style='Header.TFrame',
            padding=(AppSettings.PADDING['small'], 2)
        )

        # Create header label
        self.label = ttk.Label(
            self,
            text=text,
            font=AppSettings.get_font('header'),
            style='Header.TLabel'
        )
        self.label.pack(side='left')

        # If sortable, add sort indicator and bind click event
        if sortable:
            self.sort_indicator = ttk.Label(
                self,
                text='',
                font=AppSettings.get_font('default'),
                style='Header.TLabel'
            )
            self.sort_indicator.pack(side='left', padx=(2, 0))

            # Bind click events
            self.label.bind('<Button-1>', self._on_click)
            self.sort_indicator.bind('<Button-1>', self._on_click)

            # Change cursor to indicate clickable
            self.label.configure(cursor='hand2')
            self.sort_indicator.configure(cursor='hand2')

        # Set width if provided
        if width:
            self.configure(width=width)

    def _on_click(self, event):
        if not self.sort_command:
            return

        # Toggle sort direction
        if self.sort_direction is None:
            self.sort_direction = 'asc'
        elif self.sort_direction == 'asc':
            self.sort_direction = 'desc'
        else:
            self.sort_direction = None

        # Update sort indicator
        self._update_sort_indicator()

        # Call sort command
        if self.sort_command:
            self.sort_command(self.sort_direction)

    def _update_sort_indicator(self):
        if self.sort_direction == 'asc':
            self.sort_indicator.configure(text='▲')
        elif self.sort_direction == 'desc':
            self.sort_indicator.configure(text='▼')
        else:
            self.sort_indicator.configure(text='')