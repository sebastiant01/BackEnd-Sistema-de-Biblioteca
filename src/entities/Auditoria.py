from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_mixin, declared_attr
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey


@declarative_mixin
class Auditoria:
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    @declared_attr
    def id_usuario_crea(cls):
        return Column(
            UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=False
        )

    @declared_attr
    def id_usuario_edita(cls):
        return Column(
            UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=True
        )
