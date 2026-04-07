import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from typing import List, Optional
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.database import config
from src.entities.Prestamo import Prestamo
from src.entities.MaterialBiblioteca import MaterialBiblioteca


class PrestamoCRUD:
    """
    Clase encargada de gestionar las operaciones CRUD (Crear, Leer, Actualizar, Eliminar)
    para la entidad Prestamo en la base de datos.
    """

    def __init__(self, db_session: Optional[Session] = None):
        """
        Inicializa la clase con una sesión de base de datos.

        Args:
            db_session (Optional[Session]): Sesión de SQLAlchemy. Si no se provee,
                                            se obtiene una por defecto desde la configuración.
        """
        self.db = db_session or config.get_db()

    def crear_prestamo(
        self, id_usuario_cliente: str, id_material_prestado: str, id_usuario_sesion: str
    ) -> Optional[Prestamo]:
        """
        Crea un nuevo registro de préstamo en el sistema.

        Consideraciones de auditoría:
        - Si un usuario realiza el préstamo desde su propia cuenta: `id_usuario_cliente`
          e `id_usuario_sesion` serán iguales.
        - Si un Administrador o Bibliotecario registra el préstamo presencialmente para
          un lector: `id_usuario_cliente` es el lector, pero `id_usuario_sesion` es el
          UUID del Admin.

        Args:
            id_usuario_cliente (str): UUID del usuario que recibe el material.
            id_material_prestado (str): UUID del material (libro, revista, etc.) prestado.
            id_usuario_sesion (str): UUID del usuario que está ejecutando la acción.

        Returns:
            Optional[Prestamo]: El objeto Prestamo creado si es exitoso, o None si
                                ocurre un error de integridad o de base de datos.
        """
        print(f"--- Generando préstamo para el material {id_material_prestado} ---")
        material = (
            self.db.query(MaterialBiblioteca)
            .filter(MaterialBiblioteca.id_material == id_material_prestado)
            .first()
        )
        if not material:
            raise ValueError("Error: Material no encontrado o no existe.")

        nuevo_prestamo = Prestamo(
            id_usuario=id_usuario_cliente,
            id_material=id_material_prestado,
            estado="Activa",
            id_usuario_crea=id_usuario_sesion,
        )

        try:
            material.disponibilidad_material = False

            self.db.add(nuevo_prestamo)
            self.db.commit()
            self.db.refresh(nuevo_prestamo)
            print(f"Préstamo creado exitosamente ID: {nuevo_prestamo.id_prestamo}")
            return nuevo_prestamo
        except IntegrityError as e:
            self.db.rollback()
            print(f"Error de integridad (¿UUIDs inválidos o no existen?): {e}")
            return None
        except Exception as e:
            self.db.rollback()
            print(f"Error inesperado al crear el préstamo: {e}")
            return None

    def obtener_todos_los_prestamos(
        self, skip: int = 0, limit: int = 100
    ) -> List[Prestamo]:
        """
        Recupera el historial completo de todos los préstamos registrados en el sistema.

        Args:
            skip (int): Indica la posición desde donde se muestran los resultados de la base de datos. Por defecto en la posición 0
            limit (int): Indica el máximo de resultados que se van a mostrar. Por defecto 100

        Returns:
            List[Prestamo]: Lista de objetos Prestamo.
        """
        return self.db.query(Prestamo).offset(skip).limit(limit).all()

    def consultar_prestamo_por_id(
        self, id_prestamo_ingresado: str
    ) -> Optional[Prestamo]:
        """
        Busca un préstamo específico mediante su ID único.

        Args:
            id_prestamo_ingresado (str): El ID del préstamo a buscar.

        Returns:
            Optional[Prestamo]: El préstamo encontrado, o None si no existe.
        """
        return (
            self.db.query(Prestamo)
            .filter(Prestamo.id_prestamo == id_prestamo_ingresado)
            .first()
        )

    def consultar_prestamos_por_usuario(
        self, id_usuario_ingresado: str, skip: int = 0, limit: int = 100
    ) -> List[Prestamo]:
        """
        Recupera el historial completo de préstamos (activos e inactivos) de un
        usuario específico.

        Args:
            id_usuario_ingresado (str): ID del usuario a consultar.
            skip (int): Indica la posición desde donde se muestran los resultados de la base de datos. Por defecto en la posición 0
            limit (int): Indica el máximo de resultados que se van a mostrar. Por defecto 100

        Returns:
            List[Prestamo]: Lista de préstamos asociados al usuario.
        """
        prestamos = (
            self.db.query(Prestamo)
            .filter(Prestamo.id_usuario == id_usuario_ingresado)
            .offset(skip)
            .limit(limit)
            .all()
        )
        print(f"Se encontraron {len(prestamos)} préstamos para el usuario.")
        return prestamos

    def consultar_prestamos_activos_por_usuario(
        self, id_usuario_ingresado: str, skip: int = 0, limit: int = 100
    ) -> List[Prestamo]:
        """
        Filtra y recupera ÚNICAMENTE los préstamos que el usuario aún no ha devuelto
        (cuyo estado es 'Activa').

        Args:
            id_usuario_ingresado (str): ID del usuario a consultar.
            skip (int): Indica la posición desde donde se muestran los resultados de la base de datos. Por defecto en la posición 0
            limit (int): Indica el máximo de resultados que se van a mostrar. Por defecto 100

        Returns:
            List[Prestamo]: Lista de préstamos activos del usuario.
        """
        return (
            self.db.query(Prestamo)
            .filter(
                Prestamo.id_usuario == id_usuario_ingresado, Prestamo.estado == "Activa"
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def consultar_prestamos_por_material(
        self, id_material_ingresado: str, skip: int = 0, limit: int = 100
    ) -> List[Prestamo]:
        """
        Busca todos los préstamos asociados a un material específico.
        Útil para métricas (ej. saber cuántas veces se ha prestado un libro históricamente).

        Args:
            id_material_ingresado (str): ID del material a consultar.
            skip (int): Indica la posición desde donde se muestran los resultados de la base de datos. Por defecto en la posición 0
            limit (int): Indica el máximo de resultados que se van a mostrar. Por defecto 100

        Returns:
            List[Prestamo]: Lista de préstamos en los que ha participado el material.
        """
        return (
            self.db.query(Prestamo)
            .filter(Prestamo.id_material == id_material_ingresado)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def actualizar_estado_prestamo(
        self, id_prestamo: str, nuevo_estado: str, id_usuario_sesion: str
    ) -> Optional[Prestamo]:
        """
        Actualiza el estado de un préstamo específico (ej. de 'Activa' a 'Devuelto' o 'Atrasado')
        y registra qué usuario realizó la modificación para fines de auditoría.

        Args:
            id_prestamo (str): ID del préstamo a actualizar.
            nuevo_estado (str): El nuevo estado a asignar.
            id_usuario_sesion (str): ID del usuario (Admin/Sistema) que realiza el cambio.

        Returns:
            Optional[Prestamo]: El préstamo actualizado, o None si no se encontró o falló.
        """
        prestamo_encontrado = self.consultar_prestamo_por_id(id_prestamo)

        if not prestamo_encontrado:
            print("Error: No se encontró el préstamo para actualizar x_x")
            return None

        prestamo_encontrado.estado = nuevo_estado
        prestamo_encontrado.id_usuario_edita = id_usuario_sesion

        try:
            self.db.commit()
            self.db.refresh(prestamo_encontrado)
            print(f"Préstamo {id_prestamo} actualizado a estado '{nuevo_estado}'")
            return prestamo_encontrado
        except Exception as e:
            self.db.rollback()
            print(f"Error al actualizar el préstamo: {e}")
            return None

    def eliminar_prestamo(self, id_prestamo: str) -> bool:
        """
        Realiza una eliminación física del registro del préstamo en la base de datos.
        Advertencia: Esto borra el registro permanentemente.

        Args:
            id_prestamo (str): ID del préstamo a eliminar.

        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario.
        """
        prestamo_encontrado = self.consultar_prestamo_por_id(id_prestamo)

        if not prestamo_encontrado:
            print("Error: El préstamo no existe o ya fue eliminado.")
            return False

        try:
            self.db.delete(prestamo_encontrado)
            self.db.commit()
            print("Préstamo eliminado del sistema para siempre")
            return True
        except Exception as e:
            self.db.rollback()
            print(f"Error al eliminar préstamo: {e}")
            return False
