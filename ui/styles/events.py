from enum import Enum
from typing import List, Callable, Dict

class Channel(Enum):
    """Un agrupamiento para suscriptores del Publisher. Indica si el
    widget es un widget tk heredado 'STD' o un widget 'TTK' con estilo.

    Attributes:
        STD (1): Widgets tkinter heredados/tradicionales.
        TTK (2): Widgets tkinter temáticos.
    """
    STD = 1
    TTK = 2

class Subscriber:
    """Una clase de datos para almacenar información sobre un suscriptor
    específico del Publisher."""

    def __init__(self, name: str, func: Callable, channel: Channel):
        """Crea un suscriptor.

        Args:
            name: El nombre del suscriptor
            func: La función a llamar al enviar mensajes
            channel: El canal de suscripción
        """
        self.name = name
        self.func = func
        self.channel = channel

class Publisher:
    """Clase utilizada para publicar eventos de actualización de widgets
    para cambios de tema o configuraciones."""

    __subscribers: Dict[str, Subscriber] = {}

    @staticmethod
    def subscriber_count() -> int:
        """Retorna el número total de suscriptores."""
        return len(Publisher.__subscribers)

    @staticmethod
    def subscribe(name: str, func: Callable, channel: Channel) -> None:
        """Suscribe a un evento.

        Args:
            name: El nombre tkinter/tcl del widget
            func: Función a llamar al pasar un mensaje
            channel: Indica el canal que agrupa los suscriptores
        """
        Publisher.__subscribers[name] = Subscriber(name, func, channel)

    @staticmethod
    def unsubscribe(name: str) -> None:
        """Elimina un suscriptor.

        Args:
            name: El nombre tkinter/tcl del widget
        """
        try:
            del Publisher.__subscribers[str(name)]
        except:
            pass

    @staticmethod
    def get_subscribers(channel: Channel) -> List[Subscriber]:
        """Retorna una lista de suscriptores.

        Args:
            channel: Canal del que obtener suscriptores

        Returns:
            Lista de suscriptores del canal especificado
        """
        subs = Publisher.__subscribers.values()
        return [s for s in subs if s.channel == channel]

    @staticmethod
    def publish_message(channel: Channel, *args) -> None:
        """Publica un mensaje a todos los suscriptores.

        Args:
            channel: El nombre del canal al que suscribirse
            *args: Argumentos opcionales para pasar a los suscriptores
        """
        subs: List[Subscriber] = Publisher.get_subscribers(channel)
        for sub in subs:
            sub.func(*args)

    @staticmethod
    def clear_subscribers() -> None:
        """Reinicia todas las suscripciones."""
        Publisher.__subscribers.clear()