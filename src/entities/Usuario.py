import uuid
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy import Column, String, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.database.config import Base
from src.entities.Auditoria import Auditoria


class Usuario(Base, Auditoria):
    """
    Modelo ORM que representa a un Usuario dentro del sistema.

    Esta entidad almacena la información personal, credenciales de acceso y el nivel
    de privilegios (rol) de los usuarios. Hereda de `Base` para el mapeo declarativo
    de SQLAlchemy y de `Auditoria` para gestionar automáticamente los metadatos de
    creación y actualización en la base de datos.

    Attributes:
        id_usuario (UUID): Identificador único universal del usuario (Primary Key).
                           Se genera automáticamente mediante uuid4.
        nombre (str): Nombre(s) del usuario. Longitud máxima de 25 caracteres.
        apellido (str): Apellido(s) del usuario. Valor por defecto: "Doe".
        documento (str): Número de documento de identidad. Es único e indexado
                         para optimizar tiempos de búsqueda.
        email (str): Correo electrónico del usuario. Longitud máxima de 30 caracteres.
        telefono (str): Número de teléfono de contacto.
        username (str): Nombre de usuario para el inicio de sesión.
        contrasena (str): Hash de la contraseña del usuario (nunca en texto plano).
        rol (str): Nivel de acceso del usuario en el sistema.

    Relationships:
        prestamo (list): Colección de objetos `Prestamo` asociados a este usuario.
                         Incluye eliminación en cascada (delete-orphan).
        reserva (list): Colección de objetos `Reserva` realizados por este usuario.
                        Incluye eliminación en cascada (delete-orphan).
        sanciones (list): Colección de objetos `Sancion` aplicados a este usuario.
                          Incluye eliminación en cascada (delete-orphan).
    """

    __tablename__ = "usuarios"

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
    rol = Column(String, nullable=False, default="Usuario")

    __table_args__ = (
        CheckConstraint(
            "rol IN ('Admin', 'Usuario')",
            name="CK_Rol",
        ),
    )

    prestamo = relationship(
        "Prestamo",
        back_populates="usuario_prestamo",
        foreign_keys="[Prestamo.id_usuario]",
        cascade="all, delete-orphan",
    )

    reserva = relationship(
        "Reserva",
        back_populates="usuario",
        foreign_keys="[Reserva.id_usuario]",
        cascade="all, delete-orphan",
    )

    sanciones = relationship(
        "Sancion",
        back_populates="usuario_sancionado",
        foreign_keys="[Sancion.id_usuario]",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        """
        Proporciona una representación en formato de cadena (string) del objeto Usuario.

        Útil para procesos de depuración (debugging) y logs del sistema. Retorna los
        atributos más relevantes del usuario omitiendo datos sensibles como la contraseña.

        Returns:
            str: Representación del estado actual de la instancia.
        """
        return (
            f"<Usuario(id_usuario={self.id_usuario}, "
            f"nombre='{self.nombre}', apellido='{self.apellido}', "
            f"documento='{self.documento}', email='{self.email}', "
            f"telefono='{self.telefono}', username='{self.username}', "
            f"rol='{self.rol}')>"
        )
