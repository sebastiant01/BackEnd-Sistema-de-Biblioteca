from pydantic import BaseModel


class UsuarioLogin(BaseModel):
    username: str
    contrasena: str
