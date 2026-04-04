from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID


class PrestamoCreate(BaseModel):
    id_usuario: UUID
    id_material: UUID

    id_usuario_crea: UUID


class PrestamoUpdate(BaseModel):
    estado: Optional[str] = None

    id_usuario_edita: UUID


class PrestamoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_prestamo: UUID
    id_usuario: UUID
    id_material: UUID
    fecha_prestamo: datetime
    estado: str

    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None
    id_usuario_crea: UUID
    id_usuario_edita: Optional[UUID] = None
