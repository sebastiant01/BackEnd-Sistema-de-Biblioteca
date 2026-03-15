import uuid
import os
import sys
from sqlalchemy import Column, ForeignKey, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database.config import Base
from src.entities import Auditoria

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class Reserva(Base, Auditoria):

    __tablename__ = "Reserva"

    id_reserva = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    id_usuario = Column(UUID(as_uuid=True), ForeignKey("Usuario.id_usuario"))
    usuario_reserva = relationship("Usuario", back_populates="reservas")

    id_material = Column(
        UUID(as_uuid=True), ForeignKey("MaterialBiblioteca.id_material")
    )
    material_reservado = relationship("MaterialBiblioteca", back_populates="reservas")

    fecha_reserva = Column(DateTime(timezone=True), server_default=func.now())
    estado = Column(String, nullable=False, default="Activa")
