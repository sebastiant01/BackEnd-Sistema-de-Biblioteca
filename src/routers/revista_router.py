"""
Router de revistas para la API REST.

Expone los endpoints CRUD del recurso Revista, incluyendo búsqueda por título,
código y autor, así como la gestión de disponibilidad.

Prefix: /revistas
Tags:   revistas
"""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from src.core.exceptions import NoEncontradoError, DatosInvalidosError
from src.database.config import get_db
from src.crud.Revista_crud import RevistaCRUD
from src.schemas.revista_schema import RevistaCreate, RevistaRead, RevistaUpdate

router = APIRouter(prefix="/revistas", tags=["revistas"])


def get_revista_crud(db: Session = Depends(get_db)) -> RevistaCRUD:
    """Provee una instancia de RevistaCRUD con la sesión de base de datos activa."""
    return RevistaCRUD(db=db)


@router.get(path="/", response_model=List[RevistaRead])
def listar_revistas(
    skip: int = 0,
    limit: int = 100,
    por_titulo: Optional[str] = None,
    por_autor: Optional[UUID] = None,
    solo_disponibles: Optional[bool] = False,
    revista_crud: RevistaCRUD = Depends(get_revista_crud),
) -> List[RevistaRead]:
    """
    Lista las revistas registradas en el sistema.

    Aplica filtros opcionales de forma excluyente en el siguiente orden de
    prioridad: título → autor → disponibilidad. Si no se pasa ningún filtro,
    retorna todas las revistas paginadas con `skip` y `limit`.

    Args:
        skip: Número de registros a omitir (paginación).
        limit: Cantidad máxima de registros a retornar.
        por_titulo: Filtra revistas cuyo título coincida con el valor dado.
        por_autor: Filtra revistas del autor con el UUID dado.
        solo_disponibles: Si es True, retorna únicamente las revistas disponibles.
        revista_crud: Instancia del CRUD de revistas inyectada por dependencia.

    Returns:
        Lista de revistas que cumplen el criterio aplicado.
    """
    if por_titulo:
        return revista_crud.buscar_revistas_por_titulo(titulo=por_titulo.strip())
    if por_autor:
        return revista_crud.obtener_revistas_por_autor(id_autor=por_autor)
    if solo_disponibles:
        return revista_crud.obtener_revistas_disponibles()

    return revista_crud.obtener_revistas(skip=skip, limit=limit)


@router.get(path="/codigo/{codigo_revista}", response_model=RevistaRead)
def obtener_revista_codigo(
    codigo_revista: str, revista_crud: RevistaCRUD = Depends(get_revista_crud)
) -> RevistaRead:
    """
    Retorna una revista específica por su código de material.

    Args:
        codigo_revista: Código único del material bibliográfico (ej. R001).
        revista_crud: Instancia del CRUD de revistas inyectada por dependencia.

    Returns:
        La revista correspondiente al código proporcionado.

    Raises:
        NoEncontradoError: Si no existe una revista con ese código.
    """
    revista = revista_crud.obtener_revista_por_codigo(codigo_material=codigo_revista)
    if not revista:
        raise NoEncontradoError("Revista")
    return revista


@router.get(path="/{id_revista}", response_model=RevistaRead)
def obtener_revista(
    id_revista: UUID, revista_crud: RevistaCRUD = Depends(get_revista_crud)
) -> RevistaRead:
    """
    Retorna una revista específica por su UUID.

    Args:
        id_revista: Identificador único de la revista.
        revista_crud: Instancia del CRUD de revistas inyectada por dependencia.

    Returns:
        La revista correspondiente al UUID proporcionado.

    Raises:
        NoEncontradoError: Si no existe una revista con ese UUID.
    """
    revista = revista_crud.obtener_revista(revista_id=id_revista)
    if not revista:
        raise NoEncontradoError("Revista")
    return revista


@router.post(path="/", response_model=RevistaRead, status_code=status.HTTP_201_CREATED)
def crear_revista(
    body: RevistaCreate, revista_crud: RevistaCRUD = Depends(get_revista_crud)
) -> RevistaRead:
    """
    Crea una nueva revista en el sistema.

    Args:
        body: Datos de la revista a registrar, validados por el esquema RevistaCreate.
        revista_crud: Instancia del CRUD de revistas inyectada por dependencia.

    Returns:
        La revista recién creada con todos sus campos, incluido el UUID generado.
    """
    return revista_crud.crear_revista(
        codigo_material=body.codigo_material,
        titulo_material=body.titulo_material,
        id_autor=body.id_autor,
        volumen=body.volumen,
        numero_edicion=body.numero_edicion,
        id_usuario_crea=body.id_usuario_crea,
        disponibilidad_material=body.disponibilidad_material,
        descripcion_material=body.descripcion_material,
        fecha_material=body.fecha_material,
    )


@router.put(path="/{id_revista}", response_model=RevistaRead)
def actualizar_revista(
    id_revista: UUID,
    body: RevistaUpdate,
    revista_crud: RevistaCRUD = Depends(get_revista_crud),
) -> RevistaRead:
    """
    Actualiza los datos de una revista existente.

    Solo se actualizan los campos presentes en el cuerpo de la solicitud.
    El campo `id_usuario_edita` se extrae del body antes de pasarlo al CRUD.

    Args:
        id_revista: UUID de la revista a actualizar.
        body: Campos a modificar, validados por el esquema RevistaUpdate.
        revista_crud: Instancia del CRUD de revistas inyectada por dependencia.

    Returns:
        La revista con los datos actualizados.

    Raises:
        NoEncontradoError: Si no existe una revista con ese UUID.
    """
    id_usuario_edita = body.id_usuario_edita
    data = body.model_dump(exclude_unset=True, exclude={"id_usuario_edita"})

    revista = revista_crud.actualizar_revista(
        revista_id=id_revista, id_usuario_edita=id_usuario_edita, **data
    )

    if not revista:
        raise NoEncontradoError("Revista")
    return revista


@router.patch(path="/{id_revista}/disponibilidad", response_model=RevistaRead)
def actualizar_disponibilidad_revista(
    id_revista: UUID,
    body: RevistaUpdate,
    revista_crud: RevistaCRUD = Depends(get_revista_crud),
) -> RevistaRead:
    """
    Cambia la disponibilidad de una revista.

    Args:
        id_revista: UUID de la revista cuya disponibilidad se desea modificar.
        body: Debe incluir `disponibilidad_material` e `id_usuario_edita`.
        revista_crud: Instancia del CRUD de revistas inyectada por dependencia.

    Returns:
        La revista con la disponibilidad actualizada.

    Raises:
        DatosInvalidosError: Si `disponibilidad_material` no está presente en el body.
        NoEncontradoError: Si no existe una revista con ese UUID.
    """
    id_usuario_edita = body.id_usuario_edita
    disponible = body.disponibilidad_material
    if disponible is None:
        raise DatosInvalidosError("Campo 'disponibilidad_material' no válido.")

    revista = revista_crud.cambiar_disponibilidad(
        revista_id=id_revista, disponible=disponible, id_usuario_edita=id_usuario_edita
    )
    if not revista:
        raise NoEncontradoError("Revista")
    return revista


@router.delete(path="/{id_revista}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_revista(
    id_revista: UUID, revista_crud: RevistaCRUD = Depends(get_revista_crud)
) -> None:
    """
    Elimina una revista del sistema de forma permanente.

    Args:
        id_revista: UUID de la revista a eliminar.
        revista_crud: Instancia del CRUD de revistas inyectada por dependencia.

    Returns:
        None. Responde con HTTP 204 si la operación fue exitosa.

    Raises:
        NoEncontradoError: Si no existe una revista con ese UUID.
    """
    eliminado = revista_crud.eliminar_revista(revista_id=id_revista)
    if not eliminado:
        raise NoEncontradoError("Revista")
