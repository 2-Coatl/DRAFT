#import ui.themeengine as ttk
from ui.themeengine.widgets.dialogs.base import Dialog
#from ui.themeengine.localization import MessageCatalog


class MessageDialog(Dialog): # (message_dialog)
    """A simple modal dialog class that can be used to build simple
    message dialogs.

    Displays a message and a set of buttons. Each of the buttons in the
    message window is identified by a unique symbolic name. After the
    message window is popped up, the message box awaits for the user to
    select one of the buttons. Then it returns the symbolic name of the
    selected button. Use a `Toplevel` widget for more advanced modal
    dialog designs.
    """
