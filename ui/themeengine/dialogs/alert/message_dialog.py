import textwrap
import ui.themeengine as ttk
from ui.themeengine.utils.constants import *
from ui.themeengine import Dialog
from ui.themeengine.localization import MessageCatalog


class MessageDialog(Dialog):
    """A simple modal dialog class that can be used to build simple
    message dialogs.

    Displays a message and a set of buttons. Each of the buttons in the
    message window is identified by a unique symbolic name. After the
    message window is popped up, the message box awaits for the user to
    select one of the buttons. Then it returns the symbolic name of the
    selected button. Use a `Toplevel` widget for more advanced modal
    dialog designs.
    """

    def __init__(
        self,
        message,
        title=" ",
        buttons=None,
        command=None,
        width=50,
        parent=None,
        alert=False,
        default=None,
        padding=(20, 20),
        icon=None,
        **kwargs,
    ):
        """
        Parameters:

            message (str):
                A message to display in the message box.

            title (str):
                The string displayed as the title of the message box.
                This option is ignored on Mac OS X, where platform
                guidelines forbid the use of a title on this kind of
                dialog.

            buttons (List[str]):
                A list of buttons to appear at the bottom of the popup
                messagebox. The buttons can be a list of strings which
                will define the symbolic name and the button text.
                `['OK', 'Cancel']`. Alternatively, you can assign a
                bootstyle to each button by using the colon to separate the
                button text and the bootstyle. If no colon is found, then
                the style is set to 'primary' by default.
                `['OK:success','Cancel:danger']`.

            command (Tuple[Callable, str]):
                The function to invoke when the user closes the dialog.
                The actual command is a tuple that consists of the
                function to call and the symbolic name of the button that
                closes the dialog.

            width (int):
                The maximum number of characters per line in the message.
                If the text stretches beyond the limit, the line will break
                at the word.

            parent (Widget):
                Makes the window the logical parent of the message box.
                The messagebox is displayed on top of its parent window.

            alert (bool):
                Ring the display's bell when the dialog is shown.

            default (str):
                The symbolic name of the default button. The default
                button is invoked when the the <Return> key is pressed.
                If no default is provided, the right-most button in the
                button list will be set as the default.,

            padding  (Union[int, Tuple[int]]):
                The amount of space between the border and the widget
                contents.

            icon (str):
                An image path, path-like object or image data to be
                displayed to the left of the text.

            **kwargs (Dict):
                Other optional keyword arguments.

        Example:

            ```python
            root = tk.Tk()

            md = MessageDialog("Displays a message with buttons.")
            md.show()
            ```
        """
        super().__init__(parent, title, alert)
        self._message = message
        self._command = command
        self._width = width
        self._alert = alert
        self._default = default
        self._padding = padding
        self._icon = icon
        self._localize = kwargs.get("localize")

        if buttons is None:
            self._buttons = [
                f"{MessageCatalog.translate('Cancel')}:secondary",
                f"{MessageCatalog.translate('OK')}:primary",
            ]
        else:
            self._buttons = buttons

    def create_body(self, master):
        """Overrides the parent method; adds the message section."""
        container = ttk.Frame(master, padding=self._padding)
        if self._icon:
            try:
                # assume this is image data
                self._img = ttk.PhotoImage(data=self._icon)
                icon_lbl = ttk.Label(container, image=self._img)
                icon_lbl.pack(side=LEFT, padx=5)
            except:
                try:
                    # assume this is a file path
                    self._img = ttk.PhotoImage(file=self._icon)
                    icon_lbl = ttk.Label(container, image=self._img)
                    icon_lbl.pack(side=LEFT, padx=5)
                except:
                    # icon is neither data nor a valid file path
                    print("MessageDialog icon is invalid")

        if self._message:
            for msg in self._message.split("\n"):
                message = "\n".join(textwrap.wrap(msg, width=self._width))
                message_label = ttk.Label(container, text=message)
                message_label.pack(pady=(0, 3), fill=X, anchor=N)
        container.pack(fill=X, expand=True)

    def create_buttonbox(self, master):
        """Overrides the parent method; adds the message buttonbox"""
        frame = ttk.Frame(master, padding=(5, 5))

        button_list = []

        for i, button in enumerate(self._buttons[::-1]):
            cnf = button.split(":")
            if len(cnf) == 2:
                text, bootstyle = cnf
            else:
                text = cnf[0]
                bootstyle = "secondary"

            if self._localize == True:
                text = MessageCatalog.translate(text)

            btn = ttk.Button(frame, bootstyle=bootstyle, text=text)
            btn.configure(command=lambda b=btn: self.on_button_press(b))
            btn.pack(padx=2, side=RIGHT)
            btn.lower()  # set focus traversal left-to-right
            button_list.append(btn)

            if self._default is not None and text == self._default:
                self._initial_focus = btn
            elif self._default is None and i == 0:
                self._initial_focus = btn

        # bind default button to return key press and set focus
        self._toplevel.bind("<Return>", lambda _, b=btn: b.invoke())
        self._toplevel.bind("<KP_Enter>", lambda _, b=btn: b.invoke())

        ttk.Separator(self._toplevel).pack(fill=X)
        frame.pack(side=BOTTOM, fill=X, anchor=S)

        if not self._initial_focus:
            self._initial_focus = button_list[0]

    def on_button_press(self, button):
        """Save result, destroy the toplevel, and execute command."""
        self._result = button["text"]
        command = self._command
        if command is not None:
            command()
        self._toplevel.destroy()

    def show(self, position=None):
        """Create and display the popup messagebox."""
        super().show(position)
