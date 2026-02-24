from src.entities.Usuario import Usuario


class Empleado(Usuario):
    """
    Representa un empleado de la biblioteca dentro del sistema. Clase hija que hereda de
    la clase abstracta 'Usuario'

    Attributes:
        nombre (str): Nombre del empleado.
        DNI (str): DNI del empleado.
        usuario (str): Usuario de inicio de sesión.
        contrasena (str): Contraseña del empleado.
    """

    def __init__(self, nombre, DNI) -> None:
        """
        Inicializa una nueva instancia de un usuario de tipo empleado.

        Args:
            nombre (str): Nombre del empleado.
            DNI (str): DNI del empleado.
        """
        super().__init__(nombre, DNI)

    def mostrar_data(self) -> None:
        """
        Método que imprime los datos del empleado activo.

        Returns:
            None
        """
        print(f"Nombre: {self.nombre}, DNI: {self.DNI}")
