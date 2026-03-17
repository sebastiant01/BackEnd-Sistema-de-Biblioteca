import uuid
import enum
from typing import Optional

from database.config import Base
from sqlalchemy import Column, Date, DateTime, Boolean, String, Text, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class TipoMaterial(enum.Enum):
    """Enumeración de los tipos de material bibliográfico disponibles."""

    libro: str = "libro"
    revista: str = "revista"
    periodico: str = "periodico"


class MaterialBiblioteca(Base):
    """
    Modelo ORM para la entidad MaterialBiblioteca.

    Representa un material bibliográfico disponible en el sistema de biblioteca.
    Es la entidad padre de Libro, Revista y Periodico mediante herencia por tabla unida.

    Attributes:
        id_material:             Identificador único del material (UUID).
        codigo_material:         Código interno único del material.
        titulo_material:         Título del material bibliográfico.
        disponibilidad_material: Indica si el material está disponible para préstamo.
        descripcion_material:    Descripción opcional del material.
        fecha_material:          Fecha de publicación del material.
        tipo_material:           Tipo de material (libro, revista, periódico).
        fecha_creacion:          Fecha y hora de creación del registro.
        fecha_edicion:           Fecha y hora de la última modificación del registro.
        id_autor:                FK al autor principal del material.
        id_usuario_crea:         FK al usuario que creó el registro.
        id_usuario_edita:        FK al usuario que realizó la última modificación.
    """

    __tablename__: str = "materiales_biblioteca"

    id_material: UUID = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    codigo_material: str = Column(String(20), nullable=False, unique=True)
    titulo_material: str = Column(String(200), nullable=False)
    disponibilidad_material: bool = Column(Boolean, nullable=False, default=True)
    descripcion_material: Optional[str] = Column(Text, nullable=True)
    fecha_material: Optional[Date] = Column(Date, nullable=True)
    tipo_material: TipoMaterial = Column(Enum(TipoMaterial), nullable=False)

    fecha_creacion: DateTime = Column(
        DateTime(timezone=True), server_default=func.now()
    )
    fecha_edicion: Optional[DateTime] = Column(
        DateTime(timezone=True), onupdate=func.now()
    )

    id_autor: UUID = Column(
        UUID(as_uuid=True), ForeignKey("autores.id_autor"), nullable=False
    )

    id_usuario_crea: UUID = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=False
    )
    id_usuario_edita: Optional[UUID] = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=True
    )

    autor = relationship("Autor", back_populates="materiales_biblioteca")

    prestamo = relationship("Prestamo", back_populates="material_prestado")

    usuario_crea = relationship(
        "Usuario",
        foreign_keys=[id_usuario_crea],
    )
    usuario_edita = relationship(
        "Usuario",
        foreign_keys=[id_usuario_edita],
    )

    __mapper_args__ = {"polymorphic_on": tipo_material, "polymorphic_identity": None}

    def __repr__(self) -> str:
        return f"<MaterialBiblioteca(id_material={self.id_material}, titulo='{self.titulo_material}')>"
