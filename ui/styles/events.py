"""
Módulo de gestión de eventos para el sistema de temas.
Maneja la notificación de cambios de tema a los widgets.
"""

from enum import Enum
from typing import Dict, Callable


class Channel(Enum):
    """Define los canales de suscripción para widgets.

    Attributes:
        STD: Widgets tkinter tradicionales
        TTK: Widgets tkinter temáticos
    """
    STD = 1
    TTK = 2


class Subscriber:
    """Almacena información de un widget suscrito a cambios de tema."""

    def __init__(self, widget_id: str, callback: Callable, channel: Channel):
        """Inicializa un suscriptor.

        Args:
            widget_id: Identificador único del widget
            callback: Función a llamar cuando hay cambios
            channel: Canal de suscripción (STD o TTK)
        """
        self.widget_id = widget_id
        self.callback = callback
        self.channel = channel


class Publisher:
    """Gestiona notificaciones de cambios de tema a widgets suscritos."""

    _subscribers: Dict[str, Subscriber] = {}

    @staticmethod
    def subscribe(widget_id: str, callback: Callable, channel: Channel) -> None:
        """Suscribe un widget para recibir notificaciones.

        Args:
            widget_id: Identificador único del widget
            callback: Función a llamar en cambios de tema
            channel: Canal de suscripción
        """
        Publisher._subscribers[widget_id] = Subscriber(widget_id, callback, channel)

    @staticmethod
    def unsubscribe(widget_id: str) -> None:
        """Elimina la suscripción de un widget."""
        Publisher._subscribers.pop(widget_id, None)

    @staticmethod
    def publish_message(channel: Channel, *args) -> None:
        """Notifica a todos los suscriptores de un canal específico."""
        for subscriber in Publisher._subscribers.values():
            if subscriber.channel == channel:
                try:
                    subscriber.callback(*args)
                except Exception as e:
                    print(f"Error notificando a {subscriber.widget_id}: {e}")
                    Publisher.unsubscribe(subscriber.widget_id)