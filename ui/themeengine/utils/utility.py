from typing import Optional, Union
import tkinter as tk
import sys
import platform


def enable_high_dpi_awareness(
        root: Optional[tk.Tk] = None,
        scaling: Optional[float] = None
) -> None:
    """Habilita el soporte para pantallas de alta resolución (high DPI).

    Este método permite que las aplicaciones Tkinter se adapten correctamente
    a pantallas de alta densidad de píxeles (high DPI) en diferentes sistemas
    operativos.

    **Windows OS**
    Llame al método ANTES de crear el objeto `Tk`. No se requieren parámetros.
    Utiliza la API de Windows para indicar que la aplicación es compatible con DPI alto.
    En Windows 10+, utiliza SetProcessDpiAwarenessContext para mejor soporte.

    **Linux OS**
    Debe proporcionar los parámetros `root` y `scaling`. Llame al método
    DESPUÉS de crear el objeto `Tk`. Un número entre 1.6 y 2.0 generalmente
    es suficiente para escalar pantallas de alta resolución.

    **macOS**
    macOS maneja automáticamente la escala de la interfaz, pero se puede
    proporcionar un valor de scaling personalizado si se desea.

    !!! advertencia
        Si se proporciona el argumento `root`, entonces también debe
        proporcionarse `scaling`. De lo contrario, no tendrá efecto.

    Args:
        root (tk.Tk, opcional):
            El widget raíz de la aplicación.

        scaling (float, opcional):
            Establece el factor de escalado utilizado por Tk para
            convertir entre unidades físicas (por ejemplo, puntos,
            pulgadas o milímetros) y píxeles. Debe ser un valor positivo,
            normalmente entre 1.0 y 3.0.

    Returns:
        None

    Raises:
        ValueError: Si el valor de scaling no es positivo.

    Ejemplos:
        ```python
        # Para Windows (antes de crear Tk)
        enable_high_dpi_awareness()
        root = tk.Tk()

        # Para Linux (después de crear Tk)
        root = tk.Tk()
        enable_high_dpi_awareness(root=root, scaling=1.75)
        ```
    """
    # Validar el parámetro scaling si se proporciona
    if scaling is not None:
        if not isinstance(scaling, (int, float)):
            raise TypeError("El parámetro 'scaling' debe ser un número")
        if scaling <= 0:
            raise ValueError("El parámetro 'scaling' debe ser un valor positivo")
        if scaling > 3.0:
            import warnings
            warnings.warn(
                f"El valor de scaling ({scaling}) es inusualmente alto. "
                "Los valores típicos están entre 1.0 y 3.0."
            )

    # Detectar automáticamente el sistema operativo
    os_name = platform.system()

    # Configuración específica para Windows
    if os_name == "Windows":
        try:
            # Importar módulos necesarios para Windows
            from ctypes import windll, c_int, POINTER, HRESULT

            # Verificar la versión de Windows para usar el método más apropiado
            win_ver = sys.getwindowsversion()

            # Para Windows 10 o superior (versión 10.0+)
            if win_ver.major >= 10:
                # Valores para DPI awareness en Windows 10+
                DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2 = -4

                try:
                    # Definir el prototipo de función para SetProcessDpiAwarenessContext
                    windll.user32.SetProcessDpiAwarenessContext.restype = HRESULT
                    windll.user32.SetProcessDpiAwarenessContext.argtypes = [c_int]

                    # Usar el método más avanzado para Windows 10+
                    result = windll.user32.SetProcessDpiAwarenessContext(
                        DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2
                    )

                    if result == 0:  # Si falla, intentar con el método anterior
                        windll.user32.SetProcessDPIAware()
                except (AttributeError, OSError):
                    # Si el método avanzado no está disponible, usar el método tradicional
                    windll.user32.SetProcessDPIAware()
            else:
                # Para versiones anteriores de Windows, usar el método tradicional
                windll.user32.SetProcessDPIAware()

        except (ImportError, AttributeError, OSError) as e:
            import logging
            logging.warning(f"No se pudo habilitar el soporte de DPI alto en Windows: {e}")

    # Aplicar scaling para cualquier sistema operativo si se proporcionan root y scaling
    if root is not None and scaling is not None:
        try:
            # Comprobar que root sea realmente un objeto Tk válido
            if not isinstance(root, tk.Tk):
                raise TypeError("El parámetro 'root' debe ser una instancia de tkinter.Tk")

            # Aplicar el factor de escalado
            root.tk.call('tk', 'scaling', scaling)

            # Si estamos en Linux, aplicar configuraciones adicionales recomendadas
            if os_name == "Linux":
                # Configurar fuentes y otros elementos según sea necesario para Linux
                # Esto podría expandirse según las necesidades específicas
                pass

        except (tk.TclError, AttributeError) as e:
            import logging
            logging.warning(f"No se pudo aplicar el factor de escalado: {e}")

    # Advertir si los parámetros se proporcionaron incorrectamente
    elif (root is None and scaling is not None) or (root is not None and scaling is None):
        import warnings
        warnings.warn(
            "Para aplicar un factor de escalado, se deben proporcionar tanto 'root' como 'scaling'"
        )


def get_image_name(image):
    """Extract and return the tcl/tk image name from a PhotoImage
    object.

    Parameters:

        image (ImageTk.PhotoImage):
            A photoimage object.

    Returns:

        str:
            The tcl/tk name of the photoimage object.
    """
    return image._PhotoImage__photo.name