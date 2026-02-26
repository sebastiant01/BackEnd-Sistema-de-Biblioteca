"""
Módulo principal del Sistema de Biblioteca.
Gestiona el flujo de interacción con el usuario, menús y autenticación.
"""

from src.entities.Usuario import Usuario
from src.entities.Cliente import Cliente
from src.entities.Empleado import Empleado
from src.entities.Biblioteca import Biblioteca
from src.entities.MaterialBiblioteca import MaterialBiblioteca
from src.entities.Libro import Libro
from src.entities.Revista import Revista
from src.entities.Periodico import Periodico

# ACLARACIÓN: En este menú, sólo estaremos usando la clase "Cliente" en vez de "Empleado",
# debido a que decidimos simplificar el flujo de ejecución, y tiene casi las mismas funcionalidades
# que cliente (EN ESTE CASO), por lo cual sólo se usará "Cliente.py".s

usuarios_registrados: dict[str, Usuario] = {}
biblioteca_principal = Biblioteca("Default")

# Estas instancias de clases son creadas predeterminadamente para que
# hayan materiales disponibles y se puedan ejecutar correctamente las
# operaciones.
libro1 = Libro(
    codigo="L001",
    titulo="El Principito",
    autor="Antoine de Saint-Exupéry",
    fecha="1943",
    genero="Ficción",
    cantidad_paginas=96,
    unidades=5,
    isbn="978-0156012195",
)

libro2 = Libro(
    codigo="L002",
    titulo="Clean Code",
    autor="Robert C. Martin",
    fecha="2008",
    genero="Programación",
    cantidad_paginas=464,
    unidades=3,
    isbn="978-0132350884",
)

periodico1 = Periodico(
    codigo="P001",
    titulo="El Tiempo",
    autor="Editorial El Tiempo",
    fecha="2026-02-25",
    cantidad_paginas=40,
    unidades=20,
    seccion_principal="Política",
    ciudad_publicacion="Bogotá",
)

revista1 = Revista(
    codigo="R001",
    titulo="National Geographic",
    autor="National Geographic Society",
    fecha="2026-01",
    cantidad_paginas=120,
    unidades=7,
    categoria="Ciencia",
    numero_edicion=305,
    periodicidad="Mensual",
)

biblioteca_principal.registrar_material(
    codigo=libro1.codigo,
    autor=libro1.autor,
    titulo=libro1.titulo,
    material=libro1,
)

biblioteca_principal.registrar_material(
    codigo=libro2.codigo,
    autor=libro2.autor,
    titulo=libro2.titulo,
    material=libro2,
)

biblioteca_principal.registrar_material(
    codigo=periodico1.codigo,
    autor=periodico1.autor,
    titulo=periodico1.titulo,
    material=periodico1,
)

biblioteca_principal.registrar_material(
    codigo=revista1.codigo,
    autor=revista1.autor,
    titulo=revista1.titulo,
    material=revista1,
)


def verificar_entrada_vacia(entrada: str) -> bool:
    """
    Verifica si una cadena de texto está vacía.

    Args:
        entrada (str): El texto a validar.

    Returns:
        bool: True si la cadena está vacía (longitud 0), False en caso contrario.
    """
    if len(entrada) == 0:
        return True
    return False


def validar_fecha(fecha: str) -> bool:
    """
    Verifica si una cadena representa una fecha válida en formato DD/MM/AAAA.

    Args:
        fecha (str): La fecha a validar.

    Returns:
        bool: True si la fecha cumple el formato DD/MM/AAAA y el rango básico
        de día y mes (no contempla años bisiestos), False en caso contrario.
    """
    partes = fecha.split("/")

    if len(partes) != 3:
        return False

    dia, mes, anio = partes

    if not (dia.isdigit() and mes.isdigit() and anio.isdigit()):
        return False

    if not (len(dia) == 2 and len(mes) == 2 and len(anio) == 4):
        return False

    dias_por_mes = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    return 1 <= int(mes) <= 12 and 1 <= int(dia) <= dias_por_mes[int(mes)]


def verificar_usuario_activo(usuario: Usuario) -> str:
    """
    Determina el tipo de rol del usuario (Cliente o Empleado).

    Args:
        usuario (Usuario): La instancia del usuario a verificar.

    Returns:
        str: "Cliente" o "Empleado" según el tipo de instancia.
    """
    if isinstance(usuario, Cliente):
        return "Cliente"
    return "Empleado"


def mostrar_menu(user: Usuario) -> None:
    """
    Imprime en consola las opciones disponibles del menú principal.

    Args:
        user (Usuario): El objeto del usuario que está viendo el menú.
    """
    print(f"\n--- Bienvenido, {user.nombre} ---")
    print("Opciones:")
    print("1. Consultar material disponible")
    print("2. Prestar material")
    print("3. Devolver material")
    print("4. Registrar material")
    print("5. Mostrar catálogo")
    print("6. Ver datos de usuario")
    print("7. Cerrar sesión")


def registrarse() -> Cliente | None:
    """
    Maneja el flujo de registro de un nuevo cliente.
    Solicita DNI y nombre, validando que no existan duplicados.

    Returns:
        Cliente | None: Retorna el objeto Cliente nuevo si es exitoso,
                        o None si el usuario ya existe.
    """
    while True:
        print("Ingrese su número de documento sin separadores")
        dni = input().strip()

        if not dni.isdigit() or verificar_entrada_vacia(dni):
            print("Número inválido, por favor ingrese sólo dígitos")
            continue

        if dni in usuarios_registrados:
            print("Error: El usuario ya existe, por favor inicie sesión")
            return None

        print("Ingrese su nombre")
        nombre = input().strip()

        if verificar_entrada_vacia(nombre):
            print("El nombre no puede estar vacío, vuelva a intentar")
            continue

        user = Cliente(nombre, dni, [])
        usuarios_registrados[dni] = user

        return user


def iniciar_sesion() -> Usuario | None:
    """
    Gestiona la autenticación de un usuario existente mediante su DNI.

    Returns:
        Usuario | None: El objeto Usuario si se encuentra, None si falla o no existe.
    """
    while True:
        print("Por favor ingrese su número de documento:")
        dni = input().strip()

        if not dni.isdigit() or verificar_entrada_vacia(dni):
            print("Número inválido, por favor ingrese sólo dígitos")
            continue

        if dni in usuarios_registrados:
            user = usuarios_registrados.get(dni)
            print("Iniciando sesión...")
            return user

        print("Usuario no encontrado, por favor regístrese")
        return None


def menu_consulta() -> None:
    """
    Despliega y gestiona el submenú de búsqueda de materiales.
    Permite buscar por autor, código o título.
    """
    while True:
        print("\nIngrese una opción de búsqueda:")
        print("1. Buscar por autor")
        print("2. Buscar por código")
        print("3. Buscar por título")
        print("4. Dejar de consultar")

        opcion: str = input()

        match opcion:
            case "1":
                autor: str = input("Ingrese el nombre del autor: ")
                material_autor: list[MaterialBiblioteca] | str = (
                    biblioteca_principal.buscar_por_autor(autor)
                )

                if type(material_autor) == str:
                    print(material_autor.__str__())
                    continue

                for material in material_autor:
                    print(material.__str__())
                continue

            case "2":
                codigo: str = input("Ingrese el código del material: ").strip()
                material_codigo: list[MaterialBiblioteca] | str = (
                    biblioteca_principal.buscar_por_codigo(codigo)
                )
                print(material_codigo.__str__())
                continue

            case "3":
                titulo: str = input("Ingrese el título del material: ").strip()
                material_titulo: list[MaterialBiblioteca] | str = (
                    biblioteca_principal.buscar_por_titulo(titulo)
                )

                if type(material_titulo) == str:
                    print(material_titulo.__str__())

                for material in material_titulo:
                    print(material.__str__())
                continue

            case "4":
                break

            case _:
                print("Opción inválida, por favor vuelva a intentar")
                continue


def main() -> None:
    """
    Función principal de ejecución (Entry Point).
    Controla el ciclo de vida de la aplicación.
    """
    user: Usuario | None = None

    while True:
        print("Bienvenido al sistema de biblioteca. ¿Se encuentra registrado?")
        opcion = input("(s/n): ").strip().lower()

        if opcion == "s":
            user: Usuario | None = iniciar_sesion()
        elif opcion == "n":
            user: Usuario | None = registrarse()
        else:
            print("Opción inválida. Por favor intente otra vez")
            continue

        if user is None:
            print("Error cargando al usuario o usuario no registrado.")
            continue

        break

    while True:
        mostrar_menu(user)
        opcion: str = input("Seleccione una opción: ").strip()

        match opcion:
            case "1":
                print("Consultando material disponible...")
                menu_consulta()

            case "2":
                tipo_usuario: str = verificar_usuario_activo(user)
                if tipo_usuario == "Empleado":
                    print("Error: Sólo los clientes pueden prestar material.")
                    continue

                print("Prestando material...")
                user.prestar_material(biblioteca_principal)

            case "3":
                tipo_usuario: str = verificar_usuario_activo(user)
                if tipo_usuario == "Empleado":
                    print("Error: Sólo los clientes pueden devolver material.")
                    continue
                if not user.material_prestado:
                    print("No tiene materiales prestados.")
                    continue

                print("Devolviendo material...")
                user.devolver_material(biblioteca_principal)

            case "4":
                tipo_usuario: str = verificar_usuario_activo(user)
                if tipo_usuario == "Cliente":
                    print("Error: Sólo los empleados pueden registrar material.")
                    continue

                print("Registrando material...")

                codigo: str = input(
                    "Ingrese el código de barras del material: "
                ).strip()
                if verificar_entrada_vacia(codigo):
                    print("Saliendo de registrar material...")
                    continue

                autor: str = input(
                    "Ingrese el autor del material a registrar: "
                ).strip()
                if verificar_entrada_vacia(autor):
                    print("Saliendo de registrar material...")
                    continue

                titulo: str = input(
                    "Ingrese el título del material a registrar: "
                ).strip()
                if verificar_entrada_vacia(titulo):
                    print("Saliendo de registrar material...")
                    continue

                fecha: str = input(
                    "Ingrese el año de publicación (En formato DD/MM/AAAA): "
                ).strip()
                if verificar_entrada_vacia(fecha) and not validar_fecha(fecha):
                    print("Saliendo de registrar material...")
                    continue

                paginas: int = input(
                    "Ingrese el número de páginas del material: "
                ).strip()
                if verificar_entrada_vacia(paginas) or not paginas.isdigit():
                    print("Dato inválido. Saliendo de registrar material...")
                    continue

                unidades: int = input("Ingrese las unidades disponibles: ").strip()
                if verificar_entrada_vacia(unidades) or not unidades.isdigit():
                    print("Dato inválido. Saliendo de registrar material...")
                    continue

                material: MaterialBiblioteca = MaterialBiblioteca(
                    codigo, titulo, autor, fecha, paginas, unidades
                )
                biblioteca_principal.registrar_material(codigo, autor, titulo, material)

                print("Material registrado con éxito")

            case "5":
                print("Cargando catálogo...")
                print(biblioteca_principal.mostrar_catalogo())

            case "6":
                print("Mostrando datos de usuario...")
                user.mostrar_data()

            case "7":
                print("Cerrando sesión...")
                break

            case _:
                print("Opción inválida.")

    print("Finalizando programa...")


if __name__ == "__main__":
    main()
