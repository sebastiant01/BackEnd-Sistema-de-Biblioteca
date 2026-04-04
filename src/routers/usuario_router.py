from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import List
from uuid import UUID
from src.schemas.usuario_schema import UsuarioCreate, UsuarioRead, UsuarioUpdate

from src.crud.usuario_crud import UsuarioCRUD
from src.database.config import get_db

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


def get_usuario_crud(db: Session = Depends(get_db)) -> UsuarioCRUD:
    """Inyección de dependencias para instanciar el CRUD con la sesión actual de la base de datos."""
    return UsuarioCRUD(db_session=db)


@router.get("", response_model=List[UsuarioRead])
def listar_usuarios(
    skip: int = 0,
    limit: int = 100,
    usuario_crud: UsuarioCRUD = Depends(get_usuario_crud),
) -> List[UsuarioRead]:
    """
    Obtiene una lista paginada de todos los usuarios registrados.
    """
    return usuario_crud.obtener_todos_los_usuarios(skip=skip, limit=limit)


@router.get("/buscar", response_model=List[UsuarioRead])
def obtener_usuarios_universal(
    termino: str = Query(
        ...,
        min_length=1,
        description="Texto a buscar en todos los campos de la tabla Usuario",
    ),
    usuario_crud: UsuarioCRUD = Depends(get_usuario_crud),
) -> List[UsuarioRead]:
    """
    Realiza una búsqueda flexible coincidiendo el término con múltiples campos del usuario.
    """
    return usuario_crud.buscar_usuario_universal(termino)


@router.get("/{id_usuario}", response_model=UsuarioRead)
def obtener_usuario_por_id(
    id_usuario: UUID, usuario_crud: UsuarioCRUD = Depends(get_usuario_crud)
) -> UsuarioRead:
    """
    Consulta un usuario específico a través de su UUID.
    """
    usuario = usuario_crud.consultar_usuario_por_id(id_usuario)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Error: Usuario no encontrado"
        )
    return usuario


@router.get("/username/{username}", response_model=UsuarioRead)
def obtener_usuario_por_username(
    username: str, usuario_crud: UsuarioCRUD = Depends(get_usuario_crud)
) -> UsuarioRead:
    """
    Consulta un usuario específico a través de su nombre de usuario.
    """
    usuario = usuario_crud.consultar_usuario_por_username(username)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Error: Usuario no encontrado"
        )
    return usuario


@router.get("/email/{email}", response_model=UsuarioRead)
def obtener_usuario_por_email(
    email: str, usuario_crud: UsuarioCRUD = Depends(get_usuario_crud)
) -> UsuarioRead:
    """
    Consulta un usuario específico a través de su correo electrónico.
    """
    usuario = usuario_crud.consultar_usuario_por_email(email)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Error: Usuario no encontrado"
        )
    return usuario


@router.get("/documento/{documento}", response_model=UsuarioRead)
def obtener_usuario_por_documento(
    documento: str, usuario_crud: UsuarioCRUD = Depends(get_usuario_crud)
) -> UsuarioRead:
    """
    Consulta un usuario específico a través de su documento de identidad.
    """
    usuario = usuario_crud.consultar_usuario_por_documento(documento)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Error: Usuario no encontrado"
        )
    return usuario


@router.get("/telefono/{telefono}", response_model=UsuarioRead)
def obtener_usuario_por_telefono(
    telefono: str, usuario_crud: UsuarioCRUD = Depends(get_usuario_crud)
) -> UsuarioRead:
    """
    Consulta un usuario específico a través de su número telefónico.
    """
    usuario = usuario_crud.consultar_usuario_por_telefono(telefono)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Error: Usuario no encontrado"
        )
    return usuario


@router.post("", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def crear_usuario(
    body: UsuarioCreate, usuario_crud: UsuarioCRUD = Depends(get_usuario_crud)
) -> UsuarioRead:
    """
    Registra un nuevo usuario en la base de datos.
    """
    usuario = usuario_crud.crear_usuario(
        nombre_nuevo=body.nombre,
        apellido_nuevo=body.apellido,
        documento_nuevo=body.documento,
        email_nuevo=body.email,
        telefono_nuevo=body.telefono,
        contrasena_nueva=body.contrasena,
        rol_nuevo=body.rol,
    )
    return usuario


@router.put("/{id_usuario}", response_model=UsuarioRead)
def actualizar_usuario(
    id_usuario: UUID,
    body: UsuarioUpdate,
    id_usuario_edita: UUID,
    usuario_crud: UsuarioCRUD = Depends(get_usuario_crud),
) -> UsuarioRead:
    """
    Actualiza parcialmente los datos de un usuario e inyecta la auditoría del editor.
    """
    datos_nuevos = body.model_dump(exclude_unset=True)
    datos_nuevos["id_usuario_edita"] = id_usuario_edita
    usuario = usuario_crud.actualizar_usuario(id_usuario, **datos_nuevos)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado UnU"
        )
    return usuario


@router.delete("/{id_usuario}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(
    id_usuario: UUID, usuario_crud: UsuarioCRUD = Depends(get_usuario_crud)
) -> None:
    """
    Elimina (o inactiva) un usuario del sistema basado en su UUID.
    """
    if not usuario_crud.eliminar_usuario(id_usuario):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado o ya eliminado unu",
        )
