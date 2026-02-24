from abc import ABC, abstractmethod
from src.entities.Biblioteca import Biblioteca
from src.entities.MaterialBiblioteca import MaterialBiblioteca


class Usuario(ABC):
    """
    Representa un usuario dentro del sistema, clase abstracta que hereda a las clases hijas Cliente y Empleado.

    Attributes:
        nombre (str): Nombre del usuario.
        DNI (str): DNI del usuario.
        usuario (str): Usuario de inicio de sesión.
        contrasena (str): Contraseña del usuario.
    """

    def __init__(self, nombre: str, DNI: str):
        """
        Inicializa una nueva instancia de Biblioteca.

        Args:
            nombre (str): Nombre del usuario.
            DNI (str): DNI del usuario.
        """
        self.nombre = nombre
        self.DNI = DNI

    @abstractmethod
    def mostrar_data(self):
        """
        Método abstracto que muestra los datos del usuario activo, sea cliente o empleado.

        Returns:
            None
        """
