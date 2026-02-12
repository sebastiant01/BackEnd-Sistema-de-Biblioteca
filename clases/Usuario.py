import abc
import hashlib


class Usuario(abc.ABC):
    """
    Representa un usuario dentro del sistema, clase abstracta que hereda a las clases hijas Cliente y Empleado.

    Attributes:
        nombre (str): Nombre del usuario.
        DNI (str): DNI del usuario.
        usuario (str): Usuario de inicio de sesión.
        contrasena (str): Contraseña del usuario.
    """

    def __init__(self, nombre: str, DNI: str, usuario: str, contrasena: str):
        self.nombre = nombre
        self.DNI = DNI
        self.usuario = usuario
        self.contrasena = contrasena

    @abc.abstractmethod
    def mostrar_menu(self):
        print(
            f"Nombre: {self.nombre}, DNI: {self.DNI}, Libros prestados actualmente: {self.libros_prestados}"
        )

    @abc.abstractmethod
    def mostrar_data(self):
        print(
            f"Nombre: {self.nombre}, DNI: {self.DNI}, Libros prestados actualmente: {self.libros_prestados}"
        )


class Cliente(Usuario):
    """
    Representa un cliente dentro del sistema. Clase hija que hereda de la clase abstracta
    'Usuario'

    Attributes:
        nombre (str): Nombre del usuario. (Heredado)
        DNI (str): DNI del usuario. (Heredado)
        usuario (str): Usuario de inicio de sesión. (Heredado)
        contrasena (str): Contraseña del usuario. (Heredado)
        libros_prestados (list): Libros que el usuario tiene prestados. Es una lista de
            instancias de la clase 'Libro'
    """

    def __init__(
        self,
        nombre: str,
        DNI: str,
        usuario: str,
        contrasena: str,
        libros_prestados: list[Libro],
    ):
        super().__init__(nombre, DNI, usuario, contrasena)
        self.libros_prestados = libros_prestados

    def mostrar_menu(self):
        while True:
            print(f"--- Menú de usuario ---\n Bienvenido, {self.nombre}.")
            print(
                "Opción 1: Consultar libro, revista, etc.\n"
                "Opción 2: Prestar libro, revista, etc.\n"
                "Opción 3: Devolver libro.\n"
                "Opción 4: Ver datos de usuario.\n"
                "Opción 5: Cerrar sesión"
            )
            opcion = input("Ingrese una opción: ")
            match opcion:
                case "1":
                    print("Ingresó 'Consultar libro, revista, etc'\n")
                    # aquí iría la llamada al método de consultar libro xdxd
                case "2":
                    print("Ingresó 'Prestar libro, revista, etc.'\n")
                    # aquí iría la llamada al método de prestar libro XD
                case "3":
                    print("Ingresó 'Devolver libro'\n")
                    self.devolver_libro()
                case "4":
                    print("Ingresó 'Ver datos de usuario'\n")
                    super().mostrar_data()
                case "5":
                    print("Cerrando sesión...\n")
                    break
                case _:
                    print("Opción inválida. Por favor intente otra vez.\n")

        return "Cerrando sesión..."

    def devolver_libro(self):
        while True:
            n = 1
            for libro in self.libros_prestados:
                print(f"Opción {n}: {libro.titulo}, {libro.autor}")
                n += 1
            opcion = int(input("Ingrese una opción: "))
            try:
                lib = self.libros_prestados[opcion]
                lib.disponible = True
                lib.unidades += 1
                del self.libros_prestados[opcion]
            except Exception:
                continue
            print(f"El libro '{lib.titulo}' fue devuelto con éxito")
            break
        return

    def mostrar_data(self):
        return super().mostrar_data()


class Empleado(Usuario):
    def __init__(self, nombre, DNI, usuario, contrasena):
        super().__init__(nombre, DNI, usuario, contrasena)

    def mostrar_menu(self):
        while True:
            print(f"--- Menú de usuario ---\n Bienvenido, {self.nombre}.")
            print(
                "Opción 1: Consultar libro, revista, etc.\n"
                "Opción 2: Crear usuario\n"
                "Opción 3: Eliminar usuario\n"
                "Opción 4: Agregar libro nuevo\n"
                "Opción 5: Eliminar libro\n"
                "Opción 6: Ver datos de usuario.\n"
                "Opción 7: Cerrar sesión"
            )
            opcion = input("Ingrese una opción: ")
            match opcion:
                case "1":
                    print("Ingresó 'Consultar libro, revista, etc'\n")
                    # aquí iría la llamada al método de consultar libro
                case "2":
                    print("Ingresó 'Crear usuario'\n")
                    # aquí iría la llamada al método de crear usuario uwu
                case "3":
                    print("Ingresó 'Eliminar usuario'\n")
                    # aquí irá la llamada al método de eliminar usuario
                case "4":
                    print("Ingresó 'Agregar libro nuevo'\n")
                    # aquí irá la llamada al método de agregar libro
                case "5":
                    print("Ingresó 'Eliminar libro'\n")
                    # aquí irá la llamada al método de eliminar libro Bv
                case "6":
                    print("Ingresó 'Ver datos de usuario'\n")
                    super().mostrar_data()
                case "7":
                    print("Cerrando sesión...\n")
                    break
                case _:
                    print("Opción inválida. Por favor intente otra vez.\n")

        return "Cerrando sesión..."

    def mostrar_data(self):
        return super().mostrar_data()
