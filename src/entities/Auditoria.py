from sqlalchemy.sql import func
from typing import Optional
from sqlalchemy import DateTime, Column, ForeignKey, UUID


class Auditoria:
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(
        DateTime(timezone=True, server_default=func.now(), onupdate=func.now())
    )

    id_usuario_crea: UUID = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=False
    )
    id_usuario_edita: Optional[UUID] = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=True
    )
