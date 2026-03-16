"""
Modelo ORM para la entidad Reserva.

Representa una reserva de material bibliográfico realizada por un usuario
en el sistema de biblioteca. Incluye columnas de auditoría con
referencia a la entidad Usuario.
"""

import uuid
import enum

from database.config import Base
from sqlalchemy import Column, Date, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class EstadoReserva(enum.Enum):
    pendiente: str = "pendiente"
    completada: str = "completada"
    cancelada: str = "cancelada"


class Reserva(Base):
    """Modelo de Reserva"""

    __tablename__ = "reservas"

    id_reserva = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    fecha_reserva = Column(Date, nullable=False)
    estado_reserva = Column(Enum(EstadoReserva), nullable=False)

    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    id_usuario = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=False
    )
    id_material = Column(
        UUID(as_uuid=True),
        ForeignKey("materiales_biblioteca.id_material"),
        nullable=False,
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
    material = relationship(
        "MaterialBiblioteca",
        foreign_keys=[id_material],
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
            f"<Reserva(id_reserva={self.id_reserva}, "
            f"estado='{self.estado_reserva}', fecha='{self.fecha_reserva}')>"
        )
