import uuid
import os
import sys
from sqlalchemy import Column, String, CheckConstraint, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database.config import Base
from src.entities.Auditoria import Auditoria

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class Autor(Base, Auditoria):

    id_autor = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    nombre_autor = Column(String(50), nullable=False)
    apellido_autor = Column(String(50), nullable=True)
    nacionalidad = Column(String(50), nullable=True)
