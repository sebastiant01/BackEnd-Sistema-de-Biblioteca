import uuid
import os
import sys
from sqlalchemy import Column, String, CheckConstraint, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database.config import Base
from src.entities.MaterialBiblioteca import MaterialBiblioteca
from src.entities.Auditoria import Auditoria

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class Autor(Base, Auditoria):

    __tablename__ = "autores"

    id_autor = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    nombre_autor = Column(String(50), nullable=False)
    apellido_autor = Column(String(50), nullable=True)
    nacionalidad = Column(String(50), nullable=True)

    materiales_biblioteca = relationship(
        "MaterialBiblioteca", back_populates="autor", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return (
            f"<Autor(id_autor={self.id_autor}, "
            f"nombre_autor='{self.nombre_autor}', apellido_autor='{self.apellido_autor}', "
            f"nacionalidad='{self.nacionalidad}')>"
        )
