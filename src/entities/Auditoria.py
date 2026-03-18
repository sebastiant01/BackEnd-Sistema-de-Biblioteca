from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


class Auditoria:
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    id_usuario_crea = Column(UUID(as_uuid=True), nullable=False)

    id_usuario_edita = Column(UUID(as_uuid=True), nullable=True)
