"""
Router de sanciones para la API REST.

Expone los endpoints CRUD del recurso Sancion, incluyendo filtros
por usuario y préstamo.

Prefix: /sanciones
Tags:   sanciones
"""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from src.core.exceptions import NoEncontradoError
from src.database.config import get_db
from src.crud.Sancion_crud import SancionCRUD
from src.schemas.sancion_schema import SancionCreate, SancionRead, SancionUpdate

router = APIRouter(prefix="/sanciones", tags=["sanciones"])


def get_sancion_crud(db: Session = Depends(get_db)) -> SancionCRUD:
    """Provee una instancia de SancionCRUD con la sesión de base de datos activa."""
    return SancionCRUD(db=db)


@router.get(path="/", response_model=List[SancionRead])
def listar_sanciones(
    skip: int = 0,
    limit: int = 100,
    por_usuario: Optional[UUID] = None,
    por_prestamo: Optional[UUID] = None,
    sancion_crud: SancionCRUD = Depends(get_sancion_crud),
) -> List[SancionRead]:
    """
    Lista las sanciones registradas en el sistema.

    Aplica filtros opcionales de forma excluyente en el siguiente orden de
    prioridad: usuario → préstamo. Si no se pasa ningún filtro, retorna
    todas las sanciones paginadas con `skip` y `limit`.

    Args:
        skip: Número de registros a omitir (paginación).
        limit: Cantidad máxima de registros a retornar.
        por_usuario: Filtra sanciones del usuario con el UUID dado.
        por_prestamo: Filtra sanciones del préstamo con el UUID dado.
        sancion_crud: Instancia del CRUD de sanciones inyectada por dependencia.

    Returns:
        Lista de sanciones que cumplen el criterio aplicado.
    """
    if por_usuario:
        return sancion_crud.obtener_sanciones_por_usuario(id_usuario=por_usuario)
    if por_prestamo:
        return sancion_crud.obtener_sanciones_por_prestamo(id_prestamo=por_prestamo)

    return sancion_crud.obtener_sanciones(skip=skip, limit=limit)


@router.get(path="/{id_sancion}", response_model=SancionRead)
def obtener_sancion(
    id_sancion: UUID, sancion_crud: SancionCRUD = Depends(get_sancion_crud)
) -> SancionRead:
    """
    Retorna una sanción específica por su UUID.

    Args:
        id_sancion: Identificador único de la sanción.
        sancion_crud: Instancia del CRUD de sanciones inyectada por dependencia.

    Returns:
        La sanción correspondiente al UUID proporcionado.

    Raises:
        NoEncontradoError: Si no existe una sanción con ese UUID.
    """
    sancion = sancion_crud.obtener_sancion(sancion_id=id_sancion)
    if not sancion:
        raise NoEncontradoError("Sancion")
    return sancion


@router.post(path="/", response_model=SancionRead, status_code=status.HTTP_201_CREATED)
def crear_sancion(
    body: SancionCreate, sancion_crud: SancionCRUD = Depends(get_sancion_crud)
) -> SancionRead:
    """
    Crea una nueva sanción en el sistema.

    Args:
        body: Datos de la sanción a registrar, validados por el esquema SancionCreate.
        sancion_crud: Instancia del CRUD de sanciones inyectada por dependencia.

    Returns:
        La sanción recién creada con todos sus campos, incluido el UUID generado.
    """
    return sancion_crud.crear_sancion(
        id_usuario=body.id_usuario,
        id_prestamo=body.id_prestamo,
        fecha_inicio=body.fecha_inicio,
        dias_sancion=body.dias_sancion,
        motivo=body.motivo,
        id_usuario_crea=body.id_usuario_crea,
    )


@router.put(path="/{id_sancion}", response_model=SancionRead)
def actualizar_sancion(
    id_sancion: UUID,
    body: SancionUpdate,
    sancion_crud: SancionCRUD = Depends(get_sancion_crud),
) -> SancionRead:
    """
    Actualiza los datos de una sanción existente.

    Solo se actualizan los campos presentes en el cuerpo de la solicitud.
    El campo `id_usuario_edita` se extrae del body antes de pasarlo al CRUD.

    Args:
        id_sancion: UUID de la sanción a actualizar.
        body: Campos a modificar, validados por el esquema SancionUpdate.
        sancion_crud: Instancia del CRUD de sanciones inyectada por dependencia.

    Returns:
        La sanción con los datos actualizados.

    Raises:
        NoEncontradoError: Si no existe una sanción con ese UUID.
    """
    id_usuario_edita = body.id_usuario_edita
    data = body.model_dump(exclude_unset=True, exclude={"id_usuario_edita"})

    sancion = sancion_crud.actualizar_sancion(
        sancion_id=id_sancion, id_usuario_edita=id_usuario_edita, **data
    )

    if not sancion:
        raise NoEncontradoError("Sancion")
    return sancion


@router.delete(path="/{id_sancion}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_sancion(
    id_sancion: UUID, sancion_crud: SancionCRUD = Depends(get_sancion_crud)
) -> None:
    """
    Elimina una sanción del sistema de forma permanente.

    Args:
        id_sancion: UUID de la sanción a eliminar.
        sancion_crud: Instancia del CRUD de sanciones inyectada por dependencia.

    Returns:
        None. Responde con HTTP 204 si la operación fue exitosa.

    Raises:
        NoEncontradoError: Si no existe una sanción con ese UUID.
    """
    eliminado = sancion_crud.eliminar_sancion(sancion_id=id_sancion)
    if not eliminado:
        raise NoEncontradoError("Sancion")
