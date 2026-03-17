from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from src.entities.MaterialBiblioteca import MaterialBiblioteca, TipoMaterial


class Libro(MaterialBiblioteca):
    """
    Modelo ORM para la entidad Libro.

    Extiende MaterialBiblioteca mediante herencia por tabla unida.
    Agrega los atributos específicos de un libro.

    Attributes:
        id_libro:     FK y PK compartida con MaterialBiblioteca.
        codigo_isbn:  Código ISBN único del libro.
        genero_libro: Género literario del libro.
    """

    __tablename__: str = "libros"

    id_libro: UUID = Column(
        UUID(as_uuid=True),
        ForeignKey("materiales_biblioteca.id_material"),
        primary_key=True,
    )
    codigo_isbn: str = Column(String(20), unique=True, nullable=False)
    genero_libro: str = Column(String(50), nullable=False)

    __mapper_args__ = {"polymorphic_identity": TipoMaterial.libro}

    def __repr__(self) -> str:
        return f"<Libro(id_libro={self.id_libro}, codigo_isbn={self.codigo_isbn})>"
