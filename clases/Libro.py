class Libro:
    """
    Representa un libro con información básica.

    Attributes:
        titulo (str): Título del libro.
        autor (str): Nombre del autor del libro.
        cantidad_paginas (str): Número de páginas del libro.
        fecha_publicacion (str): Fecha de publicación.
        editorial (str): Editorial del libro.
    """

    def __init__(
        self,
        titulo: str,
        autor: str,
        cantidad_paginas: str,
        fecha_publicacion: str,
        editorial: str,
    ):
        """
        Inicializa una instancia de Libro.

        Args:
            titulo (str): Título del libro.
            autor (str): Nombre del autor.
            cantidad_paginas (str): Número de páginas.
            fecha_publicacion (str): Fecha de publicación.
            editorial (str): Editorial.
        """
        self.titulo = titulo
        self.autor = autor
        self.cantidad_paginas = cantidad_paginas
        self.fecha_publicacion = fecha_publicacion
        self.editorial = editorial

    def imprimir_datos(self):
        print(f"El titulo del libro es {self.titulo} y su autor es {self.autor}")
