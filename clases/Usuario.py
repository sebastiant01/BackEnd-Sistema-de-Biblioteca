class Usuario:
    """
    Representa un usuario, con nombre y documento.

    Attributes:
        nombre (str): Nombre del usuario.
        DNI (int): DNI del usuario.
        libros_prestados (list): Lista de libros que actualmente tiene el usuario prestados.
    """

    def __init__(self, nombre: str, DNI: str, libros_prestados: list[Libro]):
        self.nombre = nombre
        self.DNI = DNI
        self.libros_prestados = libros_prestados
        # luego vemos qué más le ponemos al usuario, primero necesitaríamos desarrollar
        # en equipo la lógica y flujo que vamos a seguir

    def mostrar_data(self):
        print(
            f"Nombre: {self.nombre}, DNI: {self.DNI}, Libros prestados actualmente: {self.libros_prestados}"
        )
