from MaterialBiblioteca import MaterialBiblioteca


class Libro(MaterialBiblioteca):
    """
    Representa un libro dentro de la biblioteca.

    Hereda de MaterialBiblioteca y añade atributos específicos
    como el género y el ISBN.

    Attributes:
        genero (str):
            Categoría o género literario del libro.

        isbn (str):
            Número estándar internacional que identifica el libro.
    """

    def __init__(
        self,
        codigo: str,
        titulo: str,
        autor: str,
        fecha: str,
        genero: str,
        cantidad_paginas: int,
        unidades: int,
        isbn: str,
    ) -> None:
        """
        Inicializa un nuevo libro.

        Args:
            codigo (str):
                Código único del libro.

            titulo (str):
                Título del libro.

            autor (str):
                Autor del libro.

            fecha (str):
                Fecha de publicación.

            genero (str):
                Género literario.

            cantidad_paginas (int):
                Número total de páginas.

            unidades (int):
                Número de ejemplares disponibles.

            isbn (str):
                Código ISBN del libro.
        """
        super().__init__(codigo, titulo, autor, fecha, cantidad_paginas, unidades)
        self.genero: str = genero
        self.isbn: str = isbn

    def __str__(self) -> str:
        """
        Devuelve una representación detallada del libro.

        Returns:
            str:
                Cadena con información completa del libro.
        """
        base: str = super().__str__
        return f"{base}" f"{self.genero} | {self.isbn}"
