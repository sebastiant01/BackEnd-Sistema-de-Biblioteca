"""
Modelo ORM para la entidad Reserva.

Representa una reserva de material bibliográfico realizada por un usuario
en el sistema de biblioteca. Incluye columnas de auditoría con
referencia a la entidad Usuario.
"""

import uuid
import enum

from src.database.config import Base
from src.entities.Auditoria import Auditoria
from sqlalchemy import Column, Date, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class EstadoReserva(enum.Enum):
    pendiente: str = "pendiente"
    completada: str = "completada"
    cancelada: str = "cancelada"


class Reserva(Base, Auditoria):
    """Modelo de Reserva"""

    __tablename__ = "reservas"

    id_reserva: UUID = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    fecha_reserva: Date = Column(Date, nullable=False)
    estado_reserva: Enum = Column(
        Enum(EstadoReserva), nullable=False, default=EstadoReserva.pendiente
    )

    id_usuario: UUID = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=False
    )
    id_material: UUID = Column(
        UUID(as_uuid=True),
        ForeignKey("materiales_biblioteca.id_material"),
        nullable=False,
    )

    usuario = relationship(
        "Usuario",
        back_populates="reserva",
        foreign_keys="[Reserva.id_usuario]",
    )

    material = relationship(
        "MaterialBiblioteca",
        back_populates="reserva",
        foreign_keys="[Reserva.id_material]",
    )

    def __repr__(self) -> str:
        return (
            f"<Reserva(id_reserva={self.id_reserva}, "
            f"estado='{self.estado_reserva}', fecha='{self.fecha_reserva}')>"
        )
