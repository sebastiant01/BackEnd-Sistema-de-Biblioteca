class MaterialBiblioteca:
    """
    Representa un material genérico dentro de una biblioteca.

    Esta clase sirve como base para distintos tipos de materiales
    (por ejemplo, libros, revistas o periódicos), estandarizando
    los atributos comunes que comparten todos ellos.

    Attributes:
        codigo (str):
            Identificador único del material.

        titulo (str):
            Título del material.

        autor (str):
            Nombre del autor del material.

        fecha (str):
            Fecha de publicación o lanzamiento.

        cantidad_paginas (int):
            Número total de páginas del material.

        unidades (int):
            Cantidad de ejemplares disponibles en la biblioteca.

        disponible (bool):
            Indica si el material está disponible para préstamo.
    """

    def __init__(
        self,
        codigo: str,
        titulo: str,
        autor: str,
        fecha: str,
        cantidad_paginas: int,
        unidades: int,
    ) -> None:
        """
        Inicializa un nuevo material de biblioteca.

        Args:
            codigo (str):
                Código único que identifica el material.

            titulo (str):
                Título del material.

            autor (str):
                Autor del material.

            fecha (str):
                Fecha de publicación.

            cantidad_paginas (int):
                Número de páginas del material.

            unidades (int):
                Número de ejemplares disponibles.
        """
        self.codigo: str = codigo
        self.titulo: str = titulo
        self.autor: str = autor
        self.fecha: str = fecha
        self.cantidad_paginas: int = cantidad_paginas
        self.unidades: int = unidades
        self.disponible: bool = True

    def __str__(self) -> str:
        """
        Devuelve una representación textual simplificada del material.

        Returns:
            str:
                Cadena con el tipo de material y sus datos principales.
        """
        return (
            f"{self.__class__.__name__}: "
            f"{self.codigo} | {self.titulo} | {self.autor} | {self.fecha}"
        )
