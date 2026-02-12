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
        """
        Inicializa una nueva instancia de Biblioteca.

        Args:
            nombre (str): Nombre del usuario.
            DNI (str): DNI del usuario.
            usuario (str): Usuario de inicio de sesión.
            contrasena (str): Contraseña del usuario.
        """
        self.nombre = nombre
        self.DNI = DNI
        self.usuario = usuario
        self.contrasena = contrasena

    @abc.abstractmethod
    def mostrar_menu(self):
        """
        Método abstracto que muestra el menú de opciones, el cual es diferente para el cliente
        que para el empleado.

        Cada menú contiene como opciones las acciones que puede hacer cada usuario
        dependiendo de su tipo

        Returns:
            None
        """
        print(
            f"Nombre: {self.nombre}, DNI: {self.DNI}, Libros prestados actualmente: {self.libros_prestados}"
        )

    @abc.abstractmethod
    def mostrar_data(self):
        """
        Método abstracto que muestra los datos del usuario activo, sea cliente o empleado.

        Returns:
            None
        """
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
        """
        Inicializa una nueva instancia de un usuario de tipo cliente.

        Args:
            nombre (str): Nombre del cliente.
            DNI (str): DNI del cliente.
            usuario (str): Usuario de inicio de sesión.
            contrasena (str): Contraseña del cliente.
            libros_prestados (list): Lista de libros prestados por el cliente actualmente.
        """
        super().__init__(nombre, DNI, usuario, contrasena)
        self.libros_prestados = libros_prestados

    def mostrar_menu(self):
        """
        Método que muestra el menú de opciones que el cliente puede hacer.

        Opciones:
            - Consultar libro: Permite buscar si un libro existe en la biblioteca
            - Prestar libro: Permite pedir prestado un libro si hay unidades disponibles
            - Devolver libro: Permite devolver un libro que el cliente pidió prestado
            - Ver datos de usuario: Permite ver los datos del cliente activo
            - Cerrar sesión: Cierra sesión de forma segura y finaliza el programa

        Returns:
            None
        """
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
        """
        Método que le permite al cliente devolver un libro de su lista de libros prestados.

        Returns:
            None
        """
        while True:
            n = 1
            for libro in self.libros_prestados:
                print(f"Opción {n}: {libro.titulo}, {libro.autor}")
                n += 1
            opcion = int(input("Ingrese una opción: "))
            try:
                lib = self.libros_prestados[opcion - 1]
                lib.disponible = True
                lib.unidades += 1
                del self.libros_prestados[opcion - 1]
            except Exception:
                print("Por favor ingrese una opción válida.")
                continue
            print(f"El libro '{lib.titulo}' fue devuelto con éxito")
            break
        return

    def mostrar_data(self):
        """
        Método que imprime los datos del cliente activo.

        Returns:
            None
        """
        return super().mostrar_data()


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

    def __init__(self, nombre, DNI, usuario, contrasena):
        """
        Inicializa una nueva instancia de un usuario de tipo empleado.

        Args:
            nombre (str): Nombre del empleado.
            DNI (str): DNI del empleado.
            usuario (str): Usuario de inicio de sesión.
            contrasena (str): Contraseña del empleado.
        """
        super().__init__(nombre, DNI, usuario, contrasena)

    def mostrar_menu(self):
        """
        Método que muestra el menú de opciones que el cliente puede hacer.

        Opciones:
            - Consultar libro: Permite buscar si un libro existe en la biblioteca
            - Crear usuario: Permite crear un usuario nuevo
            - Eliminar usuario: Permite eliminar un usuario del sistema
            - Eliminar libro: Permite eliminar un libro del catálogo
            - Ver datos de usuario: Permite ver los datos del empleado activo
            - Cerrar sesión: Cierra sesión de forma segura y finaliza el programa

        Returns:
            None
        """
        while True:
            print(f"--- Menú de usuario ---\n Bienvenido, {self.nombre}.")
            print(
                "Opción 1: Consultar libro, revista, etc.\n"
                "Opción 2: Crear usuario\n"
                "Opción 3: Eliminar usuario\n"
                "Opción 4: Eliminar libro\n"
                "Opción 5: Ver datos de usuario.\n"
                "Opción 6: Cerrar sesión"
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
                    print("Ingresó 'Eliminar libro'\n")
                    # aquí irá la llamada al método de eliminar libro Bv
                case "5":
                    print("Ingresó 'Ver datos de usuario'\n")
                    super().mostrar_data()
                case "6":
                    print("Cerrando sesión...\n")
                    break
                case _:
                    print("Opción inválida. Por favor intente otra vez.\n")

        return "Cerrando sesión..."

    def mostrar_data(self):
        """
        Método que imprime los datos del empleado activo.

        Returns:
            None
        """
        return super().mostrar_data()
