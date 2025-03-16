import tkinter

from ui.themeengine.communication.publisher import Publisher
from ui.themeengine.utils.constants import *


def on_disabled_readonly_state(event):
    """Cambia el cursor de los widgets de entrada de texto según su estado.

    Este manejador de eventos modifica el cursor de los widgets de entrada de texto
    para proporcionar retroalimentación visual sobre su estado interactivo:
    - Si el widget está deshabilitado o en modo solo lectura, cambia el cursor a una flecha ('arrow')
    - Si el widget está en estado normal, restaura el cursor al valor predeterminado ('ibeam')

    Args:
        event (Event): Objeto evento de Tkinter con referencia al widget que lo generó

    Returns:
        None: Solo modifica la propiedad 'cursor' del widget
    """
    try:
        # Obtener el widget que generó el evento
        widget = event.widget

        # Obtener el estado actual del widget ('normal', 'disabled', 'readonly', etc.)
        state = str(widget.cget('state'))

        # Obtener el tipo de cursor actual
        cursor = str(widget.cget('cursor'))

        # Si el widget está deshabilitado o en modo solo lectura
        if state in (DISABLED, READONLY):
            # Verificar si el cursor ya es 'arrow' para evitar cambios innecesarios
            if cursor == 'arrow':
                return  # El cursor ya es correcto, salir de la función
            else:
                # Cambiar el cursor a flecha para indicar que no se puede editar
                widget['cursor'] = 'arrow'
        else:
            # El widget está en estado normal/interactivo
            # Verificar si el cursor ya es 'ibeam' o vacío (valor predeterminado)
            if cursor in ('ibeam', ''):
                return  # El cursor ya es correcto, salir de la función
            else:
                # Restaurar el cursor al valor predeterminado
                # None en widgets de entrada generalmente se muestra como 'ibeam'
                widget['cursor'] = None
    except:
        # Capturar silenciosamente cualquier excepción
        # Posibles excepciones: AttributeError, TclError, etc.
        # Este enfoque prioriza la robustez para que problemas con el cursor
        # no interrumpan el funcionamiento de la aplicación
        pass


def on_select_all(event):
    """Selecciona todo el texto en un widget de entrada cuando se activa un evento.

    Implementa la funcionalidad "Seleccionar todo" (equivalente a Ctrl+A)
    detectando automáticamente el tipo de widget y aplicando los métodos adecuados.

    Args:
        event: Objeto evento de Tkinter con referencia al widget que lo generó

    Returns:
        str: 'break' para detener la propagación del evento
    """
    # Obtener el widget que generó el evento
    widget = event.widget

    # Verificar si es un widget de tipo Text (texto multilínea)
    if widget.__class__.__name__ == "Text":
        # Para widgets Text: usar los métodos específicos para selección multilínea
        widget.tag_add(SEL, "1.0", END)  # Seleccionar desde el inicio hasta el final
        # "1.0" representa línea 1, carácter 0 (inicio del texto)

        widget.mark_set(INSERT, END)  # Mover el cursor al final del texto
        widget.see(END)  # Asegurar que el final sea visible (scroll si es necesario)
    else:
        # Para otros widgets de entrada (Entry, Spinbox, Combobox)
        widget.select_range(0, END)  # Seleccionar desde el índice 0 hasta el final
        widget.icursor(END)  # Mover el cursor al final del texto

    # Retornar 'break' para detener la propagación del evento
    # Esto evita que otros manejadores procesen este evento
    # y que el widget realice su comportamiento predeterminado
    return 'break'


def apply_class_bindings(window: tkinter.Widget):
    """Aplica vinculaciones de eventos a nivel de clase para mejorar la experiencia de usuario.

    Este método configura comportamientos consistentes para grupos de widgets en toda la
    aplicación, estableciendo manejo automático del cursor, selección de texto con Ctrl+A,
    y comportamiento personalizado para activación de botones.

    Args:
        window (tkinter.Widget): La ventana o widget principal donde se aplicarán las vinculaciones
    """
    # Configurar vinculaciones para widgets de entrada de texto
    for className in ["TEntry", "TSpinbox", "TCombobox", "Text"]:
        # Vincular el evento Configure para gestionar el cursor según el estado
        # (disabled/readonly -> arrow cursor, normal -> ibeam cursor)
        window.bind_class(
            className=className,  # Clase de widget a vincular
            sequence="<Configure>",  # Evento: cuando cambia configuración
            func=on_disabled_readonly_state,  # Manejador: ajusta cursor según estado
            add="+"  # Añadir a vinculaciones existentes
        )

        # Añadir soporte para seleccionar todo el texto con Ctrl+A
        for sequence in ["<Control-a>", "<Control-A>"]:  # Ambas variantes de mayúsculas/minúsculas
            window.bind_class(
                className=className,  # Clase de widget a vincular
                sequence=sequence,  # Evento: Ctrl+A en ambos casos
                func=on_select_all  # Manejador: selecciona todo el texto
                # Sin add="+": reemplaza vinculaciones existentes para Ctrl+A
            )

    # Eliminar la vinculación predeterminada de la tecla espacio para botones
    # Esto desactiva la activación de botones al presionar espacio
    window.unbind_class("TButton", "<Key-space>")

    # Definir manejador personalizado para teclas Enter en botones
    def button_default_binding(event):
        """Activa un botón cuando se presiona Enter estando enfocado.

        Esta función intenta primero conseguir el widget por su nombre,
        y si falla, recurre a una llamada directa a Tcl/Tk.

        Args:
            event: El evento de teclado que contiene información del widget
        """
        try:
            # Intentar obtener el widget a partir de su nombre
            widget = window.nametowidget(event.widget)
            # Simular un clic en el botón
            widget.invoke()
        except KeyError:
            # Alternativa: si no se encuentra el widget por su nombre,
            # usar una llamada directa al motor Tcl/Tk subyacente
            window.tk.call(event.widget, 'invoke')

    # Vincular tecla Enter principal para activar botones
    window.bind_class(
        "TButton",  # Clase: todos los botones ttk
        "<Key-Return>",  # Evento: tecla Enter principal
        button_default_binding,  # Manejador: activar el botón
        add="+"  # Añadir a vinculaciones existentes
    )

    # Vincular tecla Enter del teclado numérico para activar botones
    window.bind_class(
        "TButton",  # Clase: todos los botones ttk
        "<KP_Enter>",  # Evento: tecla Enter del teclado numérico
        button_default_binding,  # Manejador: activar el botón
        add="+"  # Añadir a vinculaciones existentes
    )


def on_map_child(event):
    """Manejador para el evento <Map> que genera un evento virtual <<MapChild>> en el contenedor padre.

    Cuando un widget se hace visible, notifica al widget padre para permitir
    reacciones a cambios en la visibilidad de los componentes hijos.

    Args:
        event: Objeto evento con referencia al widget que se está mapeando
    """
    # Obtener el widget que generó el evento <Map> (que se está haciendo visible)
    widget: tkinter.Widget = event.widget

    try:
        # Verificar si el widget tiene un contenedor padre
        if widget.master is None:
            # Es el widget raíz de la aplicación, no tiene padre
            # No hay necesidad de generar evento, terminamos aquí
            return
        else:
            # El widget tiene un padre, generamos el evento virtual en él
            # Esto permite al contenedor reaccionar cuando sus hijos se muestran
            widget.master.event_generate('<<MapChild>>')
    except:
        # Excepción capturada, probablemente porque:
        # 1. No es un widget estándar de Tkinter
        # 2. Es un subcomponente interno como Combobox.popdown
        # 3. El widget ya fue destruido antes de completar el evento
        # En cualquier caso, terminamos silenciosamente
        return


def apply_all_bindings(window: tkinter.Widget):
    """Aplica vinculaciones de eventos globales a todos los widgets de la aplicación.

    Configura manejadores de eventos críticos para propagación de eventos de visibilidad
    y limpieza automática de recursos cuando los widgets son destruidos.

    Args:
        window (tkinter.Widget): La ventana principal para aplicar las vinculaciones
    """
    # Vincular el evento <Map> a todos los widgets de la aplicación
    # Este evento ocurre cuando un widget se hace visible en la pantalla
    window.bind_all(
        '<Map>',  # Evento: cuando un widget se hace visible
        on_map_child,  # Manejador: notifica al padre con <<MapChild>>
        '+'  # Añadir a vinculaciones existentes
    )

    # Vincular el evento <Destroy> a todos los widgets de la aplicación
    # Este evento ocurre cuando un widget es destruido
    window.bind_all(
        '<Destroy>',  # Evento: cuando un widget es destruido
        lambda e: Publisher.unsubscribe(e.widget),  # Manejador: elimina el widget del Publisher
        '+'  # Añadir a vinculaciones existentes
    )
    # La función lambda recibe el evento 'e' y accede a 'e.widget'
    # para obtener el widget que está siendo destruido y cancelar su suscripción