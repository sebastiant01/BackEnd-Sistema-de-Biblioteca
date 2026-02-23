from MaterialBiblioteca import MaterialBiblioteca


class Periodico(MaterialBiblioteca):
    """
    Representa un periódico dentro de la biblioteca.

    Hereda de MaterialBiblioteca y añade atributos específicos
    como la sección principal y la ciudad de publicación.

    Attributes:
        seccion_principal (str):
            Sección destacada del periódico (economía, deportes, política, etc.).

        ciudad_publicacion (str):
            Ciudad donde se publica el periódico.
    """

    def __init__(
        self,
        codigo: str,
        titulo: str,
        autor: str,
        fecha: str,
        cantidad_paginas: int,
        unidades: int,
        seccion_principal: str,
        ciudad_publicacion: str,
    ) -> None:
        """
        Inicializa un nuevo periódico.

        Args:
            codigo (str):
                Código único del periódico.

            titulo (str):
                Título del periódico.

            autor (str):
                Editor o responsable principal.

            fecha (str):
                Fecha de publicación.

            cantidad_paginas (int):
                Número total de páginas.

            unidades (int):
                Número de ejemplares disponibles.

            seccion_principal (str):
                Sección principal o destacada.

            ciudad_publicacion (str):
                Ciudad donde se publica.
        """
