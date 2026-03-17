"""
Modelo ORM para la entidad Sancion.

Representa una sanción aplicada a un usuario del sistema de biblioteca
como consecuencia de un préstamo no devuelto o devuelto tardíamente.
Incluye columnas de auditoría con referencia a la entidad Usuario.
"""

import uuid

from database.config import Base
from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Sancion(Base):
    """Modelo de Sancion"""

    __tablename__ = "sanciones"

    id_sancion = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    fecha_inicio = Column(Date, nullable=False)
    dias_sancion = Column(Integer, nullable=False)
    motivo = Column(String(200), nullable=False)

    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    id_usuario = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=False
    )
    id_prestamo = Column(
        UUID(as_uuid=True), ForeignKey("prestamos.id_prestamo"), nullable=False
    )
    id_usuario_creacion = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=False
    )
    id_usuario_edita = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=True
    )

    usuario = relationship(
        "Usuario",
        foreign_keys=[id_usuario],
    )
    prestamo = relationship(
        "Prestamo",
        foreign_keys=[id_prestamo],
    )
    usuario_creacion = relationship(
        "Usuario",
        foreign_keys=[id_usuario_creacion],
    )
    usuario_edita = relationship(
        "Usuario",
        foreign_keys=[id_usuario_edita],
    )

    def __repr__(self) -> str:
        return (
            f"<Sancion(id_sancion={self.id_sancion}, "
            f"dias_sancion={self.dias_sancion}, motivo='{self.motivo}')>"
        )
