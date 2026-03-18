import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from random import randint
from typing import List, Optional
from sqlalchemy import and_, or_
from sqlalchemy.exc import IntegrityError

from src.utils.security import security
from src.database import config
from src.entities.Usuario import Usuario

db = config.get_db()


def crear_usuario(
    nombre_nuevo: str,
    apellido_nuevo: str,
    documento_nuevo: str,
    email_nuevo: str,
    telefono_nuevo: str,
    contrasena_nueva: str,
    rol_nuevo: str = "Usuario",
) -> Optional[Usuario]:
    print("--- Creando usuario ---")

    nuevo_username = crear_username(nombre_nuevo, apellido_nuevo)
    contrasena_hasheada = security.hashear_contrasena(contrasena_nueva)

    nuevo_usuario = Usuario(
        nombre=nombre_nuevo,
        apellido=apellido_nuevo,
        documento=documento_nuevo,
        email=email_nuevo,
        telefono=telefono_nuevo,
        username=nuevo_username,
        contrasena=contrasena_hasheada,
        rol=rol_nuevo,
    )

    try:
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
        print(f"Usuario creado exitosamente OwO: {nuevo_usuario.username}")
        return nuevo_usuario
    except IntegrityError as e:
        db.rollback()
        print(f"Error de integridad (¿Documento o email repetido?): {e}")
        return None


def crear_username(nombre: str, apellido: str) -> str:
    """Genera un username único combinando nombre, apellido y un número aleatorio."""
    num = randint(100000, 999999)
    nom = nombre.split()[0].lower()
    ape = apellido.split()[0].lower()
    return f"{nom}{ape}{num}"


def obtener_todos_los_usuarios() -> List[Usuario]:
    return db.query(Usuario).all()


def consultar_usuario_por_id(id_ingresado: str) -> Optional[Usuario]:
    return db.query(Usuario).filter(Usuario.id_usuario == id_ingresado).first()


def consultar_usuario_por_username(username_ingresado: str) -> Optional[Usuario]:
    usuario = db.query(Usuario).filter(Usuario.username == username_ingresado).first()
    if usuario:
        print(f"Usuario encontrado B): {usuario.nombre} {usuario.apellido}")
    return usuario


def consultar_usuario_por_email(email_ingresado: str) -> Optional[Usuario]:
    usuario = db.query(Usuario).filter(Usuario.email == email_ingresado).first()
    return usuario


def consultar_usuario_por_documento(documento_ingresado: str) -> Optional[Usuario]:
    usuario = db.query(Usuario).filter(Usuario.documento == documento_ingresado).first()
    return usuario


def consultar_usuario_por_telefono(telefono_ingresado: str) -> Optional[Usuario]:
    usuario = db.query(Usuario).filter(Usuario.telefono == telefono_ingresado).first()
    return usuario


def buscar_usuario_universal(termino_busqueda: str) -> List[Usuario]:
    """
    Busca coincidencias en nombre, apellido, username, email o documento,
    gracias a los operadores or y ilike.
    """
    patron = f"%{termino_busqueda}%"
    lista_de_coincidencias = (
        db.query(Usuario)
        .filter(
            or_(
                Usuario.nombre.ilike(patron),
                Usuario.apellido.ilike(patron),
                Usuario.username.ilike(patron),
                Usuario.email.ilike(patron),
                Usuario.documento.ilike(patron),
            )
        )
        .all()
    )
    return lista_de_coincidencias


def actualizar_usuario(id_usuario: str, **kwargs) -> Optional[Usuario]:
    """
    Actualiza cualquier campo del usuario dinámicamente.
    Ejemplo de uso: actualizar_usuario(id, telefono="300123", rol="Admin")
    """
    usuario_encontrado = consultar_usuario_por_id(id_usuario)

    if not usuario_encontrado:
        print("Error: No se encontró el usuario para actualizar x_x")
        return None

    # Iteramos sobre los argumentos que mandaste (kwargs)
    for key, value in kwargs.items():
        if hasattr(usuario_encontrado, key):
            # Si están actualizando la contraseña, la hasheamos primero
            if key == "contrasena":
                value = security.hashear_contrasena(value)
            setattr(usuario_encontrado, key, value)

    try:
        db.commit()
        db.refresh(usuario_encontrado)
        print(f"Usuario {usuario_encontrado.username} actualizado con éxito uwu")
        return usuario_encontrado
    except Exception as e:
        db.rollback()
        print(f"Error al actualizar: {e}")
        return None


def eliminar_usuario(id_usuario: str) -> bool:
    """
    Eliminación física del usuario de la base de datos.
    Como arreglamos la auditoría con Soft References, esto no explotará B).
    """
    usuario_encontrado = consultar_usuario_por_id(id_usuario)

    if not usuario_encontrado:
        print("Error: El usuario no existe o ya fue eliminado.")
        return False

    try:
        db.delete(usuario_encontrado)
        db.commit()
        print(f"Usuario eliminado del sistema para siempre 💀")
        return True
    except Exception as e:
        db.rollback()
        print(f"Error al eliminar usuario: {e}")
        return False
