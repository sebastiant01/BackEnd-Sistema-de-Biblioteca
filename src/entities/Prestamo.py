import uuid
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy import Column, ForeignKey, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database.config import Base
from src.entities.Auditoria import Auditoria
from src.entities.Usuario import Usuario
from src.entities.MaterialBiblioteca import MaterialBiblioteca


class Prestamo(Base, Auditoria):
    """
    Modelo ORM que representa la entidad independiente de un Préstamo.

    Esta clase gestiona el registro histórico y el estado de los materiales que
    los usuarios retiran de la biblioteca. Al tener su propia clave primaria
    (Llave Subrogada), permite que un mismo usuario solicite el mismo material
    en diferentes momentos sin generar conflictos de integridad. Hereda de `Base`
    para SQLAlchemy y de `Auditoria` para trazabilidad.

    Attributes:
        id_prestamo (UUID): Identificador único del préstamo (Primary Key).
        id_usuario (UUID): Clave foránea que referencia al usuario que realiza el préstamo.
        id_material (UUID): Clave foránea que referencia al material bibliotecario prestado.
        fecha_prestamo (DateTime): Fecha y hora exacta en la que se generó el préstamo.
                                   Asignada automáticamente por la base de datos.
        estado (str): Estado actual del préstamo (ej. "Activa", "Devuelto", "Atrasado").
                      Valor por defecto: "Activa".

    Relationships:
        usuario_prestamo (Usuario): Relación bidireccional con la entidad `Usuario`.
                                    Permite acceder a los datos de quien pidió el préstamo.
        material_prestado (MaterialBiblioteca): Relación bidireccional con `MaterialBiblioteca`.
                                                Permite acceder a los detalles del material.
    """

    __tablename__ = "prestamos"

    id_prestamo = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    id_usuario = Column(UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"))
    usuario_prestamo = relationship(
        "Usuario", back_populates="prestamo", foreign_keys="[Prestamo.id_usuario]"
    )

    id_material = Column(
        UUID(as_uuid=True), ForeignKey("materiales_biblioteca.id_material")
    )
    material_prestado = relationship(
        "MaterialBiblioteca",
        back_populates="prestamo",
        foreign_keys="[Prestamo.id_material]",
    )

    fecha_prestamo = Column(DateTime(timezone=True), server_default=func.now())
    estado = Column(String, nullable=False, default="Activa")

    sancion_involucrada = relationship(
        "Sancion", back_populates="prestamo", foreign_keys="[Sancion.id_prestamo]"
    )

    def __repr__(self) -> str:
        """
        Genera una representación en formato de cadena (string) del Préstamo.

        Ideal para revisar el estado del préstamo en la terminal o en archivos
        de log de manera legible.

        Returns:
            str: Resumen de los atributos clave del objeto Prestamo.
        """
        return (
            f"<Prestamo(id_prestamo={self.id_prestamo}, "
            f"id_usuario='{self.id_usuario}', id_material='{self.id_material}'"
            f"fecha_prestamo='{self.fecha_prestamo}', estado='{self.estado}')>"
        )
