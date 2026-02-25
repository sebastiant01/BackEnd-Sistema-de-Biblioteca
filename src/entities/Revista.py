from src.entities.MaterialBiblioteca import MaterialBiblioteca


class Revista(MaterialBiblioteca):
    """
    Representa una revista dentro de la biblioteca.

    Hereda de MaterialBiblioteca y añade atributos específicos
    como la categoría, número de edición y periodicidad.

    Attributes:
        categoria (str):
            Categoría o temática de la revista.

        numero_edicion (int):
            Número de edición de la revista.

        periodicidad (str):
            Frecuencia de publicación (mensual, semanal, etc.).
    """

    def __init__(
        self,
        codigo: str,
        titulo: str,
        autor: str,
        fecha: str,
        cantidad_paginas: int,
        unidades: int,
        categoria: str,
        numero_edicion: int,
        periodicidad: str,
    ) -> None:
        """
        Inicializa una nueva revista.

        Args:
            codigo (str):
                Código único de la revista.

            titulo (str):
                Título de la revista.

            autor (str):
                Editor o responsable principal.

            fecha (str):
                Fecha de publicación.

            cantidad_paginas (int):
                Número total de páginas.

            unidades (int):
                Número de ejemplares disponibles.

            categoria (str):
                Categoría o temática.

            numero_edicion (int):
                Número de edición.

            periodicidad (str):
                Frecuencia de publicación.
        """
        super().__init__(codigo, titulo, autor, fecha, cantidad_paginas, unidades)
        self.categoria: str = categoria
        self.numero_edicion: int = numero_edicion
        self.periodicidad: str = periodicidad

    def __str__(self) -> str:
        """
        Devuelve una representación detallada de la revista.

        Returns:
            str:
                Cadena con información completa de la revista.
        """
        base: str = super().__str__()
        return f"{base} | {self.categoria} | Edición {self.numero_edicion} | {self.periodicidad}"
