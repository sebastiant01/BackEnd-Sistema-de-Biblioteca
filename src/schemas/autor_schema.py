from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID


class AutorCreate(BaseModel):
    nombre_autor: str
    apellido_autor: str
    nacionalidad: str
    activo: bool = True

    id_usuario_crea: UUID


class AutorUpdate(BaseModel):
    nombre_autor: Optional[str] = None
    apellido_autor: Optional[str] = None
    nacionalidad: Optional[str] = None
    activo: Optional[bool] = None

    id_usuario_edita: UUID


class AutorRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_autor: UUID
    nombre_autor: str
    apellido_autor: str
    nacionalidad: str
    activo: bool

    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None
    id_usuario_crea: UUID
    id_usuario_edita: Optional[UUID] = None
