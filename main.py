import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.utils.security import security
from src.entities.Usuario import Usuario
from src.crud import usuario_crud


def iniciar_sesion() -> Usuario:
    username = ""
    while True:
        if len(username) == 0:
            print("Ingrese su nombre de usuario (username): ")
            username = input().strip()
            if not usuario_crud.consultar_usuario_por_username(username):
                print("El usuario ingresado no existe, por favor intente nuevamente")
                continue
        print("Ingrese su contraseña: ")
        contrasena_plana = input().strip()

        if not security.verificar_contrasena_ingresada(contrasena_plana):
            print("La contraseña ingresada es incorrecta")
            continue
        print("Credenciales validadas, iniciando sesión...")
        return usuario_crud.consultar_usuario_por_username()


def registrar_usuario_nuevo() -> Usuario | None:
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

    usuario_existente_email = usuario_crud.consultar_usuario_por_email(nuevo_email)
    if usuario_existente_email:
        print("Error: ¡Ese correo ya está registrado en el sistema! x_x")
        return None

    usuario_existente_doc = usuario_crud.consultar_usuario_por_documento(
        nuevo_documento
    )
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

    nuevo_user = usuario_crud.crear_usuario(
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


usuario_activo: Usuario = None
while True:
    print("Bienvenido al sistema de la biblioteca. Se encuentra registrado?")
    opcion = input("Si/No").lower()

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
