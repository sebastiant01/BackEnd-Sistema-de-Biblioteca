from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from uuid import UUID

from src.crud.prestamo_crud import PrestamoCRUD
from src.crud.usuario_crud import UsuarioCRUD
from src.schemas.prestamo_schema import PrestamoCreate, PrestamoRead, PrestamoUpdate
from src.routers.usuario_router import get_usuario_crud
from src.database.config import get_db
from src.utils.security import Security

router = APIRouter(prefix="/prestamos", tags=["prestamos"])

gestor_seguridad = Security()


def get_prestamo_crud(db: Session = Depends(get_db)) -> PrestamoCRUD:
    """Inyección de dependencias para instanciar el CRUD de préstamos."""
    return PrestamoCRUD(db_session=db)


@router.get("", response_model=List[PrestamoRead])
def listar_prestamos(
    skip: int = 0,
    limit: int = 100,
    prestamo_crud: PrestamoCRUD = Depends(get_prestamo_crud),
) -> List[PrestamoRead]:
    """
    Obtiene una lista paginada de todos los préstamos registrados en el sistema.
    """
    return prestamo_crud.obtener_todos_los_prestamos(skip=skip, limit=limit)


@router.get("/{id_prestamo}", response_model=PrestamoRead)
def obtener_prestamo_por_id(
    id_prestamo: UUID, prestamo_crud: PrestamoCRUD = Depends(get_prestamo_crud)
) -> PrestamoRead:
    """
    Consulta los detalles de un préstamo específico a través de su UUID.
    """
    prestamo = prestamo_crud.consultar_prestamo_por_id(id_prestamo)
    if not prestamo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Prestamo no encontrado"
        )
    return prestamo


@router.get("/usuario/{id_usuario}", response_model=List[PrestamoRead])
def obtener_prestamos_por_usuario(
    id_usuario: UUID,
    prestamo_crud: PrestamoCRUD = Depends(get_prestamo_crud),
    usuario_crud: UsuarioCRUD = Depends(get_usuario_crud),
    skip: int = 0,
    limit: int = 100,
) -> List[PrestamoRead]:
    """
    Consulta el historial completo de préstamos (activos y devueltos) de un usuario específico.
    """
    usuario = usuario_crud.consultar_usuario_por_id(id_usuario)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )

    return prestamo_crud.consultar_prestamos_por_usuario(id_usuario, skip, limit)


@router.get("/usuario/{id_usuario}/activos", response_model=List[PrestamoRead])
def obtener_prestamos_activos_de_usuario(
    id_usuario: UUID,
    prestamo_crud: PrestamoCRUD = Depends(get_prestamo_crud),
    usuario_crud: UsuarioCRUD = Depends(get_usuario_crud),
) -> List[PrestamoRead]:
    """
    Consulta ÚNICAMENTE los préstamos que el usuario tiene actualmente sin devolver.
    """
    usuario = usuario_crud.consultar_usuario_por_id(id_usuario)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )

    return prestamo_crud.consultar_prestamos_activos_por_usuario(id_usuario)


@router.get("/material/{id_material}", response_model=List[PrestamoRead])
def obtener_prestamos_por_material(
    id_material: UUID,
    prestamo_crud: PrestamoCRUD = Depends(get_prestamo_crud),
    skip: int = 0,
    limit: int = 100,
) -> List[PrestamoRead]:
    """
    Consulta el historial de veces que un material específico ha sido prestado.
    """
    return prestamo_crud.consultar_prestamos_por_material(id_material, skip, limit)


@router.post(
    "",
    response_model=PrestamoRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(gestor_seguridad.verificar_admin)],
)
def crear_prestamo(
    body: PrestamoCreate, prestamo_crud: PrestamoCRUD = Depends(get_prestamo_crud)
) -> PrestamoRead:
    """
    Registra un nuevo préstamo en el sistema asociando un usuario y un material.
    """
    prestamo = prestamo_crud.crear_prestamo(
        id_usuario_cliente=body.id_usuario,
        id_material_prestado=body.id_material,
        id_usuario_sesion=body.id_usuario,
    )
    return prestamo


@router.put(
    "/{id_prestamo}",
    response_model=PrestamoRead,
    dependencies=[Depends(gestor_seguridad.verificar_admin)],
)
def actualizar_prestamo(
    id_prestamo: UUID,
    body: PrestamoUpdate,
    prestamo_crud: PrestamoCRUD = Depends(get_prestamo_crud),
) -> PrestamoRead:
    """
    Actualiza el estado de un préstamo (ej. marcar como devuelto) registrando quién hace el cambio.
    """
    prestamo_encontrado = prestamo_crud.actualizar_estado_prestamo(
        id_prestamo, body.estado, body.id_usuario_edita
    )
    if not prestamo_encontrado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Préstamo no encontrado"
        )
    return prestamo_encontrado


@router.delete(
    "/{id_prestamo}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(gestor_seguridad.verificar_admin)],
)
def eliminar_prestamo(
    id_prestamo: UUID, prestamo_crud: PrestamoCRUD = Depends(get_prestamo_crud)
) -> None:
    """
    Elimina (o inactiva) un registro de préstamo del sistema.
    """
    prestamo = prestamo_crud.eliminar_prestamo(id_prestamo)
    if not prestamo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Préstamo no encontrado o ya eliminado",
        )
