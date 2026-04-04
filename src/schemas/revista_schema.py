"""
Schemas de Pydantic para la entidad Revista.

Define los modelos de entrada y salida para los endpoints
de la API REST de Revista.
"""

from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class RevistaCreate(BaseModel):
    """Schema para crear una nueva revista."""

    codigo_material: str
    titulo_material: str
    disponibilidad_material: bool = True
    descripcion_material: Optional[str] = None
    fecha_material: Optional[date] = None
    volumen: int
    numero_edicion: int

    id_autor: UUID
    id_usuario_crea: UUID


class RevistaUpdate(BaseModel):
    """Schema para actualizar una revista existente."""

    codigo_material: Optional[str] = None
    titulo_material: Optional[str] = None
    disponibilidad_material: Optional[bool] = None
    descripcion_material: Optional[str] = None
    fecha_material: Optional[date] = None
    volumen: Optional[int] = None
    numero_edicion: Optional[int] = None

    id_autor: Optional[UUID] = None
    id_usuario_edita: Optional[UUID] = None


class RevistaRead(BaseModel):
    """Schema para leer/retornar una revista."""

    model_config = ConfigDict(from_attributes=True)

    id_revista: UUID
    id_autor: UUID
    codigo_material: str
    titulo_material: str
    disponibilidad_material: bool
    descripcion_material: Optional[str] = None
    fecha_material: Optional[date] = None
    volumen: int
    numero_edicion: int

    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None
    id_usuario_crea: UUID
    id_usuario_edita: Optional[UUID] = None
