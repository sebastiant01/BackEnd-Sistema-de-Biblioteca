"""
Schemas de Pydantic para la entidad Reserva.

Define los modelos de entrada y salida para los endpoints
de la API REST de Reserva.
"""

from datetime import date, datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class EstadoReservaSchema(str, Enum):
    """Enumeración de los estados posibles de una reserva."""

    pendiente = "pendiente"
    completada = "completada"
    cancelada = "cancelada"


class ReservaCreate(BaseModel):
    """Schema para crear una nueva reserva."""

    id_usuario: UUID
    id_material: UUID
    fecha_reserva: date


class ReservaUpdate(BaseModel):
    """Schema para actualizar una reserva existente."""

    fecha_reserva: Optional[date] = None
    estado_reserva: Optional[EstadoReservaSchema] = None


class ReservaRead(BaseModel):
    """Schema para leer/retornar una reserva."""

    model_config = {"from_attributes": True}

    id_reserva: UUID
    id_usuario: UUID
    id_material: UUID
    fecha_reserva: date
    estado_reserva: EstadoReservaSchema
    fecha_creacion: Optional[datetime] = None
    fecha_edicion: Optional[datetime] = None
    id_usuario_crea: UUID
    id_usuario_edita: Optional[UUID] = None
