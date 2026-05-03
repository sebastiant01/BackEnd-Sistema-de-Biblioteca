from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, status, Depends
from uuid import UUID

from src.crud.usuario_crud import UsuarioCRUD
from src.schemas.login_schema import UsuarioLogin
from src.utils.security import Security
from src.database.config import get_db

router = APIRouter(prefix="/auth", tags=["autenticacion"])
gestor_seguridad = Security()


@router.post("/login")
def login_usuario(credentials: UsuarioLogin, db: Session = Depends(get_db)) -> None:
    gestor_crud_usuario = UsuarioCRUD(db)
    usuario_ingresado = gestor_crud_usuario.consultar_usuario_por_username(
        credentials.username
    )
    if not usuario_ingresado or not gestor_seguridad.verificar_contrasena_ingresada(
        credentials.contrasena, usuario_ingresado.contrasena
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Username o contraseña incorrectos",
        )

    return {
        "status": "success",
        "message": "¡Bienvenido al sistema!",
        "id_usuario": usuario_ingresado.id_usuario,
        "nombre": usuario_ingresado.nombre,
        "apellido": usuario_ingresado.apellido,
        "username": usuario_ingresado.username,
        "rol": usuario_ingresado.rol,
    }
