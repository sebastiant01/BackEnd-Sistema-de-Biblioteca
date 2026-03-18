import uuid
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy import Column, String, CheckConstraint, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database.config import Base
from src.entities.MaterialBiblioteca import MaterialBiblioteca
from src.entities.Auditoria import Auditoria


class Autor(Base, Auditoria):
    """
    Modelo ORM que representa a un Autor de materiales dentro de la biblioteca.

    Esta entidad almacena los datos biográficos básicos de los creadores
    (escritores, directores, etc.) de los materiales disponibles en el sistema.
    Hereda de `Base` para el mapeo con la base de datos y de `Auditoria` para
    el registro automático de fechas de creación y modificación.

    Attributes:
        id_autor (UUID): Identificador único universal del autor (Primary Key).
                         Generado automáticamente por uuid4.
        nombre_autor (str): Nombre(s) del autor. Campo obligatorio, máximo 50 caracteres.
        apellido_autor (str): Apellido(s) del autor. Campo opcional, máximo 50 caracteres.
        nacionalidad (str): País de origen del autor. Campo opcional, máximo 50 caracteres.
        activo (bool): Representa si el autor sigue activo dentro de la base de datos.

    Relationships:
        materiales_biblioteca (list): Colección de objetos `MaterialBiblioteca`
                                      escritos o creados por este autor. Configurado
                                      con eliminación en cascada.
    """

    __tablename__ = "autores"

    id_autor: UUID = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    nombre_autor: str = Column(String(50), nullable=False)
    apellido_autor: str = Column(String(50), nullable=True)
    nacionalidad: str = Column(String(50), nullable=True)
    activo: bool = Column(Boolean, nullable=False)

    materiales_biblioteca = relationship(
        "MaterialBiblioteca",
        back_populates="autor",
        foreign_keys="[MaterialBiblioteca.id_autor]",
    )

    def __repr__(self) -> str:
        """
        Genera una representación en formato de cadena (string) del Autor.

        Proporciona un resumen legible con los datos principales del autor,
        ideal para depuración y registros del sistema.

        Returns:
            str: Representación del estado actual de la instancia Autor.
        """
        return (
            f"<Autor(id_autor={self.id_autor}, "
            f"nombre_autor='{self.nombre_autor}', apellido_autor='{self.apellido_autor}', "
            f"nacionalidad='{self.nacionalidad}')>"
        )
