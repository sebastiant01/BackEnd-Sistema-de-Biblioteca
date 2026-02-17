class Revista:
    """
    Representa una revista con información básica

    Attributes:
        titulo (str): Título de la revista
        autor (str): Autor o editor principal
        numero_edicion (str): Número de edición
        fecha_publicacion (str): Fecha de publicación
        editorial (str): Editorial de la revista
        unidades (int): Cantidad disponible
        disponible (bool): Indica si hay unidades disponibles
    """

    def __init__(
        self,
        titulo: str,
        autor: str,
        numero_edicion: str,
        fecha_publicacion: str,
        editorial: str,
        unidades: int
    ):
        self.titulo = titulo
        self.autor = autor
        self.numero_edicion = numero_edicion
        self.fecha_publicacion = fecha_publicacion
        self.editorial = editorial
        self.unidades = unidades
        self.disponible = True if unidades > 0 else False
