"""
Router de libros para la API REST.

Expone los endpoints CRUD del recurso Libro, incluyendo búsqueda por título,
género, autor y código, así como la gestión de disponibilidad.

Prefix: /libros
Tags:   libros
"""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, status, Depends
from src.core.exceptions import NoEncontradoError, DatosInvalidosError
from sqlalchemy.orm import Session
from src.database.config import get_db

from src.crud.libro_crud import LibroCRUD
from src.schemas.libro_schema import LibroCreate, LibroRead, LibroUpdate
from src.utils.security import Security

router = APIRouter(prefix="/libros", tags=["libros"])
gestor_seguridad = Security()


def get_libro_crud(db: Session = Depends(get_db)) -> LibroCRUD:
    """Provee una instancia de LibroCRUD con la sesión de base de datos activa."""
    return LibroCRUD(db=db)


@router.get(path="/", response_model=List[LibroRead])
def listar_libros(
    skip: int = 0,
    limit: int = 100,
    por_titulo: Optional[str] = None,
    por_genero: Optional[str] = None,
    solo_disponibles: Optional[bool] = False,
    libro_crud: LibroCRUD = Depends(get_libro_crud),
) -> List[LibroRead]:
    """
    Lista los libros registrados en el sistema.

    Aplica filtros opcionales de forma excluyente en el siguiente orden de
    prioridad: título → género → disponibilidad. Si no se pasa ningún filtro,
    retorna todos los libros paginados con `skip` y `limit`.

    Args:
        skip: Número de registros a omitir (paginación).
        limit: Cantidad máxima de registros a retornar.
        por_titulo: Filtra libros cuyo título coincida con el valor dado.
        por_genero: Filtra libros que pertenezcan al género dado.
        solo_disponibles: Si es True, retorna únicamente los libros disponibles.
        libro_crud: Instancia del CRUD de libros inyectada por dependencia.

    Returns:
        Lista de libros que cumplen el criterio aplicado.
    """
    if por_titulo:
        return libro_crud.buscar_libros_por_titulo(
            titulo=por_titulo.strip(), skip=skip, limit=limit
        )
    if por_genero:
        return libro_crud.buscar_libros_por_genero(
            genero=por_genero.strip(), skip=skip, limit=limit
        )
    if solo_disponibles:
        return libro_crud.obtener_libros_disponibles(skip=skip, limit=limit)

    return libro_crud.obtener_libros(skip=skip, limit=limit)


@router.get(path="/id/{id_libro}", response_model=LibroRead)
def obtener_libro(
    id_libro: UUID, libro_crud: LibroCRUD = Depends(get_libro_crud)
) -> LibroRead:
    """
    Retorna un libro específico por su UUID.

    Args:
        id_libro: Identificador único del libro.
        libro_crud: Instancia del CRUD de libros inyectada por dependencia.

    Returns:
        El libro correspondiente al UUID proporcionado.

    Raises:
        NoEncontradoError: Si no existe un libro con ese UUID.
    """
    libro = libro_crud.obtener_libro(id_libro=id_libro)
    if not libro:
        raise NoEncontradoError("Libro")
    return libro


@router.get(path="/codigo/{codigo_libro}", response_model=LibroRead)
def obtener_libro_codigo(
    codigo_libro: str, libro_crud: LibroCRUD = Depends(get_libro_crud)
) -> LibroRead:
    """
    Retorna un libro específico por su código de material.

    Args:
        codigo_libro: Código único del material bibliográfico.
        libro_crud: Instancia del CRUD de libros inyectada por dependencia.

    Returns:
        El libro correspondiente al código proporcionado.

    Raises:
        NoEncontradoError: Si no existe un libro con ese código.
    """
    libro = libro_crud.obtener_libro_codigo(codigo_libro=codigo_libro)
    if not libro:
        raise NoEncontradoError("Libro")
    return libro


@router.get(path="/autor/{id_autor}", response_model=List[LibroRead])
def obtener_libros_autor(
    id_autor: UUID, libro_crud: LibroCRUD = Depends(get_libro_crud)
) -> LibroRead:
    """
    Retorna todos los libros asociados a un autor.

    Args:
        id_autor: UUID del autor cuyos libros se desean consultar.
        libro_crud: Instancia del CRUD de libros inyectada por dependencia.

    Returns:
        Lista de libros pertenecientes al autor indicado.

    Raises:
        NoEncontradoError: Si no se encontraron libros para ese autor.
    """
    libros = libro_crud.obtener_libros_por_autor(id_autor=id_autor)
    if not libros:
        raise NoEncontradoError("Libros")
    return libros


@router.post(
    path="/", 
    response_model=LibroRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(gestor_seguridad.verificar_admin)],

    )
def crear_libro(
    body: LibroCreate, libro_crud: LibroCRUD = Depends(get_libro_crud)
) -> LibroRead:
    """
    Crea un nuevo libro en el sistema.

    Args:
        body: Datos del libro a registrar, validados por el esquema LibroCreate.
        libro_crud: Instancia del CRUD de libros inyectada por dependencia.

    Returns:
        El libro recién creado con todos sus campos, incluido el UUID generado.
    """
    return libro_crud.crear_libro(
        codigo_libro=body.codigo_material,
        titulo_libro=body.titulo_material,
        genero_libro=body.genero_libro,
        id_autor=body.id_autor,
        codigo_isbn=body.codigo_isbn,
        id_usuario_crea=body.id_usuario_crea,
        descripcion_libro=body.descripcion_material,
        fecha_libro=body.fecha_material,
        disponibilidad=body.disponibilidad_material,
    )


@router.put(
    path="/{id_libro}",
    response_model=LibroRead,
    dependencies=[Depends(gestor_seguridad.verificar_admin)],
    )
def actualizar_libro(
    id_libro: UUID, body: LibroUpdate, libro_crud: LibroCRUD = Depends(get_libro_crud)
) -> LibroRead:
    """
    Actualiza los datos de un libro existente.

    Solo se actualizan los campos presentes en el cuerpo de la solicitud.
    El campo `id_usuario_edita` se extrae del body antes de pasarlo al CRUD.

    Args:
        id_libro: UUID del libro a actualizar.
        body: Campos a modificar, validados por el esquema LibroUpdate.
        libro_crud: Instancia del CRUD de libros inyectada por dependencia.

    Returns:
        El libro con los datos actualizados.

    Raises:
        NoEncontradoError: Si no existe un libro con ese UUID.
    """
    id_usuario_edita = body.id_usuario_edita
    data = body.model_dump(exclude_unset=True, exclude={"id_usuario_edita"})
    libro = libro_crud.actualizar_libro(
        id_libro=id_libro, id_usuario_edita=id_usuario_edita, **data
    )

    if not libro:
        raise NoEncontradoError("Libro")
    return libro


@router.patch(path="/{id_libro}/disponibilidad", response_model=LibroRead)
def actualizar_disponibilidad_libro(
    id_libro: UUID, body: LibroUpdate, libro_crud: LibroCRUD = Depends(get_libro_crud)
) -> LibroRead:
    """
    Cambia la disponibilidad de un libro.

    Args:
        id_libro: UUID del libro cuya disponibilidad se desea modificar.
        body: Debe incluir `disponibilidad_material` e `id_usuario_edita`.
        libro_crud: Instancia del CRUD de libros inyectada por dependencia.

    Returns:
        El libro con la disponibilidad actualizada.

    Raises:
        DatosInvalidosError: Si `disponibilidad_material` no está presente en el body.
        NoEncontradoError: Si no existe un libro con ese UUID.
    """
    id_usuario_edita = body.id_usuario_edita
    disponible = body.disponibilidad_material
    if disponible is None:
        raise DatosInvalidosError("Campo 'disponibilidad_material' no válido.")

    libro = libro_crud.cambiar_disponibilidad(
        id_libro=id_libro, disponible=disponible, id_usuario_edita=id_usuario_edita
    )
    if not libro:
        raise NoEncontradoError("Libro")
    return libro


@router.delete(
    path="/{id_libro}", 
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(gestor_seguridad.verificar_admin)],
    )
    
def eliminar_libro(
    id_libro: UUID, libro_crud: LibroCRUD = Depends(get_libro_crud)
) -> None:
    """
    Elimina un libro del sistema de forma permanente.

    Args:
        id_libro: UUID del libro a eliminar.
        libro_crud: Instancia del CRUD de libros inyectada por dependencia.

    Returns:
        None. Responde con HTTP 204 si la operación fue exitosa.

    Raises:
        NoEncontradoError: Si no existe un libro con ese UUID.
    """
    libro = libro_crud.eliminar_libro(id_libro=id_libro)
    if not libro:
        raise NoEncontradoError("Libro")
