import ui.themeengine as ttk
from ui.themeengine import Bootstyle
from ui.themeengine.core.color import Colors
from ui.themeengine.utils.constants import *
from ui.themeengine.utils import utility

# floodgauge imports
import math

# meter imports
from PIL import Image, ImageTk, ImageDraw


# Valor para multiplicar la resolución de la imagen para suavizar el dibujo
M = 3  # Esta constante podría estar en otro lugar del framework, ajústala según sea necesario

class Meter(ttk.Frame):
    """Un medidor radial que puede usarse para mostrar el progreso de operaciones
    de larga duración o la cantidad de trabajo completado; también puede usarse
    como un dial cuando se configura como `interactive=True`.

    Este widget es muy flexible. Hay dos tipos principales de medidores
    que pueden establecerse con el parámetro `metertype`: 'full' y
    'semi', que muestran el arco del medidor en un círculo completo o
    semicírculo. También puede personalizar el arco del círculo con
    los parámetros `arcrange` y `arcoffset`.

    El indicador del medidor puede mostrarse como un color sólido o con
    rayas usando el parámetro `stripethickness`. Por defecto, el
    `stripethickness` es 0, lo que resulta en un indicador de medidor sólido.
    Un `stripethickness` mayor resulta en cuñas más grandes
    alrededor del arco del medidor.

    Existen varias opciones de texto y etiqueta. El texto central y
    el indicador del medidor se formatean con el parámetro `meterstyle`.
    Puede establecer texto a la izquierda y derecha de esta etiqueta central
    usando los parámetros `textleft` y `textright`. Esto se usa más
    comúnmente para '$', '%', u otros símbolos similares.

    Si necesita acceso a las variables que actualizan el medidor,
    puede acceder a ellas a través de `amountusedvar`, `amounttotalvar`,
    y el `labelvar`. El valor de estas propiedades también puede
    recuperarse a través del método `configure`.
    """

    def __init__(
        self,
        master=None,
        bootstyle=DEFAULT,
        arcrange=None,
        arcoffset=None,
        amounttotal=100,
        amountused=0,
        wedgesize=0,
        metersize=200,
        metertype=FULL,
        meterthickness=10,
        showtext=True,
        interactive=False,
        stripethickness=0,
        textleft=None,
        textright=None,
        textfont="-size 20 -weight bold",
        subtext=None,
        subtextstyle=DEFAULT,
        subtextfont="-size 10",
        stepsize=1,
        **kwargs,
    ):
        """
        Parámetros:

            master (Widget):
                El widget padre.

            arcrange (int):
                El rango del arco en grados desde el inicio hasta el final.

            arcoffset (int):
                La cantidad para desplazar la posición inicial del arco en grados.
                0 está en las 3 en punto.

            amounttotal (int):
                El valor máximo del medidor.

            amountused (int):
                El valor actual del medidor; mostrado en una etiqueta central
                si la propiedad `showtext` está configurada como True.

            wedgesize (int):
                Establece la longitud de la cuña indicadora alrededor del arco. Si
                es mayor que 0, esta cuña se establece como un indicador centrado
                en el valor actual del medidor.

            metersize (int):
                El medidor es cuadrado. Esto representa el tamaño de un lado
                del cuadrado medido en unidades de pantalla.

            bootstyle (str):
                Establece el color del indicador y del texto central. Uno de primary,
                secondary, success, info, warning, danger, light, dark.

            metertype ('full', 'semi'):
                Muestra el medidor como un círculo completo o semicírculo.

            meterthickness (int):
                El grosor del indicador.

            showtext (bool):
                Indica si mostrar las etiquetas de texto izquierda, central y derecha
                en el medidor.

            interactive (bool):
                Indica que el usuario puede ajustar el valor del medidor con
                interacción del ratón.

            stripethickness (int):
                El indicador puede mostrarse como una banda sólida o como
                cuñas rayadas alrededor del arco. Si el valor es mayor que
                0, el indicador cambia de sólido a rayado, donde el
                valor es el grosor de las rayas (o cuñas).

            textleft (str):
                Una cadena corta insertada a la izquierda del texto central.

            textright (str):
                Una cadena corta insertada a la derecha del texto central.

            textfont (Union[str, Font]):
                La fuente utilizada para renderizar el texto central.

            subtext (str):
                Texto suplementario que aparece debajo del texto central.

            subtextstyle (str):
                El color de bootstyle del subtexto. Uno de primary,
                secondary, success, info, warning, danger, light, dark.
                El color predeterminado es específico del tema y es un tono más claro
                basado en si es un tema 'light' o 'dark'.

            subtextfont (Union[str, Font]):
                La fuente utilizada para renderizar el subtexto.

            stepsize (int):
                Establece la cantidad en la que cambiar el indicador del medidor
                cuando se incrementa mediante interacción del ratón.

            **kwargs:
                Otros argumentos de palabras clave que se pasan directamente al
                widget `Frame` que contiene los componentes del medidor.
        """
        super().__init__(master=master, **kwargs)

        # variables del widget
        self.amountusedvar = ttk.IntVar(value=amountused)
        self.amountusedvar.trace_add("write", self._draw_meter)
        self.amounttotalvar = ttk.IntVar(value=amounttotal)
        self.labelvar = ttk.StringVar(value=subtext)

        # configuraciones varias
        self._set_arc_offset_range(metertype, arcoffset, arcrange)
        self._towardsmaximum = True
        self._metersize = utility.scale_size(self, metersize)
        self._meterthickness = utility.scale_size(self, meterthickness)
        self._stripethickness = stripethickness
        self._showtext = showtext
        self._wedgesize = wedgesize
        self._stepsize = stepsize
        self._textleft = textleft
        self._textright = textright
        self._textfont = textfont
        self._subtext = subtext
        self._subtextfont = subtextfont
        self._subtextstyle = subtextstyle
        self._bootstyle = bootstyle
        self._interactive = interactive
        self._bindids = {}

        self._setup_widget()

    def _setup_widget(self):
        self.meterframe = ttk.Frame(
            master=self, width=self._metersize, height=self._metersize
        )
        self.indicator = ttk.Label(self.meterframe)
        self.textframe = ttk.Frame(self.meterframe)
        self.textleft = ttk.Label(
            master=self.textframe,
            text=self._textleft,
            font=self._subtextfont,
            bootstyle=(self._subtextstyle, "metersubtxt"),
            anchor=S,
            padding=(0, 5),
        )
        self.textcenter = ttk.Label(
            master=self.textframe,
            textvariable=self.amountusedvar,
            bootstyle=(self._bootstyle, "meter"),
            font=self._textfont,
        )
        self.textright = ttk.Label(
            master=self.textframe,
            text=self._textright,
            font=self._subtextfont,
            bootstyle=(self._subtextstyle, "metersubtxt"),
            anchor=S,
            padding=(0, 5),
        )
        self.subtext = ttk.Label(
            master=self.meterframe,
            text=self._subtext,
            bootstyle=(self._subtextstyle, "metersubtxt"),
            font=self._subtextfont,
        )

        self.bind("<<ThemeChanged>>", self._on_theme_change)
        self.bind("<<Configure>>", self._on_theme_change)
        self._set_interactive_bind()
        self._draw_base_image()
        self._draw_meter()

        # establecer geometría del widget
        self.indicator.place(x=0, y=0)
        self.meterframe.pack()
        self._set_show_text()

    def _set_widget_colors(self):
        bootstyle = (self._bootstyle, "meter", "label")
        ttkstyle = Bootstyle.ttkstyle_name(string="-".join(bootstyle))
        textcolor = self._lookup_style_option(ttkstyle, "foreground")
        background = self._lookup_style_option(ttkstyle, "background")
        troughcolor = self._lookup_style_option(ttkstyle, "space")
        self._meterforeground = textcolor
        self._meterbackground = Colors.update_hsv(background, vd=-0.1)
        self._metertrough = troughcolor

    def _set_meter_text(self):
        """Configurar y empaquetar las etiquetas del widget en el orden apropiado"""
        self._set_show_text()
        self._set_subtext()

    def _set_subtext(self):
        if self._subtextfont:
            if self._showtext:
                self.subtext.place(relx=0.5, rely=0.6, anchor=CENTER)
            else:
                self.subtext.place(relx=0.5, rely=0.5, anchor=CENTER)

    def _set_show_text(self):
        self.textframe.pack_forget()
        self.textcenter.pack_forget()
        self.textleft.pack_forget()
        self.textright.pack_forget()
        self.subtext.pack_forget()

        if self._showtext:
            if self._subtext:
                self.textframe.place(relx=0.5, rely=0.45, anchor=CENTER)
            else:
                self.textframe.place(relx=0.5, rely=0.5, anchor=CENTER)

        self._set_text_left()
        self._set_text_center()
        self._set_text_right()
        self._set_subtext()

    def _set_text_left(self):
        if self._showtext and self._textleft:
            self.textleft.pack(side=LEFT, fill=Y)

    def _set_text_center(self):
        if self._showtext:
            self.textcenter.pack(side=LEFT, fill=Y)

    def _set_text_right(self):
        self.textright.configure(text=self._textright)
        if self._showtext and self._textright:
            self.textright.pack(side=RIGHT, fill=Y)

    def _set_interactive_bind(self):
        seq1 = "<B1-Motion>"
        seq2 = "<Button-1>"

        if self._interactive:
            self._bindids[seq1] = self.indicator.bind(
                seq1, self._on_dial_interact
            )
            self._bindids[seq2] = self.indicator.bind(
                seq2, self._on_dial_interact
            )
            return

        if seq1 in self._bindids:
            self.indicator.unbind(seq1, self._bindids.get(seq1))
            self.indicator.unbind(seq2, self._bindids.get(seq2))
            self._bindids.clear()

    def _set_arc_offset_range(self, metertype, arcoffset, arcrange):
        if metertype == SEMI:
            self._arcoffset = 135 if arcoffset is None else arcoffset
            self._arcrange = 270 if arcrange is None else arcrange
        else:
            self._arcoffset = -90 if arcoffset is None else arcoffset
            self._arcrange = 360 if arcrange is None else arcrange
        self._metertype = metertype

    def _draw_meter(self, *_):
        """Dibujar un medidor"""
        img = self._base_image.copy()
        draw = ImageDraw.Draw(img)
        if self._stripethickness > 0:
            self._draw_striped_meter(draw)
        else:
            self._draw_solid_meter(draw)

        self._meterimage = ImageTk.PhotoImage(
            img.resize((self._metersize, self._metersize), Image.BICUBIC)
        )
        self.indicator.configure(image=self._meterimage)

    def _draw_base_image(self):
        """Dibujar imagen base para ser usada en actualizaciones posteriores"""
        self._set_widget_colors()
        self._base_image = Image.new(
            mode="RGBA", size=(self._metersize * M, self._metersize * M)
        )
        draw = ImageDraw.Draw(self._base_image)

        x1 = y1 = self._metersize * M - 20
        width = self._meterthickness * M
        # medidor rayado
        if self._stripethickness > 0:
            _from = self._arcoffset
            _to = self._arcrange + self._arcoffset
            _step = 2 if self._stripethickness == 1 else self._stripethickness
            for x in range(_from, _to, _step):
                draw.arc(
                    xy=(0, 0, x1, y1),
                    start=x,
                    end=x + self._stripethickness - 1,
                    fill=self._metertrough,
                    width=width,
                )
        # medidor sólido
        else:
            draw.arc(
                xy=(0, 0, x1, y1),
                start=self._arcoffset,
                end=self._arcrange + self._arcoffset,
                fill=self._metertrough,
                width=width,
            )

    def _draw_solid_meter(self, draw: ImageDraw.Draw):
        """Dibujar un medidor sólido"""
        x1 = y1 = self._metersize * M - 20
        width = self._meterthickness * M

        if self._wedgesize > 0:
            meter_value = self._meter_value()
            draw.arc(
                xy=(0, 0, x1, y1),
                start=meter_value - self._wedgesize,
                end=meter_value + self._wedgesize,
                fill=self._meterforeground,
                width=width,
            )
        else:
            draw.arc(
                xy=(0, 0, x1, y1),
                start=self._arcoffset,
                end=self._meter_value(),
                fill=self._meterforeground,
                width=width,
            )

    def _draw_striped_meter(self, draw: ImageDraw.Draw):
        """Dibujar un medidor rayado"""
        meter_value = self._meter_value()
        x1 = y1 = self._metersize * M - 20
        width = self._meterthickness * M

        if self._wedgesize > 0:
            draw.arc(
                xy=(0, 0, x1, y1),
                start=meter_value - self._wedgesize,
                end=meter_value + self._wedgesize,
                fill=self._meterforeground,
                width=width,
            )
        else:
            _from = self._arcoffset
            _to = meter_value - 1
            _step = self._stripethickness
            for x in range(_from, _to, _step):
                draw.arc(
                    xy=(0, 0, x1, y1),
                    start=x,
                    end=x + self._stripethickness - 1,
                    fill=self._meterforeground,
                    width=width,
                )

    def _meter_value(self) -> int:
        """Calcular el valor a utilizar para dibujar la longitud del arco del
        medidor de progreso."""
        value = int(
            (self["amountused"] / self["amounttotal"]) * self._arcrange
            + self._arcoffset
        )
        return value

    def _on_theme_change(self, *_):
        self._draw_base_image()
        self._draw_meter()

    def _on_dial_interact(self, e):
        """Callback para el movimiento de arrastre del ratón en el indicador del medidor"""
        dx = e.x - self._metersize // 2
        dy = e.y - self._metersize // 2
        rads = math.atan2(dy, dx)
        degs = math.degrees(rads)

        if degs > self._arcoffset:
            factor = degs - self._arcoffset
        else:
            factor = 360 + degs - self._arcoffset

        # limitar el valor entre 0 y `amounttotal`
        amounttotal = self.amounttotalvar.get()
        lastused = self.amountusedvar.get()
        amountused = (amounttotal / self._arcrange * factor)

        # calcular la cantidad utilizada dado el tamaño de paso
        if amountused > self._stepsize // 2:
            amountused = amountused // self._stepsize * self._stepsize + self._stepsize
        else:
            amountused = 0
        # si el número es el mismo, entonces no redibujar
        if lastused == amountused:
            return
        # establecer la variable de cantidad utilizada
        if amountused < 0:
            self.amountusedvar.set(0)
        elif amountused > amounttotal:
            self.amountusedvar.set(amounttotal)
        else:
            self.amountusedvar.set(amountused)

    def _lookup_style_option(self, style: str, option: str):
        """Envoltorio alrededor del comando de búsqueda de estilo tcl"""
        value = self.tk.call(
            "ttk::style", "lookup", style, "-%s" % option, None, None
        )
        return value

    def _configure_get(self, cnf):
        """Sobreescribe el método de obtención de configuración"""
        if cnf == "arcrange":
            return self._arcrange
        elif cnf == "arcoffset":
            return self._arcoffset
        elif cnf == "amounttotal":
            return self.amounttotalvar.get()
        elif cnf == "amountused":
            return self.amountusedvar.get()
        elif cnf == "interactive":
            return self._interactive
        elif cnf == "subtextfont":
            return self._subtextfont
        elif cnf == "subtextstyle":
            return self._subtextstyle
        elif cnf == "subtext":
            return self._subtext
        elif cnf == "metersize":
            return self._metersize
        elif cnf == "bootstyle":
            return self._bootstyle
        elif cnf == "metertype":
            return self._metertype
        elif cnf == "meterthickness":
            return self._meterthickness
        elif cnf == "showtext":
            return self._showtext
        elif cnf == "stripethickness":
            return self._stripethickness
        elif cnf == "textleft":
            return self._textleft
        elif cnf == "textright":
            return self._textright
        elif cnf == "textfont":
            return self._textfont
        elif cnf == "wedgesize":
            return self._wedgesize
        elif cnf == "stepsize":
            return self._stepsize
        else:
            return super(ttk.Frame, self).configure(cnf)

    def _configure_set(self, **kwargs):
        """Sobreescribe el método de configuración"""
        meter_text_changed = False

        if "arcrange" in kwargs:
            self._arcrange = kwargs.pop("arcrange")
        if "arcoffset" in kwargs:
            self._arcoffset = kwargs.pop("arcoffset")
        if "amounttotal" in kwargs:
            amounttotal = kwargs.pop("amounttotal")
            self.amounttotalvar.set(amounttotal)
        if "amountused" in kwargs:
            amountused = kwargs.pop("amountused")
            self.amountusedvar.set(amountused)
        if "interactive" in kwargs:
            self._interactive = kwargs.pop("interactive")
            self._set_interactive_bind()
        if "subtextfont" in kwargs:
            self._subtextfont = kwargs.pop("subtextfont")
            self.subtext.configure(font=self._subtextfont)
            self.textleft.configure(font=self._subtextfont)
            self.textright.configure(font=self._subtextfont)
        if "subtextstyle" in kwargs:
            self._subtextstyle = kwargs.pop("subtextstyle")
            self.subtext.configure(bootstyle=[self._subtextstyle, "meter"])
        if "metersize" in kwargs:
            self._metersize = utility.scale_size(kwargs.pop("metersize"))
            self.meterframe.configure(
                height=self._metersize, width=self._metersize
            )
        if "bootstyle" in kwargs:
            self._bootstyle = kwargs.pop("bootstyle")
            self.textcenter.configure(bootstyle=[self._bootstyle, "meter"])
        if "metertype" in kwargs:
            self._metertype = kwargs.pop("metertype")
        if "meterthickness" in kwargs:
            self._meterthickness = self.scale_size(
                kwargs.pop("meterthickness")
            )
        if "stripethickness" in kwargs:
            self._stripethickness = kwargs.pop("stripethickness")
        if "subtext" in kwargs:
            self._subtext = kwargs.pop("subtext")
            self.subtext.configure(text=self._subtext)
            meter_text_changed = True
        if "textleft" in kwargs:
            self._textleft = kwargs.pop("textleft")
            self.textleft.configure(text=self._textleft)
            meter_text_changed = True
        if "textright" in kwargs:
            self._textright = kwargs.pop("textright")
            meter_text_changed = True
        if "showtext" in kwargs:
            self._showtext = kwargs.pop("showtext")
            meter_text_changed = True
        if "textfont" in kwargs:
            self._textfont = kwargs.pop("textfont")
            self.textcenter.configure(font=self._textfont)
        if "wedgesize" in kwargs:
            self._wedgesize = kwargs.pop("wedgesize")
        if "stepsize" in kwargs:
            self._stepsize = kwargs.pop("stepsize")
        if meter_text_changed:
            self._set_meter_text()

        try:
            if self._metertype:
                self._set_arc_offset_range(
                    metertype=self._metertype,
                    arcoffset=self._arcoffset,
                    arcrange=self._arcrange,
                )
        except AttributeError:
            return

        self._draw_base_image()
        self._draw_meter()

        # pasar configuraciones restantes a `ttk.Frame.configure`
        super(ttk.Frame, self).configure(**kwargs)

    def __getitem__(self, key: str):
        return self._configure_get(key)

    def __setitem__(self, key: str, value) -> None:
        self._configure_set(**{key: value})

    def configure(self, cnf=None, **kwargs):
        """Configurar las opciones para este widget.

        Parámetros:
            cnf (Dict[str, Any], opcional):
                Un diccionario de opciones de configuración.

            **kwargs: Argumentos de palabras clave opcionales.
        """
        if cnf is not None:
            return self._configure_get(cnf)
        else:
            self._configure_set(**kwargs)

    def step(self, delta=1):
        """Aumentar el valor del indicador en `delta`

        El indicador invertirá la dirección y contará hacia abajo una vez que
        alcance el valor máximo.

        Parámetros:

            delta (int):
                La cantidad a cambiar el indicador.
        """
        amountused = self.amountusedvar.get()
        amounttotal = self.amounttotalvar.get()
        if amountused >= amounttotal:
            self._towardsmaximum = True
            self.amountusedvar.set(amountused - delta)
        elif amountused <= 0:
            self._towardsmaximum = False
            self.amountusedvar.set(amountused + delta)
        elif self._towardsmaximum:
            self.amountusedvar.set(amountused - delta)
        else:
            self.amountusedvar.set(amountused + delta)