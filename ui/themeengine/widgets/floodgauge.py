import ui.themeengine as ttk
import ui.themeengine as tk
from ui.themeengine.utils.constants import *


class Floodgauge(ttk.Progressbar):
    """A widget that shows the status of a long-running operation
    with an optional text indicator.

    Similar to the `ttk.Progressbar`, this widget can operate in
    two modes. *determinate* mode shows the amount completed
    relative to the total amount of work to be done, and
    *indeterminate* mode provides an animated display to let the
    user know that something is happening.

    Variable are generated automatically for this widget and can be
    linked to other widgets by referencing them via the
    `textvariable` and `variable` attributes.


    Examples:

        ```python
        import themeengine as ttk
        from themeengine.constants import *

        app = ttk.Window(size=(500, 500))

        gauge = ttk.Floodgauge(
            bootstyle=INFO,
            font=(None, 24, 'bold'),
            mask='Memory Used {}%',
        )
        gauge.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        # autoincrement the gauge
        gauge.start()

        # stop the autoincrement
        gauge.stop()

        # manually update the gauge value
        gauge.configure(value=25)

        # increment the value by 10 steps
        gauge.step(10)

        app.mainloop()
        ```
    """

    def __init__(
        self,
        master=None,
        cursor=None,
        font=None,
        length=None,
        maximum=100,
        mode=DETERMINATE,
        orient=HORIZONTAL,
        bootstyle=PRIMARY,
        takefocus=False,
        text=None,
        value=0,
        mask=None,
        **kwargs,
    ):
        """
        Parameters:

            master (Widget, optional):
                Parent widget. Defaults to None.

            cursor (str, optional):
                The cursor that will appear when the mouse is over the
                progress bar. Defaults to None.

            font (Union[Font, str], optional):
                The font to use for the progress bar label.

            length (int, optional):
                Specifies the length of the long axis of the progress bar
                (width if orient = horizontal, height if if vertical);

            maximum (float, optional):
                A floating point number specifying the maximum `value`.
                Defaults to 100.

            mode ('determinate', 'indeterminate'):
                Use `indeterminate` if you cannot accurately measure the
                relative progress of the underlying process. In this mode,
                a rectangle bounces back and forth between the ends of the
                widget once you use the `Floodgauge.start()` method.
                Otherwise, use `determinate` if the relative progress can be
                calculated in advance.

            orient ('horizontal', 'vertical'):
                Specifies the orientation of the widget.

            bootstyle (str, optional):
                The style used to render the widget. Options include
                primary, secondary, success, info, warning, danger, light,
                dark.

            takefocus (bool, optional):
                This widget is not included in focus traversal by default.
                To add the widget to focus traversal, use
                `takefocus=True`.

            text (str, optional):
                A string of text to be displayed in the Floodgauge label.
                This is assigned to the attribute `Floodgauge.textvariable`

            value (float, optional):
                The current value of the progressbar. In `determinate`
                mode, this represents the amount of work completed. In
                `indeterminate` mode, it is interpreted modulo `maximum`;
                that is, the progress bar completes one "cycle" when the
                `value` increases by `maximum`.

            mask (str, optional):
                A string format that can be used to update the Floodgauge
                label every time the value is updated. For example, the
                string "{}% Storage Used" with a widget value of 45 would
                show "45% Storage Used" on the Floodgauge label. If a
                mask is set, then the `text` option is ignored.

            **kwargs:
                Other configuration options from the option database.
        """
        # progress bar value variables
        if 'variable' in kwargs:
            self._variable = kwargs.pop('variable')
        else:
            self._variable = tk.IntVar(value=value)
        if 'textvariable' in kwargs:
            self._textvariable = kwargs.pop('textvariable')
        else:
            self._textvariable = tk.StringVar(value=text)
        self._bootstyle = bootstyle
        self._font = font or "helvetica 10"
        self._mask = mask
        self._traceid = None

        super().__init__(
            master=master,
            class_="Floodgauge",
            cursor=cursor,
            length=length,
            maximum=maximum,
            mode=mode,
            orient=orient,
            bootstyle=bootstyle,
            takefocus=takefocus,
            variable=self._variable,
            **kwargs,
        )
        self._set_widget_text(self._textvariable.get())
        self.bind("<<ThemeChanged>>", self._on_theme_change)
        self.bind("<<Configure>>", self._on_theme_change)

        if self._mask is not None:
            self._set_mask()

    def _set_widget_text(self, *_):
        ttkstyle = self.cget("style")
        if self._mask is None:
            text = self._textvariable.get()
        else:
            value = self._variable.get()
            text = self._mask.format(value)
        self.tk.call("ttk::style", "configure", ttkstyle, "-text", text)
        self.tk.call("ttk::style", "configure", ttkstyle, "-font", self._font)

    def _set_mask(self):
        if self._traceid is None:
            self._traceid = self._variable.trace_add(
                "write", self._set_widget_text
            )

    def _unset_mask(self):
        if self._traceid is not None:
            self._variable.trace_remove("write", self._traceid)
        self._traceid = None

    def _on_theme_change(self, *_):
        text = self._textvariable.get()
        self._set_widget_text(text)

    def _configure_get(self, cnf):
        if cnf == "value":
            return self._variable.get()
        if cnf == "text":
            return self._textvariable.get()
        if cnf == "bootstyle":
            return self._bootstyle
        if cnf == "mask":
            return self._mask
        if cnf == "font":
            return self._font
        else:
            return super(ttk.Progressbar, self).configure(cnf=cnf)

    def _configure_set(self, **kwargs):
        if "value" in kwargs:
            self._variable.set(kwargs.pop("value"))
        if "text" in kwargs:
            self._textvariable.set(kwargs.pop("text"))
        if "bootstyle" in kwargs:
            self._bootstyle = kwargs.get("bootstyle")
        if "mask" in kwargs:
            self._mask = kwargs.pop("mask")
        if "font" in kwargs:
            self._font = kwargs.pop("font")
        if "variable" in kwargs:
            self._variable = kwargs.get("variable")
            ttk.Progressbar.configure(self, cnf=None, **kwargs)
        if "textvariable" in kwargs:
            self.textvariable = kwargs.pop("textvariable")
        else:
            ttk.Progressbar.configure(self, cnf=None, **kwargs)

    def __getitem__(self, key: str):
        return self._configure_get(cnf=key)

    def __setitem__(self, key: str, value):
        self._configure_set(**{key: value})

    def configure(self, cnf=None, **kwargs):
        """Configure the options for this widget.

        Parameters:

            cnf (Dict[str, Any], optional):
                A dictionary of configuration options.

            **kwargs:
                Optional keyword arguments.
        """
        if cnf is not None:
            return self._configure_get(cnf)
        else:
            self._configure_set(**kwargs)

    @property
    def textvariable(self):
        """Returns the textvariable object"""
        return self._textvariable

    @textvariable.setter
    def textvariable(self, value):
        """Set the new textvariable property"""
        self._textvariable = value
        self._set_widget_text(self._textvariable.get())

    @property
    def variable(self):
        """Returns the variable object"""
        return self._variable

    @variable.setter
    def variable(self, value):
        """Set the new variable object"""
        self._variable = value
        if self.cget('variable') != value:
            self.configure(variable=self._variable)