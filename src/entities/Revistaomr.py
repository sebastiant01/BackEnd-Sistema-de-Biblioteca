"""
Modelo ORM para la entidad Revista.
 
Representa una revista como tipo de material en el sistema de biblioteca,
hereda los campos de auditoría y se relaciona con MaterialBiblioteca.
"""
 
from database.config import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
 
 
class Revista(Base):
    """Modelo de Revista"""
 
    __tablename__ = "revistas"
 
    id_material = Column(
        Integer,
        ForeignKey("materiales_biblioteca.id_material"),
        primary_key=True,
        index=True,
    )
    volumen = Column(Integer, nullable=True)
    numero_edicion = Column(Integer, nullable=True)
 
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())
 
    id_usuario_creacion = Column(
        Integer, ForeignKey("usuarios.id_usuario"), nullable=False
    )
    id_usuario_edita = Column(
        Integer, ForeignKey("usuarios.id_usuario"), nullable=True
    )
 
    material = relationship("MaterialBiblioteca", back_populates="revista")
 
    usuario_creacion = relationship(
        "Usuario",
        foreign_keys=[id_usuario_creacion],
    )
    usuario_edita = relationship(
        "Usuario",
        foreign_keys=[id_usuario_edita],
    )
 
    def __repr__(self):
        return (
            f"<Revista(id_material={self.id_material}, "
            f"volumen={self.volumen}, numero_edicion={self.numero_edicion})>"
        )
 



