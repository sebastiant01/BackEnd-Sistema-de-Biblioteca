"""
Schemas de Pydantic para la entidad Sancion.

Define los modelos de entrada y salida para los endpoints
de la API REST de Sancion.
"""

from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SancionCreate(BaseModel):
    """Schema para crear una nueva sanción."""

    id_usuario: UUID
    id_prestamo: UUID
    fecha_inicio: date
    dias_sancion: int
    motivo: str

    id_usuario_crea: UUID


class SancionUpdate(BaseModel):
    """Schema para actualizar una sanción existente."""

    fecha_inicio: Optional[date] = None
    dias_sancion: Optional[int] = None
    motivo: Optional[str] = None

    id_usuario_edita: Optional[UUID] = None


class SancionRead(BaseModel):
    """Schema para leer/retornar una sanción."""

    model_config = ConfigDict(from_attributes=True)

    id_sancion: UUID
    id_usuario: UUID
    id_prestamo: UUID
    fecha_inicio: date
    dias_sancion: int
    motivo: str

    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None
    id_usuario_crea: UUID
    id_usuario_edita: Optional[UUID] = None
