"""
Router de periódicos para la API REST.

Expone los endpoints CRUD del recurso Periodico, incluyendo búsqueda por título,
ciudad de publicación, sección y código, así como la gestión de disponibilidad.

Prefix: /periodicos
Tags:   periodicos
"""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from src.core.exceptions import NoEncontradoError, DatosInvalidosError
from src.database.config import get_db
from src.crud.periodico_crud import PeriodicoCRUD
from src.schemas.libro_schema import PeriodicoCreate, PeriodicoRead, PeriodicoUpdate

router = APIRouter(prefix="/periodicos", tags=["periodicos"])


def get_periodico_crud(db: Session = Depends(get_db)) -> PeriodicoCRUD:
    """Provee una instancia de PeriodicoCRUD con la sesión de base de datos activa."""
    return PeriodicoCRUD(db=db)


@router.get(path="/", response_model=List[PeriodicoRead])
def listar_periodicos(
    skip: int = 0,
    limit: int = 100,
    por_titulo: Optional[str] = None,
    por_ciudad: Optional[str] = None,
    por_seccion: Optional[str] = None,
    solo_disponibles: Optional[bool] = False,
    periodico_crud: PeriodicoCRUD = Depends(get_periodico_crud),
) -> List[PeriodicoRead]:
    """
    Lista los periódicos registrados en el sistema.

    Aplica filtros opcionales de forma excluyente en el siguiente orden de
    prioridad: título → ciudad → sección → disponibilidad. Si no se pasa
    ningún filtro, retorna todos los periódicos paginados con `skip` y `limit`.

    Args:
        skip: Número de registros a omitir (paginación).
        limit: Cantidad máxima de registros a retornar.
        por_titulo: Filtra periódicos cuyo título coincida con el valor dado.
        por_ciudad: Filtra periódicos publicados en la ciudad dada.
        por_seccion: Filtra periódicos que pertenezcan a la sección dada.
        solo_disponibles: Si es True, retorna únicamente los periódicos disponibles.
        periodico_crud: Instancia del CRUD de periódicos inyectada por dependencia.

    Returns:
        Lista de periódicos que cumplen el criterio aplicado.
    """
    if por_titulo:
        return periodico_crud.buscar_periodicos_por_titulo(
            titulo_periodico=por_titulo.strip(), skip=skip, limit=limit
        )
    if por_ciudad:
        return periodico_crud.obtener_periodicos_por_ciudad(
            ciudad_publicacion=por_ciudad.strip(), skip=skip, limit=limit
        )
    if por_seccion:
        return periodico_crud.obtener_periodicos_por_seccion(
            seccion_periodico=por_seccion.strip(), skip=skip, limit=limit
        )
    if solo_disponibles:
        return periodico_crud.obtener_periodicos_disponibles(skip=skip, limit=limit)

    return periodico_crud.obtener_periodicos(skip=skip, limit=limit)


@router.get(path="/id/{id_periodico}", response_model=PeriodicoRead)
def obtener_periodico(
    id_periodico: UUID,
    periodico_crud: PeriodicoCRUD = Depends(get_periodico_crud),
) -> PeriodicoRead:
    """
    Retorna un periódico específico por su UUID.

    Args:
        id_periodico: Identificador único del periódico.
        periodico_crud: Instancia del CRUD de periódicos inyectada por dependencia.

    Returns:
        El periódico correspondiente al UUID proporcionado.

    Raises:
        NoEncontradoError: Si no existe un periódico con ese UUID.
    """
    periodico = periodico_crud.obtener_periodico(id_periodico=id_periodico)
    if not periodico:
        raise NoEncontradoError("Periodico")
    return periodico


@router.get(path="/codigo/{codigo_periodico}", response_model=PeriodicoRead)
def obtener_periodico_codigo(
    codigo_periodico: str,
    periodico_crud: PeriodicoCRUD = Depends(get_periodico_crud),
) -> PeriodicoRead:
    """
    Retorna un periódico específico por su código de material.

    Args:
        codigo_periodico: Código único del material bibliográfico.
        periodico_crud: Instancia del CRUD de periódicos inyectada por dependencia.

    Returns:
        El periódico correspondiente al código proporcionado.

    Raises:
        NoEncontradoError: Si no existe un periódico con ese código.
    """
    periodico = periodico_crud.obtener_periodico_codigo(
        codigo_periodico=codigo_periodico
    )
    if not periodico:
        raise NoEncontradoError("Periodico")
    return periodico


@router.get(path="/autor/{id_autor}", response_model=List[PeriodicoRead])
def obtener_periodicos_autor(
    id_autor: UUID,
    periodico_crud: PeriodicoCRUD = Depends(get_periodico_crud),
) -> List[PeriodicoRead]:
    """
    Retorna todos los periódicos asociados a un autor.

    Args:
        id_autor: UUID del autor cuyos periódicos se desean consultar.
        periodico_crud: Instancia del CRUD de periódicos inyectada por dependencia.

    Returns:
        Lista de periódicos pertenecientes al autor indicado.

    Raises:
        NoEncontradoError: Si no se encontraron periódicos para ese autor.
    """
    periodicos = periodico_crud.obtener_periodicos_por_autor(id_autor=id_autor)
    if not periodicos:
        raise NoEncontradoError("Periodicos")
    return periodicos


@router.post(
    path="/", response_model=PeriodicoRead, status_code=status.HTTP_201_CREATED
)
def crear_periodico(
    body: PeriodicoCreate,
    periodico_crud: PeriodicoCRUD = Depends(get_periodico_crud),
) -> PeriodicoRead:
    """
    Crea un nuevo periódico en el sistema.

    Args:
        body: Datos del periódico a registrar, validados por el esquema PeriodicoCreate.
        periodico_crud: Instancia del CRUD de periódicos inyectada por dependencia.

    Returns:
        El periódico recién creado con todos sus campos, incluido el UUID generado.
    """
    return periodico_crud.crear_periodico(
        codigo_periodico=body.codigo_periodico,
        titulo_periodico=body.titulo_periodico,
        id_autor=body.id_autor,
        ciudad_publicacion=body.ciudad_publicacion,
        seccion_periodico=body.seccion_periodico,
        id_usuario_crea=body.id_usuario_crea,
        disponibilidad_periodico=body.disponibilidad_periodico,
        descripcion_periodico=body.descripcion_periodico,
        fecha_periodico=body.fecha_periodico,
    )


@router.put(path="/{id_periodico}", response_model=PeriodicoRead)
def actualizar_periodico(
    id_periodico: UUID,
    body: PeriodicoUpdate,
    periodico_crud: PeriodicoCRUD = Depends(get_periodico_crud),
) -> PeriodicoRead:
    """
    Actualiza los datos de un periódico existente.

    Solo se actualizan los campos presentes en el cuerpo de la solicitud.
    El campo `id_usuario_edita` se extrae del body antes de pasarlo al CRUD.

    Args:
        id_periodico: UUID del periódico a actualizar.
        body: Campos a modificar, validados por el esquema PeriodicoUpdate.
        periodico_crud: Instancia del CRUD de periódicos inyectada por dependencia.

    Returns:
        El periódico con los datos actualizados.

    Raises:
        NoEncontradoError: Si no existe un periódico con ese UUID.
    """
    id_usuario_edita = body.id_usuario_edita
    data = body.model_dump(exclude_unset=True, exclude={"id_usuario_edita"})
    periodico = periodico_crud.actualizar_periodico(
        id_periodico=id_periodico, id_usuario_edita=id_usuario_edita, **data
    )

    if not periodico:
        raise NoEncontradoError("Periodico")
    return periodico


@router.patch(path="/{id_periodico}/disponibilidad", response_model=PeriodicoRead)
def actualizar_disponibilidad_periodico(
    id_periodico: UUID,
    body: PeriodicoUpdate,
    periodico_crud: PeriodicoCRUD = Depends(get_periodico_crud),
) -> PeriodicoRead:
    """
    Cambia la disponibilidad de un periódico.

    Args:
        id_periodico: UUID del periódico cuya disponibilidad se desea modificar.
        body: Debe incluir `disponibilidad_material` e `id_usuario_edita`.
        periodico_crud: Instancia del CRUD de periódicos inyectada por dependencia.

    Returns:
        El periódico con la disponibilidad actualizada.

    Raises:
        DatosInvalidosError: Si `disponibilidad_material` no está presente en el body.
        NoEncontradoError: Si no existe un periódico con ese UUID.
    """
    id_usuario_edita = body.id_usuario_edita
    disponible = body.disponibilidad_material
    if disponible is None:
        raise DatosInvalidosError("Campo 'disponibilidad_material' no válido.")

    periodico = periodico_crud.cambiar_disponibilidad(
        id_periodico=id_periodico,
        disponible=disponible,
        id_usuario_edita=id_usuario_edita,
    )
    if not periodico:
        raise NoEncontradoError("Periodico")
    return periodico


@router.delete(path="/{id_periodico}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_periodico(
    id_periodico: UUID,
    periodico_crud: PeriodicoCRUD = Depends(get_periodico_crud),
) -> None:
    """
    Elimina un periódico del sistema de forma permanente.

    Args:
        id_periodico: UUID del periódico a eliminar.
        periodico_crud: Instancia del CRUD de periódicos inyectada por dependencia.

    Returns:
        None. Responde con HTTP 204 si la operación fue exitosa.

    Raises:
        NoEncontradoError: Si no existe un periódico con ese UUID.
    """
    periodico = periodico_crud.eliminar_periodico(id_periodico=id_periodico)
    if not periodico:
        raise NoEncontradoError("Periodico")
