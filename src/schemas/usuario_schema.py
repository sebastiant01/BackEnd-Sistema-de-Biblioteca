from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID


class UsuarioCreate(BaseModel):
    nombre: str
    apellido: str
    documento: str
    email: EmailStr
    telefono: str
    contrasena: str
    rol: str
    id_usuario_crea: Optional[UUID] = None


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    documento: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    contrasena: Optional[str] = None
    rol: Optional[str] = None
    id_usuario_edita: UUID


class UsuarioRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_usuario: UUID
    nombre: str
    apellido: str
    documento: str
    email: EmailStr
    telefono: str
    username: str
    rol: str

    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None
    id_usuario_crea: Optional[UUID] = None
    id_usuario_edita: Optional[UUID] = None
