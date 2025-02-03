import tkinter as tk
from tkinter import ttk
from ui.components.styled_button import StyledButton
from ui.config.settings import AppSettings


class CustomDialog(tk.Toplevel):
    def __init__(
            self,
            parent,
            title,
            message,
            button_labels=None,
            dialog_type='info'
    ):
        super().__init__(parent)

        # Dialog configuration
        self.title(title)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        # Default button labels if none provided
        if button_labels is None:
            button_labels = ['Aceptar']

        # Store the result
        self.result = None

        # Main frame
        main_frame = ttk.Frame(self, padding=AppSettings.PADDING['large'])
        main_frame.pack(expand=True, fill='both')

        # Message
        message_label = ttk.Label(
            main_frame,
            text=message,
            wraplength=300,
            justify='left',
            font=AppSettings.get_font('default')
        )
        message_label.pack(pady=AppSettings.PADDING['medium'])

        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=AppSettings.PADDING['medium'])

        # Create buttons
        for i, label in enumerate(button_labels):
            button_type = 'primary' if i == 0 else 'secondary'
            StyledButton(
                button_frame,
                text=label,
                command=lambda x=i: self.button_click(x),
                button_type=button_type
            ).pack(side='left', padx=AppSettings.PADDING['small'])

        # Center the dialog on parent window
        self.center_on_parent()

        # Set focus on dialog
        self.focus_set()

    def button_click(self, value):
        self.result = value
        self.destroy()

    def center_on_parent(self):
        self.update_idletasks()
        parent = self.master

        # Get parent geometry
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()

        # Calculate position
        width = self.winfo_width()
        height = self.winfo_height()
        x = parent_x + (parent_width - width) // 2
        y = parent_y + (parent_height - height) // 2

        # Set position
        self.geometry(f'+{x}+{y}')