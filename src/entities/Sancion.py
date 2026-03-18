"""
Modelo ORM para la entidad Sancion.

Representa una sanción aplicada a un usuario del sistema de biblioteca
como consecuencia de un préstamo no devuelto o devuelto tardíamente.
Incluye columnas de auditoría con referencia a la entidad Usuario.
"""

import uuid

from src.database.config import Base
from src.entities.Auditoria import Auditoria
from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Sancion(Base, Auditoria):
    """Modelo de Sancion"""

    __tablename__ = "sanciones"

    id_sancion: UUID = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    fecha_inicio: Date = Column(Date, nullable=False)
    dias_sancion: int = Column(Integer, nullable=False)
    motivo: str = Column(String(200), nullable=False)

    id_usuario: UUID = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=False
    )

    id_prestamo: UUID = Column(
        UUID(as_uuid=True), ForeignKey("prestamos.id_prestamo"), nullable=False
    )

    usuario_sancionado = relationship(
        "Usuario",
        back_populates="sanciones",
        foreign_keys="[Sancion.id_usuario]",
    )
    prestamo = relationship(
        "Prestamo",
        back_populates="sancion_involucrada",
        foreign_keys="[Sancion.id_prestamo]",
    )

    def __repr__(self) -> str:
        return (
            f"<Sancion(id_sancion={self.id_sancion}, "
            f"dias_sancion={self.dias_sancion}, motivo='{self.motivo}')>"
        )
