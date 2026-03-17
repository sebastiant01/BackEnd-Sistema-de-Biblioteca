import uuid
import os
import sys
from sqlalchemy import Column, ForeignKey, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database.config import Base
from src.entities.Auditoria import Auditoria
from src.entities.Usuario import Usuario
from src.entities.MaterialBiblioteca import MaterialBiblioteca

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class Prestamo(Base, Auditoria):

    __tablename__ = "prestamos"

    id_prestamo = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    id_usuario = Column(UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"))
    usuario_prestamo = relationship("Usuario", back_populates="prestamo")

    id_material = Column(
        UUID(as_uuid=True), ForeignKey("materiales_biblioteca.id_material")
    )
    material_prestado = relationship("MaterialBiblioteca", back_populates="prestamo")

    fecha_prestamo = Column(DateTime(timezone=True), server_default=func.now())
    estado = Column(String, nullable=False, default="Activa")

    def __repr__(self) -> str:
        return (
            f"<Prestamo(id_prestamo={self.id_prestamo}, "
            f"id_prestamo='{self.id_prestamo}', id_usuario='{self.id_usuario}', "
            f"id_material='{self.id_material}', material_prestado='{self.material_prestado}', "
            f"fecha_prestamo='{self.fecha_prestamo}', estado='{self.estado}', "
            f"rol='{self.rol}')>"
        )
