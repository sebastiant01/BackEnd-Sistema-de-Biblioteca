class Revista:
    """
    Representa una revista dentro de la biblioteca

    Attributes:
        titulo (str): Título de la revista
        categoria (str): Categoría o temática
        numero_edicion (int): Número de edición
        disponible (bool): Indica si está disponible para préstamo
    """

    def __init__(self, titulo: str, categoria: str, numero_edicion: int, disponible: bool = True):
        self.titulo = titulo
        self.categoria = categoria
        self.numero_edicion = numero_edicion
        self.disponible = disponible

    def mostrar_data(self):
        print(
            f"Título: {self.titulo}, Categoría: {self.categoria}, "
            f"Edición: {self.numero_edicion}, Disponible: {self.disponible}"
        )
