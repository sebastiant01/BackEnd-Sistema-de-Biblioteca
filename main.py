from src.database.config import create_tables, SessionLocal

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
from src.crud.periodico_crud import PeriodicoCRUD
from src.crud.autor_crud import AutorCRUD
from src.crud.libro_crud import LibroCRUD
from src.utils.security import Security

if __name__ == "__main__":
    create_tables()
    print("Tablas verificadas correctamente en Neon.")

db = SessionLocal()


# ====== USUARIO ======


def iniciar_sesion() -> Usuario:
    gestor_crud = UsuarioCRUD(db_session=db)
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


def registrar_usuario_nuevo():
    gestor_crud = UsuarioCRUD(db_session=db)
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


# ====== HELPER AUTOR ======


def _seleccionar_autor(crud_autor) -> str | None:
    autores = crud_autor.obtener_todos_los_autores()
    if not autores:
        print("No hay autores registrados. Registre un autor primero.")
        return None
    print("\nAutores disponibles:")
    for i, a in enumerate(autores, start=1):
        print(f"  {i}. {a.nombre_autor} {a.apellido_autor or ''}")
    print("Seleccione el numero del autor: ")
    seleccion = input().strip()
    if not seleccion.isdigit() or not (1 <= int(seleccion) <= len(autores)):
        print("Seleccion invalida.")
        return None
    return autores[int(seleccion) - 1].id_autor


# ====== MENÚ AUTOR ======


def menu_autor(usuario_activo):
    """
    Despliega el menú de gestión de autores.

    Permite crear, consultar, editar y eliminar autores.
    Usa el usuario activo en sesión para los campos de auditoría.

    Args:
        usuario_activo: El usuario que tiene la sesión activa en el sistema.
    """
    crud_autor = AutorCRUD(db_session=db)

    while True:
        print("\nMENU AUTORES")
        print("1. Crear autor")
        print("2. Ver todos los autores")
        print("3. Buscar autor por nombre")
        print("4. Consultar autor por ID")
        print("5. Editar autor")
        print("6. Eliminar autor")
        print("0. Volver al menu principal")
        opcion = input("Seleccione una opcion: ").strip()

        match opcion:
            case "1":
                _crear_autor(crud_autor, usuario_activo)
            case "2":
                _listar_autores(crud_autor)
            case "3":
                _buscar_autor_por_nombre(crud_autor)
            case "4":
                _consultar_autor_por_id(crud_autor)
            case "5":
                _editar_autor(crud_autor, usuario_activo)
            case "6":
                _eliminar_autor(crud_autor, usuario_activo)
            case "0":
                print("Volviendo al menu principal...")
                break
            case _:
                print("Opcion invalida. Por favor intente de nuevo.")


def _crear_autor(crud_autor, usuario_activo):
    """
    Solicita los datos necesarios y crea un nuevo autor.

    Args:
        crud_autor: Instancia del CRUD de Autor.
        usuario_activo: Usuario en sesión para auditoría.
    """
    print("\n--- Crear nuevo autor ---")
    print("Ingrese el nombre del autor: ")
    nombre = input().strip()
    print("Ingrese el apellido (opcional, presione Enter para omitir): ")
    apellido = input().strip() or None
    print("Ingrese la nacionalidad (opcional, presione Enter para omitir): ")
    nacionalidad = input().strip() or None
    crud_autor.crear_autor(
        nombre_autor=nombre,
        apellido_autor=apellido,
        nacionalidad=nacionalidad,
        id_usuario_sesion=usuario_activo.id_usuario,
    )


def _listar_autores(crud_autor):
    """
    Lista todos los autores activos registrados en el sistema.

    Args:
        crud_autor: Instancia del CRUD de Autor.
    """
    print("\n--- Todos los autores ---")
    autores = crud_autor.obtener_todos_los_autores()
    if not autores:
        print("No hay autores registrados.")
        return
    for a in autores:
        print(
            f"ID: {a.id_autor} | Nombre: {a.nombre_autor} {a.apellido_autor or ''} | "
            f"Nacionalidad: {a.nacionalidad or 'N/A'}"
        )


def _buscar_autor_por_nombre(crud_autor):
    """
    Busca autores cuyo nombre o apellido contenga el termino ingresado.

    Args:
        crud_autor: Instancia del CRUD de Autor.
    """
    print("\n--- Buscar autor por nombre ---")
    termino = input("Ingrese el termino de busqueda: ").strip()
    autores = crud_autor.buscar_autor_por_nombre(termino)
    if not autores:
        print("No se encontraron autores con ese nombre.")
        return
    for a in autores:
        print(f"ID: {a.id_autor} | Nombre: {a.nombre_autor} {a.apellido_autor or ''}")


def _consultar_autor_por_id(crud_autor):
    """
    Busca y muestra un autor por su ID.

    Args:
        crud_autor: Instancia del CRUD de Autor.
    """
    print("\n--- Consultar autor por ID ---")
    id_autor = input("Ingrese el ID del autor: ").strip()
    autor = crud_autor.consultar_autor_por_id(id_autor)
    if not autor:
        print("No se encontro el autor.")
        return
    print(f"\nID: {autor.id_autor}")
    print(f"Nombre: {autor.nombre_autor} {autor.apellido_autor or ''}")
    print(f"Nacionalidad: {autor.nacionalidad or 'N/A'}")
    print(f"Creado: {autor.fecha_creacion}")


def _editar_autor(crud_autor, usuario_activo):
    """
    Edita los campos de un autor existente.

    Args:
        crud_autor: Instancia del CRUD de Autor.
        usuario_activo: Usuario en sesión para auditoría.
    """
    print("\n--- Editar autor ---")
    id_autor = input("Ingrese el ID del autor a editar: ").strip()
    autor = crud_autor.consultar_autor_por_id(id_autor)
    if not autor:
        print("No se encontro el autor.")
        return
    print(f"Editando: {autor.nombre_autor} {autor.apellido_autor or ''}")
    print("Presione Enter para mantener el valor actual.")
    campos = {}
    print(f"Nuevo nombre [{autor.nombre_autor}]: ")
    nuevo_nombre = input().strip()
    if nuevo_nombre:
        campos["nombre_autor"] = nuevo_nombre
    print(f"Nuevo apellido [{autor.apellido_autor or 'N/A'}]: ")
    nuevo_apellido = input().strip()
    if nuevo_apellido:
        campos["apellido_autor"] = nuevo_apellido
    print(f"Nueva nacionalidad [{autor.nacionalidad or 'N/A'}]: ")
    nueva_nacionalidad = input().strip()
    if nueva_nacionalidad:
        campos["nacionalidad"] = nueva_nacionalidad
    if not campos:
        print("No se realizaron cambios.")
        return
    crud_autor.actualizar_autor(
        id_autor=id_autor,
        id_usuario_sesion=usuario_activo.id_usuario,
        **campos,
    )


def _eliminar_autor(crud_autor, usuario_activo):
    """
    Realiza una baja logica del autor (soft delete).

    Args:
        crud_autor: Instancia del CRUD de Autor.
        usuario_activo: Usuario en sesión para auditoría.
    """
    print("\n--- Eliminar autor ---")
    id_autor = input("Ingrese el ID del autor a eliminar: ").strip()
    autor = crud_autor.consultar_autor_por_id(id_autor)
    if not autor:
        print("No se encontro el autor.")
        return
    confirmacion = input(
        f"Esta seguro que desea eliminar '{autor.nombre_autor} {autor.apellido_autor or ''}'? (si/no): "
    ).lower()
    if confirmacion != "si":
        print("Eliminacion cancelada.")
        return
    crud_autor.eliminar_autor(
        id_autor=id_autor,
        id_usuario_sesion=usuario_activo.id_usuario,
    )


# ====== MENÚ LIBRO ======


def menu_libro(usuario_activo):
    """
    Despliega el menú de gestión de libros.

    Permite crear, consultar, editar y eliminar libros.
    Usa el usuario activo en sesión para los campos de auditoría.

    Args:
        usuario_activo: El usuario que tiene la sesión activa en el sistema.
    """
    crud_libro = LibroCRUD(database=db)
    crud_autor = AutorCRUD(db_session=db)

    while True:
        print("\nMENU LIBROS")
        print("1. Crear libro")
        print("2. Ver todos los libros")
        print("3. Buscar libro por codigo")
        print("4. Buscar libro por titulo")
        print("5. Buscar libro por genero")
        print("6. Ver libros disponibles")
        print("7. Editar libro")
        print("8. Cambiar disponibilidad")
        print("9. Eliminar libro")
        print("0. Volver al menu principal")
        opcion = input("Seleccione una opcion: ").strip()

        match opcion:
            case "1":
                _crear_libro(crud_libro, crud_autor, usuario_activo)
            case "2":
                _listar_libros(crud_libro)
            case "3":
                _buscar_libro_por_codigo(crud_libro)
            case "4":
                _buscar_libro_por_titulo(crud_libro)
            case "5":
                _buscar_libro_por_genero(crud_libro)
            case "6":
                _listar_libros_disponibles(crud_libro)
            case "7":
                _editar_libro(crud_libro, usuario_activo)
            case "8":
                _cambiar_disponibilidad_libro(crud_libro, usuario_activo)
            case "9":
                _eliminar_libro(crud_libro)
            case "0":
                print("Volviendo al menu principal...")
                break
            case _:
                print("Opcion invalida. Por favor intente de nuevo.")


def _crear_libro(crud_libro, crud_autor, usuario_activo):
    """
    Solicita los datos necesarios y crea un nuevo libro.

    Args:
        crud_libro: Instancia del CRUD de Libro.
        crud_autor: Instancia del CRUD de Autor.
        usuario_activo: Usuario en sesión para auditoría.
    """
    print("\n--- Crear nuevo libro ---")
    id_autor = _seleccionar_autor(crud_autor)
    if not id_autor:
        return
    print("\nIngrese el codigo del libro (debe empezar con 'L', ej: L001): ")
    codigo = input().strip()
    print("Ingrese el titulo del libro: ")
    titulo = input().strip()
    print("Ingrese el ISBN: ")
    isbn = input().strip()
    print("Ingrese el genero literario: ")
    genero = input().strip()
    print("Ingrese la fecha de publicacion (YYYY-MM-DD) o presione Enter para omitir: ")
    fecha_str = input().strip()
    fecha = None
    if fecha_str:
        from datetime import date

        try:
            fecha = date.fromisoformat(fecha_str)
        except ValueError:
            print("Formato de fecha invalido, se omitira.")
    print("Ingrese una descripcion (opcional, presione Enter para omitir): ")
    descripcion = input().strip() or None
    try:
        libro = crud_libro.crear_libro(
            codigo_libro=codigo,
            titulo_libro=titulo,
            genero_libro=genero,
            id_autor=id_autor,
            codigo_isbn=isbn,
            id_usuario_crea=usuario_activo.id_usuario,
            descripcion_libro=descripcion,
            fecha_libro=fecha,
        )
        print(f"\nLibro creado exitosamente!")
        print(f"ID: {libro.id_libro}")
        print(f"Codigo: {libro.codigo_material}")
        print(f"Titulo: {libro.titulo_material}")
    except ValueError as e:
        print(f"Error: {e}")


def _listar_libros(crud_libro):
    """
    Lista todos los libros registrados en el sistema.

    Args:
        crud_libro: Instancia del CRUD de Libro.
    """
    print("\n--- Todos los libros ---")
    libros = crud_libro.obtener_libros()
    if not libros:
        print("No hay libros registrados.")
        return
    for l in libros:
        print(
            f"Codigo: {l.codigo_material} | Titulo: {l.titulo_material} | "
            f"ISBN: {l.codigo_isbn} | Genero: {l.genero_libro} | "
            f"Disponible: {'Si' if l.disponibilidad_material else 'No'}"
        )


def _buscar_libro_por_codigo(crud_libro):
    """
    Busca y muestra un libro por su codigo.

    Args:
        crud_libro: Instancia del CRUD de Libro.
    """
    print("\n--- Buscar libro por codigo ---")
    codigo = input("Ingrese el codigo del libro (ej: L001): ").strip()
    libro = crud_libro.obtener_libro_codigo(codigo)
    if not libro:
        print("No se encontro ningun libro con ese codigo.")
        return
    print(f"\nID: {libro.id_libro}")
    print(f"Codigo: {libro.codigo_material}")
    print(f"Titulo: {libro.titulo_material}")
    print(f"ISBN: {libro.codigo_isbn}")
    print(f"Genero: {libro.genero_libro}")
    print(f"Descripcion: {libro.descripcion_material or 'N/A'}")
    print(f"Disponible: {'Si' if libro.disponibilidad_material else 'No'}")


def _buscar_libro_por_titulo(crud_libro):
    """
    Busca libros cuyo titulo contenga el termino ingresado.

    Args:
        crud_libro: Instancia del CRUD de Libro.
    """
    print("\n--- Buscar libro por titulo ---")
    titulo = input("Ingrese el titulo a buscar: ").strip()
    libros = crud_libro.buscar_libros_por_titulo(titulo)
    if not libros:
        print("No se encontraron libros con ese titulo.")
        return
    for l in libros:
        print(
            f"Codigo: {l.codigo_material} | Titulo: {l.titulo_material} | Genero: {l.genero_libro}"
        )


def _buscar_libro_por_genero(crud_libro):
    """
    Busca libros cuyo genero contenga el termino ingresado.

    Args:
        crud_libro: Instancia del CRUD de Libro.
    """
    print("\n--- Buscar libro por genero ---")
    genero = input("Ingrese el genero a buscar: ").strip()
    libros = crud_libro.buscar_libros_por_genero(genero)
    if not libros:
        print("No se encontraron libros con ese genero.")
        return
    for l in libros:
        print(
            f"Codigo: {l.codigo_material} | Titulo: {l.titulo_material} | Genero: {l.genero_libro}"
        )


def _listar_libros_disponibles(crud_libro):
    """
    Lista los libros que estan disponibles para prestamo.

    Args:
        crud_libro: Instancia del CRUD de Libro.
    """
    print("\n--- Libros disponibles ---")
    libros = crud_libro.obtener_libros_disponibles()
    if not libros:
        print("No hay libros disponibles en este momento.")
        return
    for l in libros:
        print(
            f"Codigo: {l.codigo_material} | Titulo: {l.titulo_material} | ISBN: {l.codigo_isbn}"
        )


def _editar_libro(crud_libro, usuario_activo):
    """
    Edita los campos de un libro existente.

    Args:
        crud_libro: Instancia del CRUD de Libro.
        usuario_activo: Usuario en sesión para auditoría.
    """
    print("\n--- Editar libro ---")
    codigo = input("Ingrese el codigo del libro a editar (ej: L001): ").strip()
    libro = crud_libro.obtener_libro_codigo(codigo)
    if not libro:
        print("No se encontro ningun libro con ese codigo.")
        return
    print(f"Editando: {libro.titulo_material}")
    print("Presione Enter para mantener el valor actual.")
    campos = {}
    print(f"Nuevo titulo [{libro.titulo_material}]: ")
    nuevo_titulo = input().strip()
    if nuevo_titulo:
        campos["titulo_material"] = nuevo_titulo
    print(f"Nuevo genero [{libro.genero_libro}]: ")
    nuevo_genero = input().strip()
    if nuevo_genero:
        campos["genero_libro"] = nuevo_genero
    print(f"Nuevo ISBN [{libro.codigo_isbn}]: ")
    nuevo_isbn = input().strip()
    if nuevo_isbn:
        campos["codigo_isbn"] = nuevo_isbn
    print(f"Nueva descripcion [{libro.descripcion_material or 'N/A'}]: ")
    nueva_descripcion = input().strip()
    if nueva_descripcion:
        campos["descripcion_material"] = nueva_descripcion
    if not campos:
        print("No se realizaron cambios.")
        return
    try:
        crud_libro.actualizar_libro(
            id_libro=libro.id_libro,
            id_usuario_edita=usuario_activo.id_usuario,
            **campos,
        )
        print("\nLibro actualizado exitosamente!")
    except ValueError as e:
        print(f"Error: {e}")


def _cambiar_disponibilidad_libro(crud_libro, usuario_activo):
    """
    Cambia la disponibilidad de un libro.

    Args:
        crud_libro: Instancia del CRUD de Libro.
        usuario_activo: Usuario en sesión para auditoría.
    """
    print("\n--- Cambiar disponibilidad ---")
    codigo = input("Ingrese el codigo del libro (ej: L001): ").strip()
    libro = crud_libro.obtener_libro_codigo(codigo)
    if not libro:
        print("No se encontro ningun libro con ese codigo.")
        return
    print(
        f"Estado actual: {'Disponible' if libro.disponibilidad_material else 'No disponible'}"
    )
    print("1. Disponible")
    print("2. No disponible")
    opcion = input("Seleccione: ").strip()
    match opcion:
        case "1":
            crud_libro.cambiar_disponibilidad(
                id_libro=libro.id_libro,
                disponible=True,
                id_usuario_edita=usuario_activo.id_usuario,
            )
            print("Libro marcado como disponible.")
        case "2":
            crud_libro.cambiar_disponibilidad(
                id_libro=libro.id_libro,
                disponible=False,
                id_usuario_edita=usuario_activo.id_usuario,
            )
            print("Libro marcado como no disponible.")
        case _:
            print("Opcion invalida.")


def _eliminar_libro(crud_libro):
    """
    Elimina un libro del sistema por su codigo.

    Args:
        crud_libro: Instancia del CRUD de Libro.
    """
    print("\n--- Eliminar libro ---")
    codigo = input("Ingrese el codigo del libro a eliminar (ej: L001): ").strip()
    libro = crud_libro.obtener_libro_codigo(codigo)
    if not libro:
        print("No se encontro ningun libro con ese codigo.")
        return
    confirmacion = input(
        f"Esta seguro que desea eliminar '{libro.titulo_material}'? (si/no): "
    ).lower()
    if confirmacion != "si":
        print("Eliminacion cancelada.")
        return
    if crud_libro.eliminar_libro(libro.id_libro):
        print("Libro eliminado exitosamente.")
    else:
        print("Error al eliminar el libro.")


# ====== MENÚ REVISTA ======


def menu_revista(usuario_activo):
    """
    Despliega el menú de gestión de revistas.

    Permite crear, consultar, editar y eliminar revistas.
    Usa el usuario activo en sesión para los campos de auditoría.

    Args:
        usuario_activo: El usuario que tiene la sesión activa en el sistema.
    """
    crud_revista = RevistaCRUD(db=db)
    crud_autor = AutorCRUD(db_session=db)

    while True:
        print("\nMENU REVISTAS")
        print("1. Crear revista")
        print("2. Ver todas las revistas")
        print("3. Buscar revista por codigo")
        print("4. Editar revista")
        print("5. Eliminar revista")
        print("0. Volver al menu principal")
        opcion = input("Seleccione una opcion: ").strip()

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
                print("Volviendo al menu principal...")
                break
            case _:
                print("Opcion invalida. Por favor intente de nuevo.")


def _crear_revista(crud_revista, crud_autor, usuario_activo):
    """
    Solicita los datos necesarios y crea una nueva revista.

    Args:
        crud_revista: Instancia del CRUD de Revista.
        crud_autor: Instancia del CRUD de Autor.
        usuario_activo: Usuario en sesión para auditoría.
    """
    print("\n--- Crear nueva revista ---")
    id_autor = _seleccionar_autor(crud_autor)
    if not id_autor:
        return
    print("\nIngrese el codigo de la revista (debe empezar con 'R', ej: R001): ")
    codigo = input().strip()
    print("Ingrese el titulo de la revista: ")
    titulo = input().strip()
    print("Ingrese el volumen: ")
    try:
        volumen = int(input().strip())
    except ValueError:
        print("Error: El volumen debe ser un numero.")
        return
    print("Ingrese el numero de edicion: ")
    try:
        numero_edicion = int(input().strip())
    except ValueError:
        print("Error: El numero de edicion debe ser un numero.")
        return
    print("Ingrese la fecha de publicacion (YYYY-MM-DD) o presione Enter para omitir: ")
    fecha_str = input().strip()
    fecha = None
    if fecha_str:
        from datetime import date

        try:
            fecha = date.fromisoformat(fecha_str)
        except ValueError:
            print("Formato de fecha invalido, se omitira.")
    print("Ingrese una descripcion (opcional, presione Enter para omitir): ")
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
        print(f"\nRevista creada exitosamente!")
        print(f"ID: {revista.id_revista}")
        print(f"Codigo: {revista.codigo_material}")
        print(f"Titulo: {revista.titulo_material}")
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
            f"Codigo: {r.codigo_material} | Titulo: {r.titulo_material} | "
            f"Volumen: {r.volumen} | Edicion: {r.numero_edicion} | "
            f"Disponible: {'Si' if r.disponibilidad_material else 'No'}"
        )


def _buscar_revista_por_codigo(crud_revista):
    """
    Busca y muestra una revista por su codigo.

    Args:
        crud_revista: Instancia del CRUD de Revista.
    """
    print("\n--- Buscar revista por codigo ---")
    codigo = input("Ingrese el codigo de la revista (ej: R001): ").strip()
    revista = crud_revista.obtener_revista_por_codigo(codigo)
    if not revista:
        print("No se encontro ninguna revista con ese codigo.")
        return
    print(f"\nID: {revista.id_revista}")
    print(f"Codigo: {revista.codigo_material}")
    print(f"Titulo: {revista.titulo_material}")
    print(f"Volumen: {revista.volumen}")
    print(f"Edicion: {revista.numero_edicion}")
    print(f"Disponible: {'Si' if revista.disponibilidad_material else 'No'}")


def _editar_revista(crud_revista, usuario_activo):
    """
    Edita los campos de una revista existente.

    Args:
        crud_revista: Instancia del CRUD de Revista.
        usuario_activo: Usuario en sesión para auditoría.
    """
    print("\n--- Editar revista ---")
    codigo = input("Ingrese el codigo de la revista a editar (ej: R001): ").strip()
    revista = crud_revista.obtener_revista_por_codigo(codigo)
    if not revista:
        print("No se encontro ninguna revista con ese codigo.")
        return
    print(
        f"Editando: {revista.titulo_material} | Volumen: {revista.volumen} | Edicion: {revista.numero_edicion}"
    )
    print("Presione Enter para mantener el valor actual.")
    campos = {}
    print(f"Nuevo titulo [{revista.titulo_material}]: ")
    nuevo_titulo = input().strip()
    if nuevo_titulo:
        campos["titulo_material"] = nuevo_titulo
    print(f"Nuevo volumen [{revista.volumen}]: ")
    nuevo_volumen = input().strip()
    if nuevo_volumen:
        try:
            campos["volumen"] = int(nuevo_volumen)
        except ValueError:
            print("Volumen invalido, se mantendra el actual.")
    print(f"Nuevo numero de edicion [{revista.numero_edicion}]: ")
    nuevo_numero = input().strip()
    if nuevo_numero:
        try:
            campos["numero_edicion"] = int(nuevo_numero)
        except ValueError:
            print("Numero de edicion invalido, se mantendra el actual.")
    if not campos:
        print("No se realizaron cambios.")
        return
    try:
        crud_revista.actualizar_revista(
            revista_id=revista.id_revista,
            id_usuario_edita=usuario_activo.id_usuario,
            **campos,
        )
        print("\nRevista actualizada exitosamente!")
    except ValueError as e:
        print(f"Error: {e}")


def _eliminar_revista(crud_revista):
    """
    Elimina una revista del sistema por su codigo.

    Args:
        crud_revista: Instancia del CRUD de Revista.
    """
    print("\n--- Eliminar revista ---")
    codigo = input("Ingrese el codigo de la revista a eliminar (ej: R001): ").strip()
    revista = crud_revista.obtener_revista_por_codigo(codigo)
    if not revista:
        print("No se encontro ninguna revista con ese codigo.")
        return
    confirmacion = input(
        f"Esta seguro que desea eliminar '{revista.titulo_material}'? (si/no): "
    ).lower()
    if confirmacion != "si":
        print("Eliminacion cancelada.")
        return
    if crud_revista.eliminar_revista(revista.id_revista):
        print("Revista eliminada exitosamente.")
    else:
        print("Error al eliminar la revista.")


# ====== MENÚ PERIÓDICO ======


def menu_periodico(usuario_activo):
    """
    Despliega el menú de gestión de periódicos.

    Permite crear, consultar, editar y eliminar periódicos.
    Usa el usuario activo en sesión para los campos de auditoría.

    Args:
        usuario_activo: El usuario que tiene la sesión activa en el sistema.
    """
    crud_periodico = PeriodicoCRUD(database=db)
    crud_autor = AutorCRUD(db_session=db)

    while True:
        print("\nMENU PERIODICOS")
        print("1. Crear periodico")
        print("2. Ver todos los periodicos")
        print("3. Buscar periodico por codigo")
        print("4. Editar periodico")
        print("5. Eliminar periodico")
        print("0. Volver al menu principal")
        opcion = input("Seleccione una opcion: ").strip()

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
                print("Volviendo al menu principal...")
                break
            case _:
                print("Opcion invalida. Por favor intente de nuevo.")


def _crear_periodico(crud_periodico, crud_autor, usuario_activo):
    """
    Solicita los datos necesarios y crea un nuevo periodico.

    Args:
        crud_periodico: Instancia del CRUD de Periodico.
        crud_autor: Instancia del CRUD de Autor.
        usuario_activo: Usuario en sesión para auditoría.
    """
    print("\n--- Crear nuevo periodico ---")
    id_autor = _seleccionar_autor(crud_autor)
    if not id_autor:
        return
    print("\nIngrese el codigo del periodico (debe empezar con 'P', ej: P001): ")
    codigo = input().strip()
    print("Ingrese el titulo del periodico: ")
    titulo = input().strip()
    print("Ingrese la ciudad de publicacion: ")
    ciudad = input().strip()
    print("Ingrese la seccion del periodico (ej: deportes, politica): ")
    seccion = input().strip()
    print("Ingrese la fecha de publicacion (YYYY-MM-DD) o presione Enter para omitir: ")
    fecha_str = input().strip()
    fecha = None
    if fecha_str:
        from datetime import date

        try:
            fecha = date.fromisoformat(fecha_str)
        except ValueError:
            print("Formato de fecha invalido, se omitira.")
    print("Ingrese una descripcion (opcional, presione Enter para omitir): ")
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
        print(f"\nPeriodico creado exitosamente!")
        print(f"ID: {periodico.id_periodico}")
        print(f"Codigo: {periodico.codigo_material}")
        print(f"Titulo: {periodico.titulo_material}")
    except ValueError as e:
        print(f"Error: {e}")


def _listar_periodicos(crud_periodico):
    """
    Lista todos los periodicos registrados en el sistema.

    Args:
        crud_periodico: Instancia del CRUD de Periodico.
    """
    print("\n--- Todos los periodicos ---")
    periodicos = crud_periodico.obtener_periodicos()
    if not periodicos:
        print("No hay periodicos registrados.")
        return
    for p in periodicos:
        print(
            f"Codigo: {p.codigo_material} | Titulo: {p.titulo_material} | "
            f"Ciudad: {p.ciudad_publicacion} | Seccion: {p.seccion_periodico} | "
            f"Disponible: {'Si' if p.disponibilidad_material else 'No'}"
        )


def _buscar_periodico_por_codigo(crud_periodico):
    """
    Busca y muestra un periodico por su codigo.

    Args:
        crud_periodico: Instancia del CRUD de Periodico.
    """
    print("\n--- Buscar periodico por codigo ---")
    codigo = input("Ingrese el codigo del periodico (ej: P001): ").strip()
    periodico = crud_periodico.obtener_periodico_codigo(codigo)
    if not periodico:
        print("No se encontro ningun periodico con ese codigo.")
        return
    print(f"\nID: {periodico.id_periodico}")
    print(f"Codigo: {periodico.codigo_material}")
    print(f"Titulo: {periodico.titulo_material}")
    print(f"Ciudad: {periodico.ciudad_publicacion}")
    print(f"Seccion: {periodico.seccion_periodico}")
    print(f"Disponible: {'Si' if periodico.disponibilidad_material else 'No'}")


def _editar_periodico(crud_periodico, usuario_activo):
    """
    Edita los campos de un periodico existente.

    Args:
        crud_periodico: Instancia del CRUD de Periodico.
        usuario_activo: Usuario en sesión para auditoría.
    """
    print("\n--- Editar periodico ---")
    codigo = input("Ingrese el codigo del periodico a editar (ej: P001): ").strip()
    periodico = crud_periodico.obtener_periodico_codigo(codigo)
    if not periodico:
        print("No se encontro ningun periodico con ese codigo.")
        return
    print(f"Editando: {periodico.titulo_material}")
    print("Presione Enter para mantener el valor actual.")
    campos = {}
    print(f"Nuevo titulo [{periodico.titulo_material}]: ")
    nuevo_titulo = input().strip()
    if nuevo_titulo:
        campos["titulo_material"] = nuevo_titulo
    print(f"Nueva ciudad de publicacion [{periodico.ciudad_publicacion}]: ")
    nueva_ciudad = input().strip()
    if nueva_ciudad:
        campos["ciudad_publicacion"] = nueva_ciudad
    print(f"Nueva seccion [{periodico.seccion_periodico}]: ")
    nueva_seccion = input().strip()
    if nueva_seccion:
        campos["seccion_periodico"] = nueva_seccion
    if not campos:
        print("No se realizaron cambios.")
        return
    try:
        crud_periodico.actualizar_periodico(
            id_periodico=periodico.id_periodico,
            id_usuario_edita=usuario_activo.id_usuario,
            **campos,
        )
        print("\nPeriodico actualizado exitosamente!")
    except ValueError as e:
        print(f"Error: {e}")


def _eliminar_periodico(crud_periodico):
    """
    Elimina un periodico del sistema por su codigo.

    Args:
        crud_periodico: Instancia del CRUD de Periodico.
    """
    print("\n--- Eliminar periodico ---")
    codigo = input("Ingrese el codigo del periodico a eliminar (ej: P001): ").strip()
    periodico = crud_periodico.obtener_periodico_codigo(codigo)
    if not periodico:
        print("No se encontro ningun periodico con ese codigo.")
        return
    confirmacion = input(
        f"Esta seguro que desea eliminar '{periodico.titulo_material}'? (si/no): "
    ).lower()
    if confirmacion != "si":
        print("Eliminacion cancelada.")
        return
    if crud_periodico.eliminar_periodico(periodico.id_periodico):
        print("Periodico eliminado exitosamente.")
    else:
        print("Error al eliminar el periodico.")


# ====== MENÚ PRINCIPAL ======


def menu_principal(usuario_activo):
    """
    Despliega el menú principal del sistema de biblioteca.

    Desde aquí se puede acceder a los submenús de cada entidad.

    Args:
        usuario_activo: El usuario que tiene la sesión activa en el sistema.
    """
    while True:
        print(f"\nSISTEMA DE BIBLIOTECA")
        print(
            f"Usuario: {usuario_activo.nombre} {usuario_activo.apellido} | Rol: {usuario_activo.rol}"
        )
        print("1. Gestionar Autores")
        print("2. Gestionar Libros")
        print("3. Gestionar Revistas")
        print("4. Gestionar Periodicos")
        print("0. Cerrar sesion")
        opcion = input("Seleccione una opcion: ").strip()

        match opcion:
            case "1":
                menu_autor(usuario_activo)
            case "2":
                menu_libro(usuario_activo)
            case "3":
                menu_revista(usuario_activo)
            case "4":
                menu_periodico(usuario_activo)
            case "0":
                print("Cerrando sesion...")
                break
            case _:
                print("Opcion invalida. Por favor intente de nuevo.")


# ====== ENTRADA DEL PROGRAMA ======

usuario_activo = None
while True:
    print("Bienvenido al sistema de la biblioteca. Se encuentra registrado?")
    opcion = input("Si/No: ").lower()

    match opcion:
        case "si":
            print("Iniciando sesion...")
            usuario_activo = iniciar_sesion()
            break
        case "no":
            print("Registrando...")
            usuario_activo = registrar_usuario_nuevo()
            if not usuario_activo:
                print("Fallo el registro. Por favor intente nuevamente")
                continue
            break
        case _:
            print("Opcion invalida. Por favor intente de nuevo")

if usuario_activo:
    try:
        menu_principal(usuario_activo)
    finally:
        db.close()
