from src.entities.Usuario import Usuario
from src.entities.MaterialBiblioteca import MaterialBiblioteca
from src.entities.Biblioteca import Biblioteca


class Cliente(Usuario):
    """
    Representa un cliente dentro del sistema. Clase hija que hereda de la clase abstracta
    'Usuario'

    Attributes:
        nombre (str): Nombre del usuario. (Heredado)
        DNI (str): DNI del usuario. (Heredado)
        usuario (str): Usuario de inicio de sesión. (Heredado)
        contrasena (str): Contraseña del usuario. (Heredado)
        material_prestado (list[str]): Material que el usuario tiene prestado. Es una lista de
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

    def devolver_material(self, Biblioteca: Biblioteca) -> None:
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

    def prestar_material(self, Biblioteca: Biblioteca) -> None:
        """
        Solicita al usuario el código de un material, verifica que exista y sus unidades
        Reduce en 1 la cantidad de unidades si hay disponibles
        Si las unidades llegan a 0, el libro deja de estar disponible
        """
        while True:
            print("Ingrese el código del material que quiera prestar")
            print(
                "Si no lo conoce, ingrese 'salir' y consulte el material para ver el código"
            )
            codigo = input().strip()
            if codigo.lower() == "salir":
                return

            material = Biblioteca.buscar_por_codigo(codigo)
            if isinstance(material, MaterialBiblioteca):

                if material.unidades > 0:
                    material.unidades -= 1

                    if material.unidades == 0:
                        material.disponible = False

                    print(f"Material '{material.titulo}' prestado correctamente.")
                    self.material_prestado.append(material.codigo)
                    return
                else:
                    print("No hay unidades disponibles para prestar. Intente con otro")
                    continue
            else:
                print("No se encontró el material, intente de nuevo")
                continue

    def mostrar_data(self) -> None:
        """
        Método que imprime los datos del cliente activo.

        Returns:
            None
        """
        print(
            f"Nombre: {self.nombre}, DNI: {self.DNI}, materiales prestados actualmente: {self.material_prestado}"
        )
