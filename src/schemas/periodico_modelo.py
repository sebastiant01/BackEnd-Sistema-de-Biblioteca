from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date, datetime
from sqlalchemy.dialects.postgresql import UUID


class PeriodicoCreate(BaseModel):
    codigo_material: str
    titulo_material: str
    disponibilidad_material: bool = True
    descripcion_material: Optional[str] = None
    fecha_material: Optional[date] = None
    ciudad_publicacion: str
    seccion_periodico: str

    id_autor: UUID
    id_usuario_crea: UUID


class PeriodicoUpdate(BaseModel):
    codigo_material: Optional[str] = None
    titulo_material: Optional[str] = None
    disponibilidad_material: Optional[bool] = None
    descripcion_material: Optional[str] = None
    fecha_material: Optional[date] = None
    ciudad_publicacion: Optional[str] = None
    seccion_periodico: Optional[str] = None

    id_autor: Optional[UUID] = None
    id_usuario_edita: Optional[UUID] = None


class PeriodicoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_periodico: UUID
    id_autor: UUID
    codigo_material: str
    titulo_material: str
    disponibilidad_material: bool
    descripcion_material: Optional[str] = None
    fecha_material: Optional[date] = None
    ciudad_publicacion: str
    seccion_periodico: str

    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None
    id_usuario_creacion: UUID
    id_usuario_edita: Optional[UUID] = None
