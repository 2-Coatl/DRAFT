import tkinter
from typing import Optional, List, Any


# Lista global para almacenar objetos de mensaje que requieren inicialización
MESSAGES: List[Any] = []

def get_default_root(what: Optional[str] = None) -> tkinter.Tk:
    """
    Obtiene la ventana raíz (root) por defecto de tkinter o crea una nueva si no existe.

    Este método comprueba si existe una ventana raíz por defecto y la devuelve.
    Si no existe, puede crear una nueva o lanzar un error según los parámetros
    proporcionados y la configuración de tkinter.

    Args:
        what (Optional[str]): Descripción de la acción que se está intentando realizar.
                             Se utiliza para generar mensajes de error más informativos.

    Returns:
        tkinter.Tk: Instancia de la ventana raíz de tkinter.

    Raises:
        RuntimeError: Si tkinter está configurado para no admitir una ventana raíz por defecto
                     o si no existe una ventana raíz y se proporciona un valor para 'what'.

    """
    # Verifica si tkinter permite usar una ventana raíz por defecto
    if not tkinter._support_default_root:
        # Si no lo permite, lanza un error informando que no se ha especificado un master
        # y que tkinter está configurado para no admitir una raíz por defecto
        raise RuntimeError("No master specified and tkinter is "
                           "configured to not support default root")

    # Verifica si ya existe una ventana raíz
    if not tkinter._default_root:
        # Si se proporciona información sobre la acción que se intenta realizar,
        # lanza un error específico indicando que es demasiado pronto para esa acción
        if what:
            # Ejemplo: "Too early to configure widgets: no default root window"
            raise RuntimeError(f"Too early to {what}: no default root window")

        # Si no se proporciona 'what', crea una nueva instancia de Tk
        # que automáticamente se asignará a tkinter._default_root
        root = tkinter.Tk()

        # Verifica que la raíz creada sea la misma que se asignó a _default_root
        assert tkinter._default_root is root

    # Devuelve la ventana raíz, ya sea la existente o la recién creada
    return tkinter._default_root


def initialize_localities() -> None:
    """
    Inicializa todos los objetos de mensaje registrados en el sistema de localización.

    Esta función recorre la lista global MESSAGES y llama al método initialize()
    de cada objeto registrado. Típicamente, este método se llama durante la
    inicialización del sistema para cargar todos los archivos de mensajes
    personalizados y preparar el sistema de localización.

    La función no tiene parámetros ni valor de retorno, pero produce efectos
    secundarios al inicializar cada objeto en MESSAGES.

    Requisitos:
        - La variable global MESSAGES debe contener objetos que implementen un método initialize().
        - Cada objeto en MESSAGES es responsable de su propia inicialización específica.

    Raises:
        AttributeError: Si algún objeto en MESSAGES no tiene un método initialize().
        Exception: Cualquier excepción que pueda lanzar el método initialize() de los objetos.
    """
    # Recorre todos los objetos de mensaje registrados y llama a su método initialize()
    for m in MESSAGES:
        # Se espera que cada objeto tenga implementado un método initialize()
        # que cargue sus archivos de mensajes personalizados o realice
        # cualquier configuración específica necesaria
        m.initialize()
