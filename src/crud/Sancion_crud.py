"""
Operaciones CRUD para Sancion
"""

from typing import List, Optional
from uuid import UUID

from src.entities.Sancion import Sancion
from sqlalchemy.orm import Session


class SancionCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_sancion(
        self,
        id_usuario: UUID,
        id_prestamo: UUID,
        fecha_inicio: str,
        dias_sancion: int,
        motivo: str,
        id_usuario_crea: UUID,
    ) -> Sancion:
        """
        Crear una nueva sanción con validaciones

        Args:
            id_usuario: UUID del usuario sancionado
            id_prestamo: UUID del préstamo que originó la sanción
            fecha_inicio: Fecha de inicio de la sanción
            dias_sancion: Número de días que dura la sanción (debe ser mayor a 0)
            motivo: Descripción del motivo de la sanción (máximo 200 caracteres)
            id_usuario_crea: UUID del usuario que registra la sanción (auditoría)

        Returns:
            Sancion creada

        Raises:
            ValueError: Si los datos no son válidos
        """
        if not motivo or len(motivo.strip()) == 0:
            raise ValueError("El motivo de la sanción es obligatorio")

        if len(motivo) > 200:
            raise ValueError("El motivo no puede exceder 200 caracteres")

        if dias_sancion <= 0:
            raise ValueError("Los días de sanción deben ser mayor a 0")

        from src.entities.Usuario import Usuario

        usuario = (
            self.db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
        )
        if not usuario:
            raise ValueError("El usuario especificado no existe")

        from src.entities.Prestamo import Prestamo

        prestamo = (
            self.db.query(Prestamo).filter(Prestamo.id_prestamo == id_prestamo).first()
        )
        if not prestamo:
            raise ValueError("El préstamo especificado no existe")

        sancion = Sancion(
            id_usuario=id_usuario,
            id_prestamo=id_prestamo,
            fecha_inicio=fecha_inicio,
            dias_sancion=dias_sancion,
            motivo=motivo.strip(),
            id_usuario_crea=id_usuario_crea,
            id_usuario_edita=None,
        )
        self.db.add(sancion)
        self.db.commit()
        self.db.refresh(sancion)
        return sancion

    def obtener_sancion(self, sancion_id: UUID) -> Optional[Sancion]:
        """
        Obtener una sanción por ID

        Args:
            sancion_id: UUID de la sanción

        Returns:
            Sancion encontrada o None
        """
        return self.db.query(Sancion).filter(Sancion.id_sancion == sancion_id).first()

    def obtener_sanciones(self, skip: int = 0, limit: int = 100) -> List[Sancion]:
        """
        Obtener lista de sanciones con paginación

        Args:
            skip: Número de registros a omitir
            limit: Límite de registros a retornar

        Returns:
            Lista de sanciones
        """
        return self.db.query(Sancion).offset(skip).limit(limit).all()

    def obtener_sanciones_por_usuario(self, id_usuario: UUID) -> List[Sancion]:
        """
        Obtener todas las sanciones de un usuario específico

        Args:
            id_usuario: UUID del usuario

        Returns:
            Lista de sanciones del usuario
        """
        return self.db.query(Sancion).filter(Sancion.id_usuario == id_usuario).all()

    def obtener_sanciones_por_prestamo(self, id_prestamo: UUID) -> List[Sancion]:
        """
        Obtener todas las sanciones asociadas a un préstamo específico

        Args:
            id_prestamo: UUID del préstamo

        Returns:
            Lista de sanciones del préstamo
        """
        return self.db.query(Sancion).filter(Sancion.id_prestamo == id_prestamo).all()

    def actualizar_sancion(
        self, sancion_id: UUID, id_usuario_edita: UUID = None, **kwargs
    ) -> Optional[Sancion]:
        """
        Actualizar una sanción con validaciones

        Args:
            sancion_id: UUID de la sanción
            id_usuario_edita: UUID del usuario que edita
            **kwargs: Campos a actualizar

        Returns:
            Sancion actualizada o None

        Raises:
            ValueError: Si los datos no son válidos
        """
        sancion = self.obtener_sancion(sancion_id)
        if not sancion:
            return None

        if "motivo" in kwargs:
            motivo = kwargs["motivo"]
            if not motivo or len(motivo.strip()) == 0:
                raise ValueError("El motivo de la sanción es obligatorio")
            if len(motivo) > 200:
                raise ValueError("El motivo no puede exceder 200 caracteres")
            kwargs["motivo"] = motivo.strip()

        if "dias_sancion" in kwargs:
            if kwargs["dias_sancion"] <= 0:
                raise ValueError("Los días de sanción deben ser mayor a 0")

        if id_usuario_edita is None:
            from src.entities.Usuario import Usuario

            admin = self.db.query(Usuario).filter(Usuario.rol == "Admin").first()
            if not admin:
                raise ValueError(
                    "No se encontró un usuario administrador para editar la sanción"
                )
            id_usuario_edita = admin.id_usuario

        sancion.id_usuario_edita = id_usuario_edita

        for key, value in kwargs.items():
            if hasattr(sancion, key):
                setattr(sancion, key, value)

        self.db.commit()
        self.db.refresh(sancion)
        return sancion

    def eliminar_sancion(self, sancion_id: UUID) -> bool:
        """
        Eliminar una sanción

        Args:
            sancion_id: UUID de la sanción

        Returns:
            True si se eliminó, False si no existe
        """
        sancion = self.obtener_sancion(sancion_id)
        if sancion:
            self.db.delete(sancion)
            self.db.commit()
            return True
        return False
