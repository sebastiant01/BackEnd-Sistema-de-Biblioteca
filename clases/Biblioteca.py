class Biblioteca:
    """
    Representa una biblioteca que gestiona un catálogo de entidades
    (por ejemplo, libros) organizadas por código y por autor.

    La biblioteca permite:
        - Registrar nuevas entidades.
        - Consultar el catálogo completo.
        - Buscar entidades por autor.
        - Buscar entidades por código único.

    Attributes:
        nombre (str): Nombre identificador de la biblioteca.
        por_autor (dict[str, list[object]]): Diccionario que agrupa
            las entidades por autor. La clave es el nombre del autor
            y el valor es una lista de entidades asociadas.
        por_codigo (dict[str, object]): Diccionario que almacena
            las entidades registradas usando su código único como clave.
    """

    def __init__(self, nombre: str):
        """
        Inicializa una nueva instancia de Biblioteca.

        Args:
            nombre (str): Nombre de la biblioteca.
        """
        self.nombre: str = nombre
        self.por_autor: dict[str, list] = {}
        self.por_codigo: dict[str, object] = {}

    def registrar_entidad(self, codigo: str, autor: str, entidad: object) -> None:
        """
        Registra una nueva entidad en la biblioteca.

        La entidad se almacena:
            - En el diccionario 'por_codigo' usando su código único.
            - En el diccionario 'por_autor' agrupada bajo el nombre del autor.

        Args:
            codigo (str): Código único que identifica la entidad.
            autor (str): Nombre del autor asociado a la entidad.
            entidad (object): Objeto que se desea registrar.

        Returns:
            None
        """
        self.por_codigo[codigo] = entidad

        if autor not in self.por_autor:
            self.por_autor[autor] = []
        self.por_autor[autor].append(entidad)

    def catalogo(self) -> str:
        """
        Genera una representación textual del catálogo completo
        de la biblioteca.

        Returns:
            str: Cadena formateada con:
                - Nombre de la biblioteca.
                - Total de elementos registrados.
                - Información de cada entidad con su código.

            Si no hay elementos registrados, devuelve un mensaje
            indicando que el catálogo está vacío.
        """
        if not self.por_codigo:
            return "El catálogo está vacío."

        resultado = f"=== Catálogo de {self.nombre} ===\n"
        resultado += f"Total de elementos: {len(self.por_codigo)}\n\n"

        for codigo, entidad in self.por_codigo.items():
            resultado += f"Código: {codigo}\n"
            resultado += f"Material: {entidad}\n"
            resultado += "-" * 70 + "\n"

        return resultado

    def buscar_por_autor(self, autor: str) -> list[object] | str:
        """
        Busca entidades registradas bajo un autor específico.

        Args:
            autor (str): Nombre del autor a consultar.

        Returns:
            list[object]: Lista de entidades asociadas al autor,
                          si existe en el registro.
            str: Mensaje indicando que no hay registro del autor,
                 si no se encuentra.
        """
        return self.por_autor.get(autor, "No hay registro de este autor.")

    def buscar_por_codigo(self, codigo: str) -> object | str:
        """
        Busca una entidad por su código único.

        Args:
            codigo (str): Código identificador de la entidad.

        Returns:
            object: La entidad correspondiente si existe.
            str: Mensaje indicando que no hay registro del elemento,
                 si el código no se encuentra.
        """
        return self.por_codigo.get(codigo, "No hay registro de este elemento.")
