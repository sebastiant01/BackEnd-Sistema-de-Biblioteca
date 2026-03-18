import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from typing import List, Optional
from sqlalchemy.exc import IntegrityError

from src.database import config
from src.entities.Prestamo import Prestamo

db = config.get_db()


def crear_prestamo(
    id_usuario_cliente: str, id_material_prestado: str, id_usuario_sesion: str
) -> Optional[Prestamo]:
    """
    Crea un nuevo préstamo en el sistema.

    - Si el usuario lo hace desde su cuenta: id_usuario_cliente y id_usuario_sesion son IGUALES.
    - Si un Admin le presta el libro a un cliente presencial: id_usuario_cliente es el lector,
      pero id_usuario_sesion es el UUID del Admin.
    """
    print(f"--- Generando préstamo para el material {id_material_prestado} ---")

    nuevo_prestamo = Prestamo(
        id_usuario=id_usuario_cliente,
        id_material=id_material_prestado,
        estado="Activa",
        id_usuario_crea=id_usuario_sesion,
    )

    try:
        db.add(nuevo_prestamo)
        db.commit()
        db.refresh(nuevo_prestamo)
        print(f"Préstamo creado exitosamente ID: {nuevo_prestamo.id_prestamo}")
        return nuevo_prestamo
    except IntegrityError as e:
        db.rollback()
        print(f"Error de integridad (UUIDs inválidos o no existen?): {e}")
        return None
    except Exception as e:
        db.rollback()
        print(f"Error inesperado al crear el préstamo: {e}")
        return None


def obtener_todos_los_prestamos() -> List[Prestamo]:
    return db.query(Prestamo).all()


def consultar_prestamo_por_id(id_prestamo_ingresado: str) -> Optional[Prestamo]:
    return (
        db.query(Prestamo).filter(Prestamo.id_prestamo == id_prestamo_ingresado).first()
    )


def consultar_prestamos_por_usuario(id_usuario_ingresado: str) -> List[Prestamo]:
    """Trae el historial completo de préstamos de un usuario específico."""
    prestamos = (
        db.query(Prestamo).filter(Prestamo.id_usuario == id_usuario_ingresado).all()
    )
    print(f"Se encontraron {len(prestamos)} préstamos para el usuario.")
    return prestamos


def consultar_prestamos_activos_por_usuario(
    id_usuario_ingresado: str,
) -> List[Prestamo]:
    """Trae SOLO los préstamos que el usuario aún no ha devuelto."""
    return (
        db.query(Prestamo)
        .filter(
            Prestamo.id_usuario == id_usuario_ingresado, Prestamo.estado == "Activa"
        )
        .all()
    )


def consultar_prestamos_por_material(id_material_ingresado: str) -> List[Prestamo]:
    """Método para saber cuántas veces se ha prestado un libro en la historia."""
    return (
        db.query(Prestamo).filter(Prestamo.id_material == id_material_ingresado).all()
    )


def actualizar_estado_prestamo(
    id_prestamo: str, nuevo_estado: str, id_usuario_sesion: str
) -> Optional[Prestamo]:
    """
    Actualiza el estado de un préstamo (ej. de 'Activa' a 'Devuelto' o 'Atrasado').
    """
    prestamo_encontrado = consultar_prestamo_por_id(id_prestamo)

    if not prestamo_encontrado:
        print("Error: No se encontró el préstamo para actualizar x_x")
        return None

    prestamo_encontrado.estado = nuevo_estado

    prestamo_encontrado.id_usuario_edita = id_usuario_sesion

    try:
        db.commit()
        db.refresh(prestamo_encontrado)
        print(f"Préstamo {id_prestamo} actualizado a estado '{nuevo_estado}'")
        return prestamo_encontrado
    except Exception as e:
        db.rollback()
        print(f"Error al actualizar el préstamo: {e}")
        return None


def eliminar_prestamo(id_prestamo: str) -> bool:
    """
    Elimina físicamente el registro del préstamo.
    """
    prestamo_encontrado = consultar_prestamo_por_id(id_prestamo)

    if not prestamo_encontrado:
        print("Error: El préstamo no existe o ya fue eliminado.")
        return False

    try:
        db.delete(prestamo_encontrado)
        db.commit()
        print("Préstamo eliminado del sistema para siempre")
        return True
    except Exception as e:
        db.rollback()
        print(f"Error al eliminar préstamo: {e}")
        return False
