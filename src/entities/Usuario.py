import abc
from src.entities.Biblioteca import Biblioteca
from src.entities.MaterialBiblioteca import MaterialBiblioteca


class Usuario(abc.ABC):
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

    @abc.abstractmethod
    def mostrar_data(self):
        """
        Método abstracto que muestra los datos del usuario activo, sea cliente o empleado.

        Returns:
            None
        """


class Cliente(Usuario):
    """
    Representa un cliente dentro del sistema. Clase hija que hereda de la clase abstracta
    'Usuario'

    Attributes:
        nombre (str): Nombre del usuario. (Heredado)
        DNI (str): DNI del usuario. (Heredado)
        usuario (str): Usuario de inicio de sesión. (Heredado)
        contrasena (str): Contraseña del usuario. (Heredado)
        material_prestado (str): Material que el usuario tiene prestado. Es una lista de
            strings, cada elemento siendo el código de un material bibliográfico
    """

    def __init__(self, nombre: str, DNI: str, material_prestado: list[str]):
        """
        Inicializa una nueva instancia de un usuario de tipo cliente.

        Args:
            nombre (str): Nombre del cliente.
            DNI (str): DNI del cliente.
            material_prestado (str): Lista de materiales prestados por el cliente actualmente.
        """
        super().__init__(nombre, DNI)
        self.material_prestado = material_prestado

    def devolver_material(self) -> None:
        """
        Método que le permite al cliente devolver un material de su lista de materiales prestados.

        Returns:
            None
        """
        while True:
            n = 1
            size = len(self.material_prestado)
            for codigo in self.material_prestado:
                material = Biblioteca.buscar_por_codigo(codigo)
                if isinstance(material, MaterialBiblioteca):
                    print(f"Opción {n}: {material.titulo}, {material.autor}")
                    n += 1
                else:
                    continue

            opcion = input("Ingrese una opción: ").strip()
            if opcion.isdigit():
                opcion = int(opcion)

                if 1 <= opcion <= size:
                    codigo = self.material_prestado[opcion - 1]
                    material = Biblioteca.buscar_por_codigo(codigo)
                    if isinstance(material, MaterialBiblioteca):
                        material.disponible = True
                        material.unidades += 1
                        del self.material_prestado[opcion - 1]
                        print("Devuelto con éxito!")
                        break
                    else:
                        print("Error: No se pudo devolver")
                        continue
                else:
                    print("Por favor ingrese una opción válida.")
                    continue

        return

    def mostrar_data(self) -> None:
        """
        Método que imprime los datos del cliente activo.

        Returns:
            None
        """
        print(
            f"Nombre: {self.nombre}, DNI: {self.DNI}, materiales prestados actualmente: {self.material_prestado}"
        )


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
