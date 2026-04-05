"""
Router de reservas para la API REST.

Expone los endpoints CRUD del recurso Reserva, incluyendo filtros
por usuario, material y estado.

Prefix: /reservas
Tags:   reservas
"""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from src.core.exceptions import NoEncontradoError
from src.database.config import get_db
from src.crud.Reserva_crud import ReservaCRUD
from src.schemas.reserva_schema import ReservaCreate, ReservaRead, ReservaUpdate
from src.entities.Reserva import EstadoReserva

router = APIRouter(prefix="/reservas", tags=["reservas"])


def get_reserva_crud(db: Session = Depends(get_db)) -> ReservaCRUD:
    """Provee una instancia de ReservaCRUD con la sesión de base de datos activa."""
    return ReservaCRUD(db=db)


@router.get(path="/", response_model=List[ReservaRead])
def listar_reservas(
    skip: int = 0,
    limit: int = 100,
    por_usuario: Optional[UUID] = None,
    por_material: Optional[UUID] = None,
    por_estado: Optional[EstadoReserva] = None,
    reserva_crud: ReservaCRUD = Depends(get_reserva_crud),
) -> List[ReservaRead]:
    """
    Lista las reservas registradas en el sistema.

    Aplica filtros opcionales de forma excluyente en el siguiente orden de
    prioridad: usuario → material → estado. Si no se pasa ningún filtro,
    retorna todas las reservas paginadas con `skip` y `limit`.

    Args:
        skip: Número de registros a omitir (paginación).
        limit: Cantidad máxima de registros a retornar.
        por_usuario: Filtra reservas del usuario con el UUID dado.
        por_material: Filtra reservas del material con el UUID dado.
        por_estado: Filtra reservas por estado (pendiente, completada, cancelada).
        reserva_crud: Instancia del CRUD de reservas inyectada por dependencia.

    Returns:
        Lista de reservas que cumplen el criterio aplicado.
    """
    if por_usuario:
        return reserva_crud.obtener_reservas_por_usuario(id_usuario=por_usuario)
    if por_material:
        return reserva_crud.obtener_reservas_por_material(id_material=por_material)
    if por_estado:
        return reserva_crud.obtener_reservas_por_estado(estado=por_estado)

    return reserva_crud.obtener_reservas(skip=skip, limit=limit)


@router.get(path="/{id_reserva}", response_model=ReservaRead)
def obtener_reserva(
    id_reserva: UUID, reserva_crud: ReservaCRUD = Depends(get_reserva_crud)
) -> ReservaRead:
    """
    Retorna una reserva específica por su UUID.

    Args:
        id_reserva: Identificador único de la reserva.
        reserva_crud: Instancia del CRUD de reservas inyectada por dependencia.

    Returns:
        La reserva correspondiente al UUID proporcionado.

    Raises:
        NoEncontradoError: Si no existe una reserva con ese UUID.
    """
    reserva = reserva_crud.obtener_reserva(reserva_id=id_reserva)
    if not reserva:
        raise NoEncontradoError("Reserva")
    return reserva


@router.post(path="/", response_model=ReservaRead, status_code=status.HTTP_201_CREATED)
def crear_reserva(
    body: ReservaCreate, reserva_crud: ReservaCRUD = Depends(get_reserva_crud)
) -> ReservaRead:
    """
    Crea una nueva reserva en el sistema.

    Args:
        body: Datos de la reserva a registrar, validados por el esquema ReservaCreate.
        reserva_crud: Instancia del CRUD de reservas inyectada por dependencia.

    Returns:
        La reserva recién creada con todos sus campos, incluido el UUID generado.
    """
    return reserva_crud.crear_reserva(
        id_usuario=body.id_usuario,
        id_material=body.id_material,
        fecha_reserva=body.fecha_reserva,
        id_usuario_crea=body.id_usuario_crea,
    )


@router.put(path="/{id_reserva}", response_model=ReservaRead)
def actualizar_reserva(
    id_reserva: UUID,
    body: ReservaUpdate,
    reserva_crud: ReservaCRUD = Depends(get_reserva_crud),
) -> ReservaRead:
    """
    Actualiza los datos de una reserva existente.

    Solo se actualizan los campos presentes en el cuerpo de la solicitud.
    El campo `id_usuario_edita` se extrae del body antes de pasarlo al CRUD.

    Args:
        id_reserva: UUID de la reserva a actualizar.
        body: Campos a modificar, validados por el esquema ReservaUpdate.
        reserva_crud: Instancia del CRUD de reservas inyectada por dependencia.

    Returns:
        La reserva con los datos actualizados.

    Raises:
        NoEncontradoError: Si no existe una reserva con ese UUID.
    """
    id_usuario_edita = body.id_usuario_edita
    data = body.model_dump(exclude_unset=True, exclude={"id_usuario_edita"})

    reserva = reserva_crud.actualizar_reserva(
        reserva_id=id_reserva, id_usuario_edita=id_usuario_edita, **data
    )

    if not reserva:
        raise NoEncontradoError("Reserva")
    return reserva


@router.delete(path="/{id_reserva}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_reserva(
    id_reserva: UUID, reserva_crud: ReservaCRUD = Depends(get_reserva_crud)
) -> None:
    """
    Elimina una reserva del sistema de forma permanente.

    Args:
        id_reserva: UUID de la reserva a eliminar.
        reserva_crud: Instancia del CRUD de reservas inyectada por dependencia.

    Returns:
        None. Responde con HTTP 204 si la operación fue exitosa.

    Raises:
        NoEncontradoError: Si no existe una reserva con ese UUID.
    """
    eliminado = reserva_crud.eliminar_reserva(reserva_id=id_reserva)
    if not eliminado:
        raise NoEncontradoError("Reserva")
