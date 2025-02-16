import re
from typing import Optional


class Keywords:
    """Utilidad para el manejo y procesamiento de palabras clave en widgets.

    Esta clase proporciona funcionalidad para:
    1. Identificar clases de widgets
    2. Procesar patrones de nombres
    3. Extraer información de estilos
    """

    # Patrones de expresiones regulares para identificar widgets
    CLASS_PATTERN = r"button|label|entry|combobox|progressbar|scale|notebook"

    @staticmethod
    def ttkstyle_widget_class(widget=None, string: str = "") -> str:
        """Encuentra y retorna la clase de widget.

        Busca la clase de widget ya sea a partir de un string o de
        un widget proporcionado.

        Args:
            widget: Objeto widget a analizar.
            string: Cadena de texto a analizar.

        Returns:
            str: Clase de widget identificada o cadena vacía si no se encuentra.
        """
        # Buscar clase de widget en el patrón de string
        match = re.search(Keywords.CLASS_PATTERN, string.lower())
        if match is not None:
            widget_class = match.group(0)
            return widget_class

        # Buscar clase de widget desde el método tkinter/tcl
        if widget is None:
            return ""

        _class = widget.winfo_class()
        match = re.search(Keywords.CLASS_PATTERN, _class.lower())
        if match is not None:
            widget_class = match.group(0)
            return widget_class

        return ""