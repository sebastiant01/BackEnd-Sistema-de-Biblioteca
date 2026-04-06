from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List
from uuid import UUID

from src.crud.autor_crud import AutorCRUD
from src.database.config import get_db
from src.schemas.autor_schema import AutorCreate, AutorRead, AutorUpdate

router = APIRouter(prefix="/autores", tags=["autores"])


def get_autor_crud(db: Session = Depends(get_db)) -> AutorCRUD:
    """Inyección de dependencias para el CRUD de autores."""
    return AutorCRUD(db_session=db)


@router.get("", response_model=List[AutorRead])
def listar_autores(
    skip: int = 0, limit: int = 100, autor_crud: AutorCRUD = Depends(get_autor_crud)
) -> List[AutorRead]:
    """
    Obtiene una lista paginada de todos los autores registrados.
    """
    return autor_crud.obtener_todos_los_autores(skip=skip, limit=limit)


@router.get("/buscar", response_model=List[AutorRead])
def obtener_autor_por_nombre(
    termino_busqueda: str = Query(
        ..., description="Nombre o fragmento del nombre a buscar"
    ),
    autor_crud: AutorCRUD = Depends(get_autor_crud),
) -> List[AutorRead]:
    """
    Realiza una búsqueda flexible de autores por su nombre.
    """
    return autor_crud.buscar_autor_por_nombre(termino_busqueda=termino_busqueda)


@router.get("/{id_autor}", response_model=AutorRead)
def obtener_autor_por_id(
    id_autor: UUID, autor_crud: AutorCRUD = Depends(get_autor_crud)
) -> AutorRead:
    """
    Consulta un autor específico a través de su UUID.
    """
    autor = autor_crud.consultar_autor_por_id(id_autor)
    if not autor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Autor no encontrado"
        )
    return autor


@router.post("", response_model=AutorRead, status_code=status.HTTP_201_CREATED)
def crear_autor(
    body: AutorCreate, autor_crud: AutorCRUD = Depends(get_autor_crud)
) -> AutorRead:
    """
    Registra un nuevo autor en el sistema.
    """
    autor = autor_crud.crear_autor(
        nombre_autor=body.nombre_autor,
        apellido_autor=body.apellido_autor,
        nacionalidad=body.nacionalidad,
        id_usuario_sesion=body.id_usuario_crea,
    )
    return autor


@router.put("/{id_autor}", response_model=AutorRead)
def actualizar_autor(
    id_autor: UUID,
    body: AutorUpdate,
    autor_crud: AutorCRUD = Depends(get_autor_crud),
) -> AutorRead:
    """
    Actualiza parcialmente la información de un autor y registra quién hace la edición.
    """
    datos_nuevos = body.model_dump(exclude_unset=True)
    autor = autor_crud.actualizar_autor(id_autor, **datos_nuevos)
    if not autor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Autor no encontrado"
        )
    return autor


@router.delete("/{id_autor}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_autor(
    id_autor: UUID,
    id_usuario_edita: UUID,
    autor_crud: AutorCRUD = Depends(get_autor_crud),
) -> None:
    """
    Realiza un borrado lógico (inactivación) del autor en el sistema.
    """
    if not autor_crud.eliminar_autor(id_autor, id_usuario_edita):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Autor no encontrado"
        )
