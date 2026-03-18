"""
Modelo ORM para la entidad Revista.

Representa una revista como especialización de MaterialBiblioteca
en el sistema de biblioteca. Incluye columnas de auditoría con
referencia a la entidad Usuario.
"""

import uuid

from src.entities.MaterialBiblioteca import MaterialBiblioteca, TipoMaterial
from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Revista(MaterialBiblioteca):
    """Modelo de Revista"""

    __tablename__ = "revistas"

    id_revista = Column(
        UUID(as_uuid=True),
        ForeignKey("materiales_biblioteca.id_material"),
        primary_key=True,
    )
    volumen = Column(Integer, nullable=False)
    numero_edicion = Column(Integer, nullable=False)

    __mapper_args__ = {"polymorphic_identity": TipoMaterial.revista}

    def __repr__(self):
        return (
            f"<Revista(id_revista={self.id_revista}, "
            f"volumen={self.volumen}, numero_edicion={self.numero_edicion})>"
        )
