from ui.themeengine.localization.message_catalog import MessageCatalog

class LocaleMsgs:
    """
    Clase auxiliar para cargar catálogos de mensajes de localización sin necesidad
    de empaquetar recursos de biblioteca.

    Esta clase proporciona una forma programática de registrar traducciones en el
    sistema MessageCatalog, evitando problemas comunes con empaquetadores al crear
    aplicaciones distribuibles. Permite definir traducciones en el código fuente
    en lugar de en archivos de recursos externos.

    Attributes:
        locale (str): Código de idioma/región (e.g., "es_ES", "en_US").
        messages (tuple): Tupla que contiene listas de pares de mensajes.
    """

    def __init__(self, locale, *msgs):
        """
        Inicializa una nueva instancia de LocaleMsgs con un locale específico y mensajes opcionales.

        Esta clase ayuda a cargar un catálogo de mensajes para la localización de la aplicación
        sin necesidad de empaquetar recursos de biblioteca, lo que puede causar problemas
        con algunos empaquetadores al crear aplicaciones distribuibles.

        Args:
            locale (str): El código de idioma/región a utilizar (por ejemplo, "es_ES", "en_US").
            *msgs (list): Listas de pares de mensajes (origen, traducción) para este locale.
                         Cada lista puede contener múltiples pares.
        """
        # Almacena el código de locale (ej: "es_ES") para su uso posterior
        self.locale = locale

        # Almacena los mensajes como una tupla, cada elemento puede ser una lista de pares
        # Ejemplo: Si msgs = ([("Hello", "Hola")], [("Yes", "Sí")])
        #          self.messages será exactamente esa tupla
        self.messages = msgs

    def initialize(self):
        """
        Inicializa las traducciones de este locale en el MessageCatalog global.

        Este método procesa todos los mensajes almacenados en la instancia y los registra
        en el sistema de catálogo de mensajes para el locale especificado. Aplana la estructura
        de mensajes potencialmente anidada y utiliza MessageCatalog.set_many() para registrar
        todas las traducciones de una sola vez, lo que es más eficiente que llamadas individuales.

        Returns:
            None: Este método no retorna ningún valor, pero tiene el efecto secundario
                  de registrar las traducciones en el MessageCatalog.
        """
        # Importamos chain desde itertools para aplanar la estructura de mensajes
        from itertools import chain

        # Aplanamos la estructura de mensajes que puede estar anidada
        # Ejemplo: Si self.messages es ([("Hello", "Hola")], [("Yes", "Sí")])
        # messages será [("Hello", "Hola"), ("Yes", "Sí")]
        messages = list(chain(*self.messages))

        # Registramos todos los mensajes en el catálogo para el locale especificado
        # Desempaquetamos los mensajes para pasarlos como argumentos individuales
        MessageCatalog.set_many(self.locale, *messages)
