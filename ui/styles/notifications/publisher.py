from typing import Dict, List, Callable
from .subscriber import Subscriber
from .channel import Channel


class Publisher:
    """Gestiona las notificaciones para actualizaciones de widgets y temas.

    Implementa el patrón Singleton para centralizar la gestión de
    notificaciones en el sistema.

    Atributos:
        __subscribers: Diccionario privado de suscriptores.
    """

    __subscribers: Dict[str, Subscriber] = {}

    @classmethod
    def subscriber_count(cls) -> int:
        """Retorna el número total de suscriptores."""
        return len(cls.__subscribers)

    @classmethod
    def subscribe(cls, name: str, callback: Callable, channel: Channel) -> None:
        """Registra un nuevo suscriptor.

        Args:
            name: Identificador único del widget.
            callback: Función a llamar en la notificación.
            channel: Canal de suscripción (STD o TTK).
        """
        cls.__subscribers[name] = Subscriber(name, callback, channel)

    @classmethod
    def unsubscribe(cls, name: str) -> None:
        """Elimina un suscriptor del sistema.

        Args:
            name: Identificador del suscriptor a eliminar.
        """
        cls.__subscribers.pop(str(name), None)

    @classmethod
    def get_subscribers(cls, channel: Channel) -> List[Subscriber]:
        """Obtiene los suscriptores de un canal específico.

        Args:
            channel: Canal del cual obtener suscriptores.

        Returns:
            Lista de suscriptores del canal especificado.
        """
        return [s for s in cls.__subscribers.values() if s.channel == channel]

    @classmethod
    def publish_message(cls, channel: Channel, *args) -> None:
        """Envía una notificación a todos los suscriptores de un canal.

        Args:
            channel: Canal objetivo de la notificación.
            *args: Argumentos a pasar a los callbacks de los suscriptores.
        """
        for subscriber in cls.get_subscribers(channel):
            subscriber.callback(*args)

    @classmethod
    def clear_subscribers(cls) -> None:
        """Elimina todos los suscriptores del sistema."""
        cls.__subscribers.clear()