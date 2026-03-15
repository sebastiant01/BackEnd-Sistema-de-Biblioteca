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


class Usuario(Base, Auditoria):

    __tablename__ = "Usuarios"

    id_usuario = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    nombre = Column(String(25), nullable=False)
    apellido = Column(String(25), default="Doe")
    documento = Column(String(14), nullable=False, unique=True, index=True)
    email = Column(String(30), nullable=False)
    telefono = Column(String, nullable=False)
    username = Column(String, nullable=False)
    contrasena = Column(String(100), nullable=False)
    rol = Column(String, nullable=False, default="Cliente")

    __table_args__ = CheckConstraint(
        'rol IN ("Admin", "Usuario")',
        name="CK_Rol",
    )

    prestamo = relationship(
        "Prestamo", back_populates="propietario", cascade="all, delete-orphan"
    )
