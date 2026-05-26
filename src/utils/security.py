import hashlib, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from os import getenv

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
KEY = getenv("SECRET_KEY")
ALGORITHM = getenv("ALGORITHM")


class Security:

    def generar_hash(self, contrasena_plana: str) -> str:
        bytes_contrasena = contrasena_plana.encode("utf-8")
        hash_puro = hashlib.sha256(bytes_contrasena)
        contrasena_hasheada = hash_puro.hexdigest()

        return contrasena_hasheada

    def verificar_contrasena_ingresada(
        self, contrasena_plana: str, contrasena_hasheada_guardada: str
    ) -> bool:

        hash_intento = self.generar_hash(contrasena_plana)

        return hash_intento == contrasena_hasheada_guardada

    @staticmethod
    def verificar_token(token: str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(token, KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="El token de acceso expiró. Vuelve a iniciar sesión.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas o token modificado externamente.",
                headers={"WWW-Authenticate": "Bearer"},
            )

    @staticmethod
    def verificar_admin(payload: dict = Depends(verificar_token)):
        if not isinstance(payload, dict):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno: El payload no es un diccionario válido.",
            )

        rol_usuario = payload.get("rol")

        if rol_usuario != "Admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Error: No tienes permisos de Administrador.",
            )

        return payload


security = Security()
