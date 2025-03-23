from ui.themeengine.localization.helpers import get_default_root

class MessageCatalog:
    """
    Proporciona una interfaz para el sistema de catálogo de mensajes de Tcl/Tk (msgcat).

    Esta clase estática actúa como una fachada que facilita la internacionalización de
    aplicaciones tkinter, permitiendo traducir cadenas, cargar archivos de mensajes y
    gestionar configuraciones regionales (locales). Todos los métodos son estáticos y
    pueden utilizarse sin necesidad de instanciar la clase.

    La clase forma parte de la capa de integración del módulo de localización y trabaja
    con los comandos `::msgcat::*` del intérprete Tcl/Tk subyacente. Permite a los
    desarrolladores implementar aplicaciones en un solo idioma inicialmente, facilitando
    la adición posterior de soporte para otros idiomas.

    Métodos principales:
        translate(src): Traduce una cadena según el locale actual.
        locale(newlocale=None): Consulta o establece el locale actual.
        preferences(): Obtiene la lista de locales preferidos por el usuario.
        load(dirname): Carga archivos de mensajes desde un directorio.
        set(locale, src, translated=None): Establece una traducción específica.
        set_many(locale, *args): Establece múltiples traducciones a la vez.
        max(*src): Determina la longitud de la cadena traducida más larga.

    Ejemplo de uso:
        # Traducir una cadena
        button_text = MessageCatalog.translate("Save")

        # Cargar archivos de mensajes
        MessageCatalog.load("./locales")

        # Cambiar el locale
        MessageCatalog.locale("es_ES")

        # Establecer una traducción manualmente
        MessageCatalog.set("fr_FR", "Close", "Fermer")

        # Obtener el ancho necesario para botones
        button_width = MessageCatalog.max("OK", "Cancel", "Apply")

    Notas:
        - La clase depende de una ventana raíz tkinter inicializada.
        - Los métodos interactúan con el sistema msgcat de Tcl/Tk.
        - Se recomienda cargar archivos de mensajes al inicio de la aplicación.
        - Para mayor eficiencia en la definición de múltiples traducciones,
          utilice set_many() en lugar de múltiples llamadas a set().
    """

    @staticmethod
    def translate(src):
        """
        Traduce una cadena de texto según la configuración regional (locale) actual del usuario.

        Este es el método principal para localizar una aplicación. En lugar de usar cadenas
        en un idioma específico directamente, la aplicación puede pasar las cadenas a través
        de este método y usar el resultado. Si una aplicación está escrita para un solo idioma
        de esta manera, es fácil añadir soporte para idiomas adicionales posteriormente,
        simplemente definiendo nuevas entradas en el catálogo de mensajes.

        El método utiliza el comando `::msgcat::mc` de Tcl/Tk para realizar la traducción.
        Si no existe una traducción para la cadena proporcionada, se devuelve la cadena
        original sin modificar.

        Args:
            src (str): La cadena de texto a traducir. Normalmente está en el idioma
                      predeterminado de la aplicación (comúnmente inglés).

        Returns:
            str: La cadena traducida según la configuración regional actual, o la cadena
                 original si no existe una traducción.

        Raises:
            RuntimeError: Si no existe una ventana raíz y no se puede crear una automáticamente.

        Notes:
            - La traducción depende de los catálogos de mensajes cargados previamente.
            - El método no maneja caracteres especiales en las cadenas, lo que podría causar problemas.
        """
        # Obtiene la ventana raíz de tkinter para acceder al intérprete tcl/tk
        root = get_default_root()

        # Define el comando tcl/tk para traducción
        command = "::msgcat::mc"

        # Ejecuta el comando en el intérprete tcl/tk y devuelve el resultado
        # La cadena original se encapsula en comillas dobles para el comando tcl/tk
        return root.tk.eval(f'{command} "{src}"')

    @staticmethod
    def locale(newlocale=None):
        """
        Obtiene o establece la configuración regional (locale) actual del sistema.

        Este método permite tanto consultar el locale actual como establecer uno nuevo.
        Cuando se cambia el locale, el sistema utilizará los catálogos de mensajes
        correspondientes para las traducciones posteriores.

        El método utiliza el comando `::msgcat::mclocale` de Tcl/Tk para interactuar
        con el sistema de localización subyacente.

        Args:
            newlocale (Optional[str]): Código de localización a establecer (por ejemplo,
                                      "es_ES", "en_US", "fr_FR", etc.). Si es None o una
                                      cadena vacía, simplemente consulta el locale actual.

        Returns:
            str: Si se estableció un nuevo locale, devuelve el locale anterior.
                 Si se consultó el locale, devuelve el locale actual.

        Raises:
            RuntimeError: Si no existe una ventana raíz y no se puede crear una automáticamente.

        Notes:
            - El locale inicial se determina automáticamente a partir del entorno del usuario.
            - Cambiar el locale afecta a todas las traducciones subsiguientes en la aplicación.
            - La implementación actual no valida si el locale proporcionado es válido o está disponible.
        """
        # Obtiene la ventana raíz de tkinter para acceder al intérprete tcl/tk
        root = get_default_root()

        # Define el comando tcl/tk para gestión de locale
        command = "::msgcat::mclocale"

        # Ejecuta el comando en el intérprete tcl/tk
        # Si newlocale es None o cadena vacía, consulta el locale actual
        # Si newlocale tiene un valor, establece el nuevo locale y devuelve el anterior
        return root.tk.eval(f'{command} {newlocale or ""}')

    @staticmethod
    def preferences():
        """
        Obtiene la lista ordenada de locales preferidos por el usuario.

        Este método consulta las preferencias de idioma del usuario, basadas en su
        configuración regional. La lista devuelta está ordenada desde el locale más
        específico hasta el menos específico (más general).

        El método utiliza el comando `::msgcat::mcpreferences` de Tcl/Tk para obtener
        las preferencias del sistema de localización subyacente.

        Returns:
            List[str]: Lista de códigos de locale preferidos por el usuario, ordenados
                      de más específico a menos específico. Por ejemplo, si el usuario
                      ha especificado LANG=en_US_funky, este método devolvería
                      ["en_US_funky", "en_US", "en"]. Si no hay preferencias definidas,
                      devuelve una lista vacía.

        Raises:
            RuntimeError: Si no existe una ventana raíz y no se puede crear una automáticamente.

        Notes:
            - El resultado refleja la configuración actual del sistema y las preferencias del usuario.
            - El sistema de localización utiliza esta lista para buscar traducciones, probando
              primero el locale más específico y luego los más generales.
            - La implementación actual elimina el último elemento devuelto por Tcl/Tk, que suele
              ser una cadena vacía debido a la forma en que Tcl representa las listas.
        """
        # Obtiene la ventana raíz de tkinter para acceder al intérprete tcl/tk
        root = get_default_root()

        # Define el comando tcl/tk para obtener preferencias de locale
        command = "::msgcat::mcpreferences"

        # Ejecuta el comando y procesa el resultado
        items = root.tk.eval(command).split(" ")

        # Tcl/Tk devuelve una cadena con elementos separados por espacios,
        # típicamente con un espacio final, lo que resulta en un elemento vacío
        # al final después de dividir. Eliminamos este elemento vacío.
        if len(items) > 0:
            return items[0:-1]
        else:
            return []

    @staticmethod
    def load(dirname):
        """
        Busca y carga archivos de mensajes localizados desde un directorio específico.

        Este método busca en el directorio especificado archivos que coincidan con las
        preferencias de idioma del usuario, según lo devuelto por el método `preferences()`.
        Cada archivo encontrado es cargado en el sistema de mensajes, permitiendo
        su uso posterior para traducciones.

        El método utiliza el comando `::msgcat::mcload` de Tcl/Tk para buscar y cargar
        los archivos. Internamente, este comando busca archivos con nombres que coincidan
        con los patrones de locale preferidos (por ejemplo, "es_ES.msg", "es.msg" para
        el locale "es_ES").

        Args:
            dirname (Union[str, Path]): Ruta del directorio donde se encuentran los
                                        archivos de mensajes. Puede ser una cadena o
                                        un objeto Path.

        Returns:
            int: Número de archivos de mensajes que coincidieron con las preferencias
                 de locale y fueron cargados exitosamente.

        Raises:
            RuntimeError: Si no existe una ventana raíz y no se puede crear una automáticamente.
            FileNotFoundError: Si el directorio especificado no existe o no es accesible.
            ValueError: Si ocurre un error durante la carga de los archivos.

        Examples:
            >>> # Cargar mensajes de un directorio
            >>> num_files = MessageCatalog.load("./locales")
            >>> print(f"Se cargaron {num_files} archivos de mensajes")
            "Se cargaron 2 archivos de mensajes"

            >>> # Usar con objeto Path
            >>> from pathlib import Path
            >>> num_files = MessageCatalog.load(Path("./resources/messages"))
            >>> print(f"Se cargaron {num_files} archivos de mensajes")
            "Se cargaron 3 archivos de mensajes"

        Notes:
            - Los archivos de mensajes deben seguir el formato esperado por Tcl/Tk msgcat.
            - El método no verifica explícitamente si el directorio existe; esto se delega a Tcl/Tk.
            - Para que un archivo sea cargado, debe tener un nombre que coincida con uno de los
              locales devueltos por `preferences()` y la extensión adecuada.
        """
        # Importa Path para manejar rutas de forma independiente de la plataforma
        from pathlib import Path

        # Convierte la ruta a formato POSIX (usando / como separador)
        # Esto es necesario para que tcl/tk interprete correctamente la ruta
        msgs = Path(dirname).as_posix()

        # Obtiene la ventana raíz de tkinter para acceder al intérprete tcl/tk
        root = get_default_root()

        # Define el comando tcl/tk para cargar archivos de mensajes
        command = "::msgcat::mcload"

        # Ejecuta el comando pasando la ruta como argumento
        # [list ...] es la sintaxis de tcl para manejar correctamente espacios y caracteres especiales
        # Convierte el resultado a entero y lo devuelve
        return int(root.tk.eval(f"{command} [list {msgs}]"))

    @staticmethod
    def set(locale, src, translated=None):
        """
        Establece una traducción específica para una cadena de texto en un locale determinado.

        Este método permite definir traducciones programáticamente, sin necesidad de cargar
        archivos externos. Las traducciones establecidas se almacenan en el catálogo de
        mensajes interno de tcl/tk y serán utilizadas posteriormente por el método `translate()`
        cuando el locale activo coincida.

        El método utiliza el comando `::msgcat::mcset` de Tcl/Tk para registrar la traducción
        en el sistema de localización subyacente.

        Args:
            locale (str): Código de localización para el que se define la traducción
                         (por ejemplo, "es_ES", "en_US", "fr_FR").
            src (str): Cadena original en el idioma base (generalmente inglés) que
                      servirá como clave para la traducción.
            translated (Optional[str]): Cadena traducida al idioma identificado por `locale`.
                                      Si es None o se omite, se utiliza `src` como su propia
                                      traducción, lo que puede ser útil para términos que
                                      no requieren traducción.

        Returns:
            None: Este método no devuelve ningún valor.

        Raises:
            RuntimeError: Si no existe una ventana raíz y no se puede crear una automáticamente.

        Examples:
            >>> # Establecer una traducción específica
            >>> MessageCatalog.set("es_ES", "Hello", "Hola")

            >>> # Usar la cadena original como su propia traducción
            >>> MessageCatalog.set("fr_FR", "OK")

            >>> # Verificar la traducción (asumiendo que el locale actual es "es_ES")
            >>> MessageCatalog.translate("Hello")
            "Hola"

        Notes:
            - Este método no escapa caracteres especiales en los parámetros, lo que podría
              causar problemas con cadenas que contienen espacios, comillas u otros caracteres
              especiales en tcl/tk.
            - Las traducciones establecidas tienen precedencia sobre las cargadas desde archivos
              para el mismo locale y cadena original.
        """
        # Obtiene la ventana raíz de tkinter para acceder al intérprete tcl/tk
        root = get_default_root()

        # Define el comando tcl/tk para establecer traducciones
        command = "::msgcat::mcset"

        # Ejecuta el comando en el intérprete tcl/tk
        # Si translated es None, se usa una cadena vacía, lo que hace que tcl/tk
        # utilice src como traducción
        root.tk.eval(f'{command} {locale} {src} {translated or ""}')

    @staticmethod
    def set_many(locale, *args):
        """
        Establece múltiples traducciones simultáneamente para un locale específico.

        Este método permite definir varias traducciones a la vez para un locale determinado,
        lo que es más eficiente que llamar repetidamente al método `set()`. Los argumentos
        deben proporcionarse como pares consecutivos, donde el primer elemento de cada par
        es la cadena original y el segundo es su traducción.

        El método utiliza el comando `::msgcat::mcmset` de Tcl/Tk para registrar las
        traducciones en el sistema de localización subyacente.

        Args:
            locale (str): Código de localización para el que se definen las traducciones
                         (por ejemplo, "es_ES", "en_US", "fr_FR").
            *args (str): Serie de cadenas originales y sus traducciones, en pares.
                        Debe haber un número par de argumentos.

        Returns:
            int: Número de pares de traducción establecidos exitosamente.

        Raises:
            RuntimeError: Si no existe una ventana raíz y no se puede crear una automáticamente.
            ValueError: Si el número de argumentos en *args no es par.

        Notes:
            - Este método no verifica explícitamente que el número de argumentos sea par,
              pero el comando subyacente de tcl/tk requiere pares completos.
            - El método puede tener problemas con cadenas que contienen caracteres especiales
              como comillas, ya que utiliza un enfoque simple de formateo de cadenas.
            - Las traducciones establecidas tienen precedencia sobre las cargadas desde archivos
              para el mismo locale y cadena original.
        """
        # Verificar que el número de argumentos sea par
        if len(args) % 2 != 0:
            raise ValueError("El número de argumentos debe ser par (pares de src, translated)")

        # Obtiene la ventana raíz de tkinter para acceder al intérprete tcl/tk
        root = get_default_root()

        # Define el comando tcl/tk para establecer múltiples traducciones
        command = "::msgcat::mcmset"

        # Formatea los argumentos como una lista de cadenas con comillas
        # Esto creará una cadena como: "original1" "traducción1" "original2" "traducción2"
        messages = " ".join([f'"{x}"' for x in args])

        # Construye el comando completo
        # Las llaves {{{messages}}} son necesarias para que tcl/tk interprete correctamente
        # los argumentos como una lista
        out = f"{command} {locale} {{{messages}}}"

        # Ejecuta el comando, convierte el resultado a entero y lo devuelve
        # El valor devuelto representa el número de pares de traducción establecidos
        return int(root.tk.eval(out))

    @staticmethod
    def max(*src):
        def max(*src: str) -> int:
            """
            Determina la longitud de la cadena traducida más larga entre varias opciones.

            Este método es especialmente útil para el diseño de interfaces gráficas localizadas,
            donde los elementos como botones o etiquetas pueden variar significativamente en longitud
            según el idioma. Al conocer la longitud máxima posible, se puede reservar suficiente
            espacio para asegurar que la interfaz se vea correctamente en todos los idiomas.

            El método traduce cada cadena proporcionada según el locale actual y compara las longitudes
            de las traducciones, no de las cadenas originales. Utiliza el comando `::msgcat::mcmax`
            de Tcl/Tk para realizar esta operación.

            Args:
                *src (str): Serie de cadenas originales cuyas traducciones serán evaluadas.
                           Se debe proporcionar al menos una cadena.

            Returns:
                int: Longitud (número de caracteres) de la cadena traducida más larga.

            Raises:
                RuntimeError: Si no existe una ventana raíz y no se puede crear una automáticamente.
                ValueError: Si no se proporciona ninguna cadena para comparar.

            Examples:
                >>> # Determinar el ancho necesario para botones de diálogo
                >>> max_length = MessageCatalog.max("OK", "Cancel", "Apply")
                >>> print(f"El ancho debe ser al menos {max_length} caracteres")
                "El ancho debe ser al menos 8 caracteres"  # Si 'Cancel' se traduce como 'Cancelar'

                >>> # Usar el resultado para configurar un widget de tkinter
                >>> button_width = MessageCatalog.max("Save", "Cancel")
                >>> save_button = tk.Button(root, text="Save", width=button_width)
                >>> cancel_button = tk.Button(root, text="Cancel", width=button_width)

            Notes:
                - Este método debe usarse con el locale ya configurado al valor deseado,
                  ya que utiliza el locale actual para las traducciones.
                - Las traducciones deben estar previamente cargadas o definidas mediante
                  los métodos `load()`, `set()` o `set_many()`.
                - El método puede tener problemas con cadenas que contienen espacios, ya que
                  utiliza un enfoque simple de unión de argumentos.
            """
            # Verificar que se proporcionó al menos una cadena
            if not src:
                raise ValueError("Se debe proporcionar al menos una cadena para comparar")

            # Obtiene la ventana raíz de tkinter para acceder al intérprete tcl/tk
            root = get_default_root()

            # Define el comando tcl/tk para determinar la longitud máxima
            command = "::msgcat::mcmax"

            # Une las cadenas con espacios y ejecuta el comando
            # Esto funciona correctamente si las cadenas no contienen espacios internos
            result = root.tk.eval(f'{command} {" ".join(src)}')

            # Convierte el resultado a entero y lo devuelve
            # El valor representa la longitud de la cadena traducida más larga
            return int(result)