import jwt, os
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, status, Depends
from uuid import UUID
from datetime import datetime, timedelta, timezone

from src.crud.usuario_crud import UsuarioCRUD
from src.schemas.login_schema import UsuarioLogin
from src.schemas.usuario_schema import UsuarioCreate, UsuarioRead
from src.utils.security import Security
from src.database.config import get_db

router = APIRouter(prefix="/auth", tags=["autenticacion"])
gestor_seguridad = Security()

KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
TOKEN_EXPIRE = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


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

    payload = {
        "sub": str(usuario_ingresado.id_usuario),
        "rol": usuario_ingresado.rol,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE),
    }

    token = jwt.encode(payload, KEY, algorithm=ALGORITHM)

    return {
        "status": "success",
        "message": "¡Bienvenido al sistema!",
        "access_token": token,
        "token_type": "bearer",
    }


@router.post("/registro")
def registrar_usuario(body: UsuarioCreate, db: Session = Depends(get_db)) -> None:
    gestor_crud_usuario = UsuarioCRUD(db)

    usuario_registro = gestor_crud_usuario.crear_usuario(
        nombre_nuevo=body.nombre,
        apellido_nuevo=body.apellido,
        documento_nuevo=body.documento,
        email_nuevo=body.email,
        telefono_nuevo=body.telefono,
        contrasena_nueva=body.contrasena,
        rol_nuevo="Usuario",
        id_usuario_sesion=body.id_usuario_crea,
    )
    payload = {
        "sub": str(usuario_registro.id_usuario),
        "rol": usuario_registro.rol,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE),
    }

    token = jwt.encode(payload, KEY, algorithm=ALGORITHM)

    return {
        "status": "success",
        "message": "Registro exitoso OwO! ¡Bienvenido al sistema!",
        "access_token": token,
        "token_type": "bearer",
        "username_generado": usuario_registro.username,
    }
