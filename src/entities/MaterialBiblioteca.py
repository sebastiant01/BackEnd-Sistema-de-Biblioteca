import uuid
import enum

from database.config import Base
from sqlalchemy import Column, Date, DateTime, Boolean, String, Text, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class TipoMaterial(enum.Enum):
    libro: str = "libro"
    revista: str = "revista"
    periodico: str = "periodico"


class MaterialBiblioteca(Base):
    """Modelo de MaterialBiblioteca, representa los materiales bibliograficos disponibles."""

    __tablename__ = "materiales_biblioteca"

    id_material = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    codigo_material = Column(String(30), nullable=False, unique=True)
    titulo_material = Column(String(200), nullable=False)
    disponibilidad_material = Column(Boolean, nullable=False, default=True)
    descripcion_material = Column(Text, nullable=True)
    fecha_material = Column(Date, nullable=True)
    tipo_material = Column(Enum(TipoMaterial), nullable=False)

    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self) -> str:
        return f"<MaterialBiblioteca(id_material={self.id_material}, titulo='{self.titulo_material}')>"
