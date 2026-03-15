import uuid
import os
import sys
from sqlalchemy import Column, String, CheckConstraint, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database.config import Base
from src.entities.Auditoria import Auditoria
from src.entities.Usuario import Usuario

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class Sancion(Base, Auditoria):

  __tablename__ = "Sancion"

  id_sancion = Column(
    UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
  )
  
  id_usuario = Column(
    UUID(as_uuid=True), ForeignKey("Usuario.id_usuario")
  )
  usuario_sancionado = relationship("Usuario", back_populates="sanciones")

  id_material = Column(
    UUID(as_uuid=True), ForeignKey("MaterialBiblioteca.id_material_biblioteca")
  )
  material_involucrado = relationship("MaterialBiblioteca", back_populates="sanciones")

  fecha_inicio = Column(DateTime(timezone=True), server_default=func.now())
  dias_sancion = Column(Integer, nullable=False)
  motivo = Column(String(200), nullable=True)
  
