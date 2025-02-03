import tkinter as tk
from ui.styles.colors import ColorScheme


class StyledButton(tk.Button):
    def __init__(self, master, **kwargs):
        # Extract custom style parameters
        button_type = kwargs.pop('button_type', 'primary')

        # Configure default styling
        style_config = self._get_style_config(button_type)
        kwargs.update(style_config)

        super().__init__(master, **kwargs)

        # Bind hover events
        self.bind('<Enter>', lambda e: self._on_hover(e, button_type))
        self.bind('<Leave>', lambda e: self._on_leave(e, button_type))

    def _get_style_config(self, button_type):
        if button_type == 'primary':
            return {
                'background': ColorScheme.PRIMARY,
                'foreground': 'white',
                'font': ('Arial', 10),
                'relief': 'flat',
                'padx': 15,
                'pady': 5
            }
        elif button_type == 'secondary':
            return {
                'background': ColorScheme.SECONDARY,
                'foreground': 'black',
                'font': ('Arial', 10),
                'relief': 'flat',
                'padx': 15,
                'pady': 5
            }
        return {}

    def _on_hover(self, event, button_type):
        if button_type == 'primary':
            self.configure(background=ColorScheme.PRIMARY_HOVER)
        elif button_type == 'secondary':
            self.configure(background=ColorScheme.SECONDARY_HOVER)

    def _on_leave(self, event, button_type):
        style_config = self._get_style_config(button_type)
        self.configure(background=style_config['background'])