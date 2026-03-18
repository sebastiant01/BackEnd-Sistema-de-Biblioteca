from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from src.entities.MaterialBiblioteca import MaterialBiblioteca, TipoMaterial


class Periodico(MaterialBiblioteca):
    """
    Modelo ORM para la entidad Periodico.

    Extiende MaterialBiblioteca mediante herencia por tabla unida.
    Agrega los atributos específicos de un periódico.

    Attributes:
        id_periodico:       FK y PK compartida con MaterialBiblioteca.
        ciudad_publicacion: Ciudad donde fue publicado el periódico.
        seccion_periodico:  Sección del periódico (deportes, política, etc.).
    """

    __tablename__: str = "periodicos"

    id_periodico: UUID = Column(
        UUID(as_uuid=True),
        ForeignKey("materiales_biblioteca.id_material"),
        primary_key=True,
    )
    ciudad_publicacion: str = Column(String(150), nullable=False)
    seccion_periodico: str = Column(String(100), nullable=False)

    __mapper_args__ = {"polymorphic_identity": TipoMaterial.periodico}

    def __repr__(self) -> str:
        return f"<Periodico(id_periodico={self.id_periodico}, ciudad_publicacion={self.ciudad_publicacion})>"
