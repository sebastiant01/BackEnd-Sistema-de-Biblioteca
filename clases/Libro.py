class Libro:
    """
    Representa un libro dentro del sistema de biblioteca.

    Esta clase encapsula la información básica de un libro,
    incluyendo sus datos bibliográficos y disponibilidad.

    Attributes:
        codigo (str): Identificador único del libro dentro del sistema.
        titulo (str): Título del libro.
        autor (str): Nombre completo del autor.
        cantidad_paginas (str): Número total de páginas del libro.
        fecha_publicacion (str): Fecha de publicación del libro.
        editorial (str): Nombre de la editorial.
        unidades (int): Cantidad de ejemplares disponibles en inventario.
        isbn (str): Código ISBN del libro.
        disponible (bool): Indica si el libro está disponible para préstamo.
                          Por defecto es True.
    """

    def __init__(
        self,
        codigo: str,
        titulo: str,
        autor: str,
        cantidad_paginas: str,
        fecha_publicacion: str,
        editorial: str,
        unidades: int,
        isbn: str,
    ):
        """
        Inicializa una nueva instancia de Libro.

        Args:
            codigo (str): Código único del libro.
            titulo (str): Título del libro.
            autor (str): Nombre del autor.
            cantidad_paginas (str): Número de páginas del libro.
            fecha_publicacion (str): Fecha de publicación.
            editorial (str): Editorial del libro.
            unidades (int): Número de ejemplares disponibles.
            isbn (str): Código ISBN del libro.

        Note:
            El atributo 'disponible' se establece automáticamente en True
            al momento de crear la instancia.
        """
        self.codigo = codigo
        self.titulo = titulo
        self.autor = autor
        self.cantidad_paginas = cantidad_paginas
        self.fecha_publicacion = fecha_publicacion
        self.editorial = editorial
        self.unidades = unidades
        self.isbn = isbn
        self.disponible = True

    def __str__(self) -> str:
        """
        Devuelve una representación legible del libro.

        Returns:
            str: Cadena formateada con la información principal del libro.
        """
        return (
            f"Libro: ["
            f"Código: {self.codigo}, "
            f"Título: {self.titulo}, "
            f"Autor: {self.autor}, "
            f"Cantidad de páginas: {self.cantidad_paginas}, "
            f"Fecha: {self.fecha_publicacion}, "
            f"Editorial: {self.editorial}, "
            f"Unidades: {self.unidades}, "
            f"ISBN: {self.isbn}]"
        )
