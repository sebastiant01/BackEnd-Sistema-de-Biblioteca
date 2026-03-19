from src.database.config import create_tables

from src.entities import (
    Usuario,
    Autor,
    MaterialBiblioteca,
    Libro,
    Revista,
    Periodico,
    Prestamo,
    Reserva,
    Sancion,
)
from src.crud.usuario_crud import UsuarioCRUD
from src.crud.Revista_crud import RevistaCRUD
from src.crud.Periodico_crud import PeriodicoCRUD
from src.crud.autor_crud import AutorCRUD
from src.utils.security import Security

if __name__ == "__main__":
    create_tables()
    print("Tablas verificadas correctamente en Neon.")


def iniciar_sesion() -> Usuario:
    gestor_crud = UsuarioCRUD()
    gestor_seguridad = Security()
    username = ""
    while True:
        if len(username) == 0:
            print("Ingrese su nombre de usuario (username): ")
            username = input().strip()

            usuario = gestor_crud.consultar_usuario_por_username(username)
            if not usuario:
                print("El usuario ingresado no existe, por favor intente nuevamente")
                username = ""
                continue

        print("Ingrese su contraseña: ")
        contrasena_plana = input().strip()
        hash_guardado = usuario.contrasena

        if not gestor_seguridad.verificar_contrasena_ingresada(
            contrasena_plana, hash_guardado
        ):
            print("La contraseña ingresada es incorrecta")
            continue
        print("Credenciales validadas, iniciando sesión...")
        return gestor_crud.consultar_usuario_por_username(username)


def registrar_usuario_nuevo() -> Usuario.Usuario | None:
    gestor_crud = UsuarioCRUD()
    print(f"\nIniciando registro de usuario nuevo...")

    print("Ingrese el nombre: ")
    nuevo_nombre = input().strip()
    print("Ingrese el apellido: ")
    nuevo_apellido = input().strip()
    print("Ingrese el documento de identificación: ")
    nuevo_documento = input().strip()
    print("Ingrese el email: ")
    nuevo_email = input().strip()
    print("Ingrese el teléfono: ")
    nuevo_telefono = input().strip()
    print("Ingrese la contraseña: ")
    nueva_contrasena = input().strip()

    usuario_existente_email = gestor_crud.consultar_usuario_por_email(nuevo_email)
    if usuario_existente_email:
        print("Error: ¡Ese correo ya está registrado en el sistema! x_x")
        return None

    usuario_existente_doc = gestor_crud.consultar_usuario_por_documento(nuevo_documento)
    if usuario_existente_doc:
        print("Error: Alguien ya se registró con ese documento de identidad")
        return None

    if not nuevo_documento.isdigit():
        print(
            "Error: El documento solo puede contener números (sólo documentos colombianos)."
        )
        return None

    if not nuevo_telefono.isdigit():
        print("Error: El teléfono solo puede contener números.")
        return None

    nuevo_user = gestor_crud.crear_usuario(
        nombre_nuevo=nuevo_nombre,
        apellido_nuevo=nuevo_apellido,
        documento_nuevo=nuevo_documento,
        email_nuevo=nuevo_email,
        telefono_nuevo=nuevo_telefono,
        contrasena_nueva=nueva_contrasena,
        rol_nuevo="Usuario",
    )

    if nuevo_user:
        print(f"¡Registro exitoso! Usuario {nuevo_user.username} creado con éxito")
        return nuevo_user
    else:
        print("Falló el registro de usuario. Por favor intente de nuevo")
        return None





def menu_revista(usuario_activo):
    """
    Despliega el menú de gestión de revistas.

    Permite crear, consultar, editar y eliminar revistas.
    Usa el usuario activo en sesión para los campos de auditoría.

    Args:
        usuario_activo: El usuario que tiene la sesión activa en el sistema.
    """
    crud_revista = RevistaCRUD()
    crud_autor = AutorCRUD()

    while True:
        print("\n========== MENÚ REVISTAS ==========")
        print("1. Crear revista")
        print("2. Ver todas las revistas")
        print("3. Buscar revista por código")
        print("4. Editar revista")
        print("5. Eliminar revista")
        print("0. Volver al menú principal")
        print("====================================")

        opcion = input("Seleccione una opción: ").strip()

        match opcion:
            case "1":
                _crear_revista(crud_revista, crud_autor, usuario_activo)
            case "2":
                _listar_revistas(crud_revista)
            case "3":
                _buscar_revista_por_codigo(crud_revista)
            case "4":
                _editar_revista(crud_revista, usuario_activo)
            case "5":
                _eliminar_revista(crud_revista)
            case "0":
                print("Volviendo al menú principal...")
                break
            case _:
                print("Opción inválida. Por favor intente de nuevo.")


def _crear_revista(crud_revista, crud_autor, usuario_activo):
    """
    Solicita los datos necesarios y crea una nueva revista.

    Args:
        crud_revista: Instancia del CRUD de Revista.
        crud_autor: Instancia del CRUD de Autor.
        usuario_activo: Usuario en sesión para auditoría.
    """
    print("\n--- Crear nueva revista ---")

    autores = crud_autor.obtener_todos_los_autores()
    if not autores:
        print("No hay autores registrados. Registre un autor primero.")
        return
    print("\nAutores disponibles:")
    for a in autores:
        print(f"  ID: {a.id_autor} | {a.nombre_autor} {a.apellido_autor or ''}")

    print("\nIngrese el código de la revista (debe empezar con 'R', ej: R001): ")
    codigo = input().strip()
    print("Ingrese el título de la revista: ")
    titulo = input().strip()
    print("Ingrese el ID del autor: ")
    id_autor = input().strip()
    print("Ingrese el volumen: ")
    try:
        volumen = int(input().strip())
    except ValueError:
        print("Error: El volumen debe ser un número.")
        return
    print("Ingrese el número de edición: ")
    try:
        numero_edicion = int(input().strip())
    except ValueError:
        print("Error: El número de edición debe ser un número.")
        return
    print("Ingrese la fecha de publicación (YYYY-MM-DD) o presione Enter para omitir: ")
    fecha_str = input().strip()
    fecha = None
    if fecha_str:
        from datetime import date

        try:
            fecha = date.fromisoformat(fecha_str)
        except ValueError:
            print("Formato de fecha inválido, se omitirá.")

    print("Ingrese una descripción (opcional, presione Enter para omitir): ")
    descripcion = input().strip() or None

    try:
        revista = crud_revista.crear_revista(
            codigo_material=codigo,
            titulo_material=titulo,
            id_autor=id_autor,
            volumen=volumen,
            numero_edicion=numero_edicion,
            id_usuario_crea=usuario_activo.id_usuario,
            descripcion_material=descripcion,
            fecha_material=fecha,
        )
        print(f"\n¡Revista creada exitosamente!")
        print(f"  ID: {revista.id_revista}")
        print(f"  Código: {revista.codigo_material}")
        print(f"  Título: {revista.titulo_material}")
    except ValueError as e:
        print(f"Error: {e}")


def _listar_revistas(crud_revista):
    """
    Lista todas las revistas registradas en el sistema.

    Args:
        crud_revista: Instancia del CRUD de Revista.
    """
    print("\n--- Todas las revistas ---")
    revistas = crud_revista.obtener_revistas()
    if not revistas:
        print("No hay revistas registradas.")
        return
    for r in revistas:
        print(
            f"  Código: {r.codigo_material} | Título: {r.titulo_material} | "
            f"Volumen: {r.volumen} | Edición: {r.numero_edicion} | "
            f"Disponible: {'Sí' if r.disponibilidad_material else 'No'}"
        )


def _buscar_revista_por_codigo(crud_revista):
    """
    Busca y muestra una revista por su código.

    Args:
        crud_revista: Instancia del CRUD de Revista.
    """
    print("\n--- Buscar revista por código ---")
    codigo = input("Ingrese el código de la revista (ej: R001): ").strip()

    revista = crud_revista.obtener_revista_por_codigo(codigo)
    if not revista:
        print("No se encontró ninguna revista con ese código.")
        return

    print(f"\n  ID: {revista.id_revista}")
    print(f"  Código: {revista.codigo_material}")
    print(f"  Título: {revista.titulo_material}")
    print(f"  Volumen: {revista.volumen}")
    print(f"  Edición: {revista.numero_edicion}")
    print(f"  Disponible: {'Sí' if revista.disponibilidad_material else 'No'}")


def _editar_revista(crud_revista, usuario_activo):
    """
    Edita los campos de una revista existente.

    Args:
        crud_revista: Instancia del CRUD de Revista.
        usuario_activo: Usuario en sesión para auditoría.
    """
    print("\n--- Editar revista ---")
    codigo = input("Ingrese el código de la revista a editar (ej: R001): ").strip()

    revista = crud_revista.obtener_revista_por_codigo(codigo)
    if not revista:
        print("No se encontró ninguna revista con ese código.")
        return

    print(
        f"Editando: {revista.titulo_material} | Volumen: {revista.volumen} | Edición: {revista.numero_edicion}"
    )
    print("Presione Enter para mantener el valor actual.")

    campos = {}

    print(f"Nuevo título [{revista.titulo_material}]: ")
    nuevo_titulo = input().strip()
    if nuevo_titulo:
        campos["titulo_material"] = nuevo_titulo

    print(f"Nuevo volumen [{revista.volumen}]: ")
    nuevo_volumen = input().strip()
    if nuevo_volumen:
        try:
            campos["volumen"] = int(nuevo_volumen)
        except ValueError:
            print("Volumen inválido, se mantendrá el actual.")

    print(f"Nuevo número de edición [{revista.numero_edicion}]: ")
    nuevo_numero = input().strip()
    if nuevo_numero:
        try:
            campos["numero_edicion"] = int(nuevo_numero)
        except ValueError:
            print("Número de edición inválido, se mantendrá el actual.")

    if not campos:
        print("No se realizaron cambios.")
        return

    try:
        revista = crud_revista.actualizar_revista(
            revista_id=revista.id_revista,
            id_usuario_edita=usuario_activo.id_usuario,
            **campos,
        )
        print("\n¡Revista actualizada exitosamente!")
    except ValueError as e:
        print(f"Error: {e}")


def _eliminar_revista(crud_revista):
    """
    Elimina una revista del sistema por su código.

    Args:
        crud_revista: Instancia del CRUD de Revista.
    """
    print("\n--- Eliminar revista ---")
    codigo = input("Ingrese el código de la revista a eliminar (ej: R001): ").strip()

    revista = crud_revista.obtener_revista_por_codigo(codigo)
    if not revista:
        print("No se encontró ninguna revista con ese código.")
        return

    confirmacion = input(
        f"¿Está seguro que desea eliminar '{revista.titulo_material}'? (si/no): "
    ).lower()

    if confirmacion != "si":
        print("Eliminación cancelada.")
        return

    if crud_revista.eliminar_revista(revista.id_revista):
        print("Revista eliminada exitosamente.")
    else:
        print("Error al eliminar la revista.")




def menu_periodico(usuario_activo):
    """
    Despliega el menú de gestión de periódicos.

    Permite crear, consultar, editar y eliminar periódicos.
    Usa el usuario activo en sesión para los campos de auditoría.

    Args:
        usuario_activo: El usuario que tiene la sesión activa en el sistema.
    """
    crud_periodico = PeriodicoCRUD()
    crud_autor = AutorCRUD()

    while True:
        print("\n========== MENÚ PERIÓDICOS ==========")
        print("1. Crear periódico")
        print("2. Ver todos los periódicos")
        print("3. Buscar periódico por código")
        print("4. Editar periódico")
        print("5. Eliminar periódico")
        print("0. Volver al menú principal")
        print("======================================")

        opcion = input("Seleccione una opción: ").strip()

        match opcion:
            case "1":
                _crear_periodico(crud_periodico, crud_autor, usuario_activo)
            case "2":
                _listar_periodicos(crud_periodico)
            case "3":
                _buscar_periodico_por_codigo(crud_periodico)
            case "4":
                _editar_periodico(crud_periodico, usuario_activo)
            case "5":
                _eliminar_periodico(crud_periodico)
            case "0":
                print("Volviendo al menú principal...")
                break
            case _:
                print("Opción inválida. Por favor intente de nuevo.")


def _crear_periodico(crud_periodico, crud_autor, usuario_activo):
    """
    Solicita los datos necesarios y crea un nuevo periódico.

    Args:
        crud_periodico: Instancia del CRUD de Periódico.
        crud_autor: Instancia del CRUD de Autor.
        usuario_activo: Usuario en sesión para auditoría.
    """
    print("\n--- Crear nuevo periódico ---")

    autores = crud_autor.obtener_todos_los_autores()
    if not autores:
        print("No hay autores registrados. Registre un autor primero.")
        return
    print("\nAutores disponibles:")
    for a in autores:
        print(f"  ID: {a.id_autor} | {a.nombre_autor} {a.apellido_autor or ''}")

    print("\nIngrese el código del periódico (debe empezar con 'P', ej: P001): ")
    codigo = input().strip()
    print("Ingrese el título del periódico: ")
    titulo = input().strip()
    print("Ingrese el ID del autor: ")
    id_autor = input().strip()
    print("Ingrese la ciudad de publicación: ")
    ciudad = input().strip()
    print("Ingrese la sección del periódico (ej: deportes, política): ")
    seccion = input().strip()
    print("Ingrese la fecha de publicación (YYYY-MM-DD) o presione Enter para omitir: ")
    fecha_str = input().strip()
    fecha = None
    if fecha_str:
        from datetime import date

        try:
            fecha = date.fromisoformat(fecha_str)
        except ValueError:
            print("Formato de fecha inválido, se omitirá.")

    print("Ingrese una descripción (opcional, presione Enter para omitir): ")
    descripcion = input().strip() or None

    try:
        periodico = crud_periodico.crear_periodico(
            codigo_periodico=codigo,
            titulo_periodico=titulo,
            id_autor=id_autor,
            ciudad_publicacion=ciudad,
            seccion_periodico=seccion,
            id_usuario_crea=usuario_activo.id_usuario,
            descripcion_periodico=descripcion,
            fecha_periodico=fecha,
        )
        print(f"\n¡Periódico creado exitosamente!")
        print(f"  ID: {periodico.id_periodico}")
        print(f"  Código: {periodico.codigo_material}")
        print(f"  Título: {periodico.titulo_material}")
    except ValueError as e:
        print(f"Error: {e}")


def _listar_periodicos(crud_periodico):
    """
    Lista todos los periódicos registrados en el sistema.

    Args:
        crud_periodico: Instancia del CRUD de Periódico.
    """
    print("\n--- Todos los periódicos ---")
    periodicos = crud_periodico.obtener_periodicos()
    if not periodicos:
        print("No hay periódicos registrados.")
        return
    for p in periodicos:
        print(
            f"  Código: {p.codigo_material} | Título: {p.titulo_material} | "
            f"Ciudad: {p.ciudad_publicacion} | Sección: {p.seccion_periodico} | "
            f"Disponible: {'Sí' if p.disponibilidad_material else 'No'}"
        )


def _buscar_periodico_por_codigo(crud_periodico):
    """
    Busca y muestra un periódico por su código.

    Args:
        crud_periodico: Instancia del CRUD de Periódico.
    """
    print("\n--- Buscar periódico por código ---")
    codigo = input("Ingrese el código del periódico (ej: P001): ").strip()

    periodico = crud_periodico.obtener_periodico_codigo(codigo)
    if not periodico:
        print("No se encontró ningún periódico con ese código.")
        return

    print(f"\n  ID: {periodico.id_periodico}")
    print(f"  Código: {periodico.codigo_material}")
    print(f"  Título: {periodico.titulo_material}")
    print(f"  Ciudad: {periodico.ciudad_publicacion}")
    print(f"  Sección: {periodico.seccion_periodico}")
    print(f"  Disponible: {'Sí' if periodico.disponibilidad_material else 'No'}")


def _editar_periodico(crud_periodico, usuario_activo):
    """
    Edita los campos de un periódico existente.

    Args:
        crud_periodico: Instancia del CRUD de Periódico.
        usuario_activo: Usuario en sesión para auditoría.
    """
    print("\n--- Editar periódico ---")
    codigo = input("Ingrese el código del periódico a editar (ej: P001): ").strip()

    periodico = crud_periodico.obtener_periodico_codigo(codigo)
    if not periodico:
        print("No se encontró ningún periódico con ese código.")
        return

    print(f"Editando: {periodico.titulo_material}")
    print("Presione Enter para mantener el valor actual.")

    campos = {}

    print(f"Nuevo título [{periodico.titulo_material}]: ")
    nuevo_titulo = input().strip()
    if nuevo_titulo:
        campos["titulo_material"] = nuevo_titulo

    print(f"Nueva ciudad de publicación [{periodico.ciudad_publicacion}]: ")
    nueva_ciudad = input().strip()
    if nueva_ciudad:
        campos["ciudad_publicacion"] = nueva_ciudad

    print(f"Nueva sección [{periodico.seccion_periodico}]: ")
    nueva_seccion = input().strip()
    if nueva_seccion:
        campos["seccion_periodico"] = nueva_seccion

    if not campos:
        print("No se realizaron cambios.")
        return

    try:
        periodico = crud_periodico.actualizar_periodico(
            id_periodico=periodico.id_periodico,
            id_usuario_edita=usuario_activo.id_usuario,
            **campos,
        )
        print("\n¡Periódico actualizado exitosamente!")
    except ValueError as e:
        print(f"Error: {e}")


def _eliminar_periodico(crud_periodico):
    """
    Elimina un periódico del sistema por su código.

    Args:
        crud_periodico: Instancia del CRUD de Periódico.
    """
    print("\n--- Eliminar periódico ---")
    codigo = input("Ingrese el código del periódico a eliminar (ej: P001): ").strip()

    periodico = crud_periodico.obtener_periodico_codigo(codigo)
    if not periodico:
        print("No se encontró ningún periódico con ese código.")
        return

    confirmacion = input(
        f"¿Está seguro que desea eliminar '{periodico.titulo_material}'? (si/no): "
    ).lower()

    if confirmacion != "si":
        print("Eliminación cancelada.")
        return

    if crud_periodico.eliminar_periodico(periodico.id_periodico):
        print("Periódico eliminado exitosamente.")
    else:
        print("Error al eliminar el periódico.")


def menu_principal(usuario_activo):
    """
    Despliega el menú principal del sistema de biblioteca.

    Desde aquí se puede acceder a los submenús de cada entidad.

    Args:
        usuario_activo: El usuario que tiene la sesión activa en el sistema.
    """
    while True:
        print(f"\n========== SISTEMA DE BIBLIOTECA ==========")
        print(
            f"Usuario: {usuario_activo.nombre} {usuario_activo.apellido} | Rol: {usuario_activo.rol}"
        )
        print("1. Gestionar Revistas")
        print("2. Gestionar Periódicos")
        print("0. Cerrar sesión")
        print("============================================")

        opcion = input("Seleccione una opción: ").strip()

        match opcion:
            case "1":
                menu_revista(usuario_activo)
            case "2":
                menu_periodico(usuario_activo)
            case "0":
                print("Cerrando sesión...")
                break
            case _:
                print("Opción inválida. Por favor intente de nuevo.")

usuario_activo = None
while True:
    print("Bienvenido al sistema de la biblioteca. Se encuentra registrado?")
    opcion = input("Si/No: ").lower()

    match opcion:
        case "si":
            print("Iniciando sesión...")
            usuario_activo = iniciar_sesion()
            break

        case "no":
            print("Registrando...")
            usuario_activo = registrar_usuario_nuevo()
            if not usuario_activo:
                print("Falló el registro. Por favor intente nuevamente")
                continue
            break

        case _:
            print("Opción inválida. Por favor intente de nuevo")

if usuario_activo:
    menu_principal(usuario_activo)
