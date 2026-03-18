from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


class Auditoria:
    """
    Clase auxiliar/Mixin de auditoría para los modelos de la base de datos.

    Proporciona un registro histórico pasivo mediante "Soft References" (referencias suaves)
    para rastrear la creación y modificación de los registros. Al no usar Claves Foráneas
    (Foreign Keys) estrictas, evita el acoplamiento fuerte y previene errores de
    integridad referencial (AmbiguousForeignKeys) en el ORM.

    Attributes:
        fecha_creacion (Column[DateTime]): Fecha y hora exacta en la que se creó el registro.
            Se genera automáticamente por el motor de la base de datos (PostgreSQL).
        fecha_edicion (Column[DateTime]): Fecha y hora de la última modificación del registro.
            Se actualiza automáticamente en cada operación UPDATE.
        id_usuario_crea (Column[UUID]): Identificador único (UUID) del administrador o usuario
            que insertó el registro por primera vez. Es un campo obligatorio.
        id_usuario_edita (Column[UUID]): Identificador único (UUID) del último administrador o
            usuario que modificó el registro. Es opcional.
    """

    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    id_usuario_crea = Column(UUID(as_uuid=True), nullable=False)

    id_usuario_edita = Column(UUID(as_uuid=True), nullable=True)
