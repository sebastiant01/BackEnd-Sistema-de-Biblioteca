from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date, datetime
from uuid import UUID


class LibroCreate(BaseModel):
    codigo_material: str
    titulo_material: str
    disponibilidad_material: bool = True
    descripcion_material: Optional[str] = None
    fecha_material: Optional[date] = None
    codigo_isbn: str
    genero_libro: str

    id_autor: UUID
    id_usuario_crea: UUID


class LibroUpdate(BaseModel):
    codigo_material: Optional[str] = None
    titulo_material: Optional[str] = None
    disponibilidad_material: Optional[bool] = None
    descripcion_material: Optional[str] = None
    fecha_material: Optional[date] = None
    codigo_isbn: Optional[str] = None
    genero_libro: Optional[str] = None

    id_autor: Optional[UUID] = None
    id_usuario_edita: Optional[UUID] = None


class LibroRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_libro: UUID
    id_autor: UUID
    codigo_material: str
    titulo_material: str
    disponibilidad_material: bool
    descripcion_material: Optional[str] = None
    fecha_material: Optional[date] = None
    codigo_isbn: str
    genero_libro: str

    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None
    id_usuario_creacion: UUID
    id_usuario_edita: Optional[UUID] = None
