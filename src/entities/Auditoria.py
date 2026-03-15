from sqlalchemy.sql import func
from sqlalchemy import DateTime, Column


class Auditoria:
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(
        DateTime(timezone=True, server_default=func.now(), onupdate=func.now())
    )
