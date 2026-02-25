"""
Módulo principal del Sistema de Biblioteca.
Gestiona el flujo de interacción con el usuario, menús y autenticación.
"""

import sys
from src.entities.Usuario import Usuario
from src.entities.Cliente import Cliente
from src.entities.Empleado import Empleado
from src.entities.Biblioteca import Biblioteca
from src.entities.MaterialBiblioteca import MaterialBiblioteca

# Variables globales (snake_case según PEP 8)
usuarios_registrados: dict[str, Usuario] = {}
biblioteca_principal = Biblioteca("Default")


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

        # Nota: Se asume que Cliente recibe (nombre, dni, lista_materiales)
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

        opcion = input()

        match opcion:
            case "1":
                autor = input("Ingrese el nombre del autor: ")
                material_autor = biblioteca_principal.buscar_por_autor(autor)
                # Iteramos para mostrar cada coincidencia
                for material in material_autor:
                    print(material.__str__())
                continue

            case "2":
                codigo = input("Ingrese el código del material: ")
                material_codigo = biblioteca_principal.buscar_por_codigo(codigo)
                # Asumimos que buscar_por_codigo retorna un objeto único o manejable
                print(material_codigo.__str__())
                continue

            case "3":
                titulo = input("Ingrese el título del material: ")
                material_titulo = biblioteca_principal.buscar_por_titulo(titulo)
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
    user = None

    # 1. Bucle de Autenticación
    while True:
        print("Bienvenido al sistema de biblioteca. ¿Se encuentra registrado?")
        opcion = input("(s/n): ").strip().lower()

        if opcion == "s":
            user = iniciar_sesion()
        elif opcion == "n":
            user = registrarse()
        else:
            print("Opción inválida. Por favor intente otra vez")
            continue

        if user is None:
            print("Error cargando al usuario o usuario no registrado.")
            # Dependiendo de la lógica, aquí podrías querer repetir el bucle o salir
            # Por ahora mantenemos tu flujo: 'continue' vuelve a preguntar
            continue

        break

    # 2. Bucle Principal del Menú
    while True:
        mostrar_menu(user)
        opcion = input("Seleccione una opción: ").strip()

        match opcion:
            case "1":
                print("Consultando material disponible...")
                menu_consulta()

            case "2":
                tipo_usuario = verificar_usuario_activo(user)
                if tipo_usuario == "Empleado":
                    print("Error: Sólo los clientes pueden prestar material.")
                    continue

                print("Prestando material...")
                user.prestar_material(biblioteca_principal)

            case "3":
                tipo_usuario = verificar_usuario_activo(user)
                if tipo_usuario == "Empleado":
                    print("Error: Sólo los clientes pueden devolver material.")
                    continue
                print("Devolviendo material...")
                user.devolver_material(biblioteca_principal)

            case "4":
                tipo_usuario = verificar_usuario_activo(user)
                if tipo_usuario == "Cliente":
                    print("Error: Sólo los empleados pueden registrar material.")
                    continue

                print("Registrando material...")

                # Validación en cascada para registrar
                codigo = input("Ingrese el código de barras del material: ").strip()
                if verificar_entrada_vacia(codigo):
                    print("Saliendo de registrar material...")
                    continue

                autor = input("Ingrese el autor del material a registrar: ").strip()
                if verificar_entrada_vacia(autor):
                    print("Saliendo de registrar material...")
                    continue

                titulo = input("Ingrese el título del material a registrar: ").strip()
                if verificar_entrada_vacia(titulo):
                    print("Saliendo de registrar material...")
                    continue

                fecha = input("Ingrese el año de publicación: ").strip()
                if verificar_entrada_vacia(fecha):
                    print("Saliendo de registrar material...")
                    continue

                paginas = input("Ingrese el número de páginas del material: ").strip()
                if verificar_entrada_vacia(paginas) or not paginas.isdigit():
                    print("Dato inválido. Saliendo de registrar material...")
                    continue

                unidades = input("Ingrese las unidades disponibles: ").strip()
                if verificar_entrada_vacia(unidades) or not unidades.isdigit():
                    print("Dato inválido. Saliendo de registrar material...")
                    continue

                # Creación y registro del material
                material = MaterialBiblioteca(
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


# Bloque de ejecución estándar
if __name__ == "__main__":
    main()
