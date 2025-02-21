from typing import Callable
from .channel import Channel


class Subscriber:
    """Almacena la información de un suscriptor para el sistema de notificaciones.

    Esta clase mantiene los datos necesarios para identificar y notificar
    a un widget específico cuando ocurren cambios en el tema.

    Atributos:
        name: Identificador único del widget suscrito.
        callback: Función a ejecutar cuando se recibe una notificación.
        channel: Canal al que está suscrito el widget.
    """

    def __init__(self, name: str, callback: Callable, channel: Channel):
        """Inicializa un nuevo suscriptor.

        Args:
            name: Identificador único del widget.
            callback: Función que se llamará al notificar.
            channel: Canal de suscripción (STD o TTK).
        """
        self.name = name
        self.callback = callback
        self.channel = channel