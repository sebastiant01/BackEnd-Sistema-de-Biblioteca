from src.entities.Usuario import Usuario
from src.entities.Cliente import Cliente
from src.entities.Empleado import Empleado
from src.entities.Biblioteca import Biblioteca
from src.entities.MaterialBiblioteca import MaterialBiblioteca

usuarios_registrados: dict[str, Usuario] = {}
Biblioteca_Principal = Biblioteca("Default")


def mostrar_menu(user: Usuario) -> None:
    print(f"\n--- Bienvenido, {user.nombre}---")
    print("Opciones:")
    print("1. Consultar material disponible")
    print("2. Prestar material")
    print("3. Devolver material")
    print("4. Registrar material")
    print("5. Mostrar catálogo")
    print("6. Ver datos de usuario")
    print("7. Cerrar sesión")


def registrarse() -> Cliente:

    while True:
        print("Ingrese su número de documento sin separadores")
        DNI = input().strip()
        if not DNI.isdigit() or verificar_entrada_vacia(DNI):
            print("Número inválido, por favor ingrese sólo dígitos")
            continue
        if DNI in usuarios_registrados:
            print("Error: El usuario ya existe, por favor inicie sesión")
            return None

        print("Ingrese su nombre")
        nombre = input().strip()
        if verificar_entrada_vacia(nombre):
            print("El nombre no puede estar vacío, vuelva a intentar")
            continue

        user = Cliente(nombre, DNI, [])
        usuarios_registrados[DNI] = user

        return user


def iniciar_sesion() -> Usuario:
    while True:
        print("Por favor ingrese su número de documento:")
        DNI = input().strip()
        if not DNI.isdigit() or verificar_entrada_vacia(DNI):
            print("Número inválido, por favor ingrese sólo dígitos")
            continue
        if DNI in usuarios_registrados:
            user = usuarios_registrados.get(DNI)
            print("Iniciando sesión...")
            return user
        print("Usuario no encontrado, por favor regístrese")
        return None


def menu_consulta() -> None:
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
                material_autor = Biblioteca_Principal.buscar_por_autor(autor)
                for material in material_autor:
                    print(material.__str__())
                continue

            case "2":
                codigo = input("Ingrese el código del material: ")
                material_codigo = Biblioteca_Principal.buscar_por_codigo(codigo)
                print(material_codigo.__str__())
                continue

            case "3":
                titulo = input("Ingrese el título del material: ")
                material_titulo = Biblioteca_Principal.buscar_por_titulo(titulo)
                for material in material_titulo:
                    print(material_titulo.__str__())
                continue

            case "4":
                break

            case _:
                print("Opción inválida, por favor vuelva a intentar")
                continue


def verificar_entrada_vacia(entrada: str) -> bool:
    if len(entrada) == 0:
        return True
    return False


def verificar_usuario_activo(usuario: Usuario) -> str:
    if isinstance(usuario, Cliente):
        return "Cliente"
    return "Empleado"


def main() -> None:
    user = None
    while True:
        print("Bienvenido al sistema de biblioteca. Se encuentra registrado?")
        opcion = input("(s/n)")
        if opcion.lower() == "s":
            user = iniciar_sesion()
        elif opcion.lower() == "n":
            user = registrarse()
        else:
            print("Opción inválida. Por favor intente otra vez")
            continue

        if user is None:
            print("Error cargando al usuario. Por favor intente otra vez")
            continue

        break

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
                user.prestar_material(Biblioteca_Principal)

            case "3":
                tipo_usuario = verificar_usuario_activo(user)
                if tipo_usuario == "Empleado":
                    print("Error: Sólo los clientes pueden devolver material.")
                    continue
                print("Devolviendo material...")
                user.devolver_material(Biblioteca_Principal)

            case "4":
                tipo_usuario = verificar_usuario_activo(user)
                if tipo_usuario == "Cliente":
                    print("Error: Sólo los empleados pueden registrar material.")
                    continue

                print("Registrando material...")
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
                    print("Saliendo de registrar material...")
                    continue

                unidades = input(
                    "Ingrese las unidades disponibles del material: "
                ).strip()
                if verificar_entrada_vacia(unidades) or not unidades.isdigit():
                    print("Saliendo de registrar material...")
                    continue

                material = MaterialBiblioteca(
                    codigo, titulo, autor, fecha, paginas, unidades
                )
                Biblioteca_Principal.registrar_material(codigo, autor, titulo, material)

                print("Material registrado con éxito")

            case "5":
                print("Cargando catálogo...")
                print(Biblioteca_Principal.mostrar_catalogo())

            case "6":
                print("Mostrando datos de usuario...")
                user.mostrar_data()

            case "7":
                print("Cerrando sesión...")
                break

    print("Finalizando programa...")


main()
