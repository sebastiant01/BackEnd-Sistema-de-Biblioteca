import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from typing import List, Optional
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

from src.database import config
from src.entities.Autor import Autor

db = config.get_db()


def crear_autor(
    nombre_autor: str,
    id_usuario_sesion: str,
    apellido_autor: Optional[str] = None,
    nacionalidad: Optional[str] = None,
) -> Optional[Autor]:
    print(f"--- Registrando al autor: {nombre_autor} {apellido_autor or ''} ---")

    nuevo_autor = Autor(
        nombre_autor=nombre_autor,
        apellido_autor=apellido_autor,
        nacionalidad=nacionalidad,
        id_usuario_crea=id_usuario_sesion,
        activo=True,
    )

    try:
        db.add(nuevo_autor)
        db.commit()
        db.refresh(nuevo_autor)
        print(f"Autor creado exitosamente. ID: {nuevo_autor.id_autor}")
        return nuevo_autor
    except IntegrityError as e:
        db.rollback()
        print(f"Error de integridad al crear autor: {e}")
        return None
    except Exception as e:
        db.rollback()
        print(f"Error inesperado: {e}")
        return None


def obtener_todos_los_autores() -> List[Autor]:
    return db.query(Autor).filter(Autor.activo == True).all()


def consultar_autor_por_id(id_autor_ingresado: str) -> Optional[Autor]:
    return (
        db.query(Autor)
        .filter(Autor.id_autor == id_autor_ingresado, Autor.activo == True)
        .first()
    )


def buscar_autor_por_nombre(termino_busqueda: str) -> List[Autor]:
    patron = f"%{termino_busqueda}%"
    return (
        db.query(Autor)
        .filter(
            Autor.activo == True,
            or_(Autor.nombre_autor.ilike(patron), Autor.apellido_autor.ilike(patron)),
        )
        .all()
    )


def actualizar_autor(
    id_autor: str, id_usuario_sesion: str, **kwargs
) -> Optional[Autor]:
    autor_encontrado = consultar_autor_por_id(id_autor)

    if not autor_encontrado:
        print("Error: No se encontró el autor (o fue eliminado previamente) x_x")
        return None

    for key, value in kwargs.items():
        if hasattr(autor_encontrado, key) and key != "id_autor":
            setattr(autor_encontrado, key, value)

    autor_encontrado.id_usuario_edita = id_usuario_sesion

    try:
        db.commit()
        db.refresh(autor_encontrado)
        print(f"Autor '{autor_encontrado.nombre_autor}' actualizado con éxito")
        return autor_encontrado
    except Exception as e:
        db.rollback()
        print(f"Error al actualizar el autor: {e}")
        return None


def eliminar_autor(id_autor: str, id_usuario_sesion: str) -> bool:
    """
    Baja lógica o Soft delete: No borramos físicamente de la base de datos,
    solo pasamos 'activo' a False y registramos quién lo hizo.
    """
    autor_encontrado = consultar_autor_por_id(id_autor)

    if not autor_encontrado:
        print("Error: El autor no existe o ya estaba dado de baja.")
        return False

    autor_encontrado.activo = False

    autor_encontrado.id_usuario_edita = id_usuario_sesion

    try:
        db.commit()
        print(
            f"Autor {autor_encontrado.nombre_autor} dado de baja lógicamente (Soft Delete) 👻"
        )
        return True
    except Exception as e:
        db.rollback()
        print(f"Error al dar de baja al autor: {e}")
        return False
